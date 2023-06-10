from aiogram import Bot, Dispatcher, executor
from Token import Token
from Keyboard import *
from Text import *
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from loader import Start
import datetime

bot = Bot(Token)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    photo = open('ЛОГО.png', 'rb')
    user = message.from_user.first_name
    await bot.send_photo(message.chat.id, photo)
    await bot.send_message(message.chat.id, f"Привет👋, {user}! " + hello, reply_markup=kb)

@dp.message_handler(commands=["help"])
async def help_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=help_text, reply_markup=kb)

@dp.message_handler(lambda message: message.text == "Оставить отзыв📝")
async def record_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Мы рады, что вы захотели оставить отзыв📝. Напишите свое имя",reply_markup=anon_kb)
    await Start.start_name.set()

@dp.message_handler(state=Start.start_name)
async def name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
            data["name1"] = message.text
            name = data["name1"]
            if name != "Оставить отзыв📝":
                await bot.send_message(message.from_user.id,
                               text=f'Спасибо за ответ\nВас зовут: {name}, напишите свой отзыв')

                await Start.start_number.set()
            else:
                await message.answer('Вы вернулись на главное меню', reply_markup=kb)

@dp.message_handler(state=Start.start_number)
async def number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['number1'] = message.text
        number = data['number1']
        ikb = InlineKeyboardMarkup(row_width=1)
        ib1 = InlineKeyboardButton(text='Вернуться на главное меню🔙', callback_data='back')

        ikb.add(ib1)
        await bot.send_message(message.from_user.id,
                               text=f'Спасибо за ответ!\nВаш отзыв: {number}, если все верно напишите любое слово, если нет просьба нажать на кнопку Вернуться на Главную, чтобы начать с начала.',
                               reply_markup=ikb)
        await Start.start_timetable.set()


@dp.callback_query_handler(text='back', state=Start.start_timetable)
async def stop_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('Вы вернулись на главное меню', reply_markup=kb)
    await state.finish()


@dp.message_handler(state=Start.start_timetable)
async def timetable(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Общая оценка:",
                               reply_markup=ikb)
        await Start.start_timetable_1.set()


@dp.callback_query_handler(text='EX', state=Start.start_timetable_1)
async def vt_callback(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        await callback.message.answer(ex, reply_markup=kb_dop)
        await callback.answer('Спасибо за отзыв!')
        filePath = "Otziv.txt"
        file = open(filePath, 'a', encoding="utf-8")
        today = datetime.datetime.today()
        file.write('\n' + "************\nИмя:" + data['name1']  + '\n')
        file.write('Отзыв:' + data['number1'] + '\n')
        file.write('Общая оценка: 5\n'  + today.strftime("%Y-%m-%d-%H.%M.%S") + '\n')
        file.close()
        await state.finish()


@dp.callback_query_handler(text='GO', state=Start.start_timetable_1)
async def vt_callback(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        await callback.message.answer(good, reply_markup=kb)
        await callback.answer('Спасибо за отзыв!')
        filePath = "Otziv.txt"
        file = open(filePath, 'a', encoding="utf-8")
        today = datetime.datetime.today()
        file.write('\n' + "************\nИмя:" + data['name1'] + '\n')
        file.write('Отзыв:' + data['number1'] + '\n')
        file.write('Общая оценка: 4\n'  + today.strftime("%Y-%m-%d-%H.%M.%S") + '\n')
        file.close()
        await state.finish()

@dp.callback_query_handler(text='SAT', state=Start.start_timetable_1)
async def vt_callback(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        await callback.message.answer(sat, reply_markup=kb)
        await callback.answer('Спасибо за отзыв!')
        filePath = "Otziv.txt"
        file = open(filePath, 'a', encoding="utf-8")
        today = datetime.datetime.today()
        file.write('\n' + "************\nИмя:" + data['name1'] + '\n')
        file.write('Отзыв:' + data['number1'] + '\n')
        file.write('Общая оценка: 3\n' + today.strftime("%Y-%m-%d-%H.%M.%S") + '\n')
        file.close()
        await state.finish()

@dp.callback_query_handler(text='BAD', state=Start.start_timetable_1)
async def vt_callback(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        await callback.message.answer(bad, reply_markup=kb)
        await callback.answer('Спасибо за отзыв!')
        filePath = "Otziv.txt"
        file = open(filePath, 'a', encoding="utf-8")
        today = datetime.datetime.today()
        file.write('\n' + "************\nИмя:" + data['name1'] + '\n')
        file.write('Отзыв:' + data['number1'] + '\n')
        file.write('Общая оценка: 2\n' + today.strftime("%Y-%m-%d-%H.%M.%S") + '\n')
        file.close()
        await state.finish()

@dp.callback_query_handler(text='BAD-', state=Start.start_timetable_1)
async def vt_callback(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        await callback.message.answer(very_bad, reply_markup=kb)
        await callback.answer('Спасибо за отзыв!')
        filePath = "Otziv.txt"
        file = open(filePath, 'a', encoding="utf-8")
        today = datetime.datetime.today()
        file.write('\n' + "************\nИмя:" + data['name1'] + '\n')
        file.write('Отзыв:' + data['number1'] + '\n')
        file.write('Общая оценка: 1\n' + today.strftime("%Y-%m-%d-%H.%M.%S") + '\n')
        file.close()
        await state.finish()

@dp.message_handler(lambda message: message.text == "Получить секретный уровень 🚗")
async def about_information(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text=secret_level, reply_markup=kb)


@dp.message_handler(lambda message: message.text == "Написать разработчику📮")
async def about_help(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    operator1 = types.InlineKeyboardButton("Куликов Иван👨‍💻", url='https://t.me/E_0n9in')
    markup.add(operator1)
    await message.answer(razrab, reply_markup=markup)


@dp.message_handler(lambda message: message.text == "/information")
async def about_information(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text=info, reply_markup=kb)

@dp.message_handler(lambda message: message.text == "Часто задаваемые вопросы❓")
async def about_help(message: types.Message):
    await message.reply('Часто задаваемые вопросы:', reply_markup=faq)

@dp.callback_query_handler(text_contains='faq_')
async def faqqq(call: types.CallbackQuery):
    if call.data and call.data.startswith("faq_"):
        code = call.data[-1:]
        if code.isdigit():
            code = int(code)
        if code == 1:
            await call.message.edit_text(otvet1, reply_markup=faq)
        if code == 2:
            await call.message.edit_text(otvet2, reply_markup=faq)
        if code == 3:
            await call.message.edit_text(otvet3, reply_markup=faq)
        else:
            await bot.answer_callback_query(call.id)

@dp.message_handler(content_types=['sticker'])
async def send_sticker(message: types.Message):
    sticker_id = message.sticker.file_id
    await bot.send_sticker(message.chat.id, sticker_id)

@dp.message_handler(content_types=['voice'])
async def send_voice(message: types.Message):
    await bot.send_message(message.from_user.id, text='К сожалению, мой функционал не способен распознать Ваш голос')

if __name__ == "__main__":
    executor.start_polling(dispatcher=dp)