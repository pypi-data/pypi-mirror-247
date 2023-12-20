import os
import socket
import threading
import time

from .utils import Stream, Verify, File
from .database import DataBaseManager


class Base:
    def __init__(self, **kwargs):
        """
        客服端与服务端的基类
        :param kwargs: s
            service_host:   服务器 HOST
            service_port:   服务器 PORT
            encoding:       编码方式
            buffer_size:    每次最大传输字节数
            stream:         格式化打印
            verify:         校验
            file:           文件工具对象
        """
        self.service_host = kwargs.get('service_host', '127.0.0.1')
        self.service_port = kwargs.get('service_port', 5000)
        self.encoding = kwargs.get('encoding', 'utf8')
        self.buffer_size = kwargs.get('buffer_size', 4096)
        self.stream = Stream()
        self.verify = Verify()
        self.file = File(**kwargs)

    def __str__(self):
        return str(self.__dict__)

    def current(self, order: str) -> bool:
        """ 通用服务 """
        if order == 'help':
            self.stream.system_out_help()
        elif order == 'me':
            self.stream.system_out_normal(f'{self.username} {self.address}')
        elif order == 'clear':
            os.system('cls')
            self.stream.start_client()
        elif order == 'path':
            self.stream.system_out_path()

        return order in ['help', 'me', 'clear', 'path']


# ======================================================================================================================
class Service(Base):
    """ 服务器类 """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.max_client = kwargs.get('max_client', 5)
        self.client_pool = dict()
        self.data = DataBaseManager(**kwargs)
        self.lock = threading.Lock()

    def send_all(self, msg: str):
        # 给所有用户发送消息
        for client in self.client_pool.values():
            client.send(msg.encode(self.encoding))

    def send_user(self, user: str, to_user: str, msg: str) -> bool:
        # 给指定用户发送消息
        if to_user in self.client_pool.keys():
            self.client_pool[to_user].send(f'{user}: {msg}'.encode(self.encoding))
            return True

        elif to_user == 'all':
            self.send_all(f'[all] {user}: {msg}')
            return True

    def login_or_register(self, order: str, username: str, password: str) -> str:
        # 用户登录 or 注册
        result = 'ok'
        if order == 'login' and (not self.data.login(username, password)):
            result = 'err 用户名或密码错误'
        elif order == 'register' and (not self.data.register(username, password)):
            result = 'err 用户名已经存在, 注册失败'
        elif username in self.client_pool.keys():
            result = 'err 用户已经在线!'
        return result

    def main(self, client: socket.socket, address: tuple, username: str):
        self.client_pool[username] = client
        while True:
            try:
                try:
                    order = client.recv(self.buffer_size).decode(self.encoding)
                except Exception as e:
                    continue

                if order == 'exit':
                    # 断开连接
                    client.send('exit'.encode(self.encoding))
                    client.close()
                    self.client_pool.pop(username)
                    self.stream.system_out_warning(f'client: {username}{address} 离开聊天室')
                    self.send_all(f'用户 {username} 离开聊天室')
                    break

                elif order == 'ls':
                    # 返回所有在线用户
                    msg = ', '.join(self.client_pool.keys())
                    client.send(f'users: [{msg}]'.encode(self.encoding))

                elif order.startswith('chat'):
                    # 给指定用户发送消息
                    order = order.split(' ')
                    user = order[1]
                    msg = ' '.join(order[2:])
                    if not self.send_user(user=username, to_user=user, msg=msg):
                        # 发送失败
                        client.send(f'用户: {user}, 不存在'.encode(self.encoding))

                elif order.startswith('file'):
                    # 文件传输
                    self.lock.acquire()
                    order, filename, filesize, to, user = order.split(' ')
                    filename = os.path.basename(filename)
                    data = self.file.download_file(client=client, filesize=int(filesize), filename=filename)

                    if user in self.client_pool.keys():
                        self.stream.system_out_normal(f'文件 {filename} 将转发给: {user}')
                        self.client_pool[user].send(f'file {filename} {filesize} {username}'.encode(self.encoding))
                        self.file.upload_file(filename=filename, filesize=int(filesize), client=self.client_pool[user])

                    else:
                        # 没有此人
                        client.send(f'用户: {user} 不存在'.encode(self.encoding))
                    self.lock.release()

                elif order.startswith('repwd'):
                    # 修改密码
                    order, old_pwd, new_pwd = order.split(' ')
                    flag = self.data.re_pwd(username=username, old_pwd=old_pwd, new_pwd=new_pwd)
                    # 修改失败, 返回提示
                    if not flag:
                        client.send(f'密码不匹配, 修改失败'.encode(self.encoding))
                    else:
                        client.send(f'密码修改成功'.encode(self.encoding))

                else:
                    client.send('收到'.encode(self.encoding))
            except Exception as e:
                self.stream.system_out_error(f'client: {username}{address} 断开连接: {e}')
                client.close()
                if username in self.client_pool.keys(): self.client_pool.pop(username)
                self.send_all(f'用户: {username}, 离开聊天室')
                break

    def start(self):
        try:
            self.stream.start_service()
            self.stream.system_out_normal('letter2 2.0 service starting...')
            self.service.bind((self.service_host, self.service_port))
            self.service.listen(self.max_client)
            self.stream.system_out_win('letter2 2.0 service stared!')
            self.stream.system_out_win(f'letter2 2.0 service host: {self.service_host}')
            self.stream.system_out_win(f'letter2 2.0 service port: {self.service_port}')

            while True:
                client, address = self.service.accept()
                order = client.recv(self.buffer_size).decode(self.encoding)
                try:
                    # 登录 / 注册 校验
                    order, username, password = order.split(' ')
                    result = self.login_or_register(order=order, username=username, password=password)
                    client.send(result.encode(self.encoding))
                    if 'err' in result:
                        # 注册或登录失败
                        client.close()
                        continue

                    # 登录 / 注册 成功, 给与日志输出
                    self.stream.system_out_warning(f'client: {username}{address} 加入聊天')
                    self.send_all(f'用户 {username} 加入聊天')

                    # 开启线程为其服务
                    ts = threading.Thread(target=self.main, args=(client, address, username))
                    ts.start()
                except Exception as e:
                    self.stream.system_out_error(f'client {address}, 的错误访问: {e}')
                    client.close()

        except Exception as e:
            self.stream.system_out_error(f'服务器启动异常: {e}')
            self.service.close()


# ======================================================================================================================
class Client(Base):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.username = '离线状态'
        self.client = socket.socket()
        self.address = ''
        self.lock = threading.Lock()

    def login_or_register(self, order) -> bool:
        """ 登录 / 注册 """
        username = self.verify.username_verify()
        password = self.verify.password_verify()
        try:
            self.stream.system_out_normal(f'{order}...')
            self.client.connect((self.service_host, self.service_port))
            self.client.send(f'{order} {username} {password}'.encode(self.encoding))
            result = self.client.recv(self.buffer_size).decode(self.encoding)
            if 'ok' in result:
                self.address = self.client.getsockname()
                self.username = username
                self.stream.system_out_win(f'登录成功, 目标服务器: {self.service_host}:{self.service_port}')
                return True
            else:
                self.stream.system_out_error(result)
                self.client = socket.socket()
        except Exception as e:
            self.stream.system_out_error(f'服务器{self.service_host}:{self.service_port}, 连接失败, 请稍后重试: {e}')

    def off_main(self):
        """ 离线服务 """
        while True:
            order = self.stream.user_input().strip()
            if not order: continue
            if self.verify.order_verify(order=order):
                # 登录 / 注册, 成功的话关闭离线服务, 开启线上服务
                if order == 'login' or order == 'register':
                    if self.login_or_register(order=order):
                        self.main()
                        break

                # 注销账号
                elif order == 'exit':
                    break

                # 其它服务
                elif not self.current(order):
                    self.stream.system_out_warning(f'离线模式无法使用该指令: {order}')
            else:
                self.stream.system_out_warning('错误指令, 你可以输入 help 寻求帮助')

    def monitorUser(self):
        """ 监控客户端用户输入 """
        while True:
            order = input().strip()
            if not order: continue
            if self.verify.order_verify(order=order):
                if order == 'exit':
                    # 退出应用
                    self.client.send('exit'.encode(self.encoding))
                    break

                elif order == 'logout':
                    # 注销登录
                    self.client.send('exit'.encode(self.encoding))
                    time.sleep(0.1)
                    self.username = '离线模式'
                    self.address = ''
                    self.client = socket.socket()
                    self.off_main()
                    break

                elif order.startswith('file'):
                    self.lock.acquire()
                    # 文件传输: 校验文件真实性，告诉服务器文件要发送了，上传文件
                    order, filename, to, user = order.split(' ')
                    flag, filesize = self.file.verify(filename)
                    if not flag:
                        # 校验文件是否存在
                        self.stream.system_out_warning(f'文件不存在！或者目标是个目录！')
                        continue

                    self.client.send(f'{order} {filename} {filesize} to {user}'.encode(self.encoding))  # 告诉服务端，文件来了
                    self.file.upload_file(filename, filesize=filesize, client=self.client)
                    self.lock.release()

                elif order == 'ls' or order.startswith('chat') or order.startswith('repwd'):
                    self.client.send(order.encode(self.encoding))

                elif not self.current(order):
                    self.stream.system_out_warning(f'在线模式无法使用该指令: {order}')
            else:
                self.stream.system_out_warning('错误指令, 你可以输入 help 寻求帮助')

    def monitorService(self):
        """ 监控服务端返回 """
        while True:
            try:
                result = self.client.recv(self.buffer_size)
                if result == self.file.file_over: continue
                result = result.decode(self.encoding)
            except Exception as e:
                continue

            if result == 'exit':
                self.stream.system_out_error('goodbye :)')
                break

            if result.startswith('file'):
                self.lock.acquire()
                order, filename, filesize, old_user = result.split(' ')
                self.file.save(filename=filename, filesize=int(filesize), username=self.username, old_user=old_user,
                               client=self.client)
                self.lock.release()

            else:
                self.stream.system_out_normal(result)

    def main(self):
        """ 线上服务 """
        mu = threading.Thread(target=self.monitorUser)
        ms = threading.Thread(target=self.monitorService, daemon=True)
        mu.start()
        ms.start()
        ms.join()

    def start(self):
        self.stream.start_client()
        self.stream.system_out_normal('letter2 2.0 client starting...')
        self.stream.system_out_win('letter2 2.0 client stared!')
        self.stream.system_out_warning('目前正处于离线模式, 你可以输入 login 登录聊天室')

        # 进入离线服务
        self.off_main()