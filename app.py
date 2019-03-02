from flask import Flask, render_template, request, session, redirect, url_for, Markup
import psycopg2
import key

app = Flask(__name__)
app.secret_key = key.key()
connection = psycopg2.connect("host=localhost dbname=todo user=postgres password=postgres")
cur = connection.cursor()

@app.template_filter('cr')
def cr(arg):
    return Markup(arg.replace("\r", '<br>'))

@app.route('/')
def log_in():
    return render_template('index.html')

@app.route('/add',methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        username = session.get('name')
        cur.execute("SELECT COUNT(id) FROM task")
        rows = cur.fetchall()
        for row in rows:
            ids = row[0] + 1
        while True:
            cur.execute("select * from task where id ='"+str(ids)+"'")
            check = cur.fetchall()
            if not check:
                break
            ids = ids + 1
        cur.execute("INSERT INTO task (content, status, deadline, detail, username, id) VALUES (%s, %s, %s, %s, %s, %s)", (request.form['contents'], request.form['status'], request.form['deadline'], request.form['detail'], username, ids))
        connection.commit()
        tasks = pick()
        return redirect(url_for('display'))
    else:
        username = session.get('name')
        if not username:
            return redirect(url_for('display'))
        return render_template('add.html')

@app.route('/list', methods=['POST', 'GET'])
def display():
    if request.method == 'POST':
        username = request.form['user_name']
        password = request.form['password']
        session['name'] = username
        cur.execute("SELECT * FROM users WHERE username='" + username + "' AND password=md5('" + password + "')")
        results = cur.fetchall()
        if not results:
            return redirect(url_for('log_in'))
        else:
            tasks = pick()
            return render_template('list.html', username=username, tasks=tasks)

    else:
        username = session.get('name')
        if not username:
            return redirect(url_for('log_in'))
        tasks = pick()
        return render_template('list.html', username=username, tasks=tasks)

@app.route('/edit', methods=['POST', 'GET'])
def edit():
    if request.method == 'POST':
        no = session.get('no')
        cur.execute("UPDATE task SET content = '" + request.form['contents'] + "' WHERE id = '" + no + "'")
        cur.execute("UPDATE task SET status = '" + request.form['status'] + "' WHERE id = '" + no + "'")
        cur.execute("UPDATE task SET deadline = '" + request.form['deadline'] + "' WHERE id = '" + no + "'")
        cur.execute("UPDATE task SET detail = '" + request.form['detail'] + "' WHERE id = '" + no + "'")
        connection.commit()
        return redirect(url_for('display'))
    else:
        session['no'] = request.args.get('no', '')
        cur.execute("select username from task where id ='" + session.get('no') + "'")
        check = cur.fetchall()
        for flag in check:
            name = flag[0]
        if name == session.get('name'):
            cur.execute("select * from task where id = '" + session.get('no') + "'")
            tasks = cur.fetchall()
            return render_template('edit.html', tasks=tasks)
        else:
            tasks = pick()
            return render_template('list.html', username=session.get('name'), tasks=tasks)

@app.route('/view')
def view():
    session['no'] = request.args.get('no', '')
    cur.execute("select username from task where id ='" + session.get('no') + "'")
    check = cur.fetchall()
    for flag in check:
        name = flag[0]
    if name == session.get('name'):
        cur.execute("select * from task where id = '" + session.get('no') + "'")
        tasks = cur.fetchall()
        return render_template('view.html', tasks=tasks)
    else:
        tasks = pick()
        return render_template('list.html', username=session.get('name'), tasks=tasks)

@app.route('/regist')
def regist_disp():
    return render_template('regist.html', error="")

@app.route('/index', methods = ['POST', 'GET'])
def regist():
    if request.method == 'POST':
        username = request.form['user_name']
        password = request.form['password']
        cur.execute("SELECT * FROM users WHERE username='" + username + "'")
        check = cur.fetchall()
        if not check:
            cur.execute("INSERT INTO users (username, password) VALUES ('" + username + "', md5('" + password + "'))")
            connection.commit()
            return render_template('index.html')
        else:
            return render_template('regist.html', error="この名前はすでに使用されています")
    else:
        session.pop('name', None)
        session.pop('no', None)
        return render_template('index.html')

@app.route('/delete')
def delete():
    session['no'] = request.args.get('no', '')
    cur.execute("select username from task where id ='" + session.get('no') + "'")
    check = cur.fetchall()
    for flag in check:
        name = flag[0]
    if name == session.get('name'):
        cur.execute("delete from task where id = '" + session.get('no') + "'")
        connection.commit()
        return redirect(url_for('display'))
    else:
        tasks = pick()
        return render_template('list.html', username=session.get('name'), tasks=tasks)

def pick():
    username = session.get('name')
    cur.execute("SELECT * FROM task WHERE username='" + username + "' ORDER BY deadline ASC")
    tasks = cur.fetchall()
    return tasks

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=53487)
