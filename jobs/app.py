from flask import Flask, render_template

# Instance of the Flask class called app w/ special variable __name__ passed to
# the Flask class constructor.
app = Flask(__name__)


@app.route('/')
@app.route('/jobs')
def jobs():
    """Basic function to display all the jbos in our database."""
    return render_template('index.html')
