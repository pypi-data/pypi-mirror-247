# coding: utf-8
import os
import re
import logging

SEP = os.sep


def key_check(raw_key=None):
    if not isinstance(raw_key, str):
        raise Exception("key 必须是字符串")

    if len(raw_key) == 0:
        raise Exception("key 不能为空")

    if len(raw_key) > 128:
        raise Exception("key 长度不能超过128")

    if not (raw_key[0].isalpha() and re.search("^[_a-zA-Z0-9]+$", raw_key)):
        raise Exception("key 只能包含字母/数字/下划线,并以字母开头")


def value_check(raw_value=None):
    if not isinstance(raw_value, str):
        raise Exception("value 必须是字符串")


class WarroomMessage(object):
    def __init__(self, content, messageId=None, pushTimestamp=None):
        self.content = content
        self.messageId = messageId
        self.pushTimestamp = pushTimestamp
        self.attributes_check()

    def attributes_check(self):
        if self.messageId is not None and not isinstance(self.messageId, str):
            raise Exception("messageId must be string if not None")
        if self.messageId is not None and len(self.messageId) > 64:
            raise Exception(
                "messageId length can not greater than 64 if messageId is not None")
        if not isinstance(self.content, str):
            raise Exception("content must be string")
        if not self.content:
            raise Exception("content can not be empty string")
        # 可以为空
        if self.pushTimestamp is not None and not isinstance(self.pushTimestamp, int):
            raise Exception("pushTimestamp must be int if not None")


class HoneyGuideBase(object):
    class ActionLog(object):
        def __init__(self, context_info: dict):
            self.context = context_info
            self.params_required = None

        def info(self, msg=None):
            '''
            打印日志, mock 无需重载
            '''
            logging.info(f"{msg}")

    class keyCache(object):
        def __init__(self, context_info: dict):
            self.context = context_info
            self.params_required = None

        def getString(self, key:str):
            pass

        def setString(self, key:str, value:str):
            pass

        def cleanCache(self, key:str):
            '''
            清除缓存
            '''
            pass

    class fileCache(object):
        def __init__(self, context_info: dict):
            self.context = context_info
            self.params_required = None

        def localFilePath(self):
            pass

        def get(self, fileUuid: str):
            pass

        def save(self, filePath:str, keepDays=None):
            pass

        def isExist(self, fileUuid:str):
            pass

        def downloadUrl(self, fileUuid:str):
            pass
            
    class warroomMessageSender(object):
        def __init__(self, context_info: dict):
            self.context = context_info
            self.params_required = None

        def send(self, message: WarroomMessage):
            return {"code": 200, "content": "消息推送成功"}

    class dbConfig(object):
        def __init__(self):
            self.__host = "127.0.0.1"
            self.__password = "toor"
            self.__username = "root"
            self.__port = 3306
        
        @property
        def host(self):
            return self.__host

        @host.setter
        def host(self, value):
            if type(value) == str:
                self.__host = value
            else:
                self.__host = "127.0.0.1"

        @property
        def username(self):
            return self.__username

        @username.setter
        def username(self, value):
            if type(value) == str:
                self.__username = value
            else:
                self.__username = "root"

        @property
        def port(self):
            return self.__port

        @port.setter
        def port(self, value):
            if type(value) == int:
                self.__port = value
            else:
                self.__port = 3306

        @property
        def password(self):
            return self.__password

        @password.setter
        def password(self, value):
            if type(value) == str:
                self.__password = value
            else:
                self.__password = "toor"

        def aePassword(self):
            return self.__password

        def reportPassword(self):
            return self.__password

        def appPassword(self):
            return self.__password

        def getUsername(self, domain=""):
            return self.__username

        def getHost(self, domain=""):
            return self.__host

        def getPort(self, domain=""):
            return self.__port

    def __init__(self, context_info: dict):
        self.actionLog = self.ActionLog(context_info)
        self.keyCache = self.keyCache(context_info)
        self.fileCache = self.fileCache(context_info)
        self.warroomMessageSender = self.warroomMessageSender(context_info)
        self.dbConfig = self.dbConfig()
