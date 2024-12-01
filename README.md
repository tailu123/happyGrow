# HappyGrow - 儿童画作评分系统

HappyGrow 是一个基于 Python Flask 的 Web 应用程序，旨在为儿童画作提供智能评分和建设性反馈。通过分析画作的各种特征（如颜色丰富度、画面大小等），系统能够给出鼓励性的评分和建议，帮助孩子们在绘画过程中获得正向反馈和进步动力。

## 特性

- 🎨 智能画作分析
  - 颜色丰富度评估
  - 画面尺寸分析
  - 自动评分系统

- 💝 鼓励性反馈
  - 根据评分生成个性化建议
  - 积极正向的反馈机制
  - 激发创作热情

- 🌈 用户友好界面
  - 简洁直观的操作流程
  - 支持拖拽上传
  - 实时图片预览

## 技术栈

- 后端：Python Flask
- 前端：HTML5, CSS3, JavaScript
- 图像处理：Pillow
- 测试框架：pytest, Flask-Testing

## 快速开始

### 环境要求

- Python 3.9+
- pip

### 安装步骤

1. 克隆仓库
```bash
git clone https://github.com/yourusername/happyGrow.git
cd happyGrow
```

2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 启动应用
```bash
python app.py
```

5. 访问应用
打开浏览器访问 http://localhost:5001

## 开发指南

### 项目结构
```
happyGrow/
├── app.py              # 主应用程序
├── templates/          # HTML 模板
│   └── index.html     # 主页面
├── static/            # 静态资源
├── tests/             # 测试文件
├── requirements.txt   # 项目依赖
└── README.md          # 项目文档
```

### 运行测试

```bash
pytest test_app.py -v
```

### 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 待办事项

- [ ] 添加更多评分维度（线条流畅度、构图等）
- [ ] 集成机器学习模型
- [ ] 添加用户系统
- [ ] 支持历史记录查看
- [ ] 添加年龄段选择

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 联系方式

项目维护者 - [@yourusername](https://github.com/yourusername)

项目链接: [https://github.com/yourusername/happyGrow](https://github.com/yourusername/happyGrow)
