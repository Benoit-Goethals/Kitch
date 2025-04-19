from datetime import datetime
from sqlalchemy import Column, Integer, Text
from sqlalchemy import Enum
from sqlalchemy import String, DateTime

from domain.DatabaseModelClasses import Base


class MediaDocumentDB(Base):

    __tablename__ = 'mediadocument'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=False, nullable=False, index=True)
    path = Column(String(255), unique=False, nullable=False, index=False)
    content = Column(Text, nullable=False)

    keyword_match = Column(Text, nullable=True)
    date = Column(DateTime, default=datetime.utcnow)

