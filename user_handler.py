class User:
	def __init__(self, user_id, task_id=None, attempts=0, answer='', name='', tasks_completed=0):
		self.user_id = user_id
		self.task_id = task_id
		self.attempts = attempts
		self.answer = answer
		self.name = name
		self.tasks_completed = tasks_completed

	def set_null(self):
		self.task_id = None
		self.attempts = 0


class UserService:
	users = dict()

	def __init__(self, database):
		self.database = database
		self.__restore_data()

	def __restore_data(self):
		users = self.database.get_users()
		for user_data in users:
			new_user = User(*user_data)
			self.users.setdefault(new_user.user_id, new_user)

	def create_user(self, user_id, name):
		if user_id not in self.users.keys():
			new_user = User(user_id, name=name)
			self.users.setdefault(user_id, new_user)
			self.database.create_new_user(user_id, name)

	def get_user(self, user_id, name) -> User:
		if user_id in self.users.keys():
			return self.users[user_id]
		self.create_user(user_id, name)
		return self.get_user(user_id, name)

	def set_new_task(self, user_id, task_id):
		if user_id in self.users.keys():
			user = self.users[user_id]
			user.set_null()
			self.database.assign_new_task(user_id, task_id)
			user.task_id = task_id

	def update_user_attempts(self, user):
		self.database.update_user_attempts(user.user_id, user.attempts)

	def update_on_completion(self, user: User, successful=False):
		self.database.update_user_on_completion(user.user_id, user.task_id, successful)
		user.set_null()
