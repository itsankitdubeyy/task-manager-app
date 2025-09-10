import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

function App() {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState({ title: '', description: '' });
  const [editingTask, setEditingTask] = useState(null);

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      const response = await axios.get(`${API_BASE}/tasks`);
      setTasks(response.data);
    } catch (error) {
      console.error('Error fetching tasks:', error);
      alert('Cannot connect to backend. Make sure Flask server is running on port 5000.');
    }
  };

  const createTask = async (e) => {
    e.preventDefault();
    if (!newTask.title.trim()) return;
    
    try {
      await axios.post(`${API_BASE}/tasks`, newTask);
      setNewTask({ title: '', description: '' });
      fetchTasks();
    } catch (error) {
      console.error('Error creating task:', error);
    }
  };

  const updateTask = async (e) => {
    e.preventDefault();
    if (!editingTask.title.trim()) return;
    
    try {
      await axios.put(`${API_BASE}/tasks/${editingTask.id}`, {
        title: editingTask.title,
        description: editingTask.description
      });
      setEditingTask(null);
      fetchTasks();
    } catch (error) {
      console.error('Error updating task:', error);
    }
  };

  const deleteTask = async (taskId) => {
    if (!window.confirm('Are you sure you want to delete this task?')) return;
    
    try {
      await axios.delete(`${API_BASE}/tasks/${taskId}`);
      fetchTasks();
    } catch (error) {
      console.error('Error deleting task:', error);
    }
  };

  return (
    <div className="app">
      <h1>Task Manager</h1>
      
      <form onSubmit={createTask} className="task-form">
        <h2>Add New Task</h2>
        <input
          type="text"
          placeholder="Task title"
          value={newTask.title}
          onChange={(e) => setNewTask({ ...newTask, title: e.target.value })}
        />
        <textarea
          placeholder="Task description"
          value={newTask.description}
          onChange={(e) => setNewTask({ ...newTask, description: e.target.value })}
        />
        <button type="submit">Add Task</button>
      </form>

      {editingTask && (
        <form onSubmit={updateTask} className="task-form edit-form">
          <h2>Edit Task</h2>
          <input
            type="text"
            value={editingTask.title}
            onChange={(e) => setEditingTask({ ...editingTask, title: e.target.value })}
          />
          <textarea
            value={editingTask.description}
            onChange={(e) => setEditingTask({ ...editingTask, description: e.target.value })}
          />
          <div>
            <button type="submit">Update Task</button>
            <button type="button" onClick={() => setEditingTask(null)}>Cancel</button>
          </div>
        </form>
      )}

      <div className="tasks-list">
        <h2>Tasks ({tasks.length})</h2>
        {tasks.map(task => (
          <div key={task.id} className="task-item">
            <h3>{task.title}</h3>
            <p>{task.description}</p>
            <small>Created: {new Date(task.created_at).toLocaleDateString()}</small>
            <small>Comments: {task.comments_count}</small>
            <div className="task-actions">
              <button onClick={() => setEditingTask(task)}>Edit</button>
              <button onClick={() => deleteTask(task.id)} className="delete-btn">Delete</button>
            </div>
          </div>
        ))}
        {tasks.length === 0 && <p>No tasks found. Create your first task above!</p>}
      </div>
    </div>
  );
}

export default App;