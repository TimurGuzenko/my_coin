import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import json
import requests

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    logo = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts, logo=logo)

@app.route('/about',methods=('GET', 'POST'))
def about():
    return render_template(('about.html'))

@app.route('/contacts',methods=('GET', 'POST'))
def contacts():
    return render_template(('contacts.html'))

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    x = post['course']

    import requests
    url = f"https://min-api.cryptocompare.com/data/price?fsym={x}&tsyms=USD,EUR,RUB"
    response = requests.get(url)
    data = response.json()
    usd_price = data['USD']
    eur_price = data['EUR']
    rub_price = data['RUB']

    return render_template('post.html', post=post, usd_price=usd_price, eur_price=eur_price, rub_price=rub_price)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        course = request.form['course']
        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content, course) VALUES (?, ?, ?)',
                         (title, content, course))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        course = request.form['course']
        
        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?, course = ?'
                         ' WHERE id = ?',
                         (title, content, course, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    
    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))


# def get_coin():
#     a = {"apikey":'82932de36a7f3a2f0ca30a12270c9ec3859615f8bf55064a59ff02c3d6c38e26'}
#     url = f'https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,EUR,RUB'
#     payload = {}
#     response = request.request("GET",url, headers=a, data = payload)
#     status_code = response.status_code
#     result = response.text
#     return result