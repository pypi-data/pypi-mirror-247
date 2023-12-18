# coding: utf-8

import six

from cmcccloudsdkcore.utils.http_utils import sanitize_for_serialization


class Resources:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'type': 'str',
        'used': 'int',
        'quota': 'int'
    }

    attribute_map = {
        'type': 'type',
        'used': 'used',
        'quota': 'quota'
    }

    def __init__(self, type=None, used=None, quota=None):
        """Resources

        The model defined in cmcccloud sdk

        :param type: The param of the Resources
        :type type: str
        :param used: The param of the Resources
        :type used: int
        :param quota: The param of the Resources
        :type quota: int
        """
        
        

        self._type = None
        self._used = None
        self._quota = None
        self.discriminator = None

        if type is not None:
            self.type = type
        if used is not None:
            self.used = used
        if quota is not None:
            self.quota = quota

    @property
    def type(self):
        """Gets the type of this Resources.

        :return: The type of this Resources.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this Resources.

        :param type: The type of this Resources.
        :type type: str
        """
        self._type = type

    @property
    def used(self):
        """Gets the used of this Resources.

        :return: The used of this Resources.
        :rtype: int
        """
        return self._used

    @used.setter
    def used(self, used):
        """Sets the used of this Resources.

        :param used: The used of this Resources.
        :type used: int
        """
        self._used = used

    @property
    def quota(self):
        """Gets the quota of this Resources.

        :return: The quota of this Resources.
        :rtype: int
        """
        return self._quota

    @quota.setter
    def quota(self, quota):
        """Sets the quota of this Resources.

        :param quota: The quota of this Resources.
        :type quota: int
        """
        self._quota = quota

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                if attr in self.sensitive_list:
                    result[attr] = "****"
                else:
                    result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        import simplejson as json
        if six.PY2:
            import sys
            reload(sys)
            sys.setdefaultencoding("utf-8")
        return json.dumps(sanitize_for_serialization(self), ensure_ascii=False)

    def __repr__(self):
        """For `print`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Resources):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
