import configparser
import os


class ConfigTools:

    def __init__(self, path='../'):

        self.file = 'conf/config.ini'
        self.path = path
        con = configparser.ConfigParser()
        con.read(os.path.join(self.path, self.file), encoding='utf-8')

        # 是否使用本地文件作为数据源
        db_source = con.items('db_source')
        self.is_local = db_source[0][1].lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']

        # 获取本地文件配置
        local_items = con.items('db_local')
        self.local_items = dict(local_items)

        # 获取db_config
        db_items = con.items('db_config')
        self.db_items = dict(db_items)

        # 获取biz_type
        biz_items = con.items('biz_type')
        self.biz_items = {}
        biz_str_dict = dict(biz_items)
        for i in biz_str_dict:
            self.biz_items[int(i)] = float(biz_str_dict[i])

        # 是否使用本地文件作为数据源
        fd = con.items('fd_config')
        fd_config = dict(fd)
        self.is_fd_soft = fd_config['is_fd_soft'].lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']
        self.unused_fd = [int(i) for i in fd_config['unused_fd'].split(',')]

