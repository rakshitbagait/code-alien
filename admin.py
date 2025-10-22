import mysql.connector
from datetime import datetime
from mysql.connector import Error
print("The code is running")
try:
    c_alien_db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="code_alien_db",
        port=3306,
        connection_timeout=5,
        use_pure = True
    )
    print("Connected")
except Error as e:
    print("Error connecting:", e)

mycursor = c_alien_db.cursor()

try :
    with open('blogs.txt','r',encoding="utf-8")as file:
        blog_text = file.read()
except FileNotFoundError:
    with open("blogs.txt",'w')as file :
        file.write(" ")
        print("file created")

blog_title = input("Enter the blog title").capitalize()

# blog_text = input("Enter your blog")
image_path =input("Enter the thumbnail image path")
date_of_publish = datetime.now()

sql = "INSERT INTO blog (blog_title, blog_description, image, date_of_publish) VALUES (%s, %s, %s, %s)"
values = (blog_title, blog_text, image_path, date_of_publish)
mycursor.execute(sql, values)

c_alien_db.commit()
