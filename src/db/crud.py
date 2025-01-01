from typing import TypeVar, Generic, Type, Optional, List, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.future import select

ModelT = TypeVar("ModelT")
    

class CRUDService(Generic[ModelT]):
    """
    CRUD Wrapper for SQLAlchemy Models, with minimal abstraction
    Example:
        class UserService(CRUDService[UserModel]):
            def __init__(self):
                super().__init__(UserModel)
    """

    def __init__(self, model: Type[ModelT]):
        self.model: Type[ModelT] = model

    async def delete_model(self, session: AsyncSession, db_model: ModelT) -> None:
        """
        deletes model from the database and commits the change  

        Args:
            session: AsyncSession 
            db_model: model instance to delete
        Returns:
            bool: True if deletion was successful
        """
        await session.delete(db_model)
        await session.commit()

    async def insert_model(
        self,  model_obj: ModelT,
        session: AsyncSession,
        commit: bool = True,
        refresh: bool = False
    ) -> None:
        '''inserts a model into the database'''
        session.add(model_obj)
        if not commit:
            return
        await session.commit()
        if refresh:
            await session.refresh(model_obj)

    async def get_by(
        self,
        predicate: Any,
        session: AsyncSession,
        options: Optional[List] = None
    ) -> Optional[ModelT]:
        """
        gets a single model from the ModelT that meets the predicates
        criteria.

        Args:
            session: AsyncSession for database operations
            predicate: SQLAlchemy filter condition (e.g UserModel.id == 1)
            options: Optional list of joinedload/selectinload options (e.g [joinedload(UserModel.user_data)])
        """
        query = select(self.model).filter(predicate)
        if options:
            for option in options:
                query = query.options(option)

        result = await session.execute(query)
        return result.scalars().first()

    async def get_all(self, session: AsyncSession) -> List[ModelT]:
        result = await session.execute(select(self.model))
        return list(result.scalars().all())

    async def get_all_limit(
        self,
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        options: Optional[List] = None
    ) -> List[ModelT]:
        """
        Retrieve all records with pagination support.

        Args:
            session: AsyncSession for database operations
            skip: Number of records to skip
            limit: Maximum number of records to return
            options: Optional list of joinedload/selectinload options
        """
        query = select(self.model).offset(skip).limit(limit)
        if options:
            for option in options:
                query = query.options(option)

        result = await session.execute(query)
        return list(result.scalars().all())

    async def create(self, session: AsyncSession, obj_in: dict) -> ModelT:
        """
        accepts a pydantic model dump and creates a model instance in the database.

        Args:
            session: AsyncSession for database operations
            obj_in: Dictionary containing model attributes
        """
        db_model = self.model(**obj_in)
        await self.insert_model(db_model, session, commit=True, refresh=True)
        return db_model

    async def update(
        self,
        session: AsyncSession,
        db_model: ModelT,
        obj_in: dict
    ) -> ModelT:
        """
        updates the properties of an existing model instance in the database.

        Args:
            session: AsyncSession for database operations
            db_model: Existing database object to update
            obj_in: Dictionary containing updated attributes
        """
        for field, value in obj_in.items():
            if hasattr(db_model, field):
                setattr(db_model, field, value)

        await session.commit()
        await session.refresh(db_model)
        return db_model
