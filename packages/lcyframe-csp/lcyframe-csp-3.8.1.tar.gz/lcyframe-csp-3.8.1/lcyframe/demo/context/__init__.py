#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys, os
root_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_dir)
import platform
import logging
from argparse import ArgumentParser
from tornado.options import options, define
from lcyframe.libs import yaml2py, utils
from lcyframe.libs.context_start import AutoStartContext
from lcyframe.libs.singleton import MongoCon
from model.schema.igGenerator_schema import IdGeneratorSchema
from model.igGenerator_model import IdGeneratorModel
# from model.schema.admin_schema import AdminSchema

class InitContext(object):
    config = None
    port = config_file = None

    @classmethod
    def parse_arguments(cls):
        parser = ArgumentParser("")
        parser.add_argument("-c", "--config", dest="config", type=str, default="", help="config file path.like ./example.yml")
        parser.add_argument("-p", "--port", dest="port", type=int, default=6677, help="the port to run at")
        # args, __ = parser.parse_known_args(sys.argv[1:])
        return parser.parse_args()

    @classmethod
    def get_context(cls, config_name=None):
        if not config_name:
            logging.warning("platform >>>>>>>>>>>:" + platform.node())
            if len(sys.argv) > 1:
                args = cls.parse_arguments()
                cls.port = args.port
                cls.config_file = args.config_file
                if not cls.config_file:
                    raise Exception("please run like this：python app.py --config=example.yml")
                sys.argv = sys.argv[0]

            elif os.environ.get('YOUR_PROJECT_CONFIG_FILE'):
                cls.config_file = os.environ["YOUR_PROJECT_CONFIG_FILE"]
                if not os.path.exists(cls.config_file):
                    raise Exception("配置文件不存在")
            else:
                if platform.node() in ["Online"]:
                    cls.config_file = "server_config.yml"
                elif platform.node() in ["app", "a1320a62c9fd"]:
                    cls.config_file = "test.yml"
                elif platform.node() in ["vm"]:
                    cls.config_file = "vm_config.yml"
                elif platform.node() in ["Mac", "lcyMac.local"]:
                    cls.config_file = "localhost.yml"
                else:
                    cls.config_file = "example.yml"
        else:
            cls.config_file = config_name

        logging.warning(cls.config_file)
        if os.path.isabs(cls.config_file):
            cls.config = yaml2py.load_confog(cls.config_file)
        else:
            cls.config = yaml2py.load_confog(os.path.join(os.path.dirname(__file__), cls.config_file))
        if cls.port:
            cls.config["wsgi"]["port"] = int(cls.port)
        cls.config["config_name"] = cls.config_file.split("/")[-1]
        cls.config["ROOT"] = utils.fix_path(os.path.dirname(os.path.dirname(__file__)))
        os.environ.app_config = cls.config
        return cls.config

    @classmethod
    def init_db(cls):
        AutoStartContext.start_mongodb(cls.config["mongo_config"])


        db = MongoCon().get_database(**cls.config["mongo_config"])
        if not db.id_generator.find().count():
            doc = vars(IdGeneratorSchema())
            doc["uid"] = 10000
            db[IdGeneratorSchema.collection].insert(doc)

        if not db.admin.find().count():

            docs = vars(AdminSchema())
            docs["uid"] = 10000
            docs["nick_name"] = "nick_name"
            docs["pass_word"] = utils.gen_salt_pwd("123456", docs["salt"])
            docs["gid"] = 1
            db[AdminSchema.collection].insert(docs)
