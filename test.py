from random import randint

from db_handler import DataBase
from user_handler import UserService

db = DataBase()

matvey_loser_task_id = db.cursor.execute(
	"SELECT task_id FROM users WHERE name = 'rejectedreyna'"
).fetchone()

matvey_loser_task = db.cursor.execute(
	"SELECT word_ids FROM tasks WHERE task_id=?", (str(matvey_loser_task_id[0]),)
).fetchone()

if matvey_loser_task:
	for word_info in matvey_loser_task[0].split(';'):
		word = db.cursor.execute(
			"SELECT correct_form FROM words WHERE id=?", (word_info.split('.')[0],)
		).fetchone()
		print(word)

db.commit()

db.close()

