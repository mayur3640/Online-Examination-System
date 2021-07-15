from prettytable import PrettyTable
from datetime import datetime
from passlib.hash import sha256_crypt
import sqlite3
import json
import sys


# Making connection with database
conn = sqlite3.connect('exam.db')
cursor = conn.cursor()

# Global Keywords to store current user data
user_id = None
user_fname = ""
user_lname = ""
user_email = ""
user_password = ""
user_role = ""


#Declaring objects of preetytable
header = PrettyTable()
header.field_names = ["Welcome to Online Examination System"]

main_menu = PrettyTable()
main_menu.title = 'Main Menu'
main_menu.field_names = ["Serial Number", "Option"]
main_menu.add_row(["1", "Register - Create a new Account"])
main_menu.add_row(["2", "Login"])
main_menu.add_row(["3", "Exit"])

usersList = PrettyTable()
usersList.title = "User's List"
usersList.field_names = ["User ID","First Name","Last Name","EmailID","User Role"]

historyDetails = PrettyTable()
historyDetails.title = "Your History"
historyDetails.field_names = ["Sr No","Quiz Name","Obtained Marks","Total Marks","Total Time Taken(in sec)","Date of Attempt"]

displayTests = PrettyTable()
displayTests.title = "Available Tests"
displayTests.field_names = ["Sr No","Quiz Name"]

def student_menu_display(fname,lname):
	stud_menu = PrettyTable()
	stud_menu.title = f'Welcome "{fname.capitalize()} {lname.capitalize()}" to Online Examination System'
	stud_menu.field_names = ["Serial Number", "Option"]
	stud_menu.add_row(["1", "Attempt Test"])
	stud_menu.add_row(["2", "History"])
	stud_menu.add_row(["3", "Ranking"])
	stud_menu.add_row(["4", "Logout"])
	print(stud_menu)

def admin_menu_display(fname,lname):
	admin_menu = PrettyTable()
	admin_menu.title = f'Welcome "{fname.capitalize()} {lname.capitalize()}" to Online Examination System'
	admin_menu.field_names = ["Serial Number", "Option"]
	admin_menu.add_row(["1", "Add Test"])
	admin_menu.add_row(["2", "View all Tests"])
	admin_menu.add_row(["3", "Delete Test"])
	admin_menu.add_row(["4", "Attempt Test"])
	admin_menu.add_row(["5","History"])
	admin_menu.add_row(["6", "Ranking"])
	admin_menu.add_row(["7", "Users List"])
	admin_menu.add_row(["8", "Add Admin"])
	admin_menu.add_row(["9", "Remove Admin"])
	admin_menu.add_row(["10", "Logout"])
	print(admin_menu)

showRank = PrettyTable()
showRank.field_names = ["Rank","User ID","Full Name","Email ID","Obtained Marks","Total Marks","Total Time Taken(in sec)","Date of Attempt"]

def show_ranking(testname):
	showRank.title = f'Ranking of quiz - "{testname.capitalize()}"'

showQuestion = PrettyTable()

def register():
	print("Register Now")
	fname = input("Enter your First Name : ")
	lname = input("Enter your Last Name : ")
	email = input("Enter your EmailID : ")
	password = input("Enter your Password : ")
	db_pass = sha256_crypt.hash(str(password))
	role = "student"

	cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
	result = cursor.fetchone()
	
	if result == None:
		cursor.execute("""INSERT into users (fname,lname,email,password,role) values (?,?,?,?,?)""",(fname,lname,email,db_pass,role))
		conn.commit()
		print()
		print("*"*70)
		print("\n\t User registered Successfully!! You can Log in now\n")
		print("*"*70)
		print()
		main_screen()
	else:
		print()
		print("*"*70)
		print("\n\t User exist")
		print("\t Kindly try to login or Check your email\n")
		print("*"*70)
		print()
		main_screen()


def login():
	print("Login here")
	email = input("Enter your EmailID : ")
	password = input("Enter your Password : ")

	cursor.execute('SELECT * FROM users WHERE email = ?', (email,))

	result = cursor.fetchone()
	
	if result == None:
		print()
		print("*"*70)
		print("\n\t User not found...")
		print("\t Kindle Check your email or register yourself first...\n")
		print("*"*70)
		print()
		main_screen()
	else:
		if sha256_crypt.verify(str(password),result[4]):
			global user_id, user_fname, user_lname, user_email, user_role
			user_id = result[0]
			user_fname = result[1]				
			user_lname = result[2]				
			user_email = result[3]				
			user_role = result[5]
			if(result[5]=="student"):
				student_afterlogin()
			elif(result[5]=="admin"):
				admin_afterlogin()
		else:
			print()
			print("*"*70)
			print("\n\t Incorrect Password... Please enter correct password\n")
			print("*"*70)
			print()
			login()


def users_list():
	cursor.execute('SELECT uid,fname,lname,email,role from users');
	result = cursor.fetchall()
	print()
	for i in result:
		usersList.add_row([i[0],i[1].capitalize(),i[2].capitalize(),i[3],i[4].capitalize()])
	print(usersList)
	usersList.clear_rows()
	print()
	admin_afterlogin()


# <------------------- Common Methods ------------------->

def attempt_test():
	global user_id, user_fname, user_lname, user_email, user_role

	cursor.execute('SELECT distinct quiz_name, qid FROM quiz')
	result = cursor.fetchall()
	ls= []
	actual_ans = []
	user_ans = []
	result_ans = []
	start_time = None
	end_time = None

	if result == []:
		print()
		print("*"*70)
		print("\n\t Quiz not available... \n")
		print("*"*70)
		print()
		if(user_role == 'student'):
			student_afterlogin()
		elif(user_role == 'admin'):
			admin_afterlogin()
	else:
		print()
		cnt = 1
		for i in result:
			displayTests.add_row([cnt,i[0].capitalize()])
			ls.append([cnt,i[0],i[1]])
			cnt += 1
		print(displayTests)
		displayTests.clear_rows()
		print()

		quiz_nos = ''
		for i in range(cnt-1):
			if(i == 0):
				quiz_nos = str(i+1)
			else:
				quiz_nos = quiz_nos+"/"+str(i+1)

		quiz_op = input(f"Enter quiz number (Eg. {quiz_nos}) / to exit type 'n' : ")

		if(quiz_op.lower() == 'n' or quiz_op.lower() == 'no'):
			if(user_role == 'student'):
				student_afterlogin()
			elif(user_role == 'admin'):
				admin_afterlogin()

		elif(quiz_op.isdigit()):

			if(int(quiz_op) > len(ls) or int(quiz_op)<=0):
				print()
				print("*"*70)
				print("\n\t Incorrect choice... Please enter correct quiz number\n")
				print("*"*70)
				print()
				attempt_test()
			else:
				quiz_id = ls[int(quiz_op)-1][2]
				quiz_name = ls[int(quiz_op)-1][1]
				cursor.execute('SELECT * FROM quiz where qid = ?', (quiz_id,))
				result = cursor.fetchall()
				if(result == []):
					print()
					print("*"*70)
					print("\n\t Questions not available... Try different quiz\n")
					print("*"*70)
					print()
					attempt_test()
				else:
					start_time = datetime.now()
					for i in result:
						print()
						showQuestion.field_names = ["Question "+str(i[2]), i[3]]
						showQuestion.add_row(["1.", i[4]])
						showQuestion.add_row(["2.", i[5]])
						showQuestion.add_row(["3.", i[6]])
						showQuestion.add_row(["4.", i[7]])
						print(showQuestion)
						showQuestion.clear_rows()

						user_choice = input("Enter your choice (1/2/3/4) : ")
						user_ans.append(user_choice)
						actual_ans.append(i[8])
						print()

					end_time = datetime.now()

					print()
					print("*"*70)
					print("\n\t Test submitted Successfully...")

					difference = end_time - start_time
					diff_in_sec = int(difference.total_seconds())

					#Test result
					cnt = 0
					for i in range(0,len(result)):
						if(user_ans[i] == actual_ans[i]):
							result_ans.append('r')
							cnt+=1
						else:
							result_ans.append('w')

					print("\t You have scored : ",cnt,"/",len(result),"\n")
					print("*"*70)
					print()

					now = datetime.now()
					curr_time = now.strftime('%Y/%m/%d %I:%M:%S')

					users_ans = json.dumps(user_ans)
					results_ans = json.dumps(result_ans)

					cursor.execute("INSERT into history (uid,fname,lname,email,quiz_name,users_choices,result_choices,obtained_marks,total_marks,start_time,end_time,time_taken,doa) values (?,?,?,?,?,'"+users_ans+"','"+results_ans+"',?,?,?,?,?,?)",(user_id,user_fname,user_lname,user_email,quiz_name,cnt,len(result),start_time,end_time,diff_in_sec,curr_time))
					conn.commit()
					if(user_role == 'student'):
						student_afterlogin()
					elif(user_role == 'admin'):
						admin_afterlogin()

		elif(quiz_op.isalnum()):
			print()
			print('*'*70)
			print("\n\tInvalid choice... Please enter a valid choice.\n")
			print('*'*70)
			print()
			attempt_test()


def history():
	global user_id,user_role
	cursor.execute('SELECT quiz_name, obtained_marks, total_marks, time_taken, doa FROM history where uid = ?',(user_id,))
	result = cursor.fetchall()
	if result == []:
		print()
		print("*"*70)
		print("\n\t No data found...\n")
		print("*"*70)
		print()
		if(user_role == 'student'):
			student_afterlogin()
		elif(user_role == 'admin'):
			admin_afterlogin()
	else:
		print()
		cnt = 1
		for i in result:
			historyDetails.add_row([cnt,i[0].capitalize(),i[1],i[2],i[3],i[4]])
			cnt += 1
		print(historyDetails)
		historyDetails.clear_rows()
		print()
	if(user_role == 'student'):
		student_afterlogin()
	elif(user_role == 'admin'):
		admin_afterlogin()


def ranking():
	print()
	global user_role
	cursor.execute('SELECT uid FROM history')
	result = cursor.fetchall()
	if result == []:
		print()
		print("*"*70)
		print("\n\t No data found :( \n")
		print("*"*70)
		print()
		if(user_role == 'student'):
			student_afterlogin()
		elif(user_role == 'admin'):
			admin_afterlogin()
	else:
		cursor.execute('SELECT distinct(quiz_name) from history')
		quiz_names = cursor.fetchall()
		for i in quiz_names:
			query = f'SELECT * from history where quiz_name = "{i[0]}" order by obtained_marks DESC,time_taken ASC'
			cursor.execute(query)
			result = cursor.fetchall()
			if(result == []):
				print()
				print("No data found for quiz ",i[0])
				print()
			else:
				cnt = 1
				for item in result:
					show_ranking(i[0])
					showRank.add_row([cnt,item[0],item[1].capitalize()+" "+item[2].capitalize(),item[3],item[7],item[8],item[11],item[12]])
					cnt += 1
				print(showRank)
				showRank.clear_rows()
				print()

		if(user_role == 'student'):
			student_afterlogin()
		elif(user_role == 'admin'):
			admin_afterlogin()

# <------------------- Admin Methods ------------------->

def add_test():
	print()
	quiz_id = int(input("Enter quiz id in numeric format (Eg. 123) :\t"))
	cursor.execute('SELECT qid FROM quiz where qid = ?',(quiz_id,))
	result1 = cursor.fetchall()

	if result1 != []:
		print()
		print("*"*70)
		print("\n\t Quiz ID already Exists...")
		print("\t Use Different QuizID \n")
		print("*"*70)
		print()
		add_test()
	else:
		quiz_name = input("Enter Quiz name :\t").lower()
		cursor.execute('SELECT quiz_name FROM quiz where quiz_name = ? ',(quiz_name,))
		result2 = cursor.fetchall()

		if result2 != []:
			print()
			print("*"*70)
			print("\n\t Quiz name already Exists...")
			print("\t Use Different name \n")
			print("*"*70)
			print()
			add_test()
		else:
			no_of_que = input("Enter total number of questions :")

			if(no_of_que.isdigit()):

				for i in range(int(no_of_que)):
					que_no = i+1
					ques = input("Enter the question : ")
					op1 = input("Enter option 1 : ")
					op2 = input("Enter option 2 : ")
					op3 = input("Enter option 3 : ")
					op4 = input("Enter option 4 : ")
					ans_op = input("Enter correct option number (1/2/3/4) : ")
					
					cursor.execute("""INSERT into quiz (qid,quiz_name,que_no,question,option1,option2,option3,option4,ans_option) values (?,?,?,?,?,?,?,?,?)""",(quiz_id,quiz_name,que_no,ques,op1,op2,op3,op4,ans_op))
					conn.commit()

				print()
				print("*"*70)
				print("\n\t Quiz uploaded Successfully...\n")
				print("*"*70)
				print()
				admin_afterlogin()
			else:
				print()
				print('*'*70)
				print("\n\tInvalid number of questions... Enter valid number of questions\n")
				print('*'*70)
				print()
				add_test()


def display_test():
	cursor.execute('SELECT distinct(quiz_name) FROM quiz')
	result = cursor.fetchall()

	if result == []:
		print()
		print("*"*70)
		print("\n\t Quiz not available...\n")
		print("*"*70)
		print()
		admin_afterlogin()
	else:
		print()
		cnt = 1
		for i in result:
			displayTests.add_row([cnt,i[0].capitalize()])
			cnt += 1
		print(displayTests)
		displayTests.clear_rows()
		print()
		admin_afterlogin()


def delete_test():
	print()
	cursor.execute('SELECT distinct quiz_name, qid FROM quiz')
	result = cursor.fetchall()
	ls= []

	if result == []:
		print()
		print("*"*70)
		print("\n\t Quiz not available...\n")
		print("*"*70)
		print()
		admin_afterlogin()
	else:
		print()
		cnt = 1
		for i in result:
			displayTests.add_row([cnt,i[0].capitalize()])
			ls.append([cnt,i[0],i[1]])
			cnt += 1
		print(displayTests)
		displayTests.clear_rows()
		print()

		quiz_nos = ''
		for i in range(cnt-1):
			if(i == 0):
				quiz_nos = str(i+1)
			else:
				quiz_nos = quiz_nos+"/"+str(i+1)

		quiz_op = input(f"Enter quiz number (Eg. {quiz_nos}) : ")

		if(quiz_op.isdigit()):

			if(int(quiz_op) > len(ls) or int(quiz_op) <= 0):
				print()
				print("*"*70)
				print("\n\t Incorrect choice... Please enter correct quiz number\n")
				print("*"*70)
				print()
				delete_test()
			else:
				quiz_id = ls[int(quiz_op)-1][2]
				cursor.execute('delete from quiz where qid = ?', (quiz_id,))
				conn.commit()
				print()
				print("*"*70)
				print("\n\t Quiz Deleted Successfully :) \n")
				print("*"*70)
				print()
				admin_afterlogin()
		else:
			print()
			print('*'*70)
			print("\n\tInvalid choice... Please enter a valid choice.\n")
			print('*'*70)
			print()
			delete_test()


def add_admin():
	fname = input("Enter First Name : ")
	lname = input("Enter Last Name : ")
	email = input("Enter EmailID : ")
	password = input("Enter Password : ")
	db_pass = sha256_crypt.hash(str(password))
	role = "admin"

	cursor.execute('SELECT * FROM users WHERE email = ?', (email,))

	result = cursor.fetchone()

	if result == None:
		cursor.execute("""INSERT into users (fname,lname,email,password,role) values (?,?,?,?,?)""",(fname,lname,email,db_pass,role))
		conn.commit()
		print()
		print("*"*70)
		print("\n\t Admin added Successfully!!\n")
		print("*"*70)
		print()
		admin_afterlogin()
	elif result != None:
		cursor.execute("SELECT email, role from users where email = ?",(email,))
		res = cursor.fetchone()
		if(res[1] == 'admin'):
			print()
			print("*"*70)
			print(f"\n\t User '{email}' is already an Admin. \n")
			print("*"*70)
			print()
			admin_afterlogin()

		elif(res[1] == 'student'):
			print()
			print(f'Currently user "{res[0]}" is a student')
			user_choice = input(f'Do you want to make "{res[0]}" as admin (Y/N):\t').lower()
			if(user_choice == 'y' or user_choice == 'yes'):
				cursor.execute('UPDATE users set role = "admin" where email = ?',(email,))
				conn.commit()
				print()
				print("*"*70)
				print(f"\n\t User '{email}' is now admin \n")
				print("*"*70)
				print()
				admin_afterlogin()
			elif(user_choice == 'n' or user_choice == 'no'):
				admin_afterlogin()
			else:
				print()
				print('*'*70)
				print("\n\tInvalid choice... Please enter a valid choice.\n")
				print('*'*70)
				print()
				add_admin()

def remove_admin():
	email = input("Enter EmailID : ")

	cursor.execute('SELECT * FROM users WHERE email = ?', (email,))

	result = cursor.fetchone()

	if result == None:
		print()
		print("*"*70)
		print("\n\t User does not exists!!\n")
		print("*"*70)
		print()
		admin_afterlogin()
	elif result != None:
		cursor.execute("SELECT email, role from users where email = ?",(email,))
		res = cursor.fetchone()
		if(res[1] == 'student'):
			print()
			print("*"*70)
			print(f"\n\t User '{email}' is already student. \n")
			print("*"*70)
			print()
			admin_afterlogin()
		elif(res[1] == 'admin'):
			print()
			print(f'Currently user "{res[0]}" is a admin')
			user_choice = input(f'Do you want to make "{res[0]}" as student (Y/N):\t').lower()
			if(user_choice == 'y' or user_choice == 'yes'):
				cursor.execute('UPDATE users set role = "student" where email = ?',(email,))
				conn.commit()
				print()
				print("*"*70)
				print(f"\n\t User '{email}' is now student \n")
				print("*"*70)
				print()
				admin_afterlogin()
			elif(user_choice == 'n' or user_choice == 'no'):
				admin_afterlogin()
			else:
				print()
				print('*'*70)
				print("\n\tInvalid choice... Please enter a valid choice.\n")
				print('*'*70)
				print()
				remove_admin()

# <------------------- Main Screen Options ------------------->

def main_screen():
	print()
	print(header)
	print()
	print(main_menu)

	choice = input("Enter your choice (1/2/3) : ")

	if(choice == '1'):
		register()
	elif(choice == '2'):
		login()
	elif(choice == '3'):
		exit()
	else:
		print()
		print('*'*70)
		print("\n\tInvalid choice... Please enter a valid choice.\n")
		print('*'*70)
		print()
		main_screen()


# <------------------- Student Options ------------------->

def student_afterlogin():
	print()
	student_menu_display(user_fname,user_lname)

	choice = input("Enter your choice (1/2/3/4) : ")
	
	if(choice == '1'):
		attempt_test()
	elif(choice == '2'):
		history()
	elif(choice == '3'):
		ranking()
	elif(choice == '4'):
		main_screen()
	else:
		print()
		print('*'*70)
		print("\n\tInvalid choice... Please enter a valid choice.\n")
		print('*'*70)
		print()
		student_afterlogin()

# <------------------- Admin Options ------------------->

def admin_afterlogin():
	print()
	admin_menu_display(user_fname,user_lname)

	choice = input("Enter your choice (1/2/3/4/5/6/7/8/9/10) : ")

	if(choice == '1'):
		add_test()
	elif(choice == '2'):
		display_test()
	elif(choice == '3'):
		delete_test()
	elif(choice == '4'):
		attempt_test()
	elif(choice == '5'):
		history()
	elif(choice == '6'):
		ranking()
	elif(choice == '7'):
		users_list()
	elif(choice == '8'):
		add_admin()
	elif(choice == '9'):
		remove_admin()
	elif(choice == '10'):
		main_screen()
	else:
		print()
		print('*'*70)
		print("\n\tInvalid choice... Please enter a valid choice.\n")
		print('*'*70)
		print()
		admin_afterlogin()


if __name__ == "__main__":
	main_screen()
