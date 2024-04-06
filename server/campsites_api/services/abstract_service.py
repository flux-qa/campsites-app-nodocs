from typing import Generic, List, Optional, Tuple, Type, TypeVar

from fastapi import HTTPException
from pydantic import UUID4, BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Query, Session

from campsites_db.models import Base

ModelType = TypeVar("ModelType", bound=Base)
ModelTypeDTO = TypeVar("ModelTypeDTO", bound=BaseModel)
FilterTypeDTO = TypeVar("FilterTypeDTO", bound=BaseModel)


class AbstractService(Generic[ModelType, ModelTypeDTO, FilterTypeDTO]):
    def __init__(self, model: Type[ModelType], session: Session):
        self.model = model
        self.session = session

    def __filter(self, query: Query, filters: FilterTypeDTO) -> Query:
        # keys to exclude (sorting and pagination)
        excluded_keys = ["offset", "limit", "sort_by", "sort_dir"]
        for name in filters:
            if filters[name] is not None:
                if name in excluded_keys:
                    continue
                if name[-4:] == "__lt":
                    # greater than query
                    query = query.filter(
                        getattr(self.model, name[:-4]) <= filters[name]
                    )
                elif name[-4:] == "__gt":
                    # less than query
                    query = query.filter(
                        getattr(self.model, name[:-4]) >= filters[name]
                    )
                elif name[-4:] == "__ct":
                    # contains query
                    query = query.filter(
                        func.lower(getattr(self.model, name[:-4])).contains(
                            filters[name].lower()
                        )
                    )
                elif isinstance(filters[name], list):
                    query = query.filter(getattr(self.model, name).in_(filters[name]))
                else:
                    query = query.filter(getattr(self.model, name) == filters[name])
        return query



    def get(self, id: UUID4) -> ModelType:
        item: Optional[ModelType] = (
            self.session.query(self.model).filter_by(id=id).first()
        )
        if item is None:
            self.session.rollback()
            raise HTTPException(status_code=404, detail=f"Item with id {id} not found")
        return item


    def list(self, filters: FilterTypeDTO) -> Tuple[List[ModelType], int]:
        try:
            query = self.session.query(self.model)
            query = self.__filter(query, filters)
            query = query.order_by(
                getattr(getattr(self.model, filters["sort_by"]), filters["sort_dir"])()
            )
            num_total_results = query.count()
            query = query.limit(filters["limit"])
            query = query.offset(filters["offset"])
            result: List[ModelType] = query.all()
        except Exception:
            self.session.rollback()
        return result, num_total_results



    def create(self, item: ModelTypeDTO) -> ModelType:
        item: ModelType = self.model(**item.dict())
        self.session.add(item)
        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise HTTPException(status_code=422, detail="Item could not be created.")
        return item

    def bulk_create(self, items: List[ModelTypeDTO]) -> None:
        items: List[ModelType] = [self.model(**item.dict()) for item in items]
        self.session.add_all(items)
        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise HTTPException(status_code=422, detail="Items could not be created.")



    def update(self, id: UUID4, item: ModelTypeDTO) -> ModelType:
        db_item = self.get(id)
        if db_item is None:
            raise HTTPException(status_code=404, detail=f"Item with id {id} not found")
        for key, value in item.dict().items():
            # we want to ensure we are not overwriting the ID
            if key != "id":
                setattr(db_item, key, value)
        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
        return db_item



    def delete(self, id: UUID4) -> None:
        item = self.session.query(self.model).filter_by(id=id).first()
        if item is None:
            raise HTTPException(status_code=404, detail=f"Item with id {id} not found")
        try:
            self.session.delete(item)
            self.session.commit()
        except Exception:
            self.session.rollback()
