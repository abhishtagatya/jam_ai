from datetime import datetime

from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ConversationHistory(Base):
    __tablename__ = "conversation_history"

    uid: Mapped[str] = mapped_column(String(16), primary_key=True)
    author: Mapped[str] = mapped_column(String(32))
    role: Mapped[str] = mapped_column(String(32))
    content: Mapped[str] = mapped_column(Text)
    mention: Mapped[str] = mapped_column(String(32), nullable=True)
    function: Mapped[str] = mapped_column(String(32), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    success: Mapped[bool] = mapped_column(Boolean, default=True)
