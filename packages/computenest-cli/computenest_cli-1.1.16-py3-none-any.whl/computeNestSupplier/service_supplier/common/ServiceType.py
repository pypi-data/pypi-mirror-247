from enum import Enum


class ServiceType(Enum):
    """
    部署在用户账户下
    """
    USER = (0, "private")
    """
    托管在服务商账户下
    """
    MANAGED = (1, "managed")
    """
    纯代运维
    """
    OPERATION = (2, "operation")
    """
    POC 模式 部署在统一大账号下
    """
    POC = (3, "poc")
    """
    数据产品
    """
    DATASET = (4, "dataset")
    """
    本地部署
    """
    ON_PREMISE = (5, "onPremise")

    def __init__(self, value, outer_name):
        self._value_ = value
        self.outer_name = outer_name
