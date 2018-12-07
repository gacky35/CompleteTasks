from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)
connection = psycopg2.connect("host=localhost dbname=todo user=postgres password=postgres")
cur = connection.cursor()
session = {}

@app.route('/')
def log_in():
    return render_template('index.html')

@app.route('/add.html')
def add():
    return render_template('add.html')

@app.route('/add.html',methods=['POST'])
def adding():
    if request.method == 'POST':
        cur.execute("SELECT COUNT(id) FROM task")
        rows = cur.fetchall()
        for row in rows:
            ids = row[0] + 1
        cur.execute("INSERT INTO task (content, status, deadline, detail, username, id) VALUES (%s, %s, %s, %s, %s, %s)", (request.form['contents'], request.form['status'], request.form['deadline'], request.form['detail'], session[0], ids))
        connection.commit()
    tasks = pick()
    return render_template('list.html', username=session[0], tasks=tasks)

@app.route('/list.html', methods=['POST'])
def display():
    global session
    if request.method == 'POST':
        username = request.form['user_name']
        session[0] = username
        cur.execute("SELECT password FROM users WHERE username='" + username + "'")
        results = cur.fetchall()
        if not results:
            return render_template('index.html')
        for row in results:
            result = row[0]
        if result == request.form['password']:
            tasks = pick()
            return render_template('list.html', username=username, tasks=tasks)
        else:
            return render_template('index.html')

@app.route('/edit.html', methods=['POST'])
def edited():
    if request.method == 'POST':
        cur.execute("UPDATE task SET content = '" + request.form['contents'] + "' WHERE id = '" + session[1] + "'")
        cur.execute("UPDATE task SET status = '" + request.form['status'] + "' WHERE id = '" + session[1] + "'")
        cur.execute("UPDATE task SET deadline = '" + request.form['deadline'] + "' WHERE id = '" + session[1] + "'")
        cur.execute("UPDATE task SET detail = '" + request.form['detail'] + "' WHERE id = '" + session[1] + "'")
        connection.commit()
    tasks = pick()
    return render_template('list.html', username=session[0], tasks=tasks)

@app.route('/regist.html')
def regist_disp():
    return render_template('regist.html')

@app.route('/index.html')
def log_out():
    global session
    session = {}
    return render_template('index.html')

@app.route('/index.html', methods = ['POST'])
def regist():
    if request.method == 'POST':
        username = request.form['user_name']
        cur.execute("SELECT * FROM users WHERE username='" + username + "'")
        check = cur.fetchall()
        if not check:
            if ( request.form['password'] == request.form['confirm'] ):
                cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, request.form['password']))
                connection.commit()
                return render_template('index.html')
            else:
                return render_template('regist.html')
        return render_template('regist.html')

    return render_template('regist.html')

@app.route('/<get_id>')
def edit(get_id):
    global session
    if get_id == 'favicon.ico':
        pass
    else:
        session[1] = get_id
        cur.execute("select * from task where id = '" + get_id + "'")
        tasks = cur.fetchall()
        return render_template('edit.html', tasks=tasks)

def pick():
    cur.execute("SELECT * FROM task WHERE username='" + session[0] + "'")
    tasks = cur.fetchall()
    return tasks

if __name__ == '__main__':
    app.run(debug=True)
