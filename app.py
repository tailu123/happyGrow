from flask import Flask, render_template, request, jsonify
from PIL import Image
import io
import imghdr

app = Flask(__name__)

def analyze_drawing(image):
    """
    分析儿童画作的函数
    参数:
    - image: PIL Image对象
    返回:
    - score: 评分 (0-100)
    - feedback: 反馈建议
    """
    try:
        # 获取图片信息
        width, height = image.size
        # 转换图片以获取颜色信息
        rgb_image = image.convert('RGB')
        colors = set()
        for x in range(width):
            for y in range(height):
                colors.add(rgb_image.getpixel((x, y)))
        unique_colors = len(colors)
        
        # 基础分数
        score = 60
        
        # 根据画作的复杂度增加分数
        if unique_colors > 10:
            score += 20
        if width * height > 100000:  # 大尺寸
            score += 10
            
        # 确保分数在0-100之间
        score = min(100, max(0, score))
        
        # 生成反馈
        feedback = []
        if score >= 80:
            feedback.append("太棒了！你的画作非常丰富多彩！")
        elif score >= 60:
            feedback.append("做得不错！建议可以尝试使用更多种类的颜色。")
        else:
            feedback.append("继续加油！画画最重要的是开心！建议可以画得大一些，用更多颜色。")
            
        return score, " ".join(feedback)
    except Exception as e:
        app.logger.error(f"Error analyzing drawing: {str(e)}")
        return 60, "抱歉，评分系统遇到了一些问题，但是我相信你的画作一定很棒！"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/score', methods=['POST'])
def score_drawing():
    # 检查是否有文件上传
    if 'drawing' not in request.files:
        return jsonify({'error': '没有上传图片'}), 400
        
    file = request.files['drawing']
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
        
    try:
        # 读取图片数据
        image_bytes = file.read()
        
        # 验证文件类型
        if not imghdr.what(None, image_bytes):
            return jsonify({'error': '请上传有效的图片文件'}), 400
            
        # 分析图片
        image = Image.open(io.BytesIO(image_bytes))
        score, feedback = analyze_drawing(image)
        
        return jsonify({
            'score': score,
            'feedback': feedback
        })
    except Exception as e:
        app.logger.error(f"Error processing image: {str(e)}")
        return jsonify({'error': '处理图片时出错'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
