#!/usr/bin/env python
# coding=utf-8
from utils import *
#from app_test import __all__ as alltests
from jormungandr import i_manager, app
from instance_save import InstanceSave
import importlib
import logging


if __name__ == "__main__":
    tester = app.test_client()
    i_manager.initialisation(start_ping=False)
    i_manager.stop()
    for name, instance in i_manager.instances.iteritems():
        i_manager.instances[name] = InstanceSave(saving_directory, instance)
    tests_classes = importlib.import_module("app_test")
    for name_t in tests_classes.__all__:
        logging.info("Reading test : " + name_t)
        test = getattr(tests_classes, name_t)

        if hasattr(test, "urls"):
            test_instance = test()
            for url_key in test.urls:
                url = test_instance.get_url(url_key)
                logging.info("Requesting : " + url)
                tester.get(url)
                logging.info("file saved")
