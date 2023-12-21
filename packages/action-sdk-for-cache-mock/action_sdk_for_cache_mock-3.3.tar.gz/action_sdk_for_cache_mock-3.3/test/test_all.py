import os
from action_sdk_for_cache.action_cache_sdk import HoneyGuide


if __name__ == "__main__":
    context_info = {
        "eventId": "20191220",
        "logMode": False,
        "activieId": "80877ce9-2973-4b6d-acef-2b9d4ab569ce",
        "appName": "lark_send_message",
        "actionName": "send_msg_by_lark"
    } 
    hg_client = HoneyGuide(context_info=context_info)
    hg_client.actionLog.info("测试")
    hg_client.keyCache.setString(key="lark_group", value="雾帜消防队")
    item_cache_get_ret = hg_client.keyCache.getString(key="lark_group")
    print("item_cache_get_ret: {0}".format(item_cache_get_ret))
    file_save_ret = hg_client.fileCache.save(os.path.join(hg_client.fileCache.localFilePath(), "python_sdk/test/README.md"))
    print("file_save_ret: {0}".format(file_save_ret))
    file_uuid_value = file_save_ret
    file_download_url_ret = hg_client.fileCache.downloadUrl(fileUuid=file_uuid_value)
    print("file_download_url_ret: {0}".format(file_download_url_ret))



