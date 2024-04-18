from flask import Flask, render_template, request, session, redirect, url_for
import mysql.connector

app = Flask(__name__, template_folder="template")
app.secret_key = '@2407'  # Set a secret key for session management

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="@2407jana",
    database="testing"
)

@app.route('/')
def index():
    return render_template("signup.html")

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['fname']
        last_name = request.form['lname']
        email = request.form['email']
        password = request.form['password']

        cursor = db.cursor()
        cursor.execute("INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)", (first_name, last_name, email, password))
        db.commit()
        cursor.close()

        return 'Data submitted successfully'

@app.route('/template', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()  # Fetch the result

        # Close the cursor before executing another query
        cursor.close()

        if user:
            session['logged_in'] = True
            session['email'] = email
            return "Welcome"
        else:
            return "Unauthorized error"

    # This part will only execute if the request method is GET
    return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True)
