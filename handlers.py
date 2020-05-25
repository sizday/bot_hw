from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.dispatcher.filters import Command, Text, CommandStart
from state import DoneHW
from database import User, HW, Done
import database
from keyboards import confirm_menu
from load_all import dp

db = database.DBCommands()


@dp.message_handler(CommandStart())
async def register_user(message: types.Message):
    user = await db.add_new_user()
    if user[1] == 'old':
        text = f'Вы уже зарегистрированы'
        await message.answer(text)
    else:
        text = f'Приветствую вас, {user[0].full_name}'
        await message.answer(text)


@dp.message_handler(Command("cancel"), state=DoneHW)
async def cancel(message: types.Message, state: FSMContext):
    await message.answer("Вы отменили сдачу ДЗ")
    await state.reset_state()


@dp.message_handler(Command('hw'))
async def my_hw(message: types.Message):
    all_unmade_hw = await db.done_unmade()
    for num, done in enumerate(all_unmade_hw):
        current_hw = await db.get_hw(done.homework_id)
        text = f"<b>ДЗ</b> \t№{current_hw.id}: <u>{current_hw.title}</u>\n<b>Описание:</b> {current_hw.description}\n"
        await message.answer_document(document=current_hw.file, caption=text)
    await message.answer('Выберете номер ДЗ или нажмите /cancel')
    await DoneHW.Choose.set()


@dp.message_handler(state=DoneHW.Choose)
async def choose_hw(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    try:
        hw_id = int(message.text)
    except ValueError:
        await message.answer("Неверное значение, введите число")
        return
    await message.answer(f'Пришлите решение ДЗ №{hw_id} или нажмите /cancel')
    user = await db.get_user(chat_id)
    done = await db.get_done(student_id=user.id, homework_id=hw_id)
    await state.update_data(done=done)
    await DoneHW.Push.set()


@dp.message_handler(state=DoneHW.Push, content_types=types.ContentType.DOCUMENT)
async def push_hw(message: types.Message, state: FSMContext):
    document = message.document.file_id
    data = await state.get_data()
    done: Done = data.get("done")
    done.answer = document
    await message.answer("Подтверждаете? Нажмите /cancel чтобы отменить", reply_markup=confirm_menu)
    await DoneHW.Confirm.set()


@dp.message_handler(state=DoneHW.Confirm)
async def enter_price(message: types.Message, state: FSMContext):
    data = await state.get_data()
    done: Done = data.get("done")
    await db.update_done(done.student_id, done.homework_id)
    await message.answer('ДЗ успешно отправлено')
    await state.reset_state()


@dp.message_handler(Command('all_hw'))
async def all_homework(message: types.Message):
    all_hw = await db.list_hw()
    for num, hw in enumerate(all_hw):
        text = f"<b>ДЗ</b> \t№{hw.id}: <u>{hw.title}</u>\n<b>Описание:</b> {hw.description}\n"
        await message.answer_document(document=hw.file, caption=text)
