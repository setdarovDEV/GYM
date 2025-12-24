from sqlalchemy import create_engine, String, ForeignKey, BigInteger, Numeric, Text, SmallInteger, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

engine = create_engine("postgresql+psycopg2://postgres:1@localhost:5432/sqlalchemy")
engine.connect()

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255))
    phone_number: Mapped[str] = mapped_column(String(50))

# class Base:
#     table_name


# class Table1(Base):
#     pass
#
# class Table1(Base):
#     pass
#
# class Table1(Base):
#     pass
#
#
# class Table1(Base):
#     pass
#
# class Table1(Base):
#     pass
