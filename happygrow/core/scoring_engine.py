"""
核心评分引擎，实现各种评分维度的具体算法
"""
import numpy as np
from PIL import Image
from typing import Dict, Tuple, List
import colorsys
from collections import Counter
from ..config.config import SCORING_CRITERIA, SCORING_WEIGHTS

class ScoringEngine:
    def __init__(self, image: Image.Image):
        """
        初始化评分引擎
        
        Args:
            image: PIL Image对象
        """
        self.image = image
        self.np_image = np.array(image)
        self.width, self.height = image.size
        self.rgb_image = image.convert('RGB')

    def analyze_color_usage(self) -> Tuple[float, Dict]:
        """分析颜色使用情况"""
        # 获取所有像素的颜色
        colors = []
        for x in range(self.width):
            for y in range(self.height):
                colors.append(self.rgb_image.getpixel((x, y)))
        
        # 计算独特颜色数量
        unique_colors = len(set(colors))
        
        # 计算颜色和谐度
        harmony_score = self._calculate_color_harmony(colors)
        
        # 计算颜色覆盖率
        coverage_score = self._calculate_color_coverage()
        
        # 根据权重计算总分
        criteria = SCORING_CRITERIA['color_usage']
        color_score = (
            self._score_unique_colors(unique_colors) * criteria['unique_colors']['weight'] +
            harmony_score * criteria['color_harmony']['weight'] +
            coverage_score * criteria['color_coverage']['weight']
        )
        
        return color_score, {
            'unique_colors': unique_colors,
            'harmony_score': harmony_score,
            'coverage_score': coverage_score
        }

    def analyze_composition(self) -> Tuple[float, Dict]:
        """分析画面构图"""
        # 计算三分法得分
        thirds_score = self._analyze_rule_of_thirds()
        
        # 计算平衡性得分
        balance_score = self._analyze_balance()
        
        # 计算焦点得分
        focal_score = self._analyze_focal_point()
        
        # 根据权重计算总分
        criteria = SCORING_CRITERIA['composition']
        composition_score = (
            thirds_score * criteria['rule_of_thirds']['weight'] +
            balance_score * criteria['balance']['weight'] +
            focal_score * criteria['focal_point']['weight']
        )
        
        return composition_score, {
            'thirds_score': thirds_score,
            'balance_score': balance_score,
            'focal_score': focal_score
        }

    def analyze_creativity(self) -> Tuple[float, Dict]:
        """分析创造力表现"""
        # 分析形状多样性
        shape_variety = self._analyze_shape_variety()
        
        # 分析笔触表现力
        stroke_expression = self._analyze_stroke_expression()
        
        # 分析空间利用
        space_usage = self._analyze_space_usage()
        
        # 计算总分
        weights = SCORING_CRITERIA['creativity']
        creativity_score = (
            shape_variety * weights['variety'] +
            stroke_expression * weights['expression'] +
            space_usage * weights['uniqueness']
        )
        
        return creativity_score, {
            'shape_variety': shape_variety,
            'stroke_expression': stroke_expression,
            'space_usage': space_usage
        }

    def _calculate_color_harmony(self, colors: List[Tuple[int, int, int]]) -> float:
        """计算颜色和谐度"""
        # 转换RGB为HSV
        hsv_colors = []
        for r, g, b in colors:
            h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
            hsv_colors.append((h, s, v))
        
        # 分析色相分布
        hues = [h for h, _, _ in hsv_colors]
        hue_counts = Counter([int(h * 360) for h in hues])
        
        # 检查互补色
        harmony_score = 0
        for hue in hue_counts:
            complement = (hue + 180) % 360
            if abs(hue_counts[hue] - hue_counts[complement]) < len(colors) * 0.1:
                harmony_score += SCORING_CRITERIA['color_usage']['color_harmony']['complementary_bonus']
        
        # 标准化得分
        return min(100, harmony_score) / 100

    def _calculate_color_coverage(self) -> float:
        """计算颜色覆盖率"""
        # 转换为灰度图像
        gray = self.image.convert('L')
        np_gray = np.array(gray)
        
        # 计算非空白区域比例
        non_white_pixels = np.sum(np_gray < 250)  # 假设接近白色的像素为空白
        total_pixels = self.width * self.height
        
        coverage = non_white_pixels / total_pixels
        min_coverage = SCORING_CRITERIA['color_usage']['color_coverage']['min_coverage']
        
        return min(1.0, coverage / min_coverage)

    def _score_unique_colors(self, unique_colors: int) -> float:
        """根据独特颜色数量评分"""
        thresholds = SCORING_CRITERIA['color_usage']['unique_colors']['thresholds']
        for threshold, score in sorted(thresholds.items()):
            if unique_colors <= threshold:
                return score / 100
        return 1.0

    def _analyze_rule_of_thirds(self) -> float:
        """分析三分法构图"""
        # 将图像分为3x3网格
        h_thirds = self.height // 3
        w_thirds = self.width // 3
        
        # 计算交叉点周围的内容密度
        intersection_scores = []
        for i in [1, 2]:
            for j in [1, 2]:
                region = self.np_image[
                    (i-1)*h_thirds:(i+1)*h_thirds,
                    (j-1)*w_thirds:(j+1)*w_thirds
                ]
                density = np.mean(np.sum(region != 255, axis=2))
                intersection_scores.append(density)
        
        return np.mean(intersection_scores) / 255

    def _analyze_balance(self) -> float:
        """分析画面平衡性"""
        # 将图像分为四个象限
        h_mid = self.height // 2
        w_mid = self.width // 2
        
        quadrants = [
            self.np_image[:h_mid, :w_mid],    # 左上
            self.np_image[:h_mid, w_mid:],    # 右上
            self.np_image[h_mid:, :w_mid],    # 左下
            self.np_image[h_mid:, w_mid:]     # 右下
        ]
        
        # 计算每个象限的内容密度
        densities = []
        for quad in quadrants:
            density = np.mean(np.sum(quad != 255, axis=2))
            densities.append(density)
        
        # 计算平衡得分
        balance = 1 - np.std(densities) / np.mean(densities)
        return max(0, min(1, balance))

    def _analyze_focal_point(self) -> float:
        """分析焦点区域"""
        # 使用边缘检测找到主要内容区域
        from scipy import ndimage
        gray = np.mean(self.np_image, axis=2)
        edges = ndimage.sobel(gray)
        
        # 找到边缘密度最高的区域
        kernel_size = min(self.width, self.height) // 5
        focal_map = ndimage.uniform_filter(np.abs(edges), kernel_size)
        
        # 计算焦点得分
        max_density = np.max(focal_map)
        threshold = SCORING_CRITERIA['composition']['focal_point']['detection_threshold']
        
        return min(1.0, max_density / (255 * threshold))

    def _analyze_shape_variety(self) -> float:
        """分析形状多样性"""
        # 使用边缘检测识别形状
        from scipy import ndimage
        gray = np.mean(self.np_image, axis=2)
        edges = ndimage.sobel(gray)
        
        # 计算形状复杂度
        shape_complexity = np.sum(edges > 50) / (self.width * self.height)
        return min(1.0, shape_complexity * 5)

    def _analyze_stroke_expression(self) -> float:
        """分析笔触表现力"""
        # 计算局部方差来评估笔触变化
        from scipy.ndimage import generic_filter
        gray = np.mean(self.np_image, axis=2)
        local_std = generic_filter(gray, np.std, size=5)
        
        # 评估笔触变化的丰富程度
        stroke_variety = np.mean(local_std) / 128
        return min(1.0, stroke_variety * 2)

    def _analyze_space_usage(self) -> float:
        """分析空间利用"""
        # 计算非空白区域的分布
        gray = np.mean(self.np_image, axis=2)
        content_mask = gray < 250
        
        # 计算内容的空间分布
        x_distribution = np.mean(content_mask, axis=0)
        y_distribution = np.mean(content_mask, axis=1)
        
        # 评估空间利用的均匀性
        space_usage = (np.std(x_distribution) + np.std(y_distribution)) / 2
        return min(1.0, 1 - space_usage)
