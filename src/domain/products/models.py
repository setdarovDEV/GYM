from datetime import datetime
from sqlalchemy import Column, BigInteger, String, Integer, Boolean, DateTime, Text, ForeignKey, DECIMAL
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.core.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(BigInteger, primary_key=True, index=True)
    name_ru = Column(String(255), nullable=False)
    name_uz = Column(String(255), nullable=False)
    name_en = Column(String(255), nullable=False)
    description_ru = Column(Text, nullable=True)
    description_uz = Column(Text, nullable=True)
    description_en = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    products = relationship("Product", back_populates="category", lazy="selectin")

    def get_name(self, lang: str = "ru") -> str:
        return getattr(self, f"name_{lang}", self.name_ru)

    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name_ru})>"


class Product(Base):
    __tablename__ = "products"

    id = Column(BigInteger, primary_key=True, index=True)
    category_id = Column(BigInteger, ForeignKey('categories.id'), nullable=True)
    name_ru = Column(String(255), nullable=False)
    name_uz = Column(String(255), nullable=False)
    name_en = Column(String(255), nullable=False)
    description_ru = Column(Text, nullable=True)
    description_uz = Column(Text, nullable=True)
    description_en = Column(Text, nullable=True)
    price = Column(Integer, nullable=False)
    image_url = Column(String(500), nullable=True)
    weight_grams = Column(Integer, nullable=True)
    protein = Column(Integer, nullable=True)
    carbs = Column(Integer, nullable=True)
    fats = Column(Integer, nullable=True)
    calories = Column(Integer, nullable=True)
    is_available = Column(Boolean, default=True)
    is_popular = Column(Boolean, default=False)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    category = relationship("Category", back_populates="products")
    cart_items = relationship("CartItem", back_populates="product", lazy="selectin")
    order_items = relationship("OrderItem", back_populates="product", lazy="selectin")

    def get_name(self, lang: str = "ru") -> str:
        return getattr(self, f"name_{lang}", self.name_ru)

    def get_description(self, lang: str = "ru") -> str:
        return getattr(self, f"description_{lang}", self.description_ru)

    @property
    def price_sum(self) -> float:
        return self.price / 100

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name_ru}, price={self.price})>"