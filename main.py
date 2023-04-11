# -*- coding: UTF-8 -*-
# 导入所需的模块
from flask import Flask, request, render_template, redirect
import uuid
import sqlite3

# 创建一个flask应用
app = Flask(__name__)

# 连接数据库，并设置check_same_thread参数为False
conn = sqlite3.connect('data.db', check_same_thread=False)
c = conn.cursor()

# 创建一个表格，用于存储文字和url
c.execute('CREATE TABLE IF NOT EXISTS texts (text TEXT, url TEXT)')
conn.commit()


# 定义一个路由，用于显示主页
@app.route('/')
def index():
  # 返回一个简单的表单，让用户输入文字
  return render_template('index.html')


# 定义一个路由，用于处理表单提交
@app.route('/submit', methods=['POST'])
def submit():
  # 获取用户输入的文字
  text = request.form.get('text')
  # 生成一个唯一的字符串
  url = str(uuid.uuid4())
  # 将文字和url存入数据库
  c.execute('INSERT INTO texts VALUES (?, ?)', (text, url))
  conn.commit()
  # 获取web页面的域名
  domain = request.host_url
  # 返回一个提示信息，告诉用户他的url是什么，并加上域名
  return redirect(f'{domain}{url}')

# 定义一个路由，用于处理url访问
@app.route('/<url>')
def get_text(url):
  # 根据url查询数据库，获取对应的文字
  c.execute('SELECT text FROM texts WHERE url = ?', (url, ))
  text = c.fetchone()
  # 如果找到了文字，就返回文本，并显示一个按钮，让用户可以进入编辑页面
  if text:
    return render_template('text.html', text=text[0], url=url)
  # 如果没有找到文字，就返回一个错误信息
  else:
    return 'Invalid url'


# 定义一个路由，用于处理文本编辑
@app.route('/edit/<url>')
def edit_text(url):
  # 根据url查询数据库，获取对应的文字
  c.execute('SELECT text FROM texts WHERE url = ?', (url, ))
  text = c.fetchone()
  # 如果找到了文字，就返回一个包含操作按钮或链接的html页面
  if text:
    return render_template('edit.html', text=text[0], url=url)
  # 如果没有找到文字，就返回一个错误信息
  else:
    return 'Invalid url'


# 定义一个路由，用于处理文本更新
@app.route('/update/<url>', methods=['POST'])
def update_text(url):
  # 获取用户输入的新文字
  new_text = request.form.get('new_text')
  # 根据url更新数据库中的文字
  c.execute('UPDATE texts SET text = ? WHERE url = ?', (new_text, url))
  conn.commit()
  # 返回一个提示信息，告诉用户他的文本已经更新，并提供一个链接回到编辑页面
  return f'Your text is updated. <a href="/edit/{url}">Go back</a>'


# 定义一个路由，用于处理文本删除
@app.route('/delete/<url>')
def delete_text(url):
  # 根据url删除数据库中的文字和url
  c.execute('DELETE FROM texts WHERE url = ?', (url, ))
  conn.commit()
  # 返回一个提示信息，告诉用户他的文本已经删除，并提供一个链接回到主页
  return f'Your text is deleted. <a href="/">Go back</a>'


@app.route('/raw/<url>')
def get_raw(url):
  # 根据url查询数据库，获取对应的文字
  c.execute('SELECT text FROM texts WHERE url = ?', (url, ))
  text = c.fetchone()
  if text:
    return text[0]
  else:
    return 'Invalid url'


# 运行flask应用
if __name__ == '__main__':
  app.run(host="0.0.0.0")
