import random
from retrying import retry
from nacos import NacosClient
from nacos_cli.utils import StartNacosBeat


class RNacosClient(NacosClient):

    # 重写特殊的构造方法，以便以后添加新特性（这里暂时没有用）
    def __init__(self, server_addresses, endpoint=None, namespace=None, ak=None, sk=None, username=None, password=None):
        NacosClient.__init__(self, server_addresses, endpoint=endpoint,
                             namespace=namespace, ak=ak, sk=sk, username=username, password=password)

    # 注册服务到 nacos 中，并使用守护线程启动心跳协议
    def rewrite_add_naming_instance(self, service_name, ip, port, cluster_name=None, weight=1.0,
                                    metadata=None, enable=True, healthy=True, ephemeral=True, group_name='DEFAULT_GROUP'):
        self.add_naming_instance(service_name, ip, port, cluster_name=cluster_name,weight=weight,
            metadata=metadata, enable=enable, healthy=healthy, ephemeral=ephemeral, group_name=group_name)
        StartNacosBeat({
            'service_name': service_name, 'ip': ip, 'port': port, 'cluster_name': cluster_name,
            'weight': weight, 'metadata': metadata, 'ephemeral': ephemeral, 'group_name': group_name},
            self).call_nacos_beat()

    # 使用简单随机法，获取一个可用的 ip,port
    @retry(stop_max_attempt_number=3, wait_incrementing_increment=8000)
    def select_one_instance(self, service_name, clusters=None, namespace_id=None, group_name=None, healthy_only=False):
        list_instance = self.list_naming_instance(service_name, clusters, namespace_id, group_name, healthy_only)
        ramdom_server = random.choice(list_instance['hosts'])
        return ramdom_server['ip'], ramdom_server['port']

