from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Integer, Index, CheckConstraint
from app.models.base_model import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.exc import IntegrityError
import uuid
import time


def generate_uuid():
    return str(uuid.uuid4())

class Conversation(BaseModel):
    __tablename__ = "conversations"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(100), nullable = True)
    title = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship with messages
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

class Message(BaseModel):
    __tablename__ = "messages"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    conversation_id = Column(String(36), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
    role = Column(String(20), nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    sequence_number = Column(DateTime(timezone=True), server_default=func.now()) #Column(Integer, nullable=False, default=0)  # New sequence number column
    reaction = Column(Integer, default=-1, nullable=False) # Simple integer field with check constraint
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship with conversation
    conversation = relationship("Conversation", back_populates="messages")

    # Add index for better performance when querying messages in order
    __table_args__ = (
        Index('ix_messages_conversation_sequence', 'conversation_id', 'sequence_number'),
        CheckConstraint(
            "reaction IN (-1, 0, 1)", 
            name='valid_reaction'
        ),
    )

