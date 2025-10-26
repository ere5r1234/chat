from datetime import datetime

class ChatManager:
    def __init__(self):
        self.messages = []
        self.observers = []
    
    def add_message(self, message):
        """添加一条新消息"""
        # 确保消息包含所有必要字段
        if 'timestamp' not in message:
            message['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if 'type' not in message:
            message['type'] = 'text'
        
        if 'sender' not in message:
            message['sender'] = 'unknown'
        
        # 添加消息到列表
        self.messages.append(message)
        
        # 通知所有观察者
        self.notify_observers(message)
        
        return message
    
    def get_messages(self, limit=None):
        """获取消息列表，可选限制数量"""
        if limit:
            return self.messages[-limit:]
        return self.messages
    
    def register_observer(self, observer):
        """注册消息观察者"""
        if observer not in self.observers:
            self.observers.append(observer)
    
    def unregister_observer(self, observer):
        """注销消息观察者"""
        if observer in self.observers:
            self.observers.remove(observer)
    
    def notify_observers(self, message):
        """通知所有观察者有新消息"""
        for observer in self.observers:
            try:
                observer(message)
            except Exception as e:
                print(f"通知观察者时出错: {e}")
    
    def clear_messages(self):
        """清空所有消息"""
        self.messages.clear()
    
    def get_messages_by_sender(self, sender):
        """获取指定发送者的消息"""
        return [msg for msg in self.messages if msg.get('sender') == sender]
    
    def format_message_for_display(self, message):
        """格式化消息用于显示"""
        sender = message.get('sender', '未知')
        timestamp = message.get('timestamp', '')
        content = message.get('content', '')
        
        if sender == 'me':
            return f"我 ({timestamp}): {content}"
        else:
            return f"对方 ({timestamp}): {content}"