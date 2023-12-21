目的：Action中调用获取并存储相关信息
方法有：
    log_upload: 上传打印的日志,这样可以从系统下载日志下来方便调试action异常
    item_cache: 键值对的缓存
    file_cache_upload: 上传文件到系统
    file_cache_download_url: 从系统下载文件

    注意：
        每种方法返回格式都是:
            api请求正常时:
                {"code": 200, "content": "接口真正返回的内容"}
            api请求异常时:
                {"code": 500, "content": "http request fail for the reason of xxx"}

    add new:
        新增了dbConfig类
        包括方法:
            aePassword
            reportPassword
打包：python3.6 setup_mock.py sdist bdist_wheel
上传到pypi:twine upload dist/* 