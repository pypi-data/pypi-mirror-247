# coding: utf-8

import six

from cmcccloudsdkcore.utils.http_utils import sanitize_for_serialization


class EncryptDataRequestBody:

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
        'encryption_algorithm': 'str',
        'sequence': 'str'
    }

    attribute_map = {
        'key_id': 'key_id',
        'plain_text': 'plain_text',
        'encryption_algorithm': 'encryption_algorithm',
        'sequence': 'sequence'
    }

    def __init__(self, key_id=None, plain_text=None, encryption_algorithm=None, sequence=None):
        """EncryptDataRequestBody

        The model defined in cmcccloud sdk

        :param key_id: The param of the EncryptDataRequestBody
        :type key_id: str
        :param plain_text: The param of the EncryptDataRequestBody
        :type plain_text: str
        :param encryption_algorithm: The param of the EncryptDataRequestBody
        :type encryption_algorithm: str
        :param sequence: The param of the EncryptDataRequestBody
        :type sequence: str
        """
        
        

        self._key_id = None
        self._plain_text = None
        self._encryption_algorithm = None
        self._sequence = None
        self.discriminator = None

        self.key_id = key_id
        self.plain_text = plain_text
        if encryption_algorithm is not None:
            self.encryption_algorithm = encryption_algorithm
        if sequence is not None:
            self.sequence = sequence

    @property
    def key_id(self):
        """Gets the key_id of this EncryptDataRequestBody.

        :return: The key_id of this EncryptDataRequestBody.
        :rtype: str
        """
        return self._key_id

    @key_id.setter
    def key_id(self, key_id):
        """Sets the key_id of this EncryptDataRequestBody.

        :param key_id: The key_id of this EncryptDataRequestBody.
        :type key_id: str
        """
        self._key_id = key_id

    @property
    def plain_text(self):
        """Gets the plain_text of this EncryptDataRequestBody.

        :return: The plain_text of this EncryptDataRequestBody.
        :rtype: str
        """
        return self._plain_text

    @plain_text.setter
    def plain_text(self, plain_text):
        """Sets the plain_text of this EncryptDataRequestBody.

        :param plain_text: The plain_text of this EncryptDataRequestBody.
        :type plain_text: str
        """
        self._plain_text = plain_text

    @property
    def encryption_algorithm(self):
        """Gets the encryption_algorithm of this EncryptDataRequestBody.

        :return: The encryption_algorithm of this EncryptDataRequestBody.
        :rtype: str
        """
        return self._encryption_algorithm

    @encryption_algorithm.setter
    def encryption_algorithm(self, encryption_algorithm):
        """Sets the encryption_algorithm of this EncryptDataRequestBody.

        :param encryption_algorithm: The encryption_algorithm of this EncryptDataRequestBody.
        :type encryption_algorithm: str
        """
        self._encryption_algorithm = encryption_algorithm

    @property
    def sequence(self):
        """Gets the sequence of this EncryptDataRequestBody.

        :return: The sequence of this EncryptDataRequestBody.
        :rtype: str
        """
        return self._sequence

    @sequence.setter
    def sequence(self, sequence):
        """Sets the sequence of this EncryptDataRequestBody.

        :param sequence: The sequence of this EncryptDataRequestBody.
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
        if not isinstance(other, EncryptDataRequestBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
