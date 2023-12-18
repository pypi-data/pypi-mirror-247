# coding: utf-8

import six

from cmcccloudsdkcore.utils.http_utils import sanitize_for_serialization


class EncryptDatakeyRequestBody:

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
        'plain_text': 'str',
        'datakey_plain_length': 'str',
        'sequence': 'str'
    }

    attribute_map = {
        'key_id': 'key_id',
        'plain_text': 'plain_text',
        'datakey_plain_length': 'datakey_plain_length',
        'sequence': 'sequence'
    }

    def __init__(self, key_id=None, plain_text=None, datakey_plain_length=None, sequence=None):
        """EncryptDatakeyRequestBody

        The model defined in cmcccloud sdk

        :param key_id: The param of the EncryptDatakeyRequestBody
        :type key_id: str
        :param plain_text: The param of the EncryptDatakeyRequestBody
        :type plain_text: str
        :param datakey_plain_length: The param of the EncryptDatakeyRequestBody
        :type datakey_plain_length: str
        :param sequence: The param of the EncryptDatakeyRequestBody
        :type sequence: str
        """
        
        

        self._key_id = None
        self._plain_text = None
        self._datakey_plain_length = None
        self._sequence = None
        self.discriminator = None

        self.key_id = key_id
        self.plain_text = plain_text
        self.datakey_plain_length = datakey_plain_length
        if sequence is not None:
            self.sequence = sequence

    @property
    def key_id(self):
        """Gets the key_id of this EncryptDatakeyRequestBody.

        :return: The key_id of this EncryptDatakeyRequestBody.
        :rtype: str
        """
        return self._key_id

    @key_id.setter
    def key_id(self, key_id):
        """Sets the key_id of this EncryptDatakeyRequestBody.

        :param key_id: The key_id of this EncryptDatakeyRequestBody.
        :type key_id: str
        """
        self._key_id = key_id

    @property
    def plain_text(self):
        """Gets the plain_text of this EncryptDatakeyRequestBody.

        :return: The plain_text of this EncryptDatakeyRequestBody.
        :rtype: str
        """
        return self._plain_text

    @plain_text.setter
    def plain_text(self, plain_text):
        """Sets the plain_text of this EncryptDatakeyRequestBody.

        :param plain_text: The plain_text of this EncryptDatakeyRequestBody.
        :type plain_text: str
        """
        self._plain_text = plain_text

    @property
    def datakey_plain_length(self):
        """Gets the datakey_plain_length of this EncryptDatakeyRequestBody.

        :return: The datakey_plain_length of this EncryptDatakeyRequestBody.
        :rtype: str
        """
        return self._datakey_plain_length

    @datakey_plain_length.setter
    def datakey_plain_length(self, datakey_plain_length):
        """Sets the datakey_plain_length of this EncryptDatakeyRequestBody.

        :param datakey_plain_length: The datakey_plain_length of this EncryptDatakeyRequestBody.
        :type datakey_plain_length: str
        """
        self._datakey_plain_length = datakey_plain_length

    @property
    def sequence(self):
        """Gets the sequence of this EncryptDatakeyRequestBody.

        :return: The sequence of this EncryptDatakeyRequestBody.
        :rtype: str
        """
        return self._sequence

    @sequence.setter
    def sequence(self, sequence):
        """Sets the sequence of this EncryptDatakeyRequestBody.

        :param sequence: The sequence of this EncryptDatakeyRequestBody.
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
        if not isinstance(other, EncryptDatakeyRequestBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
