from flask import Flask, render_template, request, session
import psycopg2
import key

app = Flask(__name__)
app.secret_key = key.key()
connection = psycopg2.connect("host=localhost dbname=todo user=postgres password=postgres")
cur = connection.cursor()


@app.route('/')
def log_in():
    return render_template('index.html')

@app.route('/add.html')
def adding():
    return render_template('add.html')

@app.route('/add.html',methods=['POST'])
def add():
    if request.method == 'POST':
        username = session.get('name')
        cur.execute("SELECT COUNT(id) FROM task")
        rows = cur.fetchall()
        for row in rows:
            ids = row[0] + 1
        cur.execute("INSERT INTO task (content, status, deadline, detail, username, id) VALUES (%s, %s, %s, %s, %s, %s)", (request.form['contents'], request.form['status'], request.form['deadline'], request.form['detail'], username, ids))
        connection.commit()
    tasks = pick()
    return render_template('list.html', username=username, tasks=tasks)

@app.route('/list.html', methods=['POST'])
def display():
    if request.method == 'POST':
        session['name'] = request.form['user_name']
        password = request.form['password']
        username = session.get('name')
        cur.execute("SELECT 1 FROM users WHERE username='" + username + "' AND password=md5('" + password + "')")
        results = cur.fetchall()
        if not results:
            return render_template('index.html')
        else:
            tasks = pick()
            return render_template('list.html', username=username, tasks=tasks)

@app.route('/edit.html', methods=['POST'])
def edited():
    if request.method == 'POST':
        no = session.get('no')
        cur.execute("UPDATE task SET content = '" + request.form['contents'] + "' WHERE id = '" + no + "'")
        cur.execute("UPDATE task SET status = '" + request.form['status'] + "' WHERE id = '" + no + "'")
        cur.execute("UPDATE task SET deadline = '" + request.form['deadline'] + "' WHERE id = '" + no + "'")
        cur.execute("UPDATE task SET detail = '" + request.form['detail'] + "' WHERE id = '" + no + "'")
        connection.commit()
    tasks = pick()
    return render_template('list.html', username=session.get('name'), tasks=tasks)

@app.route('/regist.html')
def regist_disp():
    return render_template('regist.html')

@app.route('/index.html')
def log_out():
    session.pop('name', None)
    return render_template('index.html')

@app.route('/index.html', methods = ['POST'])
def regist():
    if request.method == 'POST':
        username = request.form['user_name']
        password = request.form['password']
        cur.execute("SELECT * FROM users WHERE username='" + username + "'")
        check = cur.fetchall()
        if not check:
            if ( password == request.form['confirm'] ):
                cur.execute("INSERT INTO users (username, password) VALUES ('" + username + "', md5('" + password + "'))")
                connection.commit()
                return render_template('index.html')
            else:
                return render_template('regist.html')
        return render_template('regist.html')

    return render_template('regist.html')

@app.route('/<int:get_id>')
def edit(get_id):
    session['no'] = str(get_id)
    cur.execute("select * from task where id = '" + str(get_id) + "'")
    tasks = cur.fetchall()
    return render_template('edit.html', tasks=tasks)

def pick():
    username = session.get('name')
    cur.execute("SELECT * FROM task WHERE username='" + username + "'")
    tasks = cur.fetchall()
    return tasks

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=53487)
