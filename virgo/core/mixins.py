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

    # FILTER
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

    # FIRST MATCH
    @classmethod
    def first_by(cls, **kwargs):
        session = SessionLocal()
        result = session.query(cls).filter_by(**kwargs).first()
        session.close()
        return result

    # COUNT
    @classmethod
    def count(cls, **kwargs):
        session = SessionLocal()
        if kwargs:
            total = session.query(cls).filter_by(**kwargs).count()
        else:
            total = session.query(cls).count()
        session.close()
        return total
    
    

