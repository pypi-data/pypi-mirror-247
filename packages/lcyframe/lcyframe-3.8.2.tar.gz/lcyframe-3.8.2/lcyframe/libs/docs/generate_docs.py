# coding=utf-8
import logging
import os
import sys
from lcyframe.libs.docs import start
from .template import AnanasTemplate
from threading import Thread
from traceback import format_exc
import time
from ..utils import random_string, fix_path
import shutil
import platform
from importlib import import_module

class GenerateDocs(object):

    @classmethod
    def start(cls, app):
        """
        Auto generate the docs for this project.
        :return:
        """
        if not app.kwargs.get("api_docs"):
            return

        if os.path.exists(os.path.join(app.ROOT, "conf")):
            raise Exception("Can not exists file 'conf' dir in you project. It is reserved for the docs directory.")

        if not app.api_docs.get("auto_generate"):
            return

        t = Thread(target=cls.do, args=(app, ))
        t.start()

    @classmethod
    def do(cls, app):
        new_docs_name = "%s_%s" % (random_string(3), random_string(3))
        new_docs_dir = os.path.dirname(app.docs_dir) + "/docs_%s" % new_docs_name
        docs_agree_str = cls.get_docs_agree(app)
        try:
            import signal
            # logging.info("generate docs...")
            if not os.path.exists(new_docs_dir):
                start.main(app.kwargs.get("project_name"),
                           new_docs_dir,
                           app.api_schema_dir,
                           app.errors_dir,
                           app.constant_dir,
                           app.model_dir,
                           docs_agree_str)

            AnanasTemplate(app, new_docs_dir).run(sys.executable)
            cls.change_docs(app, new_docs_dir)
            # logging.info("generate docs done!")
        except Exception as e:
            logging.warning(format_exc())
            # logging.warning("Api docs generate Faile! you can do it yourself： cd 'docs_dir' && make html")
            cls.remove_docs(new_docs_dir)

    @classmethod
    def get_docs_agree(cls, app):
        """

        :param app:
        :return:
        """
        try:
            api_docs = app.get_path(app.api_docs.get("agree_dir", "context"))
            # model_name = api_docs.replace(app.ROOT, "").lstrip("/").replace("/", ".") + ".docs_agree"
            # docs_agree = import_module(model_name)
            file = api_docs + "/docs_agree.md"
            if os.path.exists(file):
                with open(api_docs + "/docs_agree.md", "r") as p:
                    return "".join(p.readlines())
            else:
                return ""
        except Exception as e:
            logging.error("get docs_agree config error:" + str(e))
            return ""

    @classmethod
    def change_docs(cls, app, new_docs_dir):
        cls.remove_docs(app.docs_dir)
        if app.api_docs.get("output", "html") == "html":
            shutil.copytree(fix_path(os.path.join(new_docs_dir, "build/html")), app.docs_dir)
        else:
            shutil.copytree(new_docs_dir, app.docs_dir)

        shutil.copyfile(new_docs_dir + '/template/_static/images/favicon.ico', app.docs_dir + '/favicon.ico')

        cls.remove_docs(new_docs_dir)

    @classmethod
    def remove_docs(cls, docs_dir):
        if os.path.exists(docs_dir):
            shutil.rmtree(docs_dir)
