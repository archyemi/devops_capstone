import sqlite3
import logging

from flask import Flask, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
import sys
import os

number = 0


# format output
format_output = logging.Formatter('%(asctime)s: %(name)s: %(levelname)s: %(message)s')

def initialize_logger():
    log_level = os.getenv("LOGLEVEL", "DEBUG").upper()
    log_level = (
        getattr(logging, log_level)
        if log_level in ["CRITICAL", "DEBUG", "ERROR", "INFO", "WARNING",]
        else logging.DEBUG
    )

    # set logger to handle STDOUT and STDERR
    stdout_h = logging.StreamHandler(sys.stdout)
    stdout_h.setLevel(log_level)

    stderr_h = logging.StreamHandler(sys.stderr)
    stderr_h.setLevel(logging.ERROR)

    handlers = [stderr_h, stdout_h]
    logging.basicConfig(
        format='%(levelname)s:%(name)s:%(asctime)s, %(message)s',
        handlers=handlers
    )

# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    global number
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    number += 1
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    getpost = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return getpost

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    getpost = get_post(post_id)
    if getpost is None:
        app.logger.error('Trying to access a non-existing article')
        return render_template('404.html'), 404
    else:
        app.logger.info('%s article is retrieved', getpost)
        return render_template('post.html', post=getpost)
      

# Define the About Us page
@app.route('/about')
def about():
    app.logger.info('About Us page is retrieved')
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            app.logger.info('%s article is created', title)
            return redirect(url_for('index'))

    return render_template('create.html')

# Define the /healthz endpoint
@app.route('/healthz')
def healthcheck():
    response = app.response_class(
            response=json.dumps({"result":"OK - healthy"}),
            status=200,
            mimetype='application/json'
    )

    app.logger.info('Healthz request successfull')
    return response

# Define the /metrics endpoint
@app.route('/metrics')
def metrics():
    connection = get_db_connection()
    posts =  connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    response = app.response_class(
            response=json.dumps({"status":"success","code":0,"data":{"db_connection_count": number,"post_count":len(posts)}}),
            status=200,
            mimetype='application/json'
    )

    app.logger.info('Metrics request successfull')
    return response

# start the application on port 3111
if __name__ == "__main__":
    initialize_logger()
    app.run(host='0.0.0.0', port='3111')
