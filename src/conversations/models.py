from src import db
from sqlalchemy.dialects.postgresql import JSONB

class Conversations(db.Model):

    __tablename__ = "conversations"

    phone_id = db.Column(db.String(20), primary_key=True)
    # messages = db.Column(db.Array(db.String(1000)))
    messages = db.Column(JSONB)
    created_on = db.Column(db.DateTime, nullable=False)
    updated_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, phone_id, created_on, updated_on, messages=[]):
        self.phone_id = phone_id
        self.created_on = created_on
        self.updated_on = updated_on
        self.messages = messages

    def __repr__(self):
        res = f"Phone_id: {self.phone_id}\n\nMessages: {self.messages}\n\nCreated on: {self.created_on}"
        res += f"\nUpdated on: {self.updated_on}"
        return res