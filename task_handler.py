import random


class Task:
	def __init__(self, task_id: int, word_ids: str, answer: str):
		self.task_id = task_id
		self.word_ids = word_ids
		self.answer = answer


class TaskManager:
	active_tasks = dict()
	words = dict()

	def __init__(self, database):
		self.database = database
		self.__restore_data()

	def __restore_data(self):
		tasks = self.database.get_tasks()
		for task_data in tasks:
			new_task = Task(*task_data)
			self.active_tasks.setdefault(new_task.task_id, new_task)

		words = self.database.get_words()
		for word in words:
			self.words.setdefault(word[0], word)

	def get_new_task(self):
		task_info, answer = self.generate_new_word_list()
		task_id = random.randint(100, 999)
		while task_id in self.active_tasks.keys():
			task_id = random.randint(100, 999)
		self.database.create_new_task(task_id, task_info, answer)
		new_task = Task(task_id, task_info, answer)
		self.active_tasks.setdefault(task_id, new_task)
		return task_info, task_id

	def get_task(self, task_id) -> Task:
		if task_id in self.active_tasks.keys():
			return self.active_tasks[task_id]
		else:
			task_info = self.database.get_task_by_id(task_id)
			new_task = Task(*task_info)
			self.active_tasks.setdefault(task_id, new_task)
			return new_task

	def generate_new_word_list(self):
		word_ids = list(self.words.keys())
		word_list = []
		incorrect_count = random.randint(1, 3)  # defines the number of incorrect options
		while len(word_list) < 5:
			new_word_id = random.choice(word_ids)
			word_list.append({'id': new_word_id, 'is_correct': 1})
			word_ids.remove(new_word_id)

		for i in range(incorrect_count):
			next_incorrect_index = random.randint(0, 4)
			if not word_list[next_incorrect_index]['is_correct']:
				continue
			word_list[next_incorrect_index]['is_correct'] = 0
		random.shuffle(word_list)
		answer = ''
		for i in range(5):
			if word_list[i]['is_correct']:
				answer += str(i + 1)
		word_list = ';'.join(['.'.join(map(str, word_info.values())) for word_info in word_list])
		return word_list, answer

	def form_task(self, task_info: str):
		# Modifies the word list to displayed format
		task_info = task_info.split(';')
		task_text = ''
		for i in range(len(task_info)):
			word_id, is_correct = map(int, task_info[i].split('.'))
			word = self.words[word_id]
			correct_form, incorrect_form, definition = word[1], word[2], word[5]
			if definition:
				correct_form += ' ' + definition
				incorrect_form += ' ' + definition

			if is_correct:
				s = 0
				displayed_text = f'{str(i + 1)}. {correct_form}\n'
			else:
				displayed_text = f'{str(i + 1)}. {incorrect_form}\n'

			task_text += displayed_text

		return task_text
