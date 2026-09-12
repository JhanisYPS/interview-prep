from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types import ChoiceType

# conexão
engine = create_engine("sqlite:///database/database.db")

# base do banco de dados
Base = declarative_base()

# Tabela de usuário
class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String)
    email = Column("email", String, nullable=False, unique=True)
    password = Column("password", String)
    active = Column("active", Boolean)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, name: str, email: str, password: str, active: bool = True, admin: bool = False):
        self.name = name
        self.email = email
        self.password = password
        self.active = active
        self.admin = admin

class Order(Base):
    __tablename__ = "orders"

    STATUS_ORDERS = (
        ("PENDENTE", "PENDENTE"),
        ("CANCELADO", "CANCELADO"),
        ("FINALIZADO", "FINALIZADO")
    )

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    user_id = Column("user_id", Integer, ForeignKey("users.id"), nullable=False)
    total = Column("total", Float, nullable=False)
    status = Column("status", String, ChoiceType(choices=STATUS_ORDERS), default="PENDENTE") #pendente, cancelado, finalizado

    def __init__(self, user_id: int, total: float, status: str = "PENDENTE"):
        self.user_id = user_id
        self.total = total
        self.status = status

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    order_id = Column("order_id", Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column("product_id", Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column("quantity", Integer, nullable=False)
    price = Column("price", Float, nullable=False)
    #itens = 

    def __init__(self, order_id: int, product_id: int, quantity: int, price: float):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price

class Product(Base):
    __tablename__ = "products"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String, nullable=False)
    description = Column("description", String)
    price = Column("price", Float, nullable=False)
    flavor = Column("flavor", String)
    size = Column("size", String)


    def __init__(self, name: str, description: str, price: float, flavor: str , size: str ):
        self.name = name
        self.description = description
        self.price = price
        self.flavor = flavor
        self.size = size