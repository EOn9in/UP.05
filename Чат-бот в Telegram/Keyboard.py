from aiogram.types import InlineKeyboardButton,ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram import types

# ******Клавиатура Основа********
kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
razrab = types.KeyboardButton("Написать разработчику📮")
otziv = types.KeyboardButton("Оставить отзыв📝")
FAQ = types.KeyboardButton("Часто задаваемые вопросы❓")
kb.add(otziv, razrab, FAQ)

#Клавиатура FAQ
faq = types.InlineKeyboardMarkup(resize_keyboard=True)
faq_1 = InlineKeyboardButton(text="На каком языке программирования написана игра?", callback_data="faq_1")
faq_2 = InlineKeyboardButton(text="Существуют ли в игре секретные уровни?", callback_data="faq_2")
faq_3 = InlineKeyboardButton(text="Что делать если невозможно пройти уровень?", callback_data="faq_3")
faq.add(faq_1, faq_2, faq_3)

#Клавиатура отзыв/оценка
ikb = InlineKeyboardMarkup(row_width=2)
ib1 = InlineKeyboardButton(text='5', callback_data='EX')
ib2 = InlineKeyboardButton(text='4', callback_data='GO')
ib3 = InlineKeyboardButton(text='3', callback_data='SAT')
ib4 = InlineKeyboardButton(text='2', callback_data='BAD')
ib5 = InlineKeyboardButton(text='1', callback_data='BAD-')
ikb.add(ib1, ib2, ib3, ib4, ib5)

#Получение доп.уровня
kb_dop = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
level = types.KeyboardButton("Получить секретный уровень 🚗")
kb_dop.add(level)

#Анонимный отзыв
anon_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
anon_btn = types.KeyboardButton("Анонимно 🥷")
anon_kb.add(anon_btn)