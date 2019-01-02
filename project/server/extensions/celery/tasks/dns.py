
from server.main.models import (
    ZoneModel, 
    RecordModel,
    RecordTypeModel
)
from server.main.services.dns_service import DNSService
from server.worker import celery
import logging

logger = logging.getLogger(__name__)

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(3600.0, periodic_check_record_on_zone.s("Checking Record on DNS Zone"), name="Periodic check record on DNS Zone per hour")

@celery.task()
def import_record(zone_uuid):
    zone = ZoneModel.get(zone_uuid)
    if not zone:
        return "Zone not found"

    try:
        service = DNSService(
            nameserver=zone.server_name,
            keyring_name=zone.keyring_name,
            keyring_value=zone.keyring_value,
            timeout=10
        )
    except Exception as e:
        logger.exception(str(e))

    new_records = []
    records = service.import_records(domain=zone.name)
    for record in records:
        exist = RecordModel.query.filter_by(
            name=record["name"],
            zone=zone
        ).first()
        if exist:
            continue

        rtype = RecordTypeModel.get(record["rtype"])
        new_record = RecordModel(
            name=record["name"],
            content=record["content"],
            ttl=record["ttl"],
            rtype=rtype,
            zone=zone
        ).insert()
        new_records.append(new_record)
    
    logger.info(f"Successfully imported {len(records)} records from DNS Zone {zone.name}")
    logger.info(f"Added {len(new_records)} records to the database")


@celery.task()
def periodic_check_record_on_zone(arg):
    zones = ZoneModel.query.all()
    if not zones:
        return

    for zone in zones:
        try:
            service = DNSService(
                nameserver=zone.server_name,
                keyring_name=zone.keyring_name,
                keyring_value=zone.keyring_value,
                timeout=10
            )
        except Exception as e:
            logger.exception(str(e))

        new_records = []
        exist_records = RecordModel.query.filter_by(zone=zone).all()
        records = service.import_records(domain=zone.name)

        for record in records:
            exist = RecordModel.query.filter_by(
                name=record["name"],
                zone=zone
            ).first()
            if exist:
                r = list(filter(lambda x : x.name == exist.name and x.zone.name == exist.zone.name, exist_records))[0]
                exist_records.pop(exist_records.index(r))
                continue

            rtype = RecordTypeModel.get(record["rtype"])
            new_record = RecordModel(
                name=record["name"],
                content=record["content"],
                ttl=record["ttl"],
                rtype=rtype,
                zone=zone
            ).insert()
            new_records.append(new_record)
        
        logger.info(f"Successfully imported {len(records)} records from DNS Zone {zone.name}")
        logger.info(f"Added {len(new_records)} records to the database")

        if exist_records:
            logger.info(f"Notice {len(exist_records)} records not found in DNS Zone!")
            logger.info(f"Deleted {len(exist_records)} records in the database")

