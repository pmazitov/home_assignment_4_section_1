from flask import Flask, render_template, request, url_for, flash, redirect
from markupsafe import escape
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'df0331cefc6c2b9a5d0208a726a5d1c0fd37324feba25506'


messages = {'1234':
                 {'title': 'Message One',
                  'content': 'Message One Content',
                  'datetime': 'today!'},
            '5678':
                 {'title': 'Message Two',
                  'content': 'Message Two Content',
                  'datetime': 'long time ago'}
            }


@app.route('/')
def index():
    return render_template('index.html', messages=messages)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            messages[str(abs(hash(dt_string + title)))] = {'title': title,
                                                           'content': content,
                                                           'datetime': dt_string}
            return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/postpage/<string:post_id>')
def postpage(post_id=None):
    post_d = messages[post_id]
    return render_template('postpage.html',
                           title=escape(post_d['title']),
                           content=escape(post_d['content']),
                           datetime=escape(post_d['datetime'])
                          )

