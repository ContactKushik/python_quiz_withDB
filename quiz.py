import mysql.connector
import os
import sys

def create_database_and_tables():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_PASSWORD"
    )
    cursor = conn.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS quiz_app")
    cursor.execute("USE quiz_app")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username VARCHAR(255) PRIMARY KEY,
        password VARCHAR(255) NOT NULL
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scores (
        username VARCHAR(255),
        quiz_type VARCHAR(50),
        score INT,
        PRIMARY KEY (username, quiz_type),
        FOREIGN KEY (username) REFERENCES users (username)
    )""")

    conn.commit()
    cursor.close()
    conn.close()

create_database_and_tables()

users = {}
scores = {}
quizzes = {
    'python': [
        {'question': "What is the output of print(2 ** 3)?", 'options': ['6', '8', '9', '12'], 'answer': '8'},
        {'question': "Which keyword is used to create a function?", 'options': ['fun', 'def', 'func', 'define'], 'answer': 'def'},
        {'question': "What is the correct file extension for Python files?", 'options': ['.py', '.python', '.pyt', '.txt'], 'answer': '.py'},
        {'question': "What is the result of len('Hello')?", 'options': ['3', '4', '5', '6'], 'answer': '5'},
        {'question': "Which of these is not a Python data type?", 'options': ['List', 'Tuple', 'Dictionary', 'Queue'], 'answer': 'Queue'}
    ],
    'dsa': [
        {'question': "What is the time complexity of binary search?", 'options': ['O(n)', 'O(n^2)', 'O(log n)', 'O(1)'], 'answer': 'O(log n)'},
        {'question': "What data structure works on FIFO principle?", 'options': ['Stack', 'Array', 'Queue', 'Graph'], 'answer': 'Queue'},
        {'question': "What is the maximum number of nodes in a binary tree of height h?", 'options': ['2^h', '2^h - 1', '2^(h+1) - 1', 'h^2'], 'answer': '2^(h+1) - 1'},
        {'question': "Which sorting algorithm has the worst-case time complexity of O(n^2)?", 'options': ['Merge Sort', 'Quick Sort', 'Bubble Sort', 'Heap Sort'], 'answer': 'Bubble Sort'},
        {'question': "What does a stack use to function?", 'options': ['FIFO', 'LIFO', 'DFS', 'BFS'], 'answer': 'LIFO'}
    ],
    'cse': [
        {'question': "What does CPU stand for?", 'options': ['Central Process Unit', 'Central Processing Unit', 'Computer Personal Unit', 'Central Processor'], 'answer': 'Central Processing Unit'},
        {'question': "Which part of the computer is the brain?", 'options': ['RAM', 'CPU', 'Motherboard', 'Hard Drive'], 'answer': 'CPU'},
        {'question': "What does RAM stand for?", 'options': ['Random Access Memory', 'Read Access Memory', 'Ready And Memory', 'Run All Memory'], 'answer': 'Random Access Memory'},
        {'question': "What is the main function of an operating system?", 'options': ['Manage hardware resources', 'Compile code', 'Run applications', 'Store data'], 'answer': 'Manage hardware resources'},
        {'question': "Which of these is an example of system software?", 'options': ['MS Word', 'Linux', 'Photoshop', 'Chrome'], 'answer': 'Linux'}
    ]
}

users = {}
scores = {}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def register():
    username = input("Enter username: ")
    if username in users:
        print("Username already exists.")
        clear_screen()
    else:
        password = input("Enter password: ")
        users[username] = password
        clear_screen()
        print("Registration successful.")

def login():
    username = input("Enter username: ")
    if username not in users:
        clear_screen()
        print("Username not found.")
        return None
        
    password = input("Enter password: ")
    if users[username] == password:
        clear_screen()
        print("Login successful.")
        return username
    else:
        clear_screen()
        print("Incorrect password.")
        return None

def delete_user(username):
    if username in users:
        del users[username]
        scores.pop(username, None)
        clear_screen()
        print("User deleted successfully.")
    else:
        clear_screen()
        print("User not found.")

def get_high_score(username, quiz_type):
    return scores.get(username, {}).get(quiz_type, 0)

def save_score(username, quiz_type, score):
    if username not in scores:
        scores[username] = {}
    if quiz_type not in scores[username] or score > scores[username][quiz_type]:
        scores[username][quiz_type] = score

def attempt_quiz(username):
    print("1. Python\n2. DSA\n3. CSE")
    choice = input("Enter your choice (1-3): ")
    if choice == '1':
        quiz_type = 'python'
    elif choice == '2':
        quiz_type = 'dsa'
    elif choice == '3':
        quiz_type = 'cse'
    else:
        print("Invalid choice.")
        return
    score = 0
    for question in quizzes[quiz_type]:
        print(question['question'])
        for i, option in enumerate(question['options'], 1):
            print(f"{i}. {option}")
        try:
            user_choice = int(input("Enter your choice: "))
            if 1 <= user_choice <= len(question['options']):
                selected_option = question['options'][user_choice - 1]
                if selected_option == question['answer']:
                    print("Correct!")
                    score += 1
                else:
                    print(f"Incorrect. The correct answer is: {question['answer']}")
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input.")
    print(f"Your score: {score}/{len(quizzes[quiz_type])}")
    save_score(username, quiz_type, score)
    print(f"Highest score: {get_high_score(username, quiz_type)}")

while True:
    print("1. Register\n2. Login\n3. Delete User\n4. Exit")
    choice = input("Enter your choice: ")
    if choice == '1':
        register()
    elif choice == '2':
        user = login()
        if user:
            while True:
                print("1. Attempt Quiz\n2. View High Scores\n3. Logout")
                sub_choice = input("Enter your choice: ")
                if sub_choice == '1':
                    attempt_quiz(user)
                elif sub_choice == '2':
                    print(f"High Scores for {user}:")
                    for quiz, score in scores.get(user, {}).items():
                        print(f"{quiz}: {score}")
                elif sub_choice == '3':
                    break
                else:
                    print("Invalid choice.")
    elif choice == '3':
        username = input("Enter username to delete: ")
        delete_user(username)
    elif choice == '4':
        print("exiting...")
        sys.exit()
    else:
        print("Invalid choice.")
