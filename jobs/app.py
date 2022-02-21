import sqlite3
from flask import Flask, render_template, g

PATH = 'db/jobs.sqlite'

# Instance of the Flask class called app w/ special variable __name__ passed to
# the Flask class constructor.
app = Flask(__name__)


def open_connection():
    """Opens connection to database"""
    connection = getattr(g, '_connection', None)

    if connection is None:
        connection = g._connection = sqlite3.connect(PATH)

    connection.row_factory = sqlite3.Row
    return connection


def execute_sql(sql, values=(), commit=False, single=False):
    """An easier way to query the database"""
    connection = open_connection()

    cursor = connection.execute(sql, values)

    if commit is True:
        results = connection.commit()
    else:
        results = cursor.fetchone() if single else cursor.fetchall()

    cursor.close()
    return results


@app.teardown_appcontext
def close_connection(exception):
    """Ensure database connection is closed when app_context is torn down"""
    connection = getattr(g, '_connection', None)

    if connection is not None:
        connection.close()


@app.route('/')
@app.route('/jobs')
def jobs():
    """Basic function to display all the jbos in our database."""

    jobs = execute_sql('SELECT job.id, job.title, job.description, job.salary, employer.id as employer_id, employer.name as employer_name FROM job JOIN employer ON employer.id = job.employer_id')
    return render_template('index.html', jobs=jobs)


@app.route('/job/<job_id>')
def job(job_id):
    """ """
    job = execute_sql('SELECT job.id, job.title, job.description, job.salary, employer.id as employer_id, employer.name as employer_name FROM job JOIN employer ON employer.id = job.employer_id WHERE job.id = ?', [job_id], single=True)
    return render_template('job.html', job=job)


@app.route('/employer/<employer_id>')
def employer(employer_id):
    """Employer"""

    employer = execute_sql('SELECT * FROM employer WHERE id=?', [employer_id], single=True)
    jobs = execute_sql('SELECT job.id, job.title, job.description, job.salary FROM job JOIN employer ON employer.id = job.employer_id WHERE employer.id = ?', [employer_id])
    reviews = execute_sql('SELECT review, rating, title, date, status FROM review JOIN employer ON employer.id = review.employer_id WHERE employer.id = ?', [employer_id])

    return render_template('employer.html', employer=employer, jobs=jobs, reviews=reviews)
