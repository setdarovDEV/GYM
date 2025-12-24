from sqlalchemy import create_engine, String, ForeignKey, BigInteger, Numeric, Text, SmallInteger , Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from enum import Enum as PyEnum

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

    locations: Mapped[list["UserLocation"]] = relationship(back_populates="user", cascade="all, delete")
    orders: Mapped[list["Order"]] = relationship(back_populates="user")


class UserLocation(Base):
    __tablename__ = "user_locations"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String)
    longitude: Mapped[float] = mapped_column(Numeric)
    latitude: Mapped[float] = mapped_column(Numeric)

    user: Mapped["User"] = relationship(back_populates="locations")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    products: Mapped[list["Product"]] = relationship(back_populates="category")


class ProductStatus(PyEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"


# =========================
# PRODUCTS
# =========================

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="NO ACTION"))
    name: Mapped[str] = mapped_column(String(100))
    photo: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[int] = mapped_column(Numeric(12, 0))
    quantity: Mapped[int] = mapped_column(SmallInteger)

    status: Mapped[ProductStatus] = mapped_column(Enum(ProductStatus,values_callable=lambda x: [i.value for i in x]),default=ProductStatus.ACTIVE.value)

    category: Mapped["Category"] = relationship(back_populates="products")


