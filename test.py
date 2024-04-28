import sqlite3

db = sqlite3.connect('database.db')
cursor = db.cursor()

with open('allwords.txt', 'r', encoding='utf-8') as file:
	words = file.read().split('\n')
	word_id = 0
	for word_info in words:
		word_id += 1
		word_info = word_info.split(';')
		correct_form = word_info[0]
		incorrect_form = word_info[1]
		if len(word_info) >= 4:
			definition = word_info[3]
			cursor.execute(
				'INSERT INTO words VALUES(?, ?, ?, ?, ?)', (word_id, correct_form, incorrect_form, info, definition)
			)
			continue
		if len(word_info) >= 3:
			info = word_info[2]
			cursor.execute(
				'INSERT INTO words VALUES(?, ?, ?, ?, NULL)', (word_id, correct_form, incorrect_form, info)
			)
			continue

		cursor.execute(
			'INSERT INTO words VALUES(?, ?, ?, NULL, NULL)', (word_id, correct_form, incorrect_form)
		)

db.commit()
db.close()
