# **User Registration Web Application**

**Date:** July 20, 2025  
This is a simple web application for user registration built with Python, Flask, and PostgreSQL. It allows users to register their details, generates a unique 9-character alphanumeric ID for each user, and provides a way to retrieve user records using that ID.  
The application is designed to be run locally on a macOS environment.

## **Project Structure**

Ensure your project files are organized as follows:  
user-registration-app/  
├── app.py           \# The main Flask application  
└── templates/  
    ├── index.html       \# Main page with registration/retrieval forms  
    └── user\_record.html \# Page to display user details

## **Prerequisites**

Before you begin, make sure you have the following installed on your macOS machine:

1. **Homebrew**: The missing package manager for macOS. If you don't have it, install it by running this in your terminal:  
   /bin/bash \-c "$(curl \-fsSL \[https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh\](https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh))"

2. **Python 3**: macOS usually comes with Python pre-installed. You can check by running python3 \--version.  
3. **pip**: The Python package installer, which comes with Python 3\.

## **Setup and Installation Guide**

Follow these steps to get the application running.

### **Step 1: Install and Set Up PostgreSQL**

First, you need to install the PostgreSQL database and create a database for the application.

1. **Install PostgreSQL using Homebrew**:  
   brew install postgresql

2. **Start the PostgreSQL Service**: This will start the database server and keep it running in the background.  
   brew services start postgresql

3. **Create the Database and Table**:  
   * Log in to the default PostgreSQL user.  
     psql postgres

   * Inside the psql shell, create a new database named userdb:  
     CREATE DATABASE userdb;

   * Connect to your newly created database:  
     \\c userdb

   * Create the users table. **This command now includes all the new fields.**  
     CREATE TABLE users (  
         id VARCHAR(9) PRIMARY KEY,  
         full\_name VARCHAR(100) NOT NULL,  
         mobile VARCHAR(20) NOT NULL,  
         email VARCHAR(100) UNIQUE NOT NULL,  
         gender VARCHAR(20),  
         date\_of\_birth DATE,  
         address TEXT,  
         zip\_code VARCHAR(10),  
         additional\_comments TEXT,  
         registration\_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT\_TIMESTAMP  
     );

   * You can verify the table was created with \\dt.  
   * Exit the psql shell by typing \\q and pressing Enter.

### **Step 2: Install Python Dependencies**

Install Flask and psycopg2 using pip:  
pip3 install Flask psycopg2-binary

### **Step 3: Configure the Database Connection**

1. **Find Your PostgreSQL Username**: On macOS, this usually matches your Mac's username.  
   whoami

2. **Edit app.py**: Open app.py and update the user in the app.config\['DATABASE'\] dictionary.  
   **Example:** If your username is johnappleseed:  
   app.config\['DATABASE'\] \= {  
       'dbname': 'userdb',  
       'user': 'johnappleseed', \# \<-- CHANGE THIS TO YOUR USERNAME  
       'password': '',          \# Leave empty if you did not set a password  
       'host': 'localhost',  
       'port': '5432'  
   }

### **Step 4: Run the Application**

1. **Navigate to the Project Directory**:  
   cd path/to/your/user-registration-app

2. **Run the Flask App**:  
   python3 app.py

3. **Access in Browser**: Open http://127.0.0.1:5000 in your web browser.

## **How to Use the Application**

1. **To Register a User**: Fill in the "User Registration" form and click "Register & Generate ID".  
2. **To Retrieve a User**: Enter a user's unique ID into the "Retrieve User Record" form and click "Retrieve Record".