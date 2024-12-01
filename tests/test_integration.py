"""
HappyGrow 系统集成测试
"""
import pytest
import os
import io
from PIL import Image
from flask.testing import FlaskClient
from app import app

class TestHappyGrowIntegration:
    @pytest.fixture
    def client(self):
        """创建测试客户端"""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    @pytest.fixture
    def test_image(self):
        """创建测试图像"""
        # 创建一个彩色测试图像
        width, height = 400, 400
        image = Image.new('RGB', (width, height), 'white')
        
        # 添加一些彩色图案
        colors = [
            (255, 0, 0),    # 红
            (0, 255, 0),    # 绿
            (0, 0, 255),    # 蓝
            (255, 255, 0),  # 黄
            (255, 0, 255),  # 紫
        ]
        
        # 创建一个简单的彩色图案
        for x in range(width):
            for y in range(height):
                color_idx = ((x + y) // 50) % len(colors)
                image.putpixel((x, y), colors[color_idx])
        
        # 保存到字节流
        img_io = io.BytesIO()
        image.save(img_io, 'PNG')
        img_io.seek(0)
        
        return img_io
    
    def test_home_page(self, client):
        """测试主页访问"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'HappyGrow' in response.data
    
    def test_analyze_drawing_success(self, client, test_image):
        """测试成功分析画作"""
        data = {
            'file': (test_image, 'test.png'),
            'age_group': 'school'
        }
        response = client.post('/analyze', data=data, content_type='multipart/form-data')
        
        assert response.status_code == 200
        json_data = response.get_json()
        
        # 验证返回的数据结构
        assert 'scores' in json_data
        assert 'feedback' in json_data
        assert 'suggestions' in json_data
        assert 'image_path' in json_data
        
        # 验证分数
        scores = json_data['scores']
        assert 'color_usage' in scores
        assert 'composition' in scores
        assert 'creativity' in scores
        
        # 验证分数范围
        for score in scores.values():
            assert 0 <= score <= 1
        
        # 验证反馈
        feedback = json_data['feedback']
        assert 'overall' in feedback
        assert 'specific' in feedback
        assert 'encouragement' in feedback
        
        # 验证建议
        assert isinstance(json_data['suggestions'], list)
        assert len(json_data['suggestions']) > 0
    
    def test_analyze_drawing_no_file(self, client):
        """测试没有文件的情况"""
        response = client.post('/analyze', data={})
        assert response.status_code == 400
        assert b'error' in response.data
    
    def test_analyze_drawing_invalid_file(self, client):
        """测试无效文件类型"""
        data = {
            'file': (io.BytesIO(b'not an image'), 'test.txt'),
            'age_group': 'school'
        }
        response = client.post('/analyze', data=data, content_type='multipart/form-data')
        assert response.status_code == 400
    
    def test_analyze_drawing_different_age_groups(self, client, test_image):
        """测试不同年龄组"""
        age_groups = ['toddler', 'preschool', 'school', 'preteen']
        
        for age_group in age_groups:
            test_image.seek(0)  # 重置文件指针
            data = {
                'file': (test_image, 'test.png'),
                'age_group': age_group
            }
            response = client.post('/analyze', data=data, content_type='multipart/form-data')
            
            assert response.status_code == 200
            json_data = response.get_json()
            
            # 验证反馈是否包含年龄相关的内容
            feedback = json_data['feedback']
            assert feedback['encouragement']  # 应该有鼓励性的反馈
    
    def test_analyze_drawing_large_image(self, client):
        """测试大尺寸图像"""
        # 创建一个大图像
        large_image = Image.new('RGB', (5000, 5000), 'white')
        img_io = io.BytesIO()
        large_image.save(img_io, 'PNG')
        img_io.seek(0)
        
        data = {
            'file': (img_io, 'large.png'),
            'age_group': 'school'
        }
        response = client.post('/analyze', data=data, content_type='multipart/form-data')
        
        # 应该返回错误，因为图像太大
        assert response.status_code == 400
    
    def test_analyze_drawing_saves_file(self, client, test_image):
        """测试图像保存功能"""
        data = {
            'file': (test_image, 'test.png'),
            'age_group': 'school'
        }
        response = client.post('/analyze', data=data, content_type='multipart/form-data')
        
        assert response.status_code == 200
        json_data = response.get_json()
        
        # 验证文件是否被保存
        saved_path = os.path.join(app.root_path, json_data['image_path'])
        assert os.path.exists(saved_path)
        
        # 清理测试文件
        os.remove(saved_path)
