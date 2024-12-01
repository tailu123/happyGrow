"""
HappyGrow - 儿童绘画评分系统主应用
"""
from flask import Flask, request, jsonify, render_template
import os
from happygrow.services.image_service import ImageService
from happygrow.core.scoring_engine import ScoringEngine
from happygrow.core.feedback_generator import FeedbackGenerator
from happygrow.config.config import SERVER_CONFIG, BASE_DIR

app = Flask(__name__)

# 配置上传文件夹
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    """渲染主页"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_drawing():
    """分析上传的绘画"""
    try:
        # 获取文件和年龄组
        if 'file' not in request.files:
            return jsonify({'error': '未找到上传的文件'}), 400
        
        file = request.files['file']
        age_group = request.form.get('age_group', 'school')
        
        # 验证图像
        is_valid, error = ImageService.validate_image(file)
        if not is_valid:
            return jsonify({'error': error}), 400
        
        # 预处理图像
        image = ImageService.preprocess_image(file)
        
        # 保存图像
        saved_path = ImageService.save_image(image, file.filename, UPLOAD_FOLDER)
        
        # 评分分析
        scoring_engine = ScoringEngine(image)
        
        # 分析各个维度
        color_score, color_details = scoring_engine.analyze_color_usage()
        composition_score, composition_details = scoring_engine.analyze_composition()
        creativity_score, creativity_details = scoring_engine.analyze_creativity()
        
        # 整合评分
        scores = {
            'color_usage': color_score,
            'composition': composition_score,
            'creativity': creativity_score
        }
        
        details = {
            'color_usage': color_details,
            'composition': composition_details,
            'creativity': creativity_details
        }
        
        # 生成反馈
        feedback_generator = FeedbackGenerator(age_group, scores, details)
        feedback = feedback_generator.generate_feedback()
        suggestions = feedback_generator.get_improvement_suggestions()
        
        return jsonify({
            'scores': scores,
            'feedback': feedback,
            'suggestions': suggestions,
            'image_path': os.path.relpath(saved_path, BASE_DIR)
        })
        
    except Exception as e:
        app.logger.error(f"Error processing image: {str(e)}")
        return jsonify({'error': '处理图像时发生错误'}), 500

if __name__ == '__main__':
    app.run(
        host=SERVER_CONFIG['host'],
        port=SERVER_CONFIG['port'],
        debug=SERVER_CONFIG['debug']
    )
