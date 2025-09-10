# Task Manager - Flask + React

A full-stack task management application with comment functionality.

## Features

### Backend (Flask)
- Task CRUD operations (Create, Read, Update, Delete)
- Comment CRUD operations for tasks
- SQLite database with SQLAlchemy ORM
- RESTful API design
- Automated test suite

### Frontend (React)
- Task management interface
- Add, edit, delete tasks
- Responsive design
- Real-time updates

## Setup Instructions

### Backend Setup
1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Flask application:
```bash
python app.py
```

3. Run tests:
```bash
python test_app.py
```

### Frontend Setup
1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Start the React development server:
```bash
npm start
```

## API Endpoints

### Tasks
- `GET /api/tasks` - Get all tasks
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/<id>` - Update task
- `DELETE /api/tasks/<id>` - Delete task

### Comments
- `GET /api/tasks/<task_id>/comments` - Get comments for a task
- `POST /api/tasks/<task_id>/comments` - Add comment to task
- `PUT /api/comments/<id>` - Update comment
- `DELETE /api/comments/<id>` - Delete comment

## Usage
1. Start the Flask backend (runs on http://localhost:5000)
2. Start the React frontend (runs on http://localhost:3000)
3. Open your browser to http://localhost:3000 to use the application