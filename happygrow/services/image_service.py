"""
图像处理服务
"""
import os
import uuid
from datetime import datetime
from PIL import Image, UnidentifiedImageError
from werkzeug.utils import secure_filename
from ..config.config import IMAGE_CONFIG

class ImageService:
    @staticmethod
    def validate_image(file):
        """
        验证上传的图像文件
        返回 (is_valid, error_message)
        """
        if not file:
            return False, "未找到上传的文件"
        
        if not file.filename:
            return False, "文件名无效"
        
        # 检查文件扩展名
        allowed_extensions = IMAGE_CONFIG['allowed_extensions']
        if not '.' in file.filename or \
           file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            return False, f"不支持的文件类型。允许的类型: {', '.join(allowed_extensions)}"
        
        # 检查文件是否为空
        file.stream.seek(0, 2)  # 移动到文件末尾
        file_size = file.stream.tell()
        file.stream.seek(0)  # 重置文件指针
        
        if file_size == 0:
            return False, "文件为空"
        
        if file_size > IMAGE_CONFIG['max_file_size']:
            max_size_mb = IMAGE_CONFIG['max_file_size'] / (1024 * 1024)
            return False, f"文件大小超过限制 ({max_size_mb}MB)"
        
        # 验证图像格式和尺寸
        try:
            image = Image.open(file.stream)
            
            # 检查最小尺寸
            if image.size[0] < IMAGE_CONFIG['min_width'] or \
               image.size[1] < IMAGE_CONFIG['min_height']:
                return False, f"图像尺寸太小。最小尺寸: {IMAGE_CONFIG['min_width']}x{IMAGE_CONFIG['min_height']}"
            
            # 检查最大尺寸
            if image.size[0] > IMAGE_CONFIG['max_width'] or \
               image.size[1] > IMAGE_CONFIG['max_height']:
                return False, f"图像尺寸太大。最大尺寸: {IMAGE_CONFIG['max_width']}x{IMAGE_CONFIG['max_height']}"
            
            file.stream.seek(0)  # 重置文件指针
            return True, None
            
        except UnidentifiedImageError:
            return False, "无效的图像文件"
        except Exception as e:
            return False, f"图像处理错误: {str(e)}"
    
    @staticmethod
    def preprocess_image(file):
        """
        预处理图像：
        1. 转换为RGB模式
        2. 调整大小（如果需要）
        3. 标准化
        """
        image = Image.open(file.stream)
        
        # 转换为RGB模式
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # 调整大小（保持宽高比）
        if image.size[0] > IMAGE_CONFIG['max_width'] or \
           image.size[1] > IMAGE_CONFIG['max_height']:
            image.thumbnail((
                IMAGE_CONFIG['max_width'],
                IMAGE_CONFIG['max_height']
            ), Image.Resampling.LANCZOS)
        
        return image
    
    @staticmethod
    def save_image(image, original_filename, output_dir):
        """
        保存处理后的图像
        返回保存的文件路径
        """
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 生成唯一文件名
        filename = secure_filename(original_filename)
        name, ext = os.path.splitext(filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())[:8]
        new_filename = f"{name}_{timestamp}_{unique_id}.jpg"
        
        # 保存图像
        output_path = os.path.join(output_dir, new_filename)
        image.save(output_path, 'JPEG', quality=IMAGE_CONFIG['jpeg_quality'])
        
        return output_path
