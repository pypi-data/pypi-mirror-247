# coding: utf-8

import six

from cmcccloudsdkcore.utils.http_utils import sanitize_for_serialization


class CreateDatakeyRequestBody:

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
        'key_spec': 'str',
        'datakey_length': 'str',
        'sequence': 'str'
    }

    attribute_map = {
        'key_id': 'key_id',
        'key_spec': 'key_spec',
        'datakey_length': 'datakey_length',
        'sequence': 'sequence'
    }

    def __init__(self, key_id=None, key_spec=None, datakey_length=None, sequence=None):
        """CreateDatakeyRequestBody

        The model defined in cmcccloud sdk

        :param key_id: The param of the CreateDatakeyRequestBody
        :type key_id: str
        :param key_spec: The param of the CreateDatakeyRequestBody
        :type key_spec: str
        :param datakey_length: The param of the CreateDatakeyRequestBody
        :type datakey_length: str
        :param sequence: The param of the CreateDatakeyRequestBody
        :type sequence: str
        """
        
        

        self._key_id = None
        self._key_spec = None
        self._datakey_length = None
        self._sequence = None
        self.discriminator = None

        self.key_id = key_id
        if key_spec is not None:
            self.key_spec = key_spec
        if datakey_length is not None:
            self.datakey_length = datakey_length
        if sequence is not None:
            self.sequence = sequence

    @property
    def key_id(self):
        """Gets the key_id of this CreateDatakeyRequestBody.

        :return: The key_id of this CreateDatakeyRequestBody.
        :rtype: str
        """
        return self._key_id

    @key_id.setter
    def key_id(self, key_id):
        """Sets the key_id of this CreateDatakeyRequestBody.

        :param key_id: The key_id of this CreateDatakeyRequestBody.
        :type key_id: str
        """
        self._key_id = key_id

    @property
    def key_spec(self):
        """Gets the key_spec of this CreateDatakeyRequestBody.

        :return: The key_spec of this CreateDatakeyRequestBody.
        :rtype: str
        """
        return self._key_spec

    @key_spec.setter
    def key_spec(self, key_spec):
        """Sets the key_spec of this CreateDatakeyRequestBody.

        :param key_spec: The key_spec of this CreateDatakeyRequestBody.
        :type key_spec: str
        """
        self._key_spec = key_spec

    @property
    def datakey_length(self):
        """Gets the datakey_length of this CreateDatakeyRequestBody.

        :return: The datakey_length of this CreateDatakeyRequestBody.
        :rtype: str
        """
        return self._datakey_length

    @datakey_length.setter
    def datakey_length(self, datakey_length):
        """Sets the datakey_length of this CreateDatakeyRequestBody.

        :param datakey_length: The datakey_length of this CreateDatakeyRequestBody.
        :type datakey_length: str
        """
        self._datakey_length = datakey_length

    @property
    def sequence(self):
        """Gets the sequence of this CreateDatakeyRequestBody.

        :return: The sequence of this CreateDatakeyRequestBody.
        :rtype: str
        """
        return self._sequence

    @sequence.setter
    def sequence(self, sequence):
        """Sets the sequence of this CreateDatakeyRequestBody.

        :param sequence: The sequence of this CreateDatakeyRequestBody.
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
        if not isinstance(other, CreateDatakeyRequestBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
