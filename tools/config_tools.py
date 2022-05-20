import configparser
import os


class ConfigTools:

    def __init__(self, path='../conf/'):

        file = 'config.ini'
        con = configparser.ConfigParser()
        con.read(os.path.join(path, file), encoding='utf-8')

        # 获取db_config
        db_items = con.items('db_config')
        self.db_items = dict(db_items)

        # 获取biz_type
        biz_items = con.items('biz_type')
        self.biz_items = {}
        biz_str_dict = dict(biz_items)
        for i in biz_str_dict:
            self.biz_items[int(i)] = float(biz_str_dict[i])

        unused_items = con.items('unused_funder')
        self.unused_items = [int(i) for i in unused_items[0][1].split(',')]
