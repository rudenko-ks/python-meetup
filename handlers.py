from enum import Enum

from more_itertools import chunked
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    Dispatcher,
)

from menu_blocks import start_block, programs_block, performance_block
from settings import WELCOME_MESSAGE, TELEGRAM_SPEAKER_CHAT_ID, REPLY_TO_THIS_MESSAGE, WRONG_REPLY

class ConversationPoints(Enum):
    MENU = 0
    PROGRAM_SCHEDULE = 1
    PROGRAM_DESCRIPTION = 2
    EXIT_FROM_DESCRIPTION = 3
    CHOOSE_PROGRAM_FOR_QUESTION = 4
    PERFORMANCE_SPEAKERS = 5
    CHOOSE_PERFORMANCE_SPEAKER = 6
    QUESTION_FOR_SPEAKER = 7


def start(update: Update, context: CallbackContext) -> int:
    start_block(update=update)
    return ConversationPoints.MENU.value


def program(update: Update, context: CallbackContext) -> int:
    programs_block(update=update)
    return ConversationPoints.PROGRAM_SCHEDULE.value


def schedules(update: Update, context: CallbackContext) -> int:
    user_choice = update.message.text
    schedules = [
        {
            "time": "09:00",
            "performance_name": "Регистрация"
        },
        {
            "time": "10:00",
            "performance_name": "Первое выступление"
        },
        {
            "time": "10:30",
            "performance_name": "Второе выступление"
        },
    ]

    if user_choice == "Главное меню":
        start_block(update=update)
        return ConversationPoints.MENU.value

    if user_choice == "Назад":
        performances, text = performance_block(update, schedules, context)

        reply_keyboard = list(chunked(performances, 2))
        update.message.reply_text(
            text=text,
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard,
                one_time_keyboard=True,
                resize_keyboard=True
            )
        )
        return ConversationPoints.PROGRAM_DESCRIPTION.value

    performances = []
    for perforamnce_id, performance in enumerate(schedules, start=1):
        performance_name = performance["performance_name"]
        performance_time = performance["time"]
        performance = f'{perforamnce_id}.{performance_name}\n' \
                      f'Время: {performance_time}\n'
        performances.append(performance)

    text = f"У программы {user_choice} будут следующие выступления:\n\n" \
           f"{''.join(performances)}\n" \
           f"Про какое выступление вам бы хотелось узнать побольше?"

    performances = [performance["performance_name"] for performance in
                    schedules]
    performances.append("Назад")

    reply_keyboard = list(chunked(performances, 2))
    update.message.reply_text(
        text=text,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            resize_keyboard=True
        )
    )
    context.user_data["performance"] = user_choice
    return ConversationPoints.PROGRAM_DESCRIPTION.value


def get_program_description(update: Update, context: CallbackContext) -> int:
    user_choice = update.message.text

    if user_choice == "Назад":
        programs = [f'Программа №{program}' for program in range(1, 4)]
        programs_text = [f"{program_number}. {program}\n" for
                         program_number, program in
                         enumerate(programs, start=1)]
        programs.append("Главное меню")

        update.message.reply_text(
            'Сегодня у нас проходят следующие программы:\n\n'
            f'{"".join(programs_text)}\n\n'
            f'Какая программа вас заинтересовала?',
            reply_markup=ReplyKeyboardMarkup(
                keyboard=list(chunked(programs, 2)),
                one_time_keyboard=True,
                resize_keyboard=True
            ),
        )
        return ConversationPoints.PROGRAM_SCHEDULE.value

    reply_keyboard = [["Главное меню", "Назад"]]
    update.message.reply_text(
        f"Описание программы {user_choice}",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            resize_keyboard=True
        )
    )
    return ConversationPoints.EXIT_FROM_DESCRIPTION.value


def question_for_speaker(update: Update, context: CallbackContext) -> int:
    programs = [f'Программа №{program}' for program in range(1, 4)]
    programs.append("Главное меню")

    update.message.reply_text(
        "Спикеру какой программы у вас есть вопрос?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=list(chunked(programs, 2)),
            one_time_keyboard=True,
            resize_keyboard=True
        ),
    )
    return ConversationPoints.CHOOSE_PROGRAM_FOR_QUESTION.value


def get_performance_times(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [["12:00", "14:00"]]
    context.user_data["performance"] = update.message.text

    update.message.reply_text(
        "Когда было выступление?",
         reply_markup=ReplyKeyboardMarkup(
             keyboard=reply_keyboard,
             one_time_keyboard=True,
             resize_keyboard=True
         )
    )
    return ConversationPoints.PERFORMANCE_SPEAKERS.value


def get_performance_speakers(update: Update, context: CallbackContext) -> int:
    context.user_data["time"] = update.message.text
    speakers = [f"{speaker_number}. Выступающий #{speaker_number}\n" for speaker_number in range(1, 5)]
    reply_keyboard = list(chunked(speakers, 1))
    reply_keyboard.append(["Назад"])
    update.message.reply_text(
        text=f"На программе {context.user_data['performance']} в "
             f"{context.user_data['time']} выступали:\n\n",
        reply_markup=ReplyKeyboardMarkup(
             keyboard=reply_keyboard,
             one_time_keyboard=True,
             resize_keyboard=True
         )
    )
    return ConversationPoints.QUESTION_FOR_SPEAKER.value


def question(update: Update, context: CallbackContext) -> int:
    if update.message.text == "Назад":
        programs = [f'Программа №{program}' for program in range(1, 4)]
        programs.append("Главное меню")

        update.message.reply_text(
            "Спикеру какой программы у вас есть вопрос?",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=list(chunked(programs, 2)),
                one_time_keyboard=True,
                resize_keyboard=True
            ),
        )
        return ConversationPoints.CHOOSE_PROGRAM_FOR_QUESTION.value

    update.message.reply_text(
        text=f"Задайте свой вопрос:"
    )
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "Действие отменено",
        reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def forward_to_speaker(update: Update, context: CallbackContext):
    forwarded = update.message.forward(chat_id=TELEGRAM_SPEAKER_CHAT_ID)
    # For forwarded messages check sender of the original message
    # For users who have banned the link to their account in forwarded messages.
    # Settings -> Privacy and Security -> Forwaded Messages -> Set "My Contacts"
    # Solution: Insert the id of the original chat directly into the text of the message sent from there, so that later it can be parsed and retrieved
    if not forwarded.forward_from:
        context.bot.send_message(
            chat_id=TELEGRAM_SPEAKER_CHAT_ID,
            reply_to_message_id=forwarded.message_id,
            text=f'{update.message.from_user.id}\n{REPLY_TO_THIS_MESSAGE}'
        )


def forward_to_user(update: Update, context: CallbackContext):
    user_id = None
    # If user has allowed link to account in the forwarded message
    if update.message.reply_to_message.forward_from:
        user_id = update.message.reply_to_message.forward_from.id
    # If not allowed then parse his user_id
    elif REPLY_TO_THIS_MESSAGE in update.message.reply_to_message.text:
        try:
            user_id = int(update.message.reply_to_message.text.split('\n')[0])
        except ValueError:
            user_id = None
    if user_id:
        # Send answer to user
        context.bot.copy_message(
            message_id=update.message.message_id,
            chat_id=user_id,
            from_chat_id=update.message.chat_id
        )
    else:
        # If speaker reply to a NOT bot reply under a message forwarded by a user.
        context.bot.send_message(
            chat_id=TELEGRAM_SPEAKER_CHAT_ID,
            text=WRONG_REPLY
        )


def setup_dispatcher(dispatcher) -> Dispatcher:
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start)
        ],
        states={
            ConversationPoints.MENU.value: [
                MessageHandler(
                    Filters.regex('^(📆 Программа)$'),
                    program
                ),
                MessageHandler(
                    Filters.regex('^(❔Задать вопрос спикеру)$'),
                    question_for_speaker
                )
            ],
            ConversationPoints.PROGRAM_SCHEDULE.value: [
                MessageHandler(
                    Filters.text,
                    schedules
                )
            ],
            ConversationPoints.PROGRAM_DESCRIPTION.value: [
                MessageHandler(
                    Filters.text,
                    get_program_description
                )
            ],
            ConversationPoints.EXIT_FROM_DESCRIPTION.value: [
                MessageHandler(
                    Filters.regex('^(Главное меню)$'),
                    start
                ),
                MessageHandler(
                    Filters.regex('^(Назад)$'),
                    schedules
                ),
            ],
            ConversationPoints.CHOOSE_PROGRAM_FOR_QUESTION.value: [
                MessageHandler(
                    Filters.regex('^(Главное меню)$'),
                    start
                ),
                MessageHandler(
                    Filters.text,
                    get_performance_times
                ),
            ],
            ConversationPoints.PERFORMANCE_SPEAKERS.value: [
                MessageHandler(
                    Filters.text,
                    get_performance_speakers
                ),
            ],
            ConversationPoints.QUESTION_FOR_SPEAKER.value: [
                MessageHandler(
                    Filters.text,
                    question
                ),
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)
    #dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.chat(TELEGRAM_SPEAKER_CHAT_ID) & Filters.reply, forward_to_user))
    dispatcher.add_handler(MessageHandler(Filters.chat_type.private, forward_to_speaker))
    return dispatcher
