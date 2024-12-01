"""
测试评分引擎的各个组件
"""
import pytest
import numpy as np
from PIL import Image
from happygrow.core.scoring_engine import ScoringEngine

def create_test_image(width=300, height=300, colors=None):
    """创建测试图像"""
    if colors is None:
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    
    image = Image.new('RGB', (width, height), 'white')
    pixels = image.load()
    
    # 创建一个简单的图案
    for x in range(width):
        for y in range(height):
            color_idx = (x + y) % len(colors)
            pixels[x, y] = colors[color_idx]
    
    return image

class TestScoringEngine:
    @pytest.fixture
    def engine(self):
        """创建测试用的评分引擎"""
        image = create_test_image()
        return ScoringEngine(image)
    
    def test_color_usage_analysis(self, engine):
        """测试颜色使用分析"""
        score, details = engine.analyze_color_usage()
        
        assert isinstance(score, float)
        assert 0 <= score <= 1
        
        assert 'unique_colors' in details
        assert 'harmony_score' in details
        assert 'coverage_score' in details
        
        assert details['unique_colors'] >= 3  # 至少包含测试图像中的三种颜色
    
    def test_composition_analysis(self, engine):
        """测试构图分析"""
        score, details = engine.analyze_composition()
        
        assert isinstance(score, float)
        assert 0 <= score <= 1
        
        assert 'thirds_score' in details
        assert 'balance_score' in details
        assert 'focal_score' in details
    
    def test_creativity_analysis(self, engine):
        """测试创造力分析"""
        score, details = engine.analyze_creativity()
        
        assert isinstance(score, float)
        assert 0 <= score <= 1
        
        assert 'shape_variety' in details
        assert 'stroke_expression' in details
        assert 'space_usage' in details
    
    def test_with_monochrome_image(self):
        """测试单色图像"""
        image = create_test_image(colors=[(0, 0, 0)])
        engine = ScoringEngine(image)
        
        color_score, _ = engine.analyze_color_usage()
        assert color_score < 0.5  # 单色图像应该得到较低的颜色分数
    
    def test_with_colorful_image(self):
        """测试多彩图像"""
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255),
                 (255, 255, 0), (255, 0, 255), (0, 255, 255)]
        image = create_test_image(colors=colors)
        engine = ScoringEngine(image)
        
        color_score, _ = engine.analyze_color_usage()
        assert color_score > 0.5  # 丰富的颜色应该得到较高的分数
    
    def test_with_different_sizes(self):
        """测试不同尺寸的图像"""
        sizes = [(100, 100), (300, 300), (500, 500)]
        
        for width, height in sizes:
            image = create_test_image(width=width, height=height)
            engine = ScoringEngine(image)
            
            # 所有分析方法都应该能处理不同尺寸
            color_score, _ = engine.analyze_color_usage()
            comp_score, _ = engine.analyze_composition()
            crea_score, _ = engine.analyze_creativity()
            
            assert all(0 <= score <= 1 for score in [color_score, comp_score, crea_score])
