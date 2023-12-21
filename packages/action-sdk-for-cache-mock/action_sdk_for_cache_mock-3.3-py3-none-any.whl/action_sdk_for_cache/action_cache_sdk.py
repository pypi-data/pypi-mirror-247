# coding: utf-8
from action_sdk_for_cache.baseClass.action_sdk_base import HoneyGuideBase, \
    WarroomMessage, \
    key_check, \
    value_check, \
    os

from tempfile import TemporaryFile

import tempfile
import json
import uuid


class HoneyGuide(HoneyGuideBase):
    class keyCache(HoneyGuideBase.keyCache):
        def __init__(self, context_info: dict):
            self.tmp_file = TemporaryFile(mode="w+")
            super().__init__(context_info)

        def getString(self, key: str):
            key_check(key)
            self.tmp_file.seek(0)
            tmp_data = self.tmp_file.read()
            try:
                tmp_data = json.loads(tmp_data)
            except Exception as _:
                tmp_data = {}
            return tmp_data.get(key)

        def setString(self, key: str, value: str):
            key_check(key)
            value_check(value)
            self.tmp_file.seek(0)
            tmp_data = self.tmp_file.read()
            try:
                tmp_data = json.loads(tmp_data)
            except Exception as _:
                tmp_data = {}
            tmp_data[key] = value
            tmp_data = json.dumps(tmp_data)
            self.tmp_file.seek(0)
            self.tmp_file.write(tmp_data)
            return {"code": 200, "content": "保存成功"}

        def cleanCache(self, key: str):
            self.tmp_file.close()

    class fileCache(HoneyGuideBase.fileCache):
        def __init__(self, context_info: dict):
            super().__init__(context_info)
            self.tmp_path = tempfile.gettempdir()
            self.tmp_uuid_file = TemporaryFile(mode="w+")

        def localFilePath(self):
            return self.tmp_path

        def get(self, fileUuid: str):
            if len(str(fileUuid)) == 0:
                raise Exception("文件uuid为空")
            self.tmp_uuid_file.seek(0)
            uuid_data = self.tmp_uuid_file.read()
            try:
                uuid_data = json.loads(uuid_data)
            except Exception as _:
                uuid_data = {}
            file_name = uuid_data.get(fileUuid)

            if file_name is None:
                raise Exception("文件不存在")

            return file_name

        def save(self, filePath: str, keepDays=None):
            fileUuid = str(uuid.uuid4())
            self.tmp_uuid_file.seek(0)
            uuid_data = self.tmp_uuid_file.read()
            try:
                uuid_data = json.loads(uuid_data)
            except Exception as _:
                uuid_data = {}
            uuid_data[fileUuid] = filePath
            uuid_data = json.dumps(uuid_data)
            self.tmp_uuid_file.seek(0)
            self.tmp_uuid_file.write(uuid_data)
            return fileUuid

        def isExist(self, fileUuid: str):
            """
                判断文件是否存在
            """
            self.tmp_uuid_file.seek(0)
            uuid_data = self.tmp_uuid_file.read()
            try:
                uuid_data = json.loads(uuid_data)
            except Exception as _:
                uuid_data = {}
            file_path = uuid_data[fileUuid]
            if file_path is None:
                raise ValueError("文件获取异常")

            return os.path.isfile(file_path)

        def downloadUrl(self, fileUuid: str):
            self.tmp_uuid_file.seek(0)
            uuid_data = self.tmp_uuid_file.read()
            try:
                uuid_data = json.loads(uuid_data)
            except Exception as _:
                uuid_data = {}
            file_path = uuid_data[fileUuid]
            return f"https://127.0.0.1/{file_path}"

    def __init__(self, context_info: dict):
        super().__init__(context_info)
