import unittest
import json
from app import app, db, Task

class CommentAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        with app.app_context():
            db.create_all()
            # Create test task
            task = Task(title='Test Task', description='Test Description')
            db.session.add(task)
            db.session.commit()
            self.task_id = task.id

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_comment(self):
        response = self.app.post(f'/api/tasks/{self.task_id}/comments',
                               data=json.dumps({'content': 'Test comment'}),
                               content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['content'], 'Test comment')

    def test_get_comments(self):
        # Create comment first
        self.app.post(f'/api/tasks/{self.task_id}/comments',
                     data=json.dumps({'content': 'Test comment'}),
                     content_type='application/json')
        
        response = self.app.get(f'/api/tasks/{self.task_id}/comments')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['content'], 'Test comment')

    def test_update_comment(self):
        # Create comment first
        response = self.app.post(f'/api/tasks/{self.task_id}/comments',
                               data=json.dumps({'content': 'Original comment'}),
                               content_type='application/json')
        comment_id = json.loads(response.data)['id']
        
        # Update comment
        response = self.app.put(f'/api/comments/{comment_id}',
                              data=json.dumps({'content': 'Updated comment'}),
                              content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['content'], 'Updated comment')

    def test_delete_comment(self):
        # Create comment first
        response = self.app.post(f'/api/tasks/{self.task_id}/comments',
                               data=json.dumps({'content': 'To be deleted'}),
                               content_type='application/json')
        comment_id = json.loads(response.data)['id']
        
        # Delete comment
        response = self.app.delete(f'/api/comments/{comment_id}')
        self.assertEqual(response.status_code, 204)
        
        # Verify deletion
        response = self.app.get(f'/api/tasks/{self.task_id}/comments')
        data = json.loads(response.data)
        self.assertEqual(len(data), 0)

    def test_comment_for_nonexistent_task(self):
        response = self.app.post('/api/tasks/999/comments',
                               data=json.dumps({'content': 'Test comment'}),
                               content_type='application/json')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()