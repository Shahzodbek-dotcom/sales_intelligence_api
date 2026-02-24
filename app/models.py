from sqlalchemy import Column, String, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Product(Base):
    __tablename__ = "products"

    product_id = Column(String(50), primary_key=True)
    product_name = Column(String(255), nullable=False)
    category = Column(String(100))
    cost_price = Column(Float, nullable=False)


class Sale(Base):
    __tablename__ = "sales"

    order_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer)
    product_id = Column(String(50), ForeignKey("products.product_id"))
    category = Column(String(100))
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    order_date = Column(Date, nullable=False, index=True)
    region = Column(String(100), index=True)
    payment_type = Column(String(50))
    revenue = Column(Float)
    profit = Column(Float)

    # Relationship (optional, agar kerak bo'lsa)
    product = relationship("Product")