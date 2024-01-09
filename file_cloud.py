import os
os.environ['OSS_ACCESS_KEY_ID']=''
os.environ['OSS_ACCESS_KEY_SECRET']=''
import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider
from itertools import islice
import configparser

"""
创建存储空间
"""

# 从环境变量中获取访问凭证。运行本代码示例之前，请确保已设置环境变量OSS_ACCESS_KEY_ID和OSS_ACCESS_KEY_SECRET。
auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())
# 填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
# yourBucketName填写存储空间名称。
bucket = oss2.Bucket(auth, 'https://oss-cn-hangzhou.aliyuncs.com', 'ai-lanuch')

# 设置存储空间为私有读写权限。
bucket.create_bucket(oss2.models.BUCKET_ACL_PRIVATE)


"""
上传文件
"""
# -*- coding: utf-8 -*-
import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider
# 从环境变量中获取访问凭证。运行本代码示例之前，请确保已设置环境变量OSS_ACCESS_KEY_ID和OSS_ACCESS_KEY_SECRET。
auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())
# 填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
# yourBucketName填写存储空间名称。
bucket = oss2.Bucket(auth, 'https://oss-cn-hangzhou.aliyuncs.com', 'ai-lanuch')

# 上传文件到OSS。
# yourObjectName由包含文件后缀，不包含Bucket名称组成的Object完整路径，例如abc/efg/123.jpg。 云
# yourLocalFile由本地文件路径加文件名包括后缀组成，例如/users/local/myfile.txt。 本地
bucket.put_object_from_file('yourObjectName', 'yourLocalFile')


"""
下载文件
"""
# 从环境变量中获取访问凭证。运行本代码示例之前，请确保已设置环境变量OSS_ACCESS_KEY_ID和OSS_ACCESS_KEY_SECRET。
auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())
# 填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
# yourBucketName填写存储空间名称。
bucket = oss2.Bucket(auth, 'https://oss-cn-beijing.aliyuncs.com', 'ai-lanuch')

#下载OSS文件到本地文件。
# yourObjectName由包含文件后缀，不包含Bucket名称组成的Object完整路径，例如abc/efg/123.jpg。
# yourLocalFile由本地文件路径加文件名包括后缀组成，例如/users/local/myfile.txt。
bucket.get_object_to_file('red_data/SaveImages.zip','./SaveImages.zip')


"""
列举文件
"""
# 从环境变量中获取访问凭证。运行本代码示例之前，请确保已设置环境变量OSS_ACCESS_KEY_ID和OSS_ACCESS_KEY_SECRET。
auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())
# 填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
# yourBucketName填写存储空间名称。
bucket = oss2.Bucket(auth, 'https://oss-cn-beijing.aliyuncs.com', 'ai-lanuch')

# oss2.ObjectIterator用于遍历文件。
for b in islice(oss2.ObjectIterator(bucket), 2):
    print(b.key)


"""
删除文件
"""

# 从环境变量中获取访问凭证。运行本代码示例之前，请确保已设置环境变量OSS_ACCESS_KEY_ID和OSS_ACCESS_KEY_SECRET。
auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())
# 填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
# yourBucketName填写存储空间名称。
bucket = oss2.Bucket(auth, 'https://oss-cn-beijing.aliyuncs.com', 'ai-lanuch')

# yourObjectName表示删除OSS文件时需要指定包含文件后缀，不包含Bucket名称在内的完整路径，例如abc/efg/123.jpg。
bucket.delete_object('yourObjectName')





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


# 替换以下信息为你自己的上传文件的本地路径
local_file_path = '/path/to/your/local/file.txt'

# 调用上传函数
upload_to_oss(local_file_path)


