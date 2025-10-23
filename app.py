from flask import Flask, render_template,url_for,request

from flask_mail import Mail,Message
import os 
from dotenv import load_dotenv
import mysql.connector
import markdown
from smtplib import SMTP


load_dotenv()
app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MY_EMAIL')  # your email
app.config['MAIL_PASSWORD'] = os.getenv('MY_PASSWORD')  # your app password
mail = Mail(app)

def get_db_connection():
    c_alien_db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="code_alien_db",
        port=3306,
        connection_timeout=5,
        use_pure = True
    )
    return c_alien_db
@app.route("/")
def home():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT blog_id, blog_title, image FROM blog ORDER BY date_of_publish DESC")    
    blog =cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html',blogs=blog)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact",methods = ['GET','POST'])

def contact():
    return render_template("contact.html")
@app.route("/send_email",methods=["POST"])
def send_email():
    if request.method == 'POST':
        Name = request.form['Name']
        email = request.form['email']
        message = request.form['message']
        msg = Message(subject= "Contact us Form submission",
                      sender=email,
                      recipients=[os.getenv('MY_EMAIL')],
                      body=f"From:{Name}\nEmail:{email}\n\nMessage:\n{message}")
        
        subject =f"Hello {Name} from Code Alien"
        my_message =f"""Hey {Name} thank you for contacting us . 
        This is an auto generated message.
        Till than keep exploring our blogs :)."""
            
        try:
            mail.send(msg)
            try:
                with SMTP("smtp.gmail.com",587) as connection:
                    connection.starttls()
                    connection.login(os.getenv("MY_EMAIL"),os.getenv("MY_PASSWORD"))
                    connection.sendmail(
                        from_addr=os.getenv('MY_EMAIL'),
                        to_addrs=email,
                        msg=f"Subject:{subject}\n\n{my_message}"
                    )
            except Exception as e:
                        print("nahi gaya mail",e)
            return render_template("contact.html", message="Your message has been sent successfully!")

        except Exception as e:
            print(e)
            return render_template("contact.html", message="Something went wrong. Please try again.")
    #sending the reply of the user through mail




    return render_template("contact.html")

@app.route("/blog/<int:blog_id>")
def show_blog(blog_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM blog WHERE blog_id=%s", (blog_id,))
    blog = cursor.fetchone()
    cursor.close()
    conn.close()
    if blog and 'blog_description' in blog:
        blog['blog_description'] = markdown.markdown(blog['blog_description'])
    return render_template("template.html", blog=blog)
if __name__ == "__main__":
    app.run(debug =True)