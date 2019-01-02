
from . import BaseModel
from server.app import db
from server.main.services.dns_service import DNSService
from sqlalchemy.dialects.postgresql import UUID
import dns.rdatatype

class RecordTypeModel(db.Model):
    __modelname__ = "DNS Record Type"
    __tablename__ = "dns_record_types"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    value = db.Column(db.Integer)

    records = db.relationship(
        "RecordModel",
        backref="rtype",
        lazy="dynamic"
    )
    
    def __repr__(self):
        return (
            f"<{self.__class__.__name__}"
            f"(id={self.id})>"
            f"(name={self.name})>"
            f"(value={self.value})"
            f">"
        )

    @db.validates("name")
    def validate_name(self, key, name):
        name = name.upper()
        return name

    @staticmethod
    def seeding():
        RTYPE_AVAILABLES = {
            "A" : dns.rdatatype.A,
            "CNAME" : dns.rdatatype.CNAME,
            "PTR" : dns.rdatatype.PTR,
            "MX" : dns.rdatatype.MX,
            "TXT" : dns.rdatatype.TXT,
            "SRV" : dns.rdatatype.SRV
        }
        for rtype in RTYPE_AVAILABLES:
            record_type = RecordTypeModel.query.filter_by(name=rtype).first()
            if not record_type:
                record_type = RecordTypeModel(name=rtype)
            record_type.value = RTYPE_AVAILABLES[rtype]
            db.session.add(record_type)
        db.session.commit()

    @classmethod
    def get(cls, rtype):
        return cls.query.filter_by(name=rtype).first()

class RecordModel(BaseModel):
    __modelname__ = "DNS Record"
    __tablename__ = "dns_records"

    name = db.Column(db.String(255), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    ttl = db.Column(db.Integer, nullable=False)

    zone_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey("dns_zones.uuid"), nullable=False)
    record_type_id = db.Column(db.Integer, db.ForeignKey("dns_record_types.id"), nullable=False)

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}"
            f"(uuid={self.uuid})>"
            f"(name={self.name})>"
            f"(content={self.content})"
            f"(ttl={self.ttl})"
            f"(rtype={self.rtype.name})"
            f"(zone={self.zone.name})"
            f">"
        )
        
    def __str__(self):
        return (
            f"<{self.__class__.__name__}"
            f"(uuid={self.uuid})>"
            f"(name={self.name})>"
            f"(content={self.content})"
            f"(ttl={self.ttl})"
            f"(rtype={self.rtype.name})"
            f"(zone={self.zone.name})"
            f">"
        )
    
    @property
    def dns_service(self):
        return DNSService(
            nameserver=self.zone.server_name,
            keyring_name=self.zone.keyring_name,
            keyring_value=self.zone.keyring_value,
            timeout=10
        )

    def insert(self):
        super().new()

    def new(self):
        super().new()
        result = self.dns_service.add_record(**{
            "record_name": self.name,
            "record_content": self.content,
            "record_type": self.rtype.name,
            "record_ttl": self.ttl,
            "zone": self.zone.name
        })
        
        if result == "NOERROR":
            return self
        else:
            self.delete()
            raise ValueError(result)

    def update(self, **kwargs):
        if kwargs.get("name") and (self.name != kwargs.get("name")):
            self.dns_service.remove_record(**{
                "record_name": self.name,
                "zone": self.zone.name
            })

        self.name = kwargs.get("name", self.name)
        self.content = kwargs.get("content", self.content)
        self.ttl = kwargs.get("ttl", self.ttl)

        result = self.dns_service.replace_record(**{
            "record_name": self.name,
            "record_content": self.content,
            "record_type": self.rtype.name,
            "record_ttl": self.ttl
        })
        
        if result == "NOERROR":
            self.save()
            return self
        else:
            raise ValueError(result)
    
    def delete(self):
        result = self.dns_service.remove_record(**{
            "record_name": self.name,
            "zone": self.zone.name
        })
        if result == "NOERROR":
            super().delete()
        else:
            raise ValueError(result)

    @db.validates("ttl")
    def validate_ttl(self, key, ttl):
        if ttl % 60 != 0:
            raise ValueError("TTL should be multiply by 60")
        return ttl