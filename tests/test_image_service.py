"""
测试图像处理服务
"""
import pytest
import os
from PIL import Image, UnidentifiedImageError
import io
from werkzeug.datastructures import FileStorage
from happygrow.services.image_service import ImageService
from happygrow.config.config import IMAGE_CONFIG

class TestImageService:
    @pytest.fixture
    def sample_image(self):
        """创建示例图像"""
        image = Image.new('RGB', (400, 400), 'white')
        # 添加一些内容使其不是纯白图像
        for x in range(100):
            for y in range(100):
                image.putpixel((x, y), (255, 0, 0))
        return image
    
    @pytest.fixture
    def image_file(self, sample_image):
        """创建图像文件对象"""
        img_byte_arr = io.BytesIO()
        sample_image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        return FileStorage(
            stream=img_byte_arr,
            filename='test.png',
            content_type='image/png'
        )
    
    def test_validate_valid_image(self, image_file):
        """测试有效图像的验证"""
        is_valid, error = ImageService.validate_image(image_file)
        assert is_valid
        assert error is None
    
    def test_validate_no_file(self):
        """测试无文件情况"""
        is_valid, error = ImageService.validate_image(None)
        assert not is_valid
        assert error == "未找到上传的文件"
    
    def test_validate_invalid_extension(self, image_file):
        """测试无效文件扩展名"""
        image_file.filename = 'test.txt'
        is_valid, error = ImageService.validate_image(image_file)
        assert not is_valid
        assert "不支持的文件类型" in error
    
    def test_validate_corrupted_image(self):
        """测试损坏的图像文件"""
        corrupted_data = io.BytesIO(b'corrupted image data')
        file = FileStorage(
            stream=corrupted_data,
            filename='corrupted.png',
            content_type='image/png'
        )
        is_valid, error = ImageService.validate_image(file)
        assert not is_valid
        assert "无效的图像文件" in error
    
    def test_validate_empty_file(self):
        """测试空文件"""
        empty_file = FileStorage(
            stream=io.BytesIO(b''),
            filename='empty.png',
            content_type='image/png'
        )
        is_valid, error = ImageService.validate_image(empty_file)
        assert not is_valid
        assert "文件为空" in error
    
    def test_validate_size_too_small(self):
        """测试图像尺寸太小"""
        small_image = Image.new('RGB', (50, 50), 'white')
        img_io = io.BytesIO()
        small_image.save(img_io, format='PNG')
        img_io.seek(0)
        
        file = FileStorage(
            stream=img_io,
            filename='small.png',
            content_type='image/png'
        )
        is_valid, error = ImageService.validate_image(file)
        assert not is_valid
        assert "图像尺寸太小" in error
    
    def test_validate_size_too_large(self, sample_image):
        """测试文件过大"""
        large_image = Image.new('RGB', (8000, 8000), 'white')
        img_byte_arr = io.BytesIO()
        large_image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        file = FileStorage(
            stream=img_byte_arr,
            filename='large.png',
            content_type='image/png'
        )
        
        is_valid, error = ImageService.validate_image(file)
        assert not is_valid
        assert "图像尺寸太大" in error
    
    def test_preprocess_image_with_alpha(self):
        """测试处理带透明通道的图像"""
        # 创建RGBA图像
        image = Image.new('RGBA', (400, 400), (255, 255, 255, 128))
        img_io = io.BytesIO()
        image.save(img_io, format='PNG')
        img_io.seek(0)
        
        file = FileStorage(
            stream=img_io,
            filename='transparent.png',
            content_type='image/png'
        )
        
        processed = ImageService.preprocess_image(file)
        assert processed.mode == 'RGB'
        assert processed.size == (400, 400)
    
    def test_preprocess_image_resize(self):
        """测试图像缩放"""
        # 创建大图像
        large_image = Image.new('RGB', (5000, 5000), 'white')
        img_io = io.BytesIO()
        large_image.save(img_io, format='PNG')
        img_io.seek(0)
        
        file = FileStorage(
            stream=img_io,
            filename='large.png',
            content_type='image/png'
        )
        
        processed = ImageService.preprocess_image(file)
        assert processed.size[0] <= IMAGE_CONFIG['max_width']
        assert processed.size[1] <= IMAGE_CONFIG['max_height']
    
    def test_preprocess_image_invalid(self):
        """测试处理无效图像"""
        invalid_file = FileStorage(
            stream=io.BytesIO(b'invalid data'),
            filename='invalid.png',
            content_type='image/png'
        )
        
        with pytest.raises(UnidentifiedImageError):
            ImageService.preprocess_image(invalid_file)
    
    def test_save_image_creates_directory(self, sample_image, tmp_path):
        """测试保存图像时创建目录"""
        output_dir = os.path.join(str(tmp_path), 'nested', 'dir')
        saved_path = ImageService.save_image(sample_image, 'test.png', output_dir)
        
        assert os.path.exists(saved_path)
        assert os.path.isfile(saved_path)
    
    def test_save_image_unique_names(self, sample_image, tmp_path):
        """测试保存多个同名图像"""
        output_dir = str(tmp_path)
        path1 = ImageService.save_image(sample_image, 'test.png', output_dir)
        path2 = ImageService.save_image(sample_image, 'test.png', output_dir)
        
        assert path1 != path2
        assert os.path.exists(path1)
        assert os.path.exists(path2)
