# SQLAlchemy-OrderingItem

SQLAlchemy-OrderingItem provides an `OrderingItem` base for children of [`orderinglist`](https://docs.sqlalchemy.org/en/13/orm/extensions/orderinglist.html) relationships. Children of `orderinglist` relationships will exhibit more intuitive behavior when setting their parent attribute.

## Installation

```
$ pip install sqlalchemy-orderingitem
```

## Quickstart

```python
from sqlalchemy_orderingitem import OrderingItem

from sqlalchemy import Column, ForeignKey, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import sessionmaker, relationship

# standard session creation
engine = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)

    # declare orderinglist relationships
    children = relationship(
        'Child', 
        backref='parent',
        order_by='Child.index',
        collection_class=ordering_list('index')
    )


# subclass OrderingItem for children of orderinglist relationships
class Child(OrderingItem, Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parent.id'))
    index = Column(Integer)


# create database tables and instantiate parent and child
Base.metadata.create_all(engine)
parent = Parent()
child = Child()
session.add_all([parent, child])
session.commit()

# example 1: setting a child's parent attribute to Parent object
# we expect the child's index to be 0
child.parent = parent
print(child.index)

# example 2: setting a child's parent attribute to None
# we expect the child's index to be None
parent.children = [c]
child.parent = None
print(child.index)
```

Out:

```
0
None
```

If `Child` did not subclass `OrderingItem`, we would observe the following unintuitive output:

```
None
0
```

## Citation

```
@software{bowen2020sqlalchemy-orderingitem,
  author = {Dillon Bowen},
  title = {SQLAlchemy-OrderingItem},
  url = {https://dsbowen.github.io/sqlalchemy-orderingitem/},
  date = {2020-06-05},
}
```

## License

Users must cite this package in any publications which use it.

It is licensed with the MIT [License](https://github.com/dsbowen/sqlalchemy-orderingitem/blob/master/LICENSE).