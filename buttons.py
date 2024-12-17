from aiogram.types import  InlineKeyboardButton,InlineKeyboardMarkup
start_dial_but = [
    [InlineKeyboardButton(text="Начать диалог",callback_data="start")],
]
end_dial_but = [
    [InlineKeyboardButton(text="Закончить диалог",callback_data="end")]
]
start_dial=InlineKeyboardMarkup(inline_keyboard=start_dial_but)
end_dial=InlineKeyboardMarkup(inline_keyboard=end_dial_but)