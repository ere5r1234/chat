import socket
import threading
import json
import time
import platform

class NetworkManager:
    def __init__(self, message_callback=None):
        self.local_port = 5000
        self.message_callback = message_callback
        self.running = False
        self.client_socket = None
        self.server_thread = None
        self.connected_ip = None
    
    def start_listening(self):
        """启动服务器监听线程"""
        if not self.running:
            self.running = True
            self.server_thread = threading.Thread(target=self._server_loop, daemon=True)
            self.server_thread.start()
    
    def stop_listening(self):
        """停止服务器监听"""
        self.running = False
        if self.server_thread:
            self.server_thread.join(1.0)
        self._close_client()
    
    def _server_loop(self):
        """服务器监听循环"""
        server_socket = None
        try:
            # 创建TCP socket
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
                    
                    # 关闭现有连接
                    self._close_client()
                    
                    # 保存新连接
                    self.client_socket = conn
                    self.connected_ip = addr[0]
                    
                    # 处理客户端连接
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
        """处理客户端连接"""
        try:
            while self.running:
                # 接收消息
                data = conn.recv(4096)
                if not data:
                    break
                
                # 解析消息
                try:
                    message = json.loads(data.decode('utf-8'))
                    # 设置消息发送者为对方
                    message['sender'] = 'other'
                    # 回调处理消息
                    if self.message_callback:
                        self.message_callback(message)
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
        """发送消息到已连接的设备"""
        if self.client_socket:
            try:
                # 序列化消息
                data = json.dumps(message, ensure_ascii=False).encode('utf-8')
                # 发送消息
                self.client_socket.sendall(data)
                return True
            except Exception as e:
                print(f"发送消息失败: {e}")
                self._close_client()
                return False
        else:
            # 如果没有网络连接，视为本地聊天模式
            # 在本地模式下，我们可以模拟接收自己的消息
            # 但需要由应用层来处理这种情况
            print("未连接到任何设备，消息仅保存在本地")
            return False
    
    def connect_to_device(self, ip):
        """连接到指定IP的设备"""
        try:
            # 关闭现有连接
            self._close_client()
            
            # 创建新的socket连接
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((ip, self.local_port))
            self.connected_ip = ip
            
            print(f"已连接到 {ip}:{self.local_port}")
            
            # 启动接收线程
            client_thread = threading.Thread(target=self._handle_client, args=(self.client_socket, (ip, self.local_port)), daemon=True)
            client_thread.start()
            
            return True
        except Exception as e:
            print(f"连接失败: {e}")
            self._close_client()
            return False
    
    def search_lan_devices(self):
        """搜索局域网内的设备"""
        devices = []
        
        # 获取本机IP和子网
        local_ip = self.get_local_ip()
        if local_ip.startswith('127.'):
            # 如果是本地回环地址，添加本地测试设备
            devices.append({
                'name': '本地测试',
                'ip': '127.0.0.1'
            })
            return devices
        
        # 提取子网部分
        subnet = '.'.join(local_ip.split('.')[:-1])
        
        # 创建一个结果列表和锁
        results = []
        lock = threading.Lock()
        
        def scan_ip(ip):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.2)
                result = sock.connect_ex((ip, self.local_port))
                if result == 0:
                    # 获取主机名
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
        
        # 创建线程池进行扫描
        threads = []
        for i in range(1, 255):
            ip = f"{subnet}.{i}"
            if ip == local_ip:
                continue  # 跳过自己
            thread = threading.Thread(target=scan_ip, args=(ip,))
            threads.append(thread)
            thread.start()
        
        # 等待所有线程完成
        for thread in threads:
            thread.join()
        
        # 添加本地回环地址作为测试选项
        devices.append({
            'name': '本地测试',
            'ip': '127.0.0.1'
        })
        
        # 添加扫描到的设备
        devices.extend(results)
        
        return devices
    
    def get_local_ip(self):
        """获取本机IP地址"""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # 不实际连接，只是用来获取本地IP
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP
    
    def _close_client(self):
        """关闭客户端连接"""
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
            self.client_socket = None
            self.connected_ip = None
    
    def is_connected(self):
        """检查是否已连接到其他设备"""
        return self.client_socket is not None
    
    def get_connected_ip(self):
        """获取已连接设备的IP地址"""
        return self.connected_ip