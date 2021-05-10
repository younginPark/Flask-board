from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from datetime import datetime
from flaskr.models import Users, Posts
from flaskr import db

bp = Blueprint('blog', __name__)

prev_page = 0
next_page = (prev_page + 1) + 3
page_cnt = 0

@bp.route('/')
def index():
    global prev_page, next_page
    page_cnt = pagination()
    page_num = request.args.get('page_num') # 요구페이지
    if page_num is not None:
        page_num = int(page_num)
        if page_num == -1: # 이전 눌렀을 때
            if prev_page > 2: # 0보다 큰 상태이므로 이전 페이지 빼 줘야 함
                next_page = prev_page+1
                prev_page -= 3
                page_num = prev_page+1
            else:
                prev_page = 0
                page_num = 1
        elif page_num == -999: # 다음 눌렀을 때
            if next_page + 3 <= page_cnt: # 다음 페이지 +3 해도 마지막 페이지 수보다 같거나 작을 때
                prev_page = next_page - 1
                next_page += 3
                page_num = prev_page+1
            elif next_page + 3 > page_cnt: # 다음 페이지 +3 하면 마지막 페이지 수보다 작을 때
                prev_page = next_page - 1
                next_page = page_cnt+1
                page_num = prev_page+1

        posts = db.session.query(Posts.id, Posts.title, Posts.body, Posts.created, Posts.author_id, Users.username)\
            .filter(Users.id == Posts.author_id, Posts.deleted == None).order_by(Posts.created.desc()).offset((page_num-1)*5).limit(5).all()
        page_num = None
    else:
        prev_page = 0
        if prev_page + 3 > page_cnt:
            next_page = page_cnt + 1
        else:
            next_page = (prev_page + 1) + 3
        posts = db.session.query(Posts.id, Posts.title, Posts.body, Posts.created, Posts.author_id, Users.username)\
            .filter(Users.id == Posts.author_id, Posts.deleted == None).order_by(Posts.created.desc()).limit(5).all()
    posts = [dict(zip(post.keys(), post)) for post in posts]
    return render_template('blog/index.html', posts=posts, page_cnt=page_cnt, page_start=prev_page+1, page_last=next_page, page_now=page_num)

def pagination():
    global page_cnt
    post_cnt = db.session.query(Posts).filter(Posts.deleted == None).count()

    # 총 페이지 수 구하기
    if post_cnt % 5 == 0:
        page_cnt = post_cnt // 5
    else:
        page_cnt = (post_cnt // 5) + 1
    
    return page_cnt

@bp.route('/<int:id>/post')
def show_body(id):
    post = get_post(id)
    return render_template('blog/postbody.html', post=post)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            new_post = Posts(title=title, body=body, author_id=g.user['id'] , created=datetime.now())
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id, check_author=True):
    post = db.session.query(Posts.id, Posts.title, Posts.body, Posts.created, Posts.author_id, Users.username)\
        .filter(Users.id == Posts.author_id).filter(Posts.id == id).one()
    post = dict(zip(post.keys(), post))
    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))
    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post = db.session.query(Posts).filter(Posts.id == id).one()
            post.title = title
            post.body = body
            db.session.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = db.session.query(Posts).filter(Posts.id == id).one()
    post.deleted = datetime.now()
    db.session.commit()
    return redirect(url_for('blog.index'))