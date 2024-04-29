import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.utils import markdown as md
from aiogram.enums import ParseMode
import config
from helper import md_quote, valid_answer, get_correct_answer, md_bold
from task_handler import TaskManager
from replier import *
from db_handler import DataBase
from user_handler import User, UserService
import atexit

dp = Dispatcher()
database = DataBase()
user_service = UserService(database)
task_manager = TaskManager(database)



@dp.message(CommandStart())
async def handle_start(message: types.Message):
	text = get_greetings(message.from_user.full_name)
	user_service.create_user(message.from_user.id, message.from_user.full_name)
	await message.answer(text=text)


# @dp.message(Command('get_users'))
# async def handle_get_users(message: types.Message):
# 	user_service.create_user(message.from_user.id, message.from_user.full_name)
# 	users = database.get_users()
# 	await message.answer(text='; '.join(users))


@dp.message(Command('help'))
async def handle_help(message: types.Message):
	text = get_help_text()
	await message.answer(text=text)


@dp.message(Command('task'))
async def send_task(message: types.Message):
	user = user_service.get_user(message.from_user.id, message.from_user.full_name)
	new_task_info, task_id = task_manager.get_new_task()
	user_service.set_new_task(user.user_id, task_id)
	options = task_manager.form_task(new_task_info)
	text = format_task(options)
	await message.answer(text=text)


# @dp.message(Command('why'))
# async def ask_why(message: types.Message):
# 	# TODO: make the bot send additional info about given words
# 	if not current_task['is_assigned']:
# 		await message.answer(text=md.text(
# 			md_quote('Для получения нового задания используй команду /task'),
# 		))
# 	elif not current_task['is_complete']:
# 		await message.answer(text=md.text(
# 			md_quote('Ты ещё не выполнил задание'),
# 		))
# 	else:
# 		# send additional info about given words
# 		pass


@dp.message(Command('answer'))
async def give_answer(message: types.Message):
	user = user_service.get_user(message.from_user.id, message.from_user.full_name)
	if user.task_id is not None:
		current_task = task_manager.get_task(user.task_id)
		if user.attempts < 1:
			text = md.text(
				md_quote(f'Я пока не могу предоставить ответ. Попробуйте выполнить задание хотя бы один раз'),
				sep=''
			)
			await message.answer(text=text)
		else:
			user_service.update_on_completion(user)
			correct_options = get_correct_answer(current_task.word_ids, task_manager.words)
			text = md.text(
				md_quote(f'Правильный ответ: {current_task.answer}:'),
				correct_options,
				md_quote("/task - получить новое задание"),
				sep='\n'
			)
			await message.answer(text=text)
	else:
		await message.answer(text=md.text(
			md_quote('Для получения нового задания используй команду /task'),
		))


@dp.message()
async def send_message(message: types.Message):
	user = user_service.get_user(message.from_user.id, message.from_user.full_name)
	if user.task_id is not None:
		current_task = task_manager.get_task(user.task_id)
		if valid_answer(message.text):
			answer_given = []
			for n in message.text:
				if n.isdigit():
					answer_given.append(n)
			answer_given = ''.join(sorted(answer_given))
			if answer_given == current_task.answer:
				# CORRECT ANSWER GIVEN
				user.tasks_completed += 1
				user_service.update_on_completion(user, successful=True)
				correct_options = get_correct_answer(current_task.word_ids, task_manager.words)
				await message.answer_sticker(sticker=config.sticker_ids['nice_doggy'])
				await message.answer(get_congrats(current_task.answer, correct_options))
				return
			else:
				# INCORRECT ANSWER GIVEN
				user.attempts += 1
				user_service.update_user_attempts(user)
				await message.answer(
					text=md.text(
						md_quote('Ответ неверный. Попробуй ещё раз.'),
						md_quote(task_manager.form_task(current_task.word_ids)),
						md_quote('/answer - получить ответ'),
						sep='\n'
					)
				)
				return
		else:
			# wrong format received
			await message.reply(
				'Ответ должен состоять только из неповторяющихся цифр от 1 до 5. Попробуй ещё раз', parse_mode=None)
			return
	text = get_help_text()
	await message.answer(text=text)


async def main():
	logging.basicConfig(level=logging.INFO)
	bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.MARKDOWN_V2)
	atexit.register(database.close)
	await dp.start_polling(bot)


if __name__ == '__main__':
	asyncio.run(main())
