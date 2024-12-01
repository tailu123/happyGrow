"""
测试反馈生成器
"""
import pytest
from happygrow.core.feedback_generator import FeedbackGenerator

class TestFeedbackGenerator:
    @pytest.fixture
    def sample_scores(self):
        """样本评分数据"""
        return {
            'color_usage': 0.85,
            'composition': 0.75,
            'creativity': 0.90
        }
    
    @pytest.fixture
    def sample_details(self):
        """样本评分详情"""
        return {
            'color_usage': {
                'unique_colors': 15,
                'harmony_score': 0.8,
                'coverage_score': 0.9
            },
            'composition': {
                'thirds_score': 0.7,
                'balance_score': 0.8,
                'focal_score': 0.75
            },
            'creativity': {
                'shape_variety': 0.85,
                'stroke_expression': 0.95,
                'space_usage': 0.9
            }
        }
    
    def test_feedback_generation(self, sample_scores, sample_details):
        """测试反馈生成"""
        generator = FeedbackGenerator('school', sample_scores, sample_details)
        feedback = generator.generate_feedback()
        
        assert isinstance(feedback, dict)
        assert 'overall' in feedback
        assert 'specific' in feedback
        assert 'encouragement' in feedback
        
        # 确保反馈不为空
        assert all(feedback.values())
    
    def test_different_age_groups(self, sample_scores, sample_details):
        """测试不同年龄组的反馈"""
        age_groups = ['toddler', 'preschool', 'school', 'preteen']
        
        for age_group in age_groups:
            generator = FeedbackGenerator(age_group, sample_scores, sample_details)
            feedback = generator.generate_feedback()
            
            # 每个年龄组应该有特定的鼓励语
            assert feedback['encouragement']
    
    def test_low_scores_feedback(self, sample_details):
        """测试低分情况的反馈"""
        low_scores = {
            'color_usage': 0.3,
            'composition': 0.4,
            'creativity': 0.35
        }
        
        generator = FeedbackGenerator('school', low_scores, sample_details)
        feedback = generator.generate_feedback()
        suggestions = generator.get_improvement_suggestions()
        
        # 低分应该有改进建议
        assert suggestions
        assert len(suggestions) > 0
    
    def test_high_scores_feedback(self, sample_details):
        """测试高分情况的反馈"""
        high_scores = {
            'color_usage': 0.95,
            'composition': 0.90,
            'creativity': 0.95
        }
        
        generator = FeedbackGenerator('school', high_scores, sample_details)
        feedback = generator.generate_feedback()
        
        # 高分应该有表扬
        assert '出色' in feedback['overall'] or '优秀' in feedback['overall']
    
    def test_improvement_suggestions(self, sample_scores, sample_details):
        """测试改进建议生成"""
        generator = FeedbackGenerator('school', sample_scores, sample_details)
        suggestions = generator.get_improvement_suggestions()
        
        assert isinstance(suggestions, list)
        # 即使是好成绩也应该有建设性的建议
        assert len(suggestions) > 0
    
    def test_invalid_age_group(self, sample_scores, sample_details):
        """测试无效年龄组"""
        generator = FeedbackGenerator('invalid_age', sample_scores, sample_details)
        feedback = generator.generate_feedback()
        
        # 应该默认使用 school 年龄组的模板
        assert feedback['encouragement']
