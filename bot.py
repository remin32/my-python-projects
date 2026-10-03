import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import sqlite3
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from config import TOKEN, PROXY_URL

class NoteStates(StatesGroup):
    waiting_for_text = State()

async def main():
    def init_db():
        conn = sqlite3.connect("bot.db")
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS notes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        text TEXT NOT NULL
)
""")
        conn.commit()
        conn.close()
    init_db()

    session = AiohttpSession(proxy=PROXY_URL)
    bot = Bot(token=TOKEN, session=session)
    dp = Dispatcher()

    keyboard= ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Добавить")],
            [KeyboardButton(text="Показать")],
            [KeyboardButton(text="Удалить")],
        ],
        resize_keyboard=True
    )

#------------------------------------------------------------------------------

    def add_note(user_id, text):
        conn = sqlite3.connect("bot.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO notes (user_id, text) VALUES (?, ?)", (user_id, text))
        conn.commit()
        conn.close()

    def show_notes(user_id):
        conn = sqlite3.connect("bot.db")
        cur = conn.cursor()
        cur.execute("SELECT id, text FROM notes WHERE user_id = ?", (user_id,))
        rows = cur.fetchall()
        conn.close()
        return rows

    def delete_note(user_id, note_id):
        conn = sqlite3.connect("bot.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM notes WHERE id = ? AND user_id = ?", (note_id, user_id))
        conn.commit()
        conn.close()

#-------------------------------------------------------------
  
    async def show_user_notes(message: types.Message):
        user_id = str(message.from_user.id)
        rows = show_notes(user_id)
        if not rows:
            await message.answer("Пока заметок нет")
            return
        text = "\n".join([str(row[0]) + ". " + row[1] for row in rows])
        await message.answer(text)


    @dp.message(Command("start"))
    async def start(message: types.Message):
        await message.answer("Выбери действие:", reply_markup=keyboard)


    @dp.message(NoteStates.waiting_for_text)
    async def add(message: types.Message, state: FSMContext):
        user_id = str(message.from_user.id)
        add_note(user_id, message.text)
        await message.answer("Заметка добавлена")
        await state.clear()


    @dp.message(Command("delete"))
    async def delete(message: types.Message):
        user_id = str(message.from_user.id)
        a = message.text.split()
        if len(a) < 2 or not a[1].isdigit():
            await message.answer("Напиши номер заметки, например: /delete 2")
            return
        note_id = int(a[1])
        delete_note(user_id, note_id)
        await message.answer("Успешно удалено!")

#---------------------------------------------------------

    @dp.message(lambda message: message.text == "Добавить")
    async def add_button(message: types.Message, state: FSMContext):
        await message.answer("Напиши текст заметки:")
        await state.set_state(NoteStates.waiting_for_text)

    @dp.message(lambda message: message.text == "Показать")
    async def show_button(message: types.Message):
        await show_user_notes(message)

    @dp.message(lambda message: message.text == "Удалить")
    async def delete_button(message: types.Message):
        await message.answer("Напиши: /delete 'номер заметки'")

#-------------------------------------------------------------------------


#-------------------------------------------------------------------------

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())