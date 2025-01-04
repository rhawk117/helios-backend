from typing import TypeVar, Generic, Type, Optional, List, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

ModelT = TypeVar("ModelT")

class CRUDService(Generic[ModelT]):
    '''CRUD boilerplate with minimal abstraction'''

    def __init__(self, model: Type[ModelT]):
        self.model: Type[ModelT] = model

    async def delete_model(self, db: AsyncSession, db_model: ModelT) -> None:
        '''deletes a model from the database'''
        await db.delete(db_model)
        await db.commit()

    async def insert_model(
        self,  
        model_obj: ModelT,
        db: AsyncSession,
        commit: bool = True,
        refresh: bool = False
    ) -> None:
        '''inserts a model into the database'''
        db.add(model_obj)
        if not commit:
            return
        await db.commit()
        if refresh:
            await db.refresh(model_obj)

    async def get_by(
        self,
        predicate: Any,
        session: AsyncSession,
        options: Optional[List] = None
    ) -> Optional[ModelT]:
        query = select(self.model).filter(predicate)
        if options:
            for option in options:
                query = query.options(option)

        result = await session.execute(query)
        return result.scalars().first()

    async def get_all(self, db: AsyncSession) -> List[ModelT]:
        result = await db.execute(select(self.model))
        return list(result.scalars().all())

    async def get_limited(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        options: Optional[List] = None
    ) -> List[ModelT]:
        query = select(self.model).offset(skip).limit(limit)
        if options:
            for option in options:
                query = query.options(option)

        result = await db.execute(query)
        return list(result.scalars().all())

    async def create(self, db: AsyncSession, obj_in: dict) -> ModelT:
        '''creates a new model using the pydantic model schema'''
        db_model = self.model(**obj_in)
        await self.insert_model(db_model, db, commit=True, refresh=True)
        return db_model

    async def update(
        self,
        db: AsyncSession,
        db_model: ModelT,
        obj_in: dict
    ) -> ModelT:
        '''updates a model using the pydantic model schema'''
        for field, value in obj_in.items():
            if hasattr(db_model, field):
                setattr(db_model, field, value)

        await db.commit()
        await db.refresh(db_model)
        return db_model
    
    async def total_records(self, db: AsyncSession) -> int:
        '''returns the total number of records in the database'''
        ...