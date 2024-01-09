import os
os.environ['OSS_ACCESS_KEY_ID']=''
os.environ['OSS_ACCESS_KEY_SECRET']=''
import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider
from itertools import islice
import configparser

# 从环境变量中获取访问凭证。运行本代码示例之前，请确保已设置环境变量OSS_ACCESS_KEY_ID和OSS_ACCESS_KEY_SECRET。
auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())
# 填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
# yourBucketName填写存储空间名称。
bucket = oss2.Bucket(auth, 'https://oss-cn-hangzhou.aliyuncs.com', 'ai-lanuch')

# 设置存储空间为私有读写权限。
bucket.create_bucket(oss2.models.BUCKET_ACL_PRIVATE)


def load_oss_config(config_path='config.ini'):
    config = configparser.ConfigParser()
    config.read(config_path)

    oss_config = {
        'access_key_id': config.get('oss_config', 'access_key_id'),
        'access_key_secret': config.get('oss_config', 'access_key_secret'),
        'endpoint': config.get('oss_config', 'endpoint'),
        'bucket_name': config.get('oss_config', 'bucket_name'),
    }

    return oss_config


def upload_to_oss(local_file_path):
    oss_config = load_oss_config()

    # 初始化 OSS 客户端
    auth = oss2.Auth(oss_config['access_key_id'], oss_config['access_key_secret'])
    bucket = oss2.Bucket(auth, oss_config['endpoint'], oss_config['bucket_name'])

    # 上传文件
    result = bucket.put_object_from_file(local_file_path, os.path.basename(local_file_path))

    # 打印上传结果
    print(f"上传文件成功，文件URL：{result.resp.response.url}")


def Download_to_oss(cloud_path,root):
    oss_config = load_oss_config()

    # 初始化 OSS 客户端
    auth = oss2.Auth(oss_config['access_key_id'], oss_config['access_key_secret'])
    bucket = oss2.Bucket(auth, oss_config['endpoint'], oss_config['bucket_name'])

    # 上传文件
    result = bucket.get_object_to_file(os.path.join(root,os.path.basename(cloud_path)), cloud_path)

    # 打印上传结果
    print(f"下载文件成功，文件URL：{result.resp.response.url}")



