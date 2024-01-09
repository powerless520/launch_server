import datetime
import os

import yaml
import oss2


def init_bucket():
    oss_config = load_oss_config()

    # 初始化 OSS 客户端
    auth = oss2.Auth(oss_config['access_key_id'], oss_config['access_key_secret'])
    bucket = oss2.Bucket(auth, oss_config['endpoint'], oss_config['bucket_name'])
    # 设置存储空间为私有读写权限。
    # bucket.create_bucket(oss2.models.BUCKET_ACL_PRIVATE)
    return bucket


def load_oss_config(config_path='config.yaml'):
    with open(config_path, 'r') as file:
        yaml_config = yaml.safe_load(file)
    return yaml_config.get('oss_config')


def upload_to_oss(local_file_path):
    current_time = datetime.datetime.now()

    # todo update:文件信息
    # 上传文件
    result = init_bucket().put_object_from_file(local_file_path, os.path.basename(local_file_path))

    # 打印上传结果
    print(f"上传文件成功，文件URL：{result.resp.response.url}")


def download_to_oss(cloud_path, root):
    # 上传文件
    result = init_bucket().get_object_to_file(os.path.join(root, os.path.basename(cloud_path)), cloud_path)

    # 打印上传结果
    print(f"下载文件成功，文件URL：{result.resp.response.url}")


if __name__ == '__main__':
    upload_to_oss('spring_festival.png')
