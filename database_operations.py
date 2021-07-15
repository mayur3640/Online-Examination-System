import sqlite3

conn = sqlite3.connect('exam.db')

# Create a cursor
cursor = conn.cursor()

# for storing the user information
cursor.execute("""
	create table users(
		uid integer primary key,
		fname text not null,
		lname text not null,
		email text not null,
		password text not null,
		role text not null
	)"""
)

conn.commit()

# for storing mcq questions
cursor.execute("""
	create table quiz(
		qid integer,
		quiz_name text not null,
		que_no integer,
		question text not null,
		option1 text not null,
		option2 text not null,
		option3 text not null,
		option4 text not null,
		ans_option text not null
	)"""
)

conn.commit()

# for storing history of test
cursor.execute("""
	create table history(
		uid integer,
		fname text not null,
		lname text not null,
		email text not null,
		quiz_name text not null,
		users_choices text not null,
		result_choices text not null,
		obtained_marks int not null,
		total_marks int not null,
		start_time text not null,
		end_time text not null,
		time_taken int not null,
		doa text not null
	)"""
)

conn.commit()

# 12345 - $5$rounds=535000$hej1mbUd10GizdJf$pa3fMuDyeXN1JJMrp/eEMVlPTm0xGcfNoxbvJwcEAu3
cursor.execute("""INSERT into users (fname,lname,email,password,role) values (?,?,?,?,?)""",('root','admin','root@gmail.com','$5$rounds=535000$hej1mbUd10GizdJf$pa3fMuDyeXN1JJMrp/eEMVlPTm0xGcfNoxbvJwcEAu3','admin'))
conn.commit()

conn.close()