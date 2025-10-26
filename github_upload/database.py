import json
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        # 消息数据库文件路径
        self.messages_file = os.path.join('data', 'messages.json')
        # 确保数据库文件存在
        self._ensure_database_exists()
    
    def _ensure_database_exists(self):
        # 确保数据目录存在
        os.makedirs('data', exist_ok=True)
        # 如果消息数据库文件不存在，则创建
        if not os.path.exists(self.messages_file):
            with open(self.messages_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=4)
    
    def save_message(self, message):
        try:
            # 读取现有消息
            messages = self.get_messages()
            # 添加新消息
            messages.append(message)
            # 限制消息数量，防止文件过大
            if len(messages) > 1000:  # 保留最近1000条消息
                messages = messages[-1000:]
            # 保存回文件
            with open(self.messages_file, 'w', encoding='utf-8') as f:
                json.dump(messages, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"保存消息失败: {e}")
    
    def get_messages(self):
        try:
            with open(self.messages_file, 'r', encoding='utf-8') as f:
                messages = json.load(f)
            # 确保返回的是列表
            if not isinstance(messages, list):
                messages = []
            return messages
        except Exception as e:
            print(f"读取消息失败: {e}")
            return []
    
    def delete_all_messages(self):
        try:
            # 清空消息文件
            with open(self.messages_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"清空消息失败: {e}")
    
    def get_messages_by_date(self, date):
        try:
            messages = self.get_messages()
            # 过滤指定日期的消息
            target_date = date.strftime('%Y-%m-%d')
            filtered_messages = [
                msg for msg in messages 
                if 'timestamp' in msg and msg['timestamp'].startswith(target_date)
            ]
            return filtered_messages
        except Exception as e:
            print(f"获取指定日期消息失败: {e}")
            return []