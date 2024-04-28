import sqlite3 as sql


class DataBase:
	__instance = None

	def __new__(cls):
		if cls.__instance is None:
			cls.__instance = super().__new__(cls)
		return cls.__instance

	def __init__(self):
		self.db = sql.connect('database.db')
		self.cursor = self.db.cursor()

	# --- UPDATE ---
	def create_new_user(self, user_id, name):
		self.cursor.execute(
			"INSERT INTO users VALUES (?, NULL, 0, '', ?, 0)", (user_id, name,)
		)
		self.commit()

	def create_new_task(self, task_id, task_info, answer):
		self.cursor.execute(
			"INSERT INTO tasks VALUES (?, ?, ?)", (task_id, task_info, answer)
		)
		self.commit()

	def update_user_on_completion(self, user_id, task_id, successful):
		self.cursor.execute(
			"UPDATE users SET task_id=NULL, attempts=0 WHERE user_id = ?", (user_id,)
		)
		if successful:
			self.cursor.execute(
				"UPDATE users SET tasks_completed = tasks_completed + 1 WHERE user_id = ?", (user_id,)
			)
		self.delete_task(task_id)
		self.commit()

	def update_user_attempts(self, user_id, user_attempts):
		self.cursor.execute(
			"UPDATE users SET attempts=? WHERE user_id=?", (user_attempts, user_id)
		)
		self.commit()

	def assign_new_task(self, user_id, task_id):
		# clear previous task info
		previous_task = self.cursor.execute("SELECT task_id FROM users WHERE user_id = ?", (user_id,)).fetchone()
		if previous_task[0]:
			self.delete_task(previous_task[0])

		self.cursor.execute(
			"UPDATE users SET task_id = ? WHERE user_id = ?", (task_id, user_id)
		)
		self.commit()

	# --- READ ---
	def get_words(self):
		words = self.cursor.execute(
			"SELECT * FROM words"
		)
		return words.fetchall()

	def get_users(self):
		users = self.cursor.execute(
			"SELECT * FROM users"
		)
		return users.fetchall()

	def get_tasks(self):
		tasks = self.cursor.execute(
			"SELECT * FROM tasks"
		)
		return tasks.fetchall()

	def get_task_by_id(self, task_id):
		return self.cursor.execute(
			"SELECT * FROM tasks WHERE task_id=?", (task_id,)
		).fetchone()

	# --- DELETE ---
	def delete_task(self, task_id):
		self.cursor.execute("DELETE FROM tasks WHERE task_id=?", (task_id,))
		self.commit()

	def commit(self):
		self.db.commit()

	def close(self):
		self.commit()
		self.db.close()
