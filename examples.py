"""OrderingItem setup and examples"""

"""Setup"""

# 1. Import OrderingItem
from sqlalchemy_orderingitem import OrderingItem

# 2. Create session (standard)
from sqlalchemy import Column, ForeignKey, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)

    # 3. Declare orderinglist relationships
    children = relationship(
        'Child', 
        backref='parent',
        order_by='Child.index',
        collection_class=ordering_list('index')
    )
    orderingitem_children = relationship(
        'OrderingItemChild', 
        backref='parent',
        order_by='OrderingItemChild.index',
        collection_class=ordering_list('index')
    )

# This model is for demonstrating behavior without the OrderingItem subclass
class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parent.id'))
    index = Column(Integer)


# 4. Subclass OrderingItem for children of orderinglist relationships
class OrderingItemChild(OrderingItem, Base):
    __tablename__ = 'ordering_item_child'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parent.id'))
    index = Column(Integer)


# 5. Create the database tables (standard)
Base.metadata.create_all(engine)

"""Examples"""

p = Parent()
c = Child()
oic = OrderingItemChild()
session.add_all([p, c, oic])
session.commit()

"""Example 1: Setting a child's parent attribute to Parent instance"""

c.parent = p
print(c.index)
oic.parent = p
print(oic.index)

"""Example 2: Setting a child's parent attribute to None"""

p.children = [c]
c.parent = None
print(c.index)
p.orderingitem_children = [oic]
oic.parent = None
print(oic.index)