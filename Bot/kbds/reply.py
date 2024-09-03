from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

keyboard_start = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Сохранить фото',
                callback_data='save_photo'
            )
        ]
    ]
)

add_user = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Добавить пользователя',
                callback_data='add'
            )
        ]
    ]
)