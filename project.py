from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)
tasks = [
    {"id": 1, "title": "Buy groceries"},
    {"id": 2, "title": "Read a book"},
    {"id": 3, "title": "Exercise for 30 minutes"}
]

def get_new_id():
    if tasks:
        return max(task["id"] for task in tasks) + 1
    else:
        return 1

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>To-Do List</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 20px;
            }
            h1 {
                color: #333;
            }
            form {
                margin-bottom: 20px;
            }
            input[type="text"] {
                padding: 10px;
                width: 300px;
            }
            button {
                padding: 10px 15px;
                background-color: #5cb85c;
                color: white;
                border: none;
                cursor: pointer;
            }
            button:hover {
                background-color: #4cae4c;
            }
            ul {
                list-style-type: none;
                padding: 0;
            }
            li {
                margin-bottom: 10px;
            }
        </style>
    </head>
    <body>
        <h1>To-Do List</h1>
        <form action="{{ url_for('add_task') }}" method="post">
            <input type="text" name="task" placeholder="Enter a new task" required>
            <button type="submit">Add Task</button>
        </form>
        <ul>
            {% for task in tasks %}
                <li>
                    {{ task.title }}
                    <form action="{{ url_for('delete_task', task_id=task.id) }}" method="post" style="display:inline;">
                        <button type="submit">Delete</button>
                    </form>
                </li>
            {% endfor %}
        </ul>
    </body>
    </html>
    ''', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task_title = request.form.get('task')
    if task_title:
        new_task = {"id": get_new_id(), "title": task_title}
        tasks.append(new_task)
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
