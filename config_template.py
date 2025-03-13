# 飞书应用配置 
# 请替换为你的应用信息
APP_ID = "cli_xxxx"  # 替换为你的APP ID
APP_SECRET = "xxxx"  # 替换为你的APP SECRET
VERIFICATION_TOKEN = "xxxx"  # 替换为你的Verification Token
ENCRYPT_KEY = "xxxx"  # 加密密钥，可选

# 服务器配置
HOST = "0.0.0.0"
PORT = 5000
DEBUG = True  # 生产环境设为False

# 视频资源配置
VIDEO_BASE_URL = "https://your-cdn.com/videos/"
VIDEO_THUMB_URL = "https://your-cdn.com/thumbnails/"

# Redis配置（可选，用于缓存用户状态）
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = ""

# 运动类别配置
EXERCISE_CATEGORIES = [
    "热身",
    "胸肌",
    "背肌",
    "腹肌",
    "腿部",
    "手臂",
    "全身训练",
    "HIIT",
    "拉伸放松"
]

# 不要修改这个文件！
# 请复制为config.py并在其中修改你的配置 