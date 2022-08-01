from flask import Flask, render_template, abort, request, flash
from flask import redirect, url_for
from flask import Blueprint
from models import Posts
from start import db


postsbp = Blueprint('posts', __name__)


# def get_db_connection():
#     conn = sqlite3.connect('database.db')
#     conn.row_factory = sqlite3.Row
#     return conn


@postsbp.route('/')
def main():
    posts_ = Posts.query.all()
    return render_template('main.html', posts=posts_)


@postsbp.route('/post/<int:post_id>')
def show_post(post_id):
    posts_ = Posts.query.filter_by(id=post_id).first()
    if posts_ is None:
        abort(404)
    return render_template('post.html', post=posts_)


@postsbp.route('/post/create', methods=('GET', 'POST'))
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Укажите заголовок!!!')
        if not content:
            flash("Укажите содержание!!!")
        else:
            posts_ = Posts(title=title, content=content)
            db.session.add(posts_)
            db.session.commit()
            return redirect(url_for('posts.index'))
    return render_template('create.html')


@postsbp.route('/post/edit/<int:post_id>', methods=('GET', 'POST'))
def edit_post(post_id):
    posts_ = Posts.query.filter_by(id=post_id).first()

    if request.method == 'POST':
        posts_.title = request.form['title']
        posts_.content = request.form['content']

        if not posts_.title:
            flash('Укажите заголовок!!!')
        if not posts_.content:
            flash("Укажите содержание!!!")

        db.session.add(posts_)
        db.session.commit()
        return redirect(url_for('posts.show_post', post_id=post_id))
    return render_template('edit.html', post=posts_)


@postsbp.route('/post/delete/<int:post_id>', methods=('POST',))
def delete_post(post_id):
    posts_= Posts.query.filter_by(id=post_id).first()
    db.session.delete(posts_)
    db.session.commit()
    flash(f'"{posts_["title"]}" был удалён')
    return redirect(url_for('posts.main'))
