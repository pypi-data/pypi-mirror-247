import os
from io import BytesIO
# from BaseColor.base_colors import hyellow, hred
from minio import Minio
import logging
from urllib.parse import urlparse


# def printer(name, text, *args):
#     log_ext = ' '.join([str(x) for x in args]) if args else ''
#     log_str = f"[{hyellow(name)}] {text} {log_ext}"
#     print(log_str)


class MinioOpt:
    """Minio操作类"""

    def __init__(self, host, port, access_key, secret_key, bucket_name=None, **kwargs):
        # 连接minio
        self.minioClient = Minio(f"{host}:{port}", access_key=access_key, secret_key=secret_key, secure=False)

        # # 初始化桶，不存在就创建
        # bucket_name = bucket_name.strip()
        # self._init_bucket()

    def _init_bucket(self, bucket_name):
        if bucket_name:
            try:
                if not self.minioClient.bucket_exists(bucket_name):
                    self.minioClient.make_bucket(bucket_name, location="cn-northFalse")
            except Exception as IBE:
                print(
                    "MINIO-init",
                    f"Error in checking minio bucket: {hyellow(bucket_name)}  -->{hred(IBE)}"
                )
                return False
            return True

    def save_file(self, bucket_name, object_name, path):
        """
        将文件上传到文件系统
        bucket: 存储桶
        object_name: 上传文件的名称：1.jpg
        path: 文件路径：/tmp/1.jpg

        return: etag: 对象的etag值。
        """
        try:
            etag = self.minioClient.fput_object(bucket_name, object_name, path)
        except Exception as err:
            return False, str(err), None

        return True, "", etag

    def save_data(self, bucket_name, object_name, data, length, content_type="application/octet-stream", metadata=None):
        """
        将文件对象上传到文件系统
        bucket: 存储桶
        object_name: 对象名
        data: io.RawIOBase, 任何实现了io.RawIOBase的python对象。
        length: 对象的总长度。
        content_type: 对象的Content type。
        path: 文件路径：/tmp/1.jpg
        metadata: dict, 其它元数据

        return: etag: 对象的etag值。

        外层使用姿势：
            bucket = 'my_bucket'
            object_name = 'my_object'
            minio_ins = MinioStorage()
            with open('my-testfile', 'rb') as file_data:
                file_stat = os.stat('my-testfile')
                minio_ins.save_data(bucket, object_name, file_data, file_stat.st_size)
        """


        try:
            etag = self.minioClient.put_object(bucket_name, object_name, data, length)
            return True, "", etag
        except Exception as err:
            return False, str(err), None

    def save_bytes(self, bucket_name, object_name, file_bytes, content_type=None, metadata=None):
        if isinstance(file_bytes, str):
            file_bytes = file_bytes.encode()
        file_length = len(file_bytes)
        io = BytesIO(file_bytes)
        io.seek(0)
        return self.save_data(bucket_name=bucket_name, object_name=object_name, data=io, length=file_length, content_type=content_type, metadata=metadata)

    def get_file_object(self, bucket_name, object_name):
        """
        获取文件对象
        bucket: 存储桶
        object_name: 上传文件的名称：1.jpg
        """
        try:
            file_object = self.minioClient.get_object(bucket_name, object_name, request_headers=None)
            return True, "", file_object
        except Exception as err:
            return False, str(err), None

    def load_file(self, bucket_name, object_name, file_path):
        """
        下载并将文件保存到本地
        bucket: 存储桶
        object_name: 上传文件的名称：1.jpg
        file_path: 要存储的本地文件路径：/tmp/1.jpg
        注意：本API支持的最大文件大小是5GB
        返回文件对象
        """
        try:
            file_object = self.minioClient.fget_object(bucket_name, object_name, file_path)
        except Exception as err:
            return False, str(err), None

        return True, "", file_object

    def remove_file(self, bucket_name, object_name):
        """
        删除存储文件
        bucket: 存储桶
        object_name: 上传文件的名称：1.jpg
        """
        try:
            self.minioClient.remove_object(bucket_name, object_name)
        except Exception as err:
            return False, str(err)

        return True, ""

    def remove_incomplete_file(self, bucket_name, object_name):
        """
        删除一个未完整上传的文件
        bucket: 存储桶
        object_name: 上传文件的名称：1.jpg
        """
        try:
            self.minioClient.remove_incomplete_upload(bucket_name, object_name)
        except Exception as err:
            return False, str(err)
        return True, ""

    def presigned_get_object(self, bucket_name, object_name):
        """
        生成查看URL
        """
        try:
            url = self.minioClient.presigned_get_object(bucket_name, object_name)
        except Exception as err:
            return False, str(err)

        parse = urlparse(url)
        return True, parse.path + "?" + parse.query

if __name__ == '__main__':
    if hasattr(os.environ, "app_config"):
        config = os.environ.app_config
        mino_config = config["MINIO"]
    else:
        mino_config = {"HOST": "10.96.128.45", "PORT": 9000, "ACCESS_KEY": "admin", "SECRET_KEY": "root123456",
                       "BUCKET_NAME": "html-bucket"}
    MINIO_HOST = mino_config["HOST"]
    MINIO_PORT = mino_config["PORT"]
    MINIO_ACCESS_KEY = mino_config["ACCESS_KEY"]
    MINIO_SECRET_KEY = mino_config["SECRET_KEY"]
    # MINIO_BUCKET_NAME = mino_config["BUCKET_NAME"]
    BUCKET_AVATAR = mino_config["BUCKET_AVATAR"]
    BUCKET_AUTHORIZEDOC = mino_config["BUCKET_AUTHORIZEDOC"]
    BUCKET_FOLLOWUP = mino_config["BUCKET_FOLLOWUP"]

    test_minio = MinioOpt(MINIO_HOST, MINIO_PORT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY)

    # test_minio = MinioOpt(
    #     host="10.96.128.45",
    #     port=9000,
    #     access_key="admin",
    #     secret_key="root123456",
    #     bucket_name="html-bucket"
    # )

    # test_sta, test_err, test_tag = test_minio.save_file(
    #     object_name=""".env""",
    #     path="./../../conf/.env"
    # )
    # test_post_sta, test_post_err, test_post_tag = test_minio.save_bytes(
    #     object_name="""a.txt""",
    #     file_bytes="123ahwdgalibwliaubhwfliuabwfliybaliyf"
    # )
    # print("test_post_sta:", test_post_sta)
    # print("test_post_err:", test_post_err)
    # print("test_post_tag:", test_post_tag[0])

    # test_sta, test_err, test_tag = test_minio.get_file_object(
    #     "a.txt",
    # )
    # with open('my-testfile', 'wb') as file_data:
    #     for d in test_tag.stream(32 * 1024):
    #         file_data.write(d)

    # 上传授权文件
    with open('2d37df83750ac67caafaa2b83f51b93b.pdf', 'rb') as file_data:
        file_stat = os.stat('2d37df83750ac67caafaa2b83f51b93b.pdf')
        test_post_sta, test_post_err, test_post_tag = test_minio.save_data(
            bucket_name="authorizedoc",
            object_name="2d37df83750ac67caafaa2b83f51b93b.pdf",
            data=file_data,
            length=file_stat.st_size
        )
        print("test_post_sta:", test_post_sta)
        print("test_post_err:", test_post_err)
        print("test_post_tag:", test_post_tag)

    result = test_minio.presigned_get_authorizedoc("2d37df83750ac67caafaa2b83f51b93b.pdf")
    print(result)

    # 上传跟进文件
    with open('2d37df83750ac67caafaa2b83f51b93b.pdf', 'rb') as file_data:
        file_stat = os.stat('2d37df83750ac67caafaa2b83f51b93b.pdf')
        test_post_sta, test_post_err, test_post_tag = test_minio.save_data(
            bucket_name="followup",
            object_name="2d37df83750ac67caafaa2b83f51b93b.pdf",
            data=file_data,
            length=file_stat.st_size
        )
        print("test_post_sta:", test_post_sta)
        print("test_post_err:", test_post_err)
        print("test_post_tag:", test_post_tag)

    result = test_minio.presigned_get_followup("2d37df83750ac67caafaa2b83f51b93b.pdf")
    print(result)
