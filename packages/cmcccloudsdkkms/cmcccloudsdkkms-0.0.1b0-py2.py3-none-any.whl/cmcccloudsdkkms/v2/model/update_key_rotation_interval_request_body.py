# coding: utf-8

import six

from cmcccloudsdkcore.utils.http_utils import sanitize_for_serialization


class UpdateKeyRotationIntervalRequestBody:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'key_id': 'str',
        'rotation_interval': 'int',
        'sequence': 'str'
    }

    attribute_map = {
        'key_id': 'key_id',
        'rotation_interval': 'rotation_interval',
        'sequence': 'sequence'
    }

    def __init__(self, key_id=None, rotation_interval=None, sequence=None):
        """UpdateKeyRotationIntervalRequestBody

        The model defined in cmcccloud sdk

        :param key_id: The param of the UpdateKeyRotationIntervalRequestBody
        :type key_id: str
        :param rotation_interval: The param of the UpdateKeyRotationIntervalRequestBody
        :type rotation_interval: int
        :param sequence: The param of the UpdateKeyRotationIntervalRequestBody
        :type sequence: str
        """
        
        

        self._key_id = None
        self._rotation_interval = None
        self._sequence = None
        self.discriminator = None

        self.key_id = key_id
        self.rotation_interval = rotation_interval
        if sequence is not None:
            self.sequence = sequence

    @property
    def key_id(self):
        """Gets the key_id of this UpdateKeyRotationIntervalRequestBody.

        :return: The key_id of this UpdateKeyRotationIntervalRequestBody.
        :rtype: str
        """
        return self._key_id

    @key_id.setter
    def key_id(self, key_id):
        """Sets the key_id of this UpdateKeyRotationIntervalRequestBody.

        :param key_id: The key_id of this UpdateKeyRotationIntervalRequestBody.
        :type key_id: str
        """
        self._key_id = key_id

    @property
    def rotation_interval(self):
        """Gets the rotation_interval of this UpdateKeyRotationIntervalRequestBody.

        :return: The rotation_interval of this UpdateKeyRotationIntervalRequestBody.
        :rtype: int
        """
        return self._rotation_interval

    @rotation_interval.setter
    def rotation_interval(self, rotation_interval):
        """Sets the rotation_interval of this UpdateKeyRotationIntervalRequestBody.

        :param rotation_interval: The rotation_interval of this UpdateKeyRotationIntervalRequestBody.
        :type rotation_interval: int
        """
        self._rotation_interval = rotation_interval

    @property
    def sequence(self):
        """Gets the sequence of this UpdateKeyRotationIntervalRequestBody.

        :return: The sequence of this UpdateKeyRotationIntervalRequestBody.
        :rtype: str
        """
        return self._sequence

    @sequence.setter
    def sequence(self, sequence):
        """Sets the sequence of this UpdateKeyRotationIntervalRequestBody.

        :param sequence: The sequence of this UpdateKeyRotationIntervalRequestBody.
        :type sequence: str
        """
        self._sequence = sequence

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
        if not isinstance(other, UpdateKeyRotationIntervalRequestBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
