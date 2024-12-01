from PIL import Image, ImageDraw

def create_test_image():
    # 创建一个100x100的白色图片
    img = Image.new('RGB', (100, 100), 'white')
    draw = ImageDraw.Draw(img)

    # 画一个简单的圆
    draw.ellipse([20, 20, 80, 80], outline='black', fill='red')

    # 保存图片
    img.save('test_drawing.jpg')

if __name__ == '__main__':
    create_test_image()
