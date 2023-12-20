from .utils import Stream
import pymysql


class DataBaseManager:
    def __init__(self, **kwargs):
        self.mysql_host = kwargs.get('mysql_host', '127.0.0.1')
        self.mysql_port = kwargs.get('mysql_port', 3306)
        self.mysql_username = kwargs.get('mysql_username', 'root')
        self.mysql_password = kwargs.get('mysql_password', '1234')
        self.mysql_database = kwargs.get('mysql_database', 'letter')
        self.stream = Stream()
        self.connection = pymysql.connect(host=self.mysql_host, port=self.mysql_port,
                                          user=self.mysql_username, password=self.mysql_password,
                                          database=self.mysql_database)

        self.init_database()

    def login(self, username: str, password: str) -> bool:
        cursor = self.connection.cursor()
        cursor.execute('select * from letter_user where username = "%s"' % username)
        user = cursor.fetchall()
        if user:
            # 用户存在
            cursor.close()
            return user[0][2] == password

        cursor.close()
        return False

    def register(self, username: str, password: str) -> bool:
        cursor = self.connection.cursor()
        result = cursor.execute('select * from letter_user where username = "%s"' % username)
        if result:
            # 如果用户已经存在
            cursor.close()
            return False

        cursor.execute('insert into letter_user(username, password) values("%s", "%s")' % (username, password))
        self.connection.commit()
        cursor.close()
        return True

    def re_pwd(self, username: str, old_pwd: str, new_pwd: str) -> bool:
        cursor = self.connection.cursor()
        cursor.execute('select * from letter_user where username = "%s"' % username)
        user = cursor.fetchall()
        if user and user[0][2] == old_pwd:
            # 如果用户存在且密码匹配
            cursor.execute('update letter_user set password = "%s" where username = "%s"' % (new_pwd, username))
            self.connection.commit()
            cursor.close()
            return True

        cursor.close()
        return False

    def init_database(self):
        cursor = self.connection.cursor()
        result = cursor.execute(f'show tables where Tables_in_{self.mysql_database} = "letter_user"')
        if result == 0:
            self.stream.system_out_normal('正在初始化数据库中！')
            cursor.execute("""
                create table if not exists letter_user(
                    id int primary key auto_increment,
                    username varchar(20) not null unique,
                    password varchar(32)
                )
            """)
            self.stream.system_out_normal('表 letter_user 构建完毕')
        cursor.close()
