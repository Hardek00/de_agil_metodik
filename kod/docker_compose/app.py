from flask import Flask, render_template
import psycopg2
import os
import time

app = Flask(__name__)

def get_users():
    """Get users from database"""
    try:
        # Wait a bit for database to be ready
        time.sleep(1)
        
        # Connect to database
        conn = psycopg2.connect(
            host='database',
            database='webapp',
            user='postgres',
            password='secret123'
        )
        cursor = conn.cursor()
        
        # Get all users
        cursor.execute('SELECT id, username FROM users ORDER BY id')
        users = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return users, None
        
    except Exception as e:
        return [], str(e)

@app.route('/')
def home():
    """Show users in HTML page"""
    users, error = get_users()
    return render_template('index.html', users=users, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
