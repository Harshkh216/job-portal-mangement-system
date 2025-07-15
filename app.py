from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_PATH = 'database/job_portal.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/jobs')
def jobs():
    conn = get_db_connection()
    jobs = conn.execute('SELECT * FROM jobs').fetchall()
    conn.close()
    return render_template('jobs.html', jobs=jobs)

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']
    conn = get_db_connection()
    jobs = conn.execute("SELECT * FROM jobs WHERE title LIKE ?", ('%' + keyword + '%',)).fetchall()
    conn.close()
    return render_template('jobs.html', jobs=jobs)

@app.route('/apply/<int:job_id>', methods=['GET', 'POST'])
def apply(job_id):
    conn = get_db_connection()
    job = conn.execute('SELECT * FROM jobs WHERE id = ?', (job_id,)).fetchone()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        conn.execute('INSERT INTO applications (job_id, name, email) VALUES (?, ?, ?)', (job_id, name, email))
        conn.commit()
        conn.close()
        return redirect(url_for('applied'))
    return render_template('apply.html', job=job)

@app.route('/applied')
def applied():
    conn = get_db_connection()
    apps = conn.execute('''
        SELECT applications.id, name, email, title, company FROM applications 
        JOIN jobs ON applications.job_id = jobs.id
    ''').fetchall()
    conn.close()
    return render_template('applied.html', apps=apps)

@app.route('/delete/<int:app_id>')
def delete(app_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM applications WHERE id = ?', (app_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('applied'))

if __name__ == '__main__':
    app.run(debug=True)