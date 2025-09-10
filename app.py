from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app, origins=['http://localhost:3000', 'http://localhost:3001', 'http://localhost:3002', 'http://127.0.0.1:3000', 'http://127.0.0.1:3001', 'http://127.0.0.1:3002'])

db = SQLAlchemy(app)

# Models
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    comments = db.relationship('Comment', backref='task', lazy=True, cascade='all, delete-orphan')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Root route
@app.route('/')
def home():
    return jsonify({
        'message': 'Task Manager API',
        'endpoints': {
            'tasks': '/api/tasks',
            'comments': '/api/tasks/<task_id>/comments'
        }
    })

# Task CRUD APIs
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'created_at': task.created_at.isoformat(),
        'comments_count': len(task.comments)
    } for task in tasks])

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    task = Task(title=data['title'], description=data.get('description', ''))
    db.session.add(task)
    db.session.commit()
    return jsonify({'id': task.id, 'title': task.title, 'description': task.description}), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    task.title = data['title']
    task.description = data.get('description', '')
    db.session.commit()
    return jsonify({'id': task.id, 'title': task.title, 'description': task.description})

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return '', 204

# Comment CRUD APIs
@app.route('/api/tasks/<int:task_id>/comments', methods=['GET'])
def get_comments(task_id):
    Task.query.get_or_404(task_id)  # Ensure task exists
    comments = Comment.query.filter_by(task_id=task_id).all()
    return jsonify([{
        'id': comment.id,
        'content': comment.content,
        'task_id': comment.task_id,
        'created_at': comment.created_at.isoformat()
    } for comment in comments])

@app.route('/api/tasks/<int:task_id>/comments', methods=['POST'])
def create_comment(task_id):
    Task.query.get_or_404(task_id)  # Ensure task exists
    data = request.get_json()
    comment = Comment(content=data['content'], task_id=task_id)
    db.session.add(comment)
    db.session.commit()
    return jsonify({
        'id': comment.id,
        'content': comment.content,
        'task_id': comment.task_id,
        'created_at': comment.created_at.isoformat()
    }), 201

@app.route('/api/comments/<int:comment_id>', methods=['PUT'])
def update_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    data = request.get_json()
    comment.content = data['content']
    db.session.commit()
    return jsonify({
        'id': comment.id,
        'content': comment.content,
        'task_id': comment.task_id,
        'created_at': comment.created_at.isoformat()
    })

@app.route('/api/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)