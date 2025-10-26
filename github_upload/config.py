import json
import os

class Config:
    def __init__(self):
        # 配置文件路径
        self.config_file = os.path.join('data', 'config.json')
        # 默认配置
        self.default_config = {
            'username': '用户',
            'local_port': 5000,
            'message_history_limit': 1000
        }
        # 确保配置文件存在
        self._ensure_config_file_exists()
        # 加载配置
        self._load_config()
    
    def _ensure_config_file_exists(self):
        # 确保数据目录存在
        os.makedirs('data', exist_ok=True)
        # 如果配置文件不存在，则创建
        if not os.path.exists(self.config_file):
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.default_config, f, ensure_ascii=False, indent=4)
    
    def _load_config(self):
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except Exception:
            # 如果读取失败，使用默认配置
            self.config = self.default_config.copy()
            # 重新写入配置文件
            self.save_config()
    
    def save_config(self):
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=4)
        except Exception:
            # 保存失败时忽略错误
            pass
    
    def get_username(self):
        return self.config.get('username', self.default_config['username'])
    
    def set_username(self, username):
        self.config['username'] = username
        self.save_config()
    
    def get_local_port(self):
        return self.config.get('local_port', self.default_config['local_port'])
    
    def get_message_history_limit(self):
        return self.config.get('message_history_limit', self.default_config['message_history_limit'])