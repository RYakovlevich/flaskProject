import sqlite3
from flask import Flask, render_template, abort, request, flash
from flask import redirect, url_for
from flask import Blueprint


posts_bp = Blueprint('posts', __name__)


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@posts_bp.route('/')
def main():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('main.html', posts=posts)


@posts_bp.route('/post/<int:post_id>')
def show_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id=?', (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return render_template('post.html', post=post)


@posts_bp.route('/post/create', methods=('GET', 'POST'))
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Укажите заголовок!!!')
        if not content:
            flash("Укажите содержание!!!")
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) values (?, ?)', (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('main'))
    return render_template('create.html')


@posts_bp.route('/post/edit/<int:post_id>', methods=('GET', 'POST'))
def edit_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id=?', (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)

    if request.method=='POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Укажите заголовок!!!')
        if not content:
            flash("Укажите содержание!!!")
        if content and title:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title=?, content=? WHERE id =?', (title, content, post_id))
            conn.commit()
            conn.close()
            return redirect(url_for('posts.show_post', post_id=post_id))

    return render_template('edit.html', post=post)


@posts_bp.route('/post/delete/<int:post_id>', methods=('POST',))
def delete_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id=?', (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)

    conn = get_db_connection()
    conn.execute(f'DELETE FROM posts WHERE id={post_id}')
    conn.commit()
    conn.close()
    flash(f'"{post["title"]}" был удалён')
    return redirect(url_for('posts.main'))