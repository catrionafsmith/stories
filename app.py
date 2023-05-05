import os
import mysql.connector

import openai
from flask import Flask, redirect, render_template, request, url_for, session

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
app.secret_key = b'_5#y2L"Fkkk4Q8z\n\xec]/'


# Set up database connection
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="glendelvine3255",
  database="bedtimebard"
)

@app.route("/", methods=("GET", "POST"))
def index():
    # if request.method == "GET":
    #     return render_template("index.html")
    
    if request.method == "POST":
        name = request.form["name"]
        monster = request.form["monster"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(name, monster),
            temperature=0.8,
            max_tokens=4000,
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.0
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result") 
    return render_template("index.html", result=result)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']

        # Create cursor
        cursor = db.cursor()

        # Insert user into database
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
        db.commit()

        # Close cursor
        cursor.close()

        # Redirect to login page
        return redirect(url_for('login'))
    # If the request method is GET, render the registration form
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #Get form data
        username = request.form['username']
        password = request.form['password']

        # Create cursor
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            # User exists, set session variables
            session['loggedin'] = True
            session['id'] = user[0]
            session['username'] = user[1]

            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # User doesn't exist or password is incorrect, show error message
            error = 'Invalid credentials. Please try again.'
            return render_template('login.html', error=error)

    # GET request or invalid POST data, show login form
    return render_template('login.html')

@app.route('/home')
def home():
    # Check if user is logged in
    if 'loggedin' in session:
        return 'Welcome, ' + session['username'] + '!'
    else:
        # User is not logged in, redirect to login page
        return redirect(url_for('login'))

def generate_prompt(name, monster):
    # Prompt v1
    # return f"You are an expert children's author who specialises in writing engaging stories, with multiple cliffhanger points. Please write a 400 word story, with a cliffhanger after around every 100 words. At each cliffhanger point please write ['COMPLETE BEDTIME TASK TO CONTINUE'] The story should be about a kid called {name}, who travels to a magical land and battles {monster}."
    return f"You are an expert children's author who specialises in writing engaging stories. Please write a 400 word story. The story should be about a kid called {name}, who travels to a magical land and battles {monster}."

if __name__ == "__main__":
    app.run(debug=True)