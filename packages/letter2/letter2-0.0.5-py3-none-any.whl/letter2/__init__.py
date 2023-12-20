def service(**kwargs):
    """
    返回一个服务器对象
    # 数据库配置【以下都是默认值】
    mysql_host='localhost',
    mysql_port=3306,
    mysql_user='root',
    mysql_database='letter',
    mysql_password='1234',

    # 服务器端配置【以下都是默认值】
    service_host='localhost',
    service_port=5000,
    max_client=5,
    encoding='utf8'

    # 文件传输配置【以下都是默认值】
    file_speed = 2048
    """
    from .core import Service
    return Service(**kwargs)


def client(**kwargs):
    """
    返回一个客服端对象
    service_host: 服务端地址, default: localhost
    service_port: 服务端端口, default: 5000
    encoding: 编码方式， default: utf-8

     # 文件传输配置【以下都是默认值】
    file_speed = 2048
    """
    from .core import Client
    return Client(**kwargs)
