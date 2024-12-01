# 贡献指南

感谢你考虑为 HappyGrow 项目做出贡献！

## 开发流程

1. Fork 本仓库
2. 克隆你的 Fork
```bash
git clone https://github.com/your-username/happyGrow.git
```

3. 创建新分支
```bash
git checkout -b feature/your-feature-name
```

4. 进行更改并提交
```bash
git add .
git commit -m "Add some feature"
```

5. 推送到你的 Fork
```bash
git push origin feature/your-feature-name
```

6. 创建 Pull Request

## 代码规范

- 遵循 PEP 8 Python 代码风格指南
- 所有新功能必须包含测试
- 保持代码简洁清晰
- 添加必要的注释
- 使用有意义的变量和函数名

## 测试

- 确保所有测试通过
```bash
pytest test_app.py -v
```
- 添加新功能时编写相应的测试用例
- 保持测试覆盖率

## 提交信息规范

提交信息应该清晰描述更改内容，建议使用以下格式：

- feat: 新功能
- fix: 修复问题
- docs: 文档更改
- style: 代码格式化
- refactor: 代码重构
- test: 测试相关
- chore: 构建过程或辅助工具的变动

例如：
```
feat: 添加用户评分历史功能
fix: 修复图片上传大小限制问题
docs: 更新 README 安装说明
```

## 问题反馈

- 使用 GitHub Issues 提交问题
- 清晰描述问题和复现步骤
- 提供相关的日志和截图
- 说明运行环境和版本信息

## 功能建议

- 在提出新功能建议前，请先查看现有的 Issues
- 清晰描述新功能的用途和价值
- 如果可能，提供具体的实现思路

## 行为准则

- 保持友善和专业
- 尊重其他贡献者
- 接受建设性的批评和建议
- 关注项目的长期发展

## 许可证

通过贡献代码，你同意你的贡献将采用项目的 MIT 许可证。
