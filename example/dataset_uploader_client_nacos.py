
from __future__ import print_function

import logging

import dataset_pb2
import dataset_pb2_grpc

from nacos_cli.nacos_channel import RoundrobinChannel

from nacos_cli.nacos_agent import RNacosClient

SERVER_ADDRESSES = "172.16.2.81:8848"
NAMESPACE = ""
USERNAME = "nacos"
PASSWORD = "nacos"
CLUSTER = "DEFAULT"

client = RNacosClient(SERVER_ADDRESSES, namespace=NAMESPACE, username=USERNAME, password=PASSWORD)


def run():
    opts = [("grpc.lb_policy_name", "round_robin",)]
    with RoundrobinChannel('ai.intellicloud.xbrain.rpc.DataSetUploader', client, opts, None, None) as channel:
        stub = dataset_pb2_grpc.DataSetUploaderStub(channel)
        for _ in range(10):
            response = stub.UploadSample(dataset_pb2.UploadSampleRequest(taskId=123, image='base64'))
            print("DatasetUploader client received: " + response.message)


if __name__ == '__main__':
    logging.basicConfig()
    run()
