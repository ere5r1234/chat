# CrossPlatformChat

跨平台聊天应用，支持Windows和Android。

## 项目结构

- `main.py`: 应用程序主入口
- `buildozer.spec`: Buildozer配置文件（用于Android打包）
- `config.py`: 配置管理模块
- `database.py`: 数据库管理模块
- `network.py`: 网络通信模块
- `chat_manager.py`: 聊天管理模块
- `requirements.txt`: Python依赖列表

## 在GitHub Codespaces中构建Android APK

1. 将此仓库克隆到GitHub
2. 打开GitHub Codespaces
3. 在终端中运行以下命令：

```bash
# 安装依赖
sudo apt-get update
sudo apt-get install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev
sudo pip install --upgrade pip
sudo pip install cython kivy buildozer

# 构建APK
buildozer android debug
```

## 依赖说明

请确保安装以下Python库：
- kivy
- pyyaml

可以通过`pip install -r requirements.txt`安装所有依赖。