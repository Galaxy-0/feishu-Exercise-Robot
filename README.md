# 飞书运动指导机器人

一款基于飞书平台的运动指导机器人，为企业员工提供专业的运动健身服务、视频教学和健康管理。

## 项目介绍

本项目通过飞书平台打造一个运动指导机器人，提供以下核心功能：

- 👨‍🏫 **运动指南与动作示范**：提供专业的运动指导和动作示范
- 📅 **个性化训练计划**：根据用户水平和目标生成定制训练方案
- 🎬 **指导视频分享**：高质量训练视频和动作要点讲解
- ✅ **训练打卡与记录**：记录训练数据，培养运动习惯
- 🏆 **成就系统**：完成挑战解锁成就，增强运动动力

## 技术架构

- **后端**：Python + Flask
- **API集成**：飞书开放平台API
- **数据存储**：飞书多维表格 + 云文档
- **视频服务**：CDN + 飞书云存储

## 快速开始

### 环境准备

```bash
# 克隆仓库
git clone git@github.com:Galaxy-0/feishu-Exercise-Robot.git
cd feishu-Exercise-Robot

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 配置飞书应用

1. 在[飞书开放平台](https://open.feishu.cn/app)创建应用
2. 配置应用权限：
   - `im:message` (读写消息)
   - `im:message.group_at:readonly` (获取群组消息)
   - `contact:user.base:readonly` (获取用户基本信息)
3. 配置事件订阅URL
4. 配置机器人功能

### 本地开发

```bash
# 复制配置模板
cp config_template.py config.py
# 编辑config.py填入你的APP_ID和APP_SECRET

# 启动开发服务器
python app.py
```

## 项目结构

```
feishu-Exercise-Robot/
├── app.py                 # 主应用入口
├── requirements.txt       # 项目依赖
├── config_template.py     # 配置模板
├── README.md              # 项目说明
├── LICENSE                # 许可证
├── static/                # 静态资源
├── templates/             # 模板文件
└── app/                   # 应用代码
    ├── handlers/          # 事件处理器
    ├── models/            # 数据模型
    ├── services/          # 业务逻辑
    └── utils/             # 工具函数
```

## 功能模块

### 基础会话功能
- 关键词匹配(热身、胸肌、腹肌等)
- 帮助指令(/help)
- 交互式卡片回复

### 训练计划管理
- 创建个性化训练计划
- 查看当日训练内容
- 调整训练难度

### 视频指导系统
- 按类别查询训练视频
- 视频卡片交互
- 动作要点讲解

### 训练追踪与打卡
- 训练完成打卡
- 训练数据统计
- 连续打卡挑战

## 部署指南

### 测试环境
```bash
# 使用gunicorn启动
gunicorn -w 4 -b 127.0.0.1:8000 app:app
```

### 生产环境
```bash
# 使用supervisord管理进程
supervisord -c supervisord.conf
```

## 贡献指南

1. Fork本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

## 许可证

本项目采用MIT许可证 - 详情请参阅[LICENSE](LICENSE)文件

## 联系方式

如有问题或建议，请通过Issues提交或联系项目维护者。

---

🏋️‍♀️ **让健康运动融入每个飞书用户的生活！** 🏋️‍♂️ 