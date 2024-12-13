from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.common.model import Base, id_key


class Record(Base):
    """User table"""

    __tablename__ = 'records'

    id: Mapped[id_key] = mapped_column(init=False)
    bot_token: Mapped[str] = mapped_column(String(255), comment='bot token')
    chat_id: Mapped[str] = mapped_column(String(255), comment='chat id')
    message: Mapped[str] = mapped_column(String, comment='message')
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='SET NULL'), comment='records user id')
    sent_time: Mapped[datetime | None] = mapped_column(DateTime, default=None, comment='sent time')
    sent_response: Mapped[str] = mapped_column(String, default='', comment='sent status')

    user: Mapped['User'] = relationship('User', init=False)  # noqa: F821
