from datetime import datetime
from sqlalchemy import DateTime, String, TypeDecorator
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, declarative_base

# 스키마의 기본 클래스

Base = declarative_base()


class EnumType(TypeDecorator):
    impl = String
    cache_ok = True

    def __init__(self, enum_class, length=50):
        super().__init__(length)
        self.enum_class = enum_class

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return value.name  # Enum의 값을 문자열로 저장

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return self.enum_class[value]  # 문자열을 다시 Enum으로 변환


class BaseEntity(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),  # INSERT 시 서버에서 시간 생성
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),  # INSERT 시 서버에서 시간 생성
        onupdate=func.now(),  # UPDATE 시 자동 업데이트
        nullable=False,
    )
