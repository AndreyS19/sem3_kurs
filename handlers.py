from contextlib import suppress
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from app.buttons import start_dial, end_dial
from aiogram import types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from app.data_processing import send_message, send_message_dialogue, data_set, data_reset, extract_text,data_reset_closing

dp = Router()
class MainStates(StatesGroup):
    dialogueState = State("end")
@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) :
    await state.update_data(dialogueState='end')
    await closeInlines(message)
    data_reset(message.from_user.id)
    await message.answer(f"Привет, {message.from_user.full_name} ! "
                         "добро пожаловать в бот-учитель по программированию "
                         "задай интересующий тебя вопрос или общайся с ботом в режиме диалога", reply_markup=start_dial)
@dp.callback_query(F.data == 'start')
async def button_press(callback: CallbackQuery,state: FSMContext):
    await callback.message.edit_reply_markup(callback.message.text)
    await callback.message.answer("Диалог начат",reply_markup=end_dial)
    #await state.update_data(msgId=msg.message_id)
    await state.update_data(dialogueState='start')
@dp.callback_query(F.data == 'end')
async def button_press(callback: CallbackQuery,state: FSMContext):
    await callback.message.edit_reply_markup(callback.message.text)
    await callback.message.answer("Диалог закончен", reply_markup=start_dial)
    #await state.update_data(msgId=msg.message_id)
    await state.update_data(dialogueState='end')
    data_reset(callback.message.chat.id)
@dp.message()
async def ai_message_handler(message: types.Message,state: FSMContext) :

    try:
        data = await state.get_data()
        await closeInlines(message)
        await message.bot.send_chat_action(message.chat.id, "typing")
        if message.text:
            try:

                if data.get("dialogueState")=='start':
                    print("идет диалог")
                    data_set(message.from_user.id,message.text,"user")
                    msg=await message.answer(extract_text(send_message_dialogue(message.from_user.id)), reply_markup=end_dial)
                    data_set(message.from_user.id,msg.text,"assistant")
                else:
                    await message.answer(extract_text(send_message(message.text)),reply_markup=start_dial)
                #await state.update_data(msgId=msg.message_id)
                print(await state.get_data())
            except TelegramBadRequest:
                if data.get("dialogue")=='start':
                    await message.answer("Ошибка, напишите позже. " ,reply_markup=end_dial)
                else:
                    await message.answer("Ошибка, напишите позже. ",reply_markup=start_dial)
                #await state.update_data(msgId=msg.message_id)
        else:
            if data.get("dialogue") == 'start':
                await message.answer("Я могу отвечать только на текстовые сообщения!", reply_markup=end_dial)
            else:
                await message.answer("Я могу отвечать только на текстовые сообщения!", reply_markup=start_dial)
            #await state.update_data(msgId=msg.message_id)
    except TypeError:
        await message.answer("Произошла ошибка при обработке сообщения.")
async def closeInlines(message: types.Message ):
    with suppress(TelegramBadRequest):
        await message.bot.edit_message_reply_markup(
            message.from_user.id, message.message_id-1, reply_markup=None
        )