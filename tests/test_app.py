import unittest
from app import app
from flask_testing import TestCase
import json
import os
from io import BytesIO

class TestDrawingApp(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        # 确保测试图片存在
        if not os.path.exists('test_drawing.jpg'):
            from create_test_image import create_test_image
            create_test_image()

    def test_home_page(self):
        response = self.client.get('/')
        self.assert200(response)
        self.assert_template_used('index.html')

    def test_score_drawing(self):
        # 测试图片上传和评分
        with open('test_drawing.jpg', 'rb') as img:
            response = self.client.post('/score', 
                data={'drawing': (img, 'test_drawing.jpg')})
            self.assert200(response)
            data = json.loads(response.data)
            self.assertIn('score', data)
            self.assertIn('feedback', data)
            self.assertTrue(isinstance(data['score'], int))
            self.assertTrue(isinstance(data['feedback'], str))
            self.assertTrue(0 <= data['score'] <= 100)

    def test_error_handling(self):
        # 测试无文件上传
        response = self.client.post('/score')
        self.assertEqual(response.status_code, 400)
        
        # 测试空文件名
        empty_file = BytesIO()
        response = self.client.post('/score', 
            data={'drawing': (empty_file, '')})
        self.assertEqual(response.status_code, 400)
        
        # 测试无效文件类型
        text_file = BytesIO(b'This is not an image')
        response = self.client.post('/score', 
            data={'drawing': (text_file, 'test.txt')})
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
