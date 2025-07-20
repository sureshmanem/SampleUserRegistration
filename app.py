import string
import random
import psycopg2
from flask import Flask, request, render_template, redirect, url_for, g

# --- Flask App and Database Configuration ---

app = Flask(__name__)

# IMPORTANT: Replace these with your actual PostgreSQL credentials
app.config['DATABASE'] = {
    'dbname': 'userdb',
    'user': 'lallu', # Your PostgreSQL username (often 'postgres' by default)
    'password': '',      # Your PostgreSQL password (leave empty if none)
    'host': 'localhost',
    'port': '5432'
}

# --- Database Connection Handling ---

def get_db():
    """Opens a new database connection if there is none yet for the current application context."""
    if 'db' not in g:
        db_config = app.config['DATABASE']
        g.db = psycopg2.connect(
            dbname=db_config['dbname'],
            user=db_config['user'],
            password=db_config['password'],
            host=db_config['host'],
            port=db_config['port']
        )
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    """Closes the database again at the end of the request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

# --- Core Logic ---

def is_id_unique(user_id):
    """Checks if a given ID already exists in the database."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id FROM users WHERE id = %s;", (user_id,))
    is_unique = cursor.fetchone() is None
    cursor.close()
    return is_unique

def generate_unique_id():
    """Generates a unique 9-character alphanumeric ID that is not in the database."""
    chars = string.ascii_letters + string.digits
    while True:
        new_id = ''.join(random.choices(chars, k=9))
        if is_id_unique(new_id):
            return new_id

# --- Web Routes ---

@app.route('/', methods=['GET'])
def index():
    """Displays the main page with both registration and retrieval forms."""
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    """Handles new user registration."""
    db = None # FIX 1: Initialize db to None
    try:
        # Get data from the form
        full_name = request.form['fullName']
        mobile = request.form['mobile']
        email = request.form['email']

        # Generate unique ID and save to database
        user_id = generate_unique_id()
        
        db = get_db()
        cursor = db.cursor()
        
        # SQL statement to insert a new record
        sql = "INSERT INTO users (id, full_name, mobile, email) VALUES (%s, %s, %s, %s);"
        cursor.execute(sql, (user_id, full_name, mobile, email))
        
        db.commit() # Commit the transaction to make the changes permanent
        cursor.close()
        
        # Redirect to a page showing the new user's record
        return redirect(url_for('get_user_by_id', user_id=user_id, success=True))

    except psycopg2.Error as e:
        # Handle potential database errors (e.g., duplicate email)
        if db: # FIX 2: Only rollback if the connection was successful
            db.rollback() 
        error_message = f"Database error: {e}"
        return render_template('index.html', registration_error=error_message)
    
@app.route('/retrieve', methods=['POST'])
def retrieve():
    """Handles the retrieval form submission by redirecting to the correct URL."""
    user_id = request.form['userId']
    return redirect(url_for('get_user_by_id', user_id=user_id))


@app.route('/user/<string:user_id>')
def get_user_by_id(user_id):
    """Fetches and displays a user's record from the database."""
    db = get_db()
    cursor = db.cursor()
    
    # Fetch user data by ID
    cursor.execute("SELECT full_name, mobile, email FROM users WHERE id = %s;", (user_id,))
    user_record = cursor.fetchone()
    cursor.close()
    
    user = None
    if user_record:
        user = {
            'fullName': user_record[0],
            'mobile': user_record[1],
            'email': user_record[2]
        }
        
    # Check if this is a redirect from a successful registration
    success_message = "User registered successfully!" if request.args.get('success') else None
    
    return render_template('user_record.html', user=user, user_id=user_id, success_message=success_message)

if __name__ == '__main__':
    app.run(debug=True)