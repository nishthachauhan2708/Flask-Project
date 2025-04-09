from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

# In-memory storage for blog posts
posts = [
    {'id': 1, 'title': 'First Post', 'content': 'This is the content of the first post.'},
    {'id': 2, 'title': 'Second Post', 'content': 'This is the content of the second post.'}
]

# Home route to display all posts
@app.route('/')
def index():
    return render_template_string('''
    <!doctype html>
    <title>Simple Blog</title>
    <h1>Simple Blog</h1>
    <a href="{{ url_for('add') }}">Add New Post</a>
    <ul>
      {% for post in posts %}
        <li>
          <a href="{{ url_for('view', post_id=post.id) }}">{{ post.title }}</a>
          <a href="{{ url_for('edit', post_id=post.id) }}">Edit</a>
          <form action="{{ url_for('delete', post_id=post.id) }}" method="post" style="display:inline;">
            <button type="submit">Delete</button>
          </form>
        </li>
      {% endfor %}
    </ul>
    ''', posts=posts)

# Route to view a single post
@app.route('/post/<int:post_id>')
def view(post_id):
    post = next((p for p in posts if p['id'] == post_id), None)
    if post is None:
        return 'Post not found!', 404
    return render_template_string('''
    <!doctype html>
    <title>{{ post.title }}</title>
    <h1>{{ post.title }}</h1>
    <p>{{ post.content }}</p>
    <a href="{{ url_for('index') }}">Back to Home</a>
    ''', post=post)

# Route to add a new post
@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        new_id = max((post['id'] for post in posts), default=0) + 1
        title = request.form['title']
        content = request.form['content']
        posts.append({'id': new_id, 'title': title, 'content': content})
        return redirect(url_for('index'))
    return render_template_string('''
    <!doctype html>
    <title>Add New Post</title>
    <h1>Add New Post</h1>
    <form method="post">
      <label for="title">Title</label>
      <input type="text" id="title" name="title" required>
      <label for="content">Content</label>
      <textarea id="content" name="content" required></textarea>
      <button type="submit">Add</button>
    </form>
    <a href="{{ url_for('index') }}">Back to Home</a>
    ''')

# Route to edit an existing post
@app.route('/edit/<int:post_id>', methods=('GET', 'POST'))
def edit(post_id):
    post = next((p for p in posts if p['id'] == post_id), None)
    if post is None:
        return 'Post not found!', 404
    if request.method == 'POST':
        post['title'] = request.form['title']
        post['content'] = request.form['content']
        return redirect(url_for('index'))
    return render_template_string('''
    <!doctype html>
    <title>Edit Post</title>
    <h1>Edit Post</h1>
    <form method="post">
      <label for="title">Title</label>
      <input type="text" id="title" name="title" value="{{ post.title }}" required>
      <label for="content">Content</label>
      <textarea id="content" name="content" required>{{ post.content }}</textarea>
      <button type="submit">Update</button>
    </form>
    <a href="{{ url_for('index') }}">Back to Home</a>
    ''', post=post)

# Route to delete a post
@app.route('/delete/<int:post_id>', methods=('POST',))
def delete(post_id):
    global posts
    posts = [p for p in posts if p['id'] != post_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
