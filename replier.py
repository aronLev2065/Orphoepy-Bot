from aiogram.utils import markdown as md
from helper import md_quote, md_bold


def get_greetings(user_full_name):
	"""
	Command: /start
	"""
	text = md.text(
		md.text(
			md_quote("Привет,"),
			md.bold(user_full_name),
			"\\!",
		),
		"",
		md.text(
			md_quote("Если ты учишься в"),
			md.bold('11 классе'),
			md_quote("и хочешь подтянуть ударения для ЕГЭ по русскому языку, то этот чат для тебя!"),
			sep=' '
		),
		"",
		# md.text(
		# 	md_quote("Несколько раз в день я буду присылать тебе задания на подобии"),
		# 	md.underline("№4"),
		# 	md_quote("ЕГЭ."),
		# 	md_quote("После выполнения тобой задания, ты сможешь получать обратную связь по ошибкам и любым вопросам."),
		# 	md_quote("Также в конце дня ты сможешь посмотреть полную статистику по заданию, чтобы понять,"),
		# 	md_quote("над чем стоит поработать.\n"),
		# 	sep=' '
		# ),
		md_quote("Чтобы узнать больше о моих способностях, отправь команду /help"),
		sep='\n'
	)
	return text


def get_help_text():
	"""
	Command: /help
	"""
	text = md.text(
		md_quote('Для получения нового задания отправь команду /task.'),
		md_quote('Если ты хочешь получить правильный ответ на задание, отправь команду /answer.'),
		md_quote('Все команды доступны по кнопке "Menu".'),
		sep='\n'
	)
	return text


def format_task(options_formatted):
	"""
	Command: /task
	"""
	text = md.text(
		md.text(
			md_quote('Укажи варианты ответов, в которых'),
			md.bold('верно'),
			md_quote('выделена буква, обозначающая ударный гласный звук.'),
			md_quote('Запиши номера ответов.'),
			sep=' '
		),
		md_quote(options_formatted),
		sep='\n'
	)
	return text


def get_congrats(answer, options):
	"""
	Sent on correct answer
	"""
	text = md.text(
		md_quote("💪Все верно!"),
		md_quote(f'Правильный ответ: {answer}:'),
		options,
		md_quote("/task - получить новое задание"),
		sep='\n'
	)
	return text
