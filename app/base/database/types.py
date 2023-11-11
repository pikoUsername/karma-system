import uuid

from pydantic import UUID4
from sqlalchemy import CHAR, TypeDecorator
from sqlalchemy.dialects.postgresql import UUID


class GUID(TypeDecorator):  # pragma: no cover
    """
    Независимый от типа базы данных тип

    Если база данных не иммет тип UUID
    то она применяется тип Char(36).

    * Спизжено из fastapi_users_db_sqlalchemy.generics,
      Сделано потому как не хотелось бы иметь прямых зависимостей
      от библиотеки fastapi_users
    """

    class UUIDChar(CHAR):
        python_type = UUID4  # type: ignore

    impl = UUIDChar
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == "postgresql":
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return str(uuid.UUID(value))
            else:
                return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value
