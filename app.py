#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import logging

# 尝试导入配置文件，如果不存在则使用模板
try:
    import config
except ImportError:
    import config_template as config
    print("警告: 使用配置模板! 请复制config_template.py为config.py并更新配置")

# 初始化Flask应用
app = Flask(__name__)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 导入飞书SDK
try:
    from lark_oapi import lark
    from lark_oapi.client import Client
    # 初始化飞书客户端
    client = Client(config.APP_ID, config.APP_SECRET, lark.DOMAIN_FEISHU)
except ImportError:
    logger.error("飞书SDK未安装. 请运行: pip install lark-oapi")
    client = None

# 示例运动数据库
exercise_data = {
    "热身": [
        {"name": "开合跳", "duration": "1分钟", "video_id": "v1"},
        {"name": "高抬腿", "duration": "1分钟", "video_id": "v2"}
    ],
    "胸肌": [
        {"name": "俯卧撑", "sets": "3组x12次", "video_id": "v3"},
        {"name": "斜板俯卧撑", "sets": "3组x10次", "video_id": "v4"}
    ],
    "腹肌": [
        {"name": "卷腹", "sets": "3组x15次", "video_id": "v5"},
        {"name": "平板支撑", "duration": "30秒x3次", "video_id": "v6"}
    ]
}

# 视频ID与URL映射
video_urls = {
    "v1": "https://yourcdn.com/videos/jumping_jacks.mp4",
    "v2": "https://yourcdn.com/videos/high_knees.mp4",
    "v3": "https://yourcdn.com/videos/pushups.mp4",
    "v4": "https://yourcdn.com/videos/incline_pushups.mp4",
    "v5": "https://yourcdn.com/videos/crunches.mp4",
    "v6": "https://yourcdn.com/videos/plank.mp4"
}

@app.route("/")
def index():
    return "飞书运动指导机器人服务正在运行中!"

@app.route("/webhook/event", methods=["POST"])
def handle_event():
    # 验证请求
    event = json.loads(request.data)
    logger.info(f"收到事件: {event.get('type')}")
    
    # 验证Token
    if "challenge" in event:
        return jsonify({"challenge": event["challenge"]})
    
    # 处理消息事件
    if event.get("type") == "im.message.receive_v1":
        message_data = event.get("event")
        if not message_data:
            return jsonify({"status": "success"})
            
        # 获取消息内容
        message_type = message_data.get("message").get("message_type")
        if message_type != "text":
            return jsonify({"status": "success"})
            
        content = json.loads(message_data.get("message").get("content"))
        text = content.get("text", "").strip()
        
        # 处理消息
        chat_id = message_data.get("message").get("chat_id")
        
        # 处理运动指令
        if "帮助" in text or "help" in text:
            send_help_message(chat_id)
        elif any(keyword in text for keyword in exercise_data.keys()):
            # 识别用户想要哪类运动
            for category in exercise_data.keys():
                if category in text:
                    send_exercise_guide(chat_id, category)
                    break
        else:
            # 默认响应
            send_text_message(chat_id, "您好！我是您的运动助手。\n可以发送：热身、胸肌、腹肌等关键词获取训练指导。\n发送"帮助"查看更多功能。")
    
    return jsonify({"status": "success"})

def send_text_message(chat_id, text):
    if not client:
        logger.error("飞书客户端未初始化")
        return
        
    try:
        client.im.message.create(
            {
                "receive_id": chat_id,
                "content": json.dumps({"text": text}),
                "msg_type": "text"
            }
        )
    except Exception as e:
        logger.error(f"发送消息失败: {str(e)}")

def send_help_message(chat_id):
    help_text = (
        "🏋️‍♀️ 运动助手使用指南 🏋️‍♂️\n\n"
        "发送以下关键词获取对应训练指导：\n"
        "· 热身 - 获取热身动作\n"
        "· 胸肌 - 胸肌训练计划\n" 
        "· 腹肌 - 腹肌训练计划\n\n"
        "发送"视频+动作名称"获取指导视频，如：视频 俯卧撑"
    )
    send_text_message(chat_id, help_text)

def send_exercise_guide(chat_id, category):
    if not client:
        logger.error("飞书客户端未初始化")
        return
        
    # 构建卡片消息
    exercises = exercise_data.get(category, [])
    if not exercises:
        send_text_message(chat_id, f"抱歉，暂无{category}相关训练")
        return
    
    # 构建卡片
    card = {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": f"{category}训练计划"},
            "template": "blue"
        },
        "elements": []
    }
    
    # 添加动作列表
    for idx, exercise in enumerate(exercises):
        card["elements"].append({
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"**{idx+1}. {exercise['name']}**\n" + 
                           (f"组数：{exercise['sets']}" if 'sets' in exercise else f"时长：{exercise['duration']}")
            }
        })
    
    # 添加视频按钮
    card["elements"].append({"tag": "hr"})
    buttons = []
    for exercise in exercises:
        buttons.append({
            "tag": "button",
            "text": {"tag": "plain_text", "content": f"查看{exercise['name']}视频"},
            "type": "primary",
            "value": exercise['video_id']
        })
    
    card["elements"].append({
        "tag": "action",
        "actions": buttons
    })
    
    try:
        # 发送卡片消息
        client.im.message.create(
            {
                "receive_id": chat_id,
                "content": json.dumps({"elements": [card]}),
                "msg_type": "interactive"
            }
        )
    except Exception as e:
        logger.error(f"发送卡片消息失败: {str(e)}")
        # 尝试发送文本消息作为备选
        text_content = f"{category}训练计划:\n"
        for idx, exercise in enumerate(exercises):
            text_content += f"{idx+1}. {exercise['name']} - "
            text_content += f"组数：{exercise['sets']}\n" if 'sets' in exercise else f"时长：{exercise['duration']}\n"
        send_text_message(chat_id, text_content)

if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG) 