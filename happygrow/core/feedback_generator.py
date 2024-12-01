"""
反馈生成器，根据评分结果生成个性化的反馈建议
"""
from typing import Dict, List
from ..config.config import FEEDBACK_TEMPLATES, AGE_GROUPS

class FeedbackGenerator:
    def __init__(self, age_group: str, scores: Dict[str, float], details: Dict[str, Dict]):
        """
        初始化反馈生成器
        
        Args:
            age_group: 年龄组
            scores: 各维度的评分
            details: 评分详情
        """
        self.age_group = age_group
        self.scores = scores
        self.details = details
        self.templates = FEEDBACK_TEMPLATES

    def generate_feedback(self) -> Dict[str, str]:
        """生成综合反馈"""
        feedback = {
            'overall': self._generate_overall_feedback(),
            'specific': self._generate_specific_feedback(),
            'encouragement': self._generate_age_specific_encouragement()
        }
        return feedback

    def _generate_overall_feedback(self) -> str:
        """生成总体评价"""
        avg_score = sum(self.scores.values()) / len(self.scores)
        
        if avg_score >= 0.85:
            return "你的画作非常出色！展现了丰富的想象力和良好的艺术感觉。"
        elif avg_score >= 0.7:
            return "这是一幅很棒的作品！可以看出你在创作时投入了很多心思。"
        elif avg_score >= 0.5:
            return "你的画作很有特色，继续坚持创作，相信会做得更好！"
        else:
            return "每一次创作都是一次成长，保持热爱艺术的心，继续加油！"

    def _generate_specific_feedback(self) -> str:
        """生成具体维度的反馈"""
        feedback_parts = []
        
        # 颜色运用反馈
        color_score = self.scores.get('color_usage', 0)
        if color_score >= 0.85:
            feedback_parts.append(self.templates['color_usage']['excellent'])
        elif color_score >= 0.7:
            feedback_parts.append(self.templates['color_usage']['good'])
        elif color_score >= 0.5:
            feedback_parts.append(self.templates['color_usage']['fair'])
        else:
            feedback_parts.append(self.templates['color_usage']['needs_improvement'])
        
        # 构图反馈
        composition_score = self.scores.get('composition', 0)
        if composition_score >= 0.85:
            feedback_parts.append(self.templates['composition']['excellent'])
        elif composition_score >= 0.7:
            feedback_parts.append(self.templates['composition']['good'])
        elif composition_score >= 0.5:
            feedback_parts.append(self.templates['composition']['fair'])
        else:
            feedback_parts.append(self.templates['composition']['needs_improvement'])
        
        return " ".join(feedback_parts)

    def _generate_age_specific_encouragement(self) -> str:
        """生成年龄相适的鼓励"""
        age_templates = self.templates['age_specific'].get(self.age_group, 
                                                         self.templates['age_specific']['school'])
        
        return f"{age_templates['positive']} {age_templates['encourage']}"

    def get_improvement_suggestions(self) -> List[str]:
        """生成改进建议"""
        suggestions = []
        
        # 根据各维度得分生成具体建议
        if self.scores.get('color_usage', 0) < 0.7:
            if self.details['color_usage']['unique_colors'] < 10:
                suggestions.append("尝试使用更多种类的颜色来丰富画面。")
            if self.details['color_usage']['harmony_score'] < 0.6:
                suggestions.append("可以尝试使用互补色来增加画面的视觉效果。")
        
        if self.scores.get('composition', 0) < 0.7:
            if self.details['composition']['balance_score'] < 0.6:
                suggestions.append("注意画面的平衡性，可以让主要内容更均匀地分布。")
            if self.details['composition']['focal_score'] < 0.6:
                suggestions.append("可以让画面的主要内容更加突出。")
        
        if self.scores.get('creativity', 0) < 0.7:
            if self.details['creativity']['shape_variety'] < 0.6:
                suggestions.append("尝试画一些不同形状的内容，让画面更加丰富。")
            if self.details['creativity']['space_usage'] < 0.6:
                suggestions.append("可以多利用画面的空间，不要局限在某一个区域。")
        
        return suggestions
