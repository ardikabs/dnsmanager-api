
from server.app import db
from server.main.models import BaseModel

  
class ZoneModel(BaseModel):
    __modelname__ = "DNS Zone"
    __tablename__ = "dns_zones"

    name = db.Column(db.String(255), nullable=False)
    server_name = db.Column(db.String(255), nullable=False)
    server_address = db.Column(db.String(255), nullable=False)
    keyring_name = db.Column(db.String(255), nullable=False)
    keyring_value = db.Column(db.String(255), nullable=False)

    records = db.relationship(
        "RecordModel",
        backref="zone",
        lazy="dynamic",
        cascade='delete, delete-orphan'
    )

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}"
            f"(uuid={self.uuid})>"
            f"(name={self.name})>"
            f"(server_name={self.server_name})"
            f"(server_address={self.server_address})"
            f"(keyring_name={self.keyring_name})"
            f"(keyring_value={self.keyring_value})"
            f">"
        )

    def __str__(self):
        return (
            f"<{self.__class__.__name__}"
            f"(uuid={self.uuid})>"
            f"(name={self.name})>"
            f"(server_name={self.server_name})"
            f"(server_address={self.server_address})"
            f"(keyring_name={self.keyring_name})"
            f"(keyring_value={self.keyring_value})"
            f">"
        )

    def update(self, **kwargs):
        self.name = kwargs.get("name", self.name)
        self.server_name = kwargs.get("server_name", self.server_name)
        self.server_address = kwargs.get("server_address", self.server_address)
        self.keyring_name = kwargs.get("keyring_name", self.keyring_name)
        self.keyring_value = kwargs.get("keyring_value", self.keyring_value)
        self.save()
        return self

    @db.validates("name")
    def validate_name(self, key, name):
        name = name.lower()
        return name
    
    @classmethod
    def get_name(cls, name):
        return cls.query.filter_by(name=name).first()