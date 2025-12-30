from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create(self, telegram_id: int, **defaults):
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()

        if user:
            for key, value in defaults.items():
                if hasattr(user, key):
                    setattr(user, key, value)
        else:
            user = User(telegram_id=telegram_id, **defaults)
            self.session.add(user)

        await self.session.commit()
        return user