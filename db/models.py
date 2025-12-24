from datetime import datetime
from sqlalchemy import create_engine, String, ForeignKey, BigInteger, Numeric, Text, SmallInteger, Enum, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, declared_attr, Session, sessionmaker
from enum import Enum as PyEnum
from os import getenv
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(f"postgresql+psycopg2://{load_dotenv("DB_USER")}:{getenv("DB_PASSWORD")}@localhost:{getenv("DB_PORT")}/{getenv("DB_NAME")}")
session = Session(engine)
engine.connect()

class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(cls):
        if cls.__name__[-1] in ['s']:
            return cls.__name__.lower() + "es"
        return cls.__name__.lower() + "s"

class User(Base):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255))
    phone_number: Mapped[str] = mapped_column(String(50))

    locations: Mapped[list["UserLocation"]] = relationship(back_populates="user")
    orders: Mapped[list["Order"]] = relationship(back_populates="user")
    payments: Mapped[list["Payment"]] = relationship(back_populates="user")

class UserLocation(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String)
    longitude: Mapped[float] = mapped_column(Numeric)
    latitude: Mapped[float] = mapped_column(Numeric)

    user: Mapped["User"] = relationship(back_populates="locations")

class Category(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    products: Mapped[list["Product"]] = relationship(back_populates="category")

class ProductStatus(PyEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class Product(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categorys.id", ondelete="NO ACTION"))
    name: Mapped[str] = mapped_column(String(100))
    photo: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[int] = mapped_column(Numeric(12, 0))
    quantity: Mapped[int] = mapped_column(SmallInteger)
    status: Mapped[ProductStatus] = mapped_column(Enum(ProductStatus, values_callable=lambda x: [i.value for i in x]), default=ProductStatus.ACTIVE.value)

    category: Mapped["Category"] = relationship(back_populates="products") #

class Courier(Base):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255))
    phone_number: Mapped[str] = mapped_column(String(50))
    transport: Mapped[str] = mapped_column(String)

    deliveries: Mapped[list["Delivery"]] = relationship(back_populates="courier")

class DeliveryStatus(PyEnum):
    DELIVERED = "delivered"
    PROCESSING = "processing"

class Delivery(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    price: Mapped[int] = mapped_column(Numeric(12, 0), default=0)
    status: Mapped[DeliveryStatus] = mapped_column(Enum(DeliveryStatus, values_callable=lambda x: [i.value for i in x]), default=DeliveryStatus.PROCESSING.value)
    courier_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("couriers.id", ondelete="NO ACTION"))
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    courier: Mapped["Courier"] = relationship(back_populates="deliveries")
    orders: Mapped[list["Order"]] = relationship(back_populates="delivery")

class OrderStatus(PyEnum):
    PROCESS = "process"
    CANCELED = "canceled"
    COMPLETED = "completed"

class Order(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    total: Mapped[int] = mapped_column(Numeric(12, 0), default=0)
    delivery_id: Mapped[int] = mapped_column(ForeignKey("deliverys.id"))
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus, values_callable=lambda x: [i.value for i in x]),default=OrderStatus.PROCESS.value)
    order_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="orders")
    delivery: Mapped["Delivery"] = relationship(back_populates="orders")
    items: Mapped[list["OrderItem"]] = relationship(back_populates="order")
    payments: Mapped["Payment"] = relationship(back_populates="order")

class OrderItem(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"))
    quantity: Mapped[int] = mapped_column(SmallInteger)
    amount: Mapped[int] = mapped_column(Numeric(12, 0), default=0)

    order: Mapped["Order"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship()

class Payment(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="NO ACTION"))
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="NO ACTION"))
    pay_amount: Mapped[int] = mapped_column(Numeric(12, 0))
    pay_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    order: Mapped["Order"] = relationship(back_populates="payments")
    user: Mapped["User"] = relationship(back_populates="payments")

Base.metadata.create_all(engine)