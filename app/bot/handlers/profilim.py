
import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy import create_engine, String, BigInteger
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    age: Mapped[int] = mapped_column(BigInteger, nullable=True)
    gender: Mapped[str] = mapped_column(String(10), nullable=True)
    height: Mapped[int] = mapped_column(BigInteger, nullable=True)
    weight: Mapped[int] = mapped_column(BigInteger, nullable=True)

Base.metadata.create_all(engine)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

class ProfileStates(StatesGroup):
    age = State()
    gender = State()
    height = State()
    weight = State()

def get_gender_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Erkak"), KeyboardButton(text="Ayol")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def get_user(telegram_id):
    return session.query(User).filter_by(telegram_id=telegram_id).first()

def create_or_update_user(telegram_id: int, username: str, field: str = None, value = None):
    user = get_user(telegram_id)
    if not user:
        user = User(telegram_id=telegram_id, username=username)
        session.add(user)
        session.commit()

    if field and value is not None:
        setattr(user, field, value)
        session.commit()
    return user

@dp.message(F.text == "profilim")
async def profile_handler(message: types.Message, state: FSMContext):
    user = create_or_update_user(message.from_user.id, message.from_user.username)

    if not user.age:
        await message.answer("📅 Yoshingizni kiriting:", reply_markup=ReplyKeyboardRemove())
        await state.set_state(ProfileStates.age)
        return

    if not user.gender:
        await message.answer("👤 Jinsingizni tanlang:", reply_markup=get_gender_keyboard())
        await state.set_state(ProfileStates.gender)
        return

    if not user.height:
        await message.answer("📏 Bo'yingizni kiriting (sm):", reply_markup=ReplyKeyboardRemove())
        await state.set_state(ProfileStates.height)
        return

    if not user.weight:
        await message.answer("⚖️ Vazningizni kiriting (kg):", reply_markup=ReplyKeyboardRemove())
        await state.set_state(ProfileStates.weight)
        return

    await message.answer(
        f"✅ Profilingiz to'liq:\n"
        f"Yosh: {user.age}\n"
        f"Jins: {user.gender}\n"
        f"Bo'y: {user.height} sm\n"
        f"Vazn: {user.weight} kg"
    )

@dp.message(ProfileStates.age)
async def age_handler(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Iltimos, son kiriting.")
        return
    create_or_update_user(message.from_user.id, message.from_user.username, 'age', int(message.text))
    await state.set_state(ProfileStates.gender)
    await message.answer("👤 Jinsingizni tanlang:", reply_markup=get_gender_keyboard())

@dp.message(ProfileStates.gender)
async def gender_handler(message: types.Message, state: FSMContext):
    if message.text not in ["Erkak", "Ayol"]:
        await message.answer("Iltimos, tugmalardan birini tanlang.")
        return
    create_or_update_user(message.from_user.id, message.from_user.username, 'gender', message.text)
    await state.set_state(ProfileStates.height)
    await message.answer("📏 Bo'yingizni kiriting (sm):", reply_markup=ReplyKeyboardRemove())

@dp.message(ProfileStates.height)
async def height_handler(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Iltimos, son kiriting.")
        return
    create_or_update_user(message.from_user.id, message.from_user.username, 'height', int(message.text))
    await state.set_state(ProfileStates.weight)
    await message.answer("⚖️ Vazningizni kiriting (kg):", reply_markup=ReplyKeyboardRemove())

@dp.message(ProfileStates.weight)
async def weight_handler(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Iltimos, son kiriting.")
        return
    create_or_update_user(message.from_user.id, message.from_user.username, 'weight', int(message.text))
    await state.clear()
    user = get_user(message.from_user.id)
    await message.answer(
        f"✅ Profilingiz saqlandi:\n"
        f"Yosh: {user.age}\n"
        f"Jins: {user.gender}\n"
        f"Bo'y: {user.height} sm\n"
        f"Vazn: {user.weight} kg"
    )

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
