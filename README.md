# Online Examination System
The project is implementation of examination system using the Python with the help of Sqlite3 Database.
<br>

# Prerequisites
> Python 3.6.x <br>
> Sqlite3 3.34.0 <br>
> Prettytable 2.1.0 <br>
> Passlib 1.7.4 <br>

# Installation
The following commands will install all the dependencies
> pip install db-sqlite3 <br>
> pip install prettytable <br>
> pip install passlib <br>

# Features 
> **Common Features** <br>
>> Register <br>
>> Login <br>
>
> **For Normal User** <br>
>> Attempt Test <br>
>> Get History <br>
>> Get Overall Ranking <br>
>
> **For Admin** <br>
>> Add Test <br>
>> Attempt Test <br>
>> Display all available Tests <br>
>> Delete Test <br>
>> Add Admin <br>
>> Remove Admin <br>
>> Get Registered User's List <br>
>> Get History <br>
>> Get Overall Ranking <br>

# File Structure
> **database_operations.py**
>> This file is used to perform the database operation like create all the required tables. <br>
>> It consist of 3 tables <br>
>>> **Users** - This table is used to store the user's personal data. <br>
>>> **Quiz** - This table is used to store all the questions and answers. <br>
>>> **History** - This table is used to store the user's performance in each test with marks and time taken. <br>
>
> **main.py**
>> This is the main python file which contains all the logic of examination system. <br>
>> It has various user-defined functions for respective operation. <br>
>> The function details are as follows - <br>
>>> **register** - It contains the logic to register a user. <br>
>>> **login** - It contains the logic for the login. <br>
>>> **users_list** - This function will display all the registered users. <br>
>>> **attempt_test** - It will show all the available tests and user can attempt any available test. <br>
>>> **add_test** - This function is used to add a new quiz in database. <br>
>>> **display_test** - It is use to see all available tests. <br>
>>> **delete_test** - This function is used to delete the available tests. <br>
>>> **add_admin** - It will used to add admin. <br>
>>> **remove_admin** - This function is used to remove the admin. <br>
>>> **history** - It will show the user's history. <br>
>>> **ranking** - This function is used to see the overall ranking test wise. <br>
<br>

# Steps to run Project
> **Step 1** - Run database_operations.py file using <code> py database_operations.py </code> <br>
> **Step 2** - After executing the above file, it will generate the <code> exam.db </code> which is a database file. <br>
> **Step 3** - After creating database, run the main.py file using <code> py main.py </code>. <br>
> **Step 4** - That's it. <br>
