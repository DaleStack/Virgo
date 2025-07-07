from virgo.core.database import SessionLocal
from sqlalchemy.orm import joinedload

class BaseModelMixin:
    # CREATE
    @classmethod
    def create(cls, **kwargs):
        session = SessionLocal()
        obj = cls(**kwargs)
        session.add(obj)
        session.commit()
        session.refresh(obj)
        session.close()
        return obj

    # UPDATE
    def update(self, **kwargs):
        session = SessionLocal()
        for key, value in kwargs.items():
            setattr(self, key, value)
        session.add(self)
        session.commit()
        session.refresh(self)
        session.close()
        return self

    # DELETE
    def delete(self):
        session = SessionLocal()
        session.delete(self)
        session.commit()
        session.close()

    # GET BY ID
    @classmethod
    def get_by_id(cls, id):
        session = SessionLocal()
        obj = session.get(cls, id)
        session.close()
        return obj
    
    # GET BY ID WRAPPER
    @classmethod
    def get(cls, id):
        return cls.get_by_id(id)

    # ALL
    @classmethod
    def all(cls, load: list = None):
        session = SessionLocal()
        query = session.query(cls)
        if load:
            for relation in load:
                query = query.options(joinedload(getattr(cls, relation)))  # FIX
        results = query.all()
        session.close()
        return results

    # FILTER BY
    @classmethod
    def filter_by(cls, load: list = None, **kwargs):
        session = SessionLocal()
        query = session.query(cls)
        if load:
            for relation in load:
                query = query.options(joinedload(getattr(cls, relation)))  # FIX
        results = query.filter_by(**kwargs).all()
        session.close()
        return results
    
    # ORDER BY
    @classmethod
    def order_by(cls, field, direction="asc", load=None):
        session = SessionLocal()
        query = session.query(cls)

        if load:
            for relation in load:
                query = query.options(joinedload(getattr(cls, relation)))

        column = getattr(cls, field)
        if direction == "desc":
            column = column.desc()

        results = query.order_by(column).all()
        session.close()
        return results

    # FIRST MATCH
    @classmethod
    def first_by(cls, **kwargs):
        session = SessionLocal()
        result = session.query(cls).filter_by(**kwargs).first()
        session.close()
        return result
    
    # FILTER + ORDER_BY
    @classmethod
    def filter_and_order_by(cls, *, load=None, order_field=None, direction="asc", **filters):
        session = SessionLocal()
        query = session.query(cls)

        if load:
            for relation in load:
                query = query.options(joinedload(getattr(cls, relation)))

        if filters:
            query = query.filter_by(**filters)

        if order_field:
            column = getattr(cls, order_field)
            if direction == "desc":
                column = column.desc()
            query = query.order_by(column)

        results = query.all()
    
    

