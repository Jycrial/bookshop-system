from flask import render_template, request, url_for, flash, redirect
from books import *

"""
路由
"""

# home
@app.route(r"/")
def home():
    data_dict = select_all_as_dict("select * from books order by id asc")
    return render_template(r"home.html", posts=data_dict)

# about
@app.route(r"/about")
def about():
    return render_template(r"about.html")

# edit
@app.route(r"/posts/<int:id>/edit", methods=('GET', 'POST', ))
def edit(id):
    post = select_all_as_dict(f"select * from books where id = {id}")[0]
    is_delete = request.form.get('isdelete', False)
    if is_delete:
        with get_db_conn() as conn:
                with conn.cursor() as cs:
                    cs.execute(f"delete from books where id = {post['id']}")
                    should_change = select_all_as_dict(f"select * from books where id > {id} order by id")
                    for s in should_change:
                        cs.execute(f"update books SET id = {s['id'] - 1} where id = {s['id']}")
                    conn.commit()
                    flash('删除成功！')
                    return redirect(url_for('home'))
    

    if request.method == 'POST':
        name = request.form['name']
        author = request.form['author']
        price = request.form['price']
        description = request.form['description']

        if not name:
            flash('请输入书名')
        elif not author:
            flash('请输入作者姓名')
        elif not price:
            flash('请输入定价')
        elif not description:
            flash('请输入描述')
        else:
            with get_db_conn() as conn:
                with conn.cursor() as cs:
                    cs.execute(f"delete from books where id = {post['id']}")
                    cs.execute(f"""INSERT INTO books (id, name, author, price, isbn, num, description)
                                VALUES
                                ({post['id']}, '{name}', '{author}', {price}, {post['isbn']}, {post['num']}, '{description}')
                                """)
                    conn.commit()

                    flash('保存成功！')
                    return redirect(url_for('home'))

    return render_template(r"edit.html", post=post)

# new
@app.route(r"/new", methods=('GET', 'POST', ))
def new():
    posts = select_all_as_dict(f"select isbn from books order by id")
    new_id = select_all_as_dict(f"select * from books order by id asc")[-1]['id'] + 1
    isbn_lists = [str(d['isbn']) for d in posts]

    if request.method == 'POST':
        name = request.form['name']
        author = request.form['author']
        isbn = request.form['isbn']
        num = request.form['num']
        price = request.form['price']
        description = request.form['description']

        if not name:
            flash('请输入书名')
        elif not author:
            flash('请输入作者姓名')
        elif not price:
            flash('请输入定价')
        elif not isbn or isbn in isbn_lists:
            flash('请输入正确的ISBN')
        elif not num:
            flash('请输入数量')
        elif not description:
            flash('请输入描述')
        else:
            with get_db_conn() as conn:
                with conn.cursor() as cs:
                    cs.execute(f"""INSERT INTO books (id, name, author, price, isbn, num, description)
                                VALUES
                                ({new_id}, '{name}', '{author}', {price}, {isbn}, {num}, '{description}')
                                """)
                    conn.commit()

                    flash('保存成功！')
                    return redirect(url_for('home'))

    return render_template(r"new.html")

# search
@app.route(r"/search", methods=('GET', 'POST', ))
def search():
    book_result = None
    if request.method == 'POST':
        name = request.form['name']
        if not name:
            book_result = select_all_as_dict(f"select * from books order by id")
        else:
            book_result = select_all_as_dict(f"select * from books where name like '%{name}%' order by id")
        flash('查找成功！')
    return render_template(r"search.html", book_result = book_result)