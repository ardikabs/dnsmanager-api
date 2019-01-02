import datetime
from server.app import db
from server.main.utils import current_datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID


class BaseModel(db.Model):
    __abstract__ = True
    uuid = db.Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=current_datetime)
    modified_at = db.Column(db.DateTime(timezone=True), default=current_datetime, onupdate=current_datetime)
 
    def __repr__(self):
        return (f"<{self.__class__.__name__}(id={self.id})>")

    def new(self):
        db.session.add(self)    
        self.save()

    def update(self, **kwargs):
        raise NotImplementedError

    def delete(self):
        db.session.delete(self)
        self.save()

    def save(self):
        db.session.commit()

    @classmethod
    def get(cls, uuid):
        return cls.query.filter_by(uuid=uuid).first()