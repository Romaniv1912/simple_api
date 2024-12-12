from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.common.model import Base, id_key


class Record(Base):
    """User table"""

    __tablename__ = 'records'

    id: Mapped[id_key]
    bot_token: Mapped[str] = mapped_column(String(255), comment='bot token')
    chat_id: Mapped[str] = mapped_column(String(255), comment='chat id')
    message: Mapped[str] = mapped_column(String, comment='message')
    sent_time: Mapped[datetime | None] = mapped_column(DateTime, comment='sent time')
    sent_response: Mapped[str] = mapped_column(String, comment='sent status')

    # User records one-to-many
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey('users.id', ondelete='SET NULL'), default=None, comment='records user id'
    )
