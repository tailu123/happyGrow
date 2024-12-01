"""
配置文件，包含评分标准和系统设置
"""
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).parent.parent.parent

# 服务器配置
SERVER_CONFIG = {
    'host': '0.0.0.0',
    'port': 5001,
    'debug': True
}

# 图像处理配置
IMAGE_CONFIG = {
    'allowed_extensions': {'png', 'jpg', 'jpeg', 'gif'},
    'min_width': 200,
    'min_height': 200,
    'max_width': 4096,
    'max_height': 4096,
    'max_file_size': 10 * 1024 * 1024,  # 10MB
    'jpeg_quality': 85,
    'upload_folder': 'uploads'
}

# 年龄组配置
AGE_GROUPS = {
    'toddler': {'min': 2, 'max': 4},
    'preschool': {'min': 4, 'max': 6},
    'school': {'min': 6, 'max': 9},
    'preteen': {'min': 9, 'max': 12}
}

# 评分维度权重
SCORING_WEIGHTS = {
    'color_usage': 0.25,         # 颜色运用
    'composition': 0.20,         # 构图
    'creativity': 0.20,          # 创造力
    'technique': 0.15,           # 技巧运用
    'detail_level': 0.10,        # 细节程度
    'line_quality': 0.10         # 线条质量
}

# 评分标准
SCORING_CRITERIA = {
    'color_usage': {
        'unique_colors': {
            'weight': 0.4,
            'thresholds': {
                5: 60,   # 5种颜色以下得60分
                10: 75,  # 5-10种颜色得75分
                15: 85,  # 10-15种颜色得85分
                20: 95   # 15种以上颜色得95分
            }
        },
        'color_harmony': {
            'weight': 0.3,
            'complementary_bonus': 10,
            'analogous_bonus': 8
        },
        'color_coverage': {
            'weight': 0.3,
            'min_coverage': 0.4  # 最小颜色覆盖率
        }
    },
    'composition': {
        'rule_of_thirds': {
            'weight': 0.4,
            'grid_size': 3
        },
        'balance': {
            'weight': 0.3,
            'quadrant_threshold': 0.2  # 每个象限的最小内容占比
        },
        'focal_point': {
            'weight': 0.3,
            'detection_threshold': 0.15
        }
    },
    'creativity': {
        'uniqueness': 0.4,
        'variety': 0.3,
        'expression': 0.3
    }
}

# 反馈模板
FEEDBACK_TEMPLATES = {
    'color_usage': {
        'excellent': "你对颜色的运用非常出色！使用了丰富的色彩来表达你的想法。",
        'good': "你运用了很好的色彩搭配，继续尝试使用更多样的颜色会让画面更生动。",
        'fair': "建议可以尝试使用更多种类的颜色，这样可以让你的作品更加丰富多彩。",
        'needs_improvement': "可以尝试使用更多颜色来装饰你的画作，每种颜色都能表达不同的心情。"
    },
    'composition': {
        'excellent': "画面构图非常协调，主体突出，布局合理。",
        'good': "构图不错，可以考虑让主要内容更加突出。",
        'fair': "尝试把主要内容放在画面的黄金分割点上，会让画面更加吸引人。",
        'needs_improvement': "建议在开始画之前先想想画面的整体布局，这样会让作品更加出色。"
    },
    'age_specific': {
        'toddler': {
            'positive': "你的线条充满活力，这正是小朋友最珍贵的特质！",
            'encourage': "继续画画，每次画画都是一次新的冒险！"
        },
        'preschool': {
            'positive': "你对细节的观察越来越仔细了，真棒！",
            'encourage': "尝试画出更多你喜欢的东西，让画面更丰富多彩！"
        },
        'school': {
            'positive': "你的画作表现力很强，能看出你的用心！",
            'encourage': "可以尝试画一些更有挑战性的主题，相信你一定能做得很好！"
        },
        'preteen': {
            'positive': "你的艺术表现力正在不断提升，继续保持！",
            'encourage': "尝试学习一些新的绘画技巧，会让你的作品更上一层楼！"
        }
    }
}
