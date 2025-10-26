from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.window import Window
import socket
import threading
import json
import os
from datetime import datetime
import sys

# 确保数据目录存在
def ensure_data_directory():
    os.makedirs('data', exist_ok=True)

class Config:
    def __init__(self):
        self.config_file = os.path.join('data', 'config.json')
        self.default_config = {
            'username': '用户',
            'local_port': 5000
        }
        self._ensure_config_file_exists()
        self._load_config()
    
    def _ensure_config_file_exists(self):
        ensure_data_directory()
        if not os.path.exists(self.config_file):
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.default_config, f, ensure_ascii=False, indent=4)
    
    def _load_config(self):
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except Exception:
            self.config = self.default_config.copy()
            self.save_config()
    
    def save_config(self):
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=4)
        except Exception:
            pass
    
    def get_username(self):
        return self.config.get('username', self.default_config['username'])
    
    def set_username(self, username):
        self.config['username'] = username
        self.save_config()

class DatabaseManager:
    def __init__(self):
        self.messages_file = os.path.join('data', 'messages.json')
        self._ensure_database_exists()
    
    def _ensure_database_exists(self):
        ensure_data_directory()
        if not os.path.exists(self.messages_file):
            with open(self.messages_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=4)
    
    def save_message(self, message):
        try:
            messages = self.get_messages()
            messages.append(message)
            if len(messages) > 1000:
                messages = messages[-1000:]
            with open(self.messages_file, 'w', encoding='utf-8') as f:
                json.dump(messages, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"保存消息失败: {e}")
    
    def get_messages(self):
        try:
            with open(self.messages_file, 'r', encoding='utf-8') as f:
                messages = json.load(f)
            if not isinstance(messages, list):
                messages = []
            return messages
        except Exception as e:
            print(f"读取消息失败: {e}")
            return []
    
    def delete_all_messages(self):
        try:
            with open(self.messages_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"清空消息失败: {e}")

class NetworkManager:
    def __init__(self, message_callback=None):
        self.local_port = 5000
        self.message_callback = message_callback
        self.running = False
        self.client_socket = None
        self.server_thread = None
        self.connected_ip = None
    
    def start_listening(self):
        if not self.running:
            self.running = True
            self.server_thread = threading.Thread(target=self._server_loop, daemon=True)
            self.server_thread.start()
    
    def stop_listening(self):
        self.running = False
        if self.server_thread:
            self.server_thread.join(1.0)
        self._close_client()
    
    def _server_loop(self):
        server_socket = None
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind(('0.0.0.0', self.local_port))
            server_socket.listen(1)
            server_socket.settimeout(1.0)
            
            print(f"服务器已启动，监听端口 {self.local_port}")
            
            while self.running:
                try:
                    conn, addr = server_socket.accept()
                    print(f"接受连接来自 {addr}")
                    
                    self._close_client()
                    
                    self.client_socket = conn
                    self.connected_ip = addr[0]
                    
                    client_thread = threading.Thread(target=self._handle_client, args=(conn, addr), daemon=True)
                    client_thread.start()
                except socket.timeout:
                    continue
                except Exception as e:
                    print(f"接受连接时出错: {e}")
        except Exception as e:
            print(f"服务器启动失败: {e}")
        finally:
            if server_socket:
                server_socket.close()
    
    def _handle_client(self, conn, addr):
        try:
            while self.running:
                data = conn.recv(4096)
                if not data:
                    break
                
                try:
                    message = json.loads(data.decode('utf-8'))
                    message['sender'] = 'other'
                    if self.message_callback:
                        Clock.schedule_once(lambda dt, msg=message: self.message_callback(msg))
                except json.JSONDecodeError:
                    print(f"接收的消息不是有效的JSON格式")
        except Exception as e:
            print(f"处理客户端连接时出错: {e}")
        finally:
            conn.close()
            self.client_socket = None
            self.connected_ip = None
            print(f"客户端 {addr} 已断开连接")
    
    def send_message(self, message):
        if self.client_socket:
            try:
                data = json.dumps(message, ensure_ascii=False).encode('utf-8')
                self.client_socket.sendall(data)
                return True
            except Exception as e:
                print(f"发送消息失败: {e}")
                self._close_client()
                return False
        else:
            print("未连接到任何设备，消息仅保存在本地")
            return False
    
    def connect_to_device(self, ip):
        try:
            self._close_client()
            
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((ip, self.local_port))
            self.connected_ip = ip
            
            print(f"已连接到 {ip}:{self.local_port}")
            
            client_thread = threading.Thread(target=self._handle_client, args=(self.client_socket, (ip, self.local_port)), daemon=True)
            client_thread.start()
            
            return True
        except Exception as e:
            print(f"连接失败: {e}")
            self._close_client()
            return False
    
    def search_lan_devices(self):
        devices = []
        
        local_ip = self.get_local_ip()
        if local_ip.startswith('127.'):
            devices.append({
                'name': '本地测试',
                'ip': '127.0.0.1'
            })
            return devices
        
        subnet = '.'.join(local_ip.split('.')[:-1])
        
        results = []
        lock = threading.Lock()
        
        def scan_ip(ip):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.2)
                result = sock.connect_ex((ip, self.local_port))
                if result == 0:
                    try:
                        hostname = socket.gethostbyaddr(ip)[0]
                    except:
                        hostname = f"设备-{ip.split('.')[-1]}"
                    
                    with lock:
                        results.append({
                            'name': hostname,
                            'ip': ip
                        })
                sock.close()
            except:
                pass
        
        threads = []
        for i in range(1, 255):
            ip = f"{subnet}.{i}"
            if ip == local_ip:
                continue
            thread = threading.Thread(target=scan_ip, args=(ip,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        devices.append({
            'name': '本地测试',
            'ip': '127.0.0.1'
        })
        
        devices.extend(results)
        
        return devices
    
    def get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP
    
    def _close_client(self):
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
            self.client_socket = None
            self.connected_ip = None
    
    def is_connected(self):
        return self.client_socket is not None
    
    def get_connected_ip(self):
        return self.connected_ip

class ChatScreen(Screen):
    def __init__(self, **kwargs):
        super(ChatScreen, self).__init__(**kwargs)
        self.network_manager = NetworkManager(self.on_message_received)
        self.database = DatabaseManager()
        self.config = Config()
        
        # 创建主布局
        main_layout = BoxLayout(orientation='vertical')
        
        # 创建顶部状态栏
        status_bar = BoxLayout(size_hint_y=0.1, height=50)
        self.status_label = Label(text='未连接 - 本地模式')
        status_bar.add_widget(self.status_label)
        
        # 创建消息显示区域
        self.messages_scroll = ScrollView()
        self.messages_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.messages_layout.bind(minimum_height=self.messages_layout.setter('height'))
        self.messages_scroll.add_widget(self.messages_layout)
        
        # 创建输入区域
        input_layout = BoxLayout(size_hint_y=0.15, height=80)
        self.message_input = TextInput(multiline=True, hint_text='输入消息...')
        send_button = Button(text='发送')
        send_button.bind(on_press=self.send_message)
        
        input_layout.add_widget(self.message_input)
        input_layout.add_widget(send_button)
        
        main_layout.add_widget(status_bar)
        main_layout.add_widget(self.messages_scroll)
        main_layout.add_widget(input_layout)
        
        self.add_widget(main_layout)
        
        # 加载历史消息
        self.load_history_messages()
        
        # 开始监听消息
        self.network_manager.start_listening()
        
        # 定时更新状态
        Clock.schedule_interval(self.update_status, 1.0)
    
    def update_status(self, dt):
        connected_ip = self.network_manager.get_connected_ip()
        if connected_ip:
            self.status_label.text = f'已连接到: {connected_ip}'
        else:
            self.status_label.text = '未连接 - 本地模式'
    
    def send_message(self, instance):
        message_text = self.message_input.text.strip()
        if message_text:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            message = {
                'type': 'text',
                'content': message_text,
                'timestamp': timestamp,
                'sender': 'me'
            }
            
            # 保存到数据库
            self.database.save_message(message)
            
            # 显示消息
            self.add_message_to_ui(message)
            
            # 通过网络发送（如果有连接）
            self.network_manager.send_message(message)
            
            # 清空输入框
            self.message_input.text = ''
    
    def on_message_received(self, message):
        # 保存到数据库
        self.database.save_message(message)
        
        # 显示消息
        self.add_message_to_ui(message)
    
    def add_message_to_ui(self, message):
        # 根据发送者决定消息位置和样式
        if message['sender'] == 'me':
            message_label = Label(
                text=f"{self.config.get_username()} ({message['timestamp']}): {message['content']}",
                halign='right',
                valign='middle',
                text_size=(Window.width * 0.7, None),
                size_hint_y=None,
                height='40dp',
                color=(0, 0.5, 1, 1)
            )
        else:
            message_label = Label(
                text=f"对方 ({message['timestamp']}): {message['content']}",
                halign='left',
                valign='middle',
                text_size=(Window.width * 0.7, None),
                size_hint_y=None,
                height='40dp',
                color=(0, 1, 0.5, 1)
            )
        
        self.messages_layout.add_widget(message_label)
        # 滚动到底部
        Clock.schedule_once(self.scroll_to_bottom, 0.1)
    
    def scroll_to_bottom(self, dt):
        self.messages_scroll.scroll_y = 0
    
    def load_history_messages(self):
        # 加载历史消息并显示
        messages = self.database.get_messages()
        for message in messages:
            self.add_message_to_ui(message)

class ContactScreen(Screen):
    def __init__(self, **kwargs):
        super(ContactScreen, self).__init__(**kwargs)
        self.network_manager = NetworkManager(None)
        
        main_layout = BoxLayout(orientation='vertical')
        
        # 搜索按钮
        search_button = Button(text='搜索局域网设备', size_hint_y=0.1, height=50)
        search_button.bind(on_press=self.search_devices)
        
        # IP输入和连接按钮
        ip_layout = BoxLayout(size_hint_y=0.1, height=50)
        self.ip_input = TextInput(hint_text='输入IP地址')
        connect_button = Button(text='连接')
        connect_button.bind(on_press=lambda x: self.connect_to_ip())
        
        ip_layout.add_widget(self.ip_input)
        ip_layout.add_widget(connect_button)
        
        # 联系人列表
        self.contacts_scroll = ScrollView()
        self.contacts_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.contacts_layout.bind(minimum_height=self.contacts_layout.setter('height'))
        self.contacts_scroll.add_widget(self.contacts_layout)
        
        main_layout.add_widget(search_button)
        main_layout.add_widget(ip_layout)
        main_layout.add_widget(self.contacts_scroll)
        
        self.add_widget(main_layout)
    
    def search_devices(self, instance):
        # 显示加载中提示
        self.contacts_layout.clear_widgets()
        loading_label = Label(text='正在搜索设备，请稍候...', size_hint_y=None, height=50)
        self.contacts_layout.add_widget(loading_label)
        
        # 在后台线程中搜索设备
        threading.Thread(target=self._search_devices_thread, daemon=True).start()
    
    def _search_devices_thread(self):
        devices = self.network_manager.search_lan_devices()
        # 在主线程中更新UI
        Clock.schedule_once(lambda dt, devices=devices: self._update_device_list(devices))
    
    def _update_device_list(self, devices):
        # 清空现有列表
        self.contacts_layout.clear_widgets()
        
        if not devices:
            no_devices_label = Label(text='未发现任何设备', size_hint_y=None, height=50)
            self.contacts_layout.add_widget(no_devices_label)
        else:
            # 添加设备到列表
            for device in devices:
                device_button = Button(
                    text=f"{device['name']} ({device['ip']})",
                    size_hint_y=None,
                    height=50
                )
                device_button.bind(on_press=lambda btn, ip=device['ip']: self.connect_to_device(ip))
                self.contacts_layout.add_widget(device_button)
    
    def connect_to_device(self, ip):
        # 连接到指定IP的设备
        success = self.network_manager.connect_to_device(ip)
        if success:
            # 更新全局网络管理器连接
            self.manager.network_manager = self.network_manager
            self.manager.current = 'chat'
            # 显示成功提示
            self._show_popup('连接成功', f'已连接到 {ip}')
        else:
            self._show_popup('连接失败', '无法连接到指定设备，请检查网络设置')
    
    def connect_to_ip(self):
        ip = self.ip_input.text.strip()
        if ip:
            self.connect_to_device(ip)
    
    def _show_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.6, 0.4)
        )
        popup.open()
        # 2秒后自动关闭
        Clock.schedule_once(lambda dt: popup.dismiss(), 2)

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.config = Config()
        self.network_manager = NetworkManager(None)
        
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # 用户名设置
        username_layout = BoxLayout(size_hint_y=0.1, height=50)
        username_label = Label(text='用户名:')
        self.username_input = TextInput(text=self.config.get_username())
        
        username_layout.add_widget(username_label)
        username_layout.add_widget(self.username_input)
        
        # IP地址显示
        ip_layout = BoxLayout(size_hint_y=0.1, height=50)
        ip_label = Label(text='本机IP:')
        self.ip_value_label = Label(text=self.get_local_ip())
        
        ip_layout.add_widget(ip_label)
        ip_layout.add_widget(self.ip_value_label)
        
        # 保存按钮
        save_button = Button(text='保存设置', size_hint_y=0.1, height=50)
        save_button.bind(on_press=self.save_settings)
        
        # 清空消息按钮
        clear_messages_button = Button(text='清空聊天记录', size_hint_y=0.1, height=50)
        clear_messages_button.bind(on_press=self.clear_messages)
        
        main_layout.add_widget(username_layout)
        main_layout.add_widget(ip_layout)
        main_layout.add_widget(save_button)
        main_layout.add_widget(clear_messages_button)
        
        self.add_widget(main_layout)
    
    def get_local_ip(self):
        # 获取本机IP地址
        return self.network_manager.get_local_ip()
    
    def save_settings(self, instance):
        # 保存用户名设置
        self.config.set_username(self.username_input.text)
        # 显示保存成功提示
        self._show_popup('设置已保存', '用户名已更新')
    
    def clear_messages(self, instance):
        # 清空聊天记录
        db = DatabaseManager()
        db.delete_all_messages()
        self._show_popup('操作成功', '聊天记录已清空')
    
    def _show_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.6, 0.4)
        )
        popup.open()
        # 2秒后自动关闭
        Clock.schedule_once(lambda dt: popup.dismiss(), 2)

class ChatApp(App):
    def build(self):
        # 设置窗口大小
        Window.size = (400, 600)
        
        # 创建屏幕管理器
        self.sm = ScreenManager()
        
        # 添加聊天屏幕
        self.chat_screen = ChatScreen(name='chat')
        self.sm.add_widget(self.chat_screen)
        
        # 添加联系人屏幕
        self.contact_screen = ContactScreen(name='contacts')
        self.sm.add_widget(self.contact_screen)
        
        # 添加设置屏幕
        self.settings_screen = SettingsScreen(name='settings')
        self.sm.add_widget(self.settings_screen)
        
        # 创建底部导航栏
        main_layout = BoxLayout(orientation='vertical')
        main_layout.add_widget(self.sm)
        
        # 底部导航栏
        nav_bar = BoxLayout(size_hint_y=0.1, height=60)
        chat_button = Button(text='聊天')
        chat_button.bind(on_press=lambda x: setattr(self.sm, 'current', 'chat'))
        
        contacts_button = Button(text='联系人')
        contacts_button.bind(on_press=lambda x: setattr(self.sm, 'current', 'contacts'))
        
        settings_button = Button(text='设置')
        settings_button.bind(on_press=lambda x: setattr(self.sm, 'current', 'settings'))
        
        nav_bar.add_widget(chat_button)
        nav_bar.add_widget(contacts_button)
        nav_bar.add_widget(settings_button)
        
        main_layout.add_widget(nav_bar)
        
        # 确保数据目录存在
        ensure_data_directory()
        
        return main_layout
    
    def on_stop(self):
        # 应用关闭时停止网络服务
        self.chat_screen.network_manager.stop_listening()

if __name__ == '__main__':
    # 确保数据目录存在
    ensure_data_directory()
    ChatApp().run()