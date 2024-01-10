import os
from urllib.parse import unquote

import yaml
import oss2


class OssClient:

    def __init__(self, config_path='config.yaml'):
        self.oss_config = self.load_oss_config(config_path)
        self.bucket = self.init_bucket()

    def init_bucket(self):
        oss_config = self.load_oss_config()

        # 初始化 OSS 客户端
        auth = oss2.Auth(oss_config['access_key_id'], oss_config['access_key_secret'])
        bucket = oss2.Bucket(auth, oss_config['endpoint'], oss_config['bucket_name'])
        # 设置存储空间为私有读写权限。
        # bucket.create_bucket(oss2.models.BUCKET_ACL_PRIVATE)
        return bucket

    def load_oss_config(self, config_path='config.yaml'):
        with open(config_path, 'r') as file:
            yaml_config = yaml.safe_load(file)
        return yaml_config.get('oss_config')

    # 上传文件到oss
    def upload_to_oss(self, local_file_path):
        object_file = os.path.basename(local_file_path)
        path = os.path.join('generate', object_file)
        # 上传文件
        result = self.init_bucket().put_object_from_file(path, local_file_path)
        # 打印上传结果
        print(f"上传文件成功，文件URL：{unquote(result.resp.response.url)}")
        return unquote(result.resp.response.url)

    # 从oss下载文件
    def download_from_oss(self, cloud_path, root):
        # 上传文件
        result = self.init_bucket().get_object_to_file(cloud_path, os.path.join(root, os.path.basename(cloud_path)))

        # 打印上传结果
        print(f"下载文件成功，文件URL：{unquote(result.resp.response.url)}")

    def download_from_oss_easy(self, cloud_path):
        # 上传文件
        result = self.init_bucket().get_object(cloud_path)

        # 打印上传结果
        print(f"下载文件成功，文件URL：{unquote(result.resp.response.url)}")


if __name__ == '__main__':
    ossClient = OssClient()
    # ossClient.upload_to_oss('demo.py')  # 生成图片默认放这里
    ossClient.download_from_oss('generate/spring_festival.png', './')
