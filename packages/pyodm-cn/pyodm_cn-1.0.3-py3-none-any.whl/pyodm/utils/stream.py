
from pyodm.utils.search.odm_dfs import ODMDfs
from pyodm.utils.odm_utils import OdmUtils


class Stream:
    def __init__(self, data):
        self.dfs = self.dfs_clazz()(data)

    def find(self, _lambda):
        return Optional(self.dfs.find(_lambda=_lambda))

    def dfs_clazz(self): return ODMDfs


class Optional:
    def __init__(self, data):
        self._data = data

    def get(self):
        return self._data

    def find(self, _lambda):
        return self.as_stream().find(_lambda=_lambda)

    def update(self, **attributes):
        """
        更新 ODM 的属性
        :param attributes:
        :type attributes:
        :return:
        :rtype:
        """
        for name, value in attributes.items():
            self._data.__dict__.get(name).set_value(value)
        return self

    def update_text(self, value):
        """
        更新 ODM 的文本值
        :param value:
        :type value:
        :return:
        :rtype:
        """
        self._data.set_value(value)
        return self

    def merge(self, name, odm_element):
        """
        合并 两个 ODM ELEMENT
        前提是 odm_element 和 当前的 element 相同
        OneElement ,以当前元素为基准，合并属性，并且 合并子元素
        ManyElement , 在原有的元素上，添加新的元素
        :param name:
        :type name:
        :param odm_element:
        :type odm_element:
        :return:
        :rtype:
        """
        # if self._data.get_name() != odm_element.get_name():
        #     raise Exception(f'{self._data.get_name()} is different {odm_element.get_name()}')
        OdmUtils.merge(self._data, odm_element)

    def append(self, name, odm_element):
        """
        ManyElements 添加一个元素
        :return:
        :rtype:
        """
        if OdmUtils.is_many_elements(self._data.__dict__.get(name)):
            OdmUtils.append(self._data.__dict__.get(name), odm_element)
        else:
            raise Exception(f"{name} is not ManyElements")

    def as_stream(self):
        return Stream(self._data)
