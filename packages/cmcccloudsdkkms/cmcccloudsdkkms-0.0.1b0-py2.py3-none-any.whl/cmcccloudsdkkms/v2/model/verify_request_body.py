# coding: utf-8

import six

from cmcccloudsdkcore.utils.http_utils import sanitize_for_serialization


class VerifyRequestBody:

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
        'message': 'str',
        'signature': 'str',
        'signing_algorithm': 'str',
        'message_type': 'str',
        'sequence': 'str'
    }

    attribute_map = {
        'key_id': 'key_id',
        'message': 'message',
        'signature': 'signature',
        'signing_algorithm': 'signing_algorithm',
        'message_type': 'message_type',
        'sequence': 'sequence'
    }

    def __init__(self, key_id=None, message=None, signature=None, signing_algorithm=None, message_type=None, sequence=None):
        """VerifyRequestBody

        The model defined in cmcccloud sdk

        :param key_id: The param of the VerifyRequestBody
        :type key_id: str
        :param message: The param of the VerifyRequestBody
        :type message: str
        :param signature: The param of the VerifyRequestBody
        :type signature: str
        :param signing_algorithm: The param of the VerifyRequestBody
        :type signing_algorithm: str
        :param message_type: The param of the VerifyRequestBody
        :type message_type: str
        :param sequence: The param of the VerifyRequestBody
        :type sequence: str
        """
        
        

        self._key_id = None
        self._message = None
        self._signature = None
        self._signing_algorithm = None
        self._message_type = None
        self._sequence = None
        self.discriminator = None

        self.key_id = key_id
        self.message = message
        self.signature = signature
        self.signing_algorithm = signing_algorithm
        if message_type is not None:
            self.message_type = message_type
        if sequence is not None:
            self.sequence = sequence

    @property
    def key_id(self):
        """Gets the key_id of this VerifyRequestBody.

        :return: The key_id of this VerifyRequestBody.
        :rtype: str
        """
        return self._key_id

    @key_id.setter
    def key_id(self, key_id):
        """Sets the key_id of this VerifyRequestBody.

        :param key_id: The key_id of this VerifyRequestBody.
        :type key_id: str
        """
        self._key_id = key_id

    @property
    def message(self):
        """Gets the message of this VerifyRequestBody.

        :return: The message of this VerifyRequestBody.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this VerifyRequestBody.

        :param message: The message of this VerifyRequestBody.
        :type message: str
        """
        self._message = message

    @property
    def signature(self):
        """Gets the signature of this VerifyRequestBody.

        :return: The signature of this VerifyRequestBody.
        :rtype: str
        """
        return self._signature

    @signature.setter
    def signature(self, signature):
        """Sets the signature of this VerifyRequestBody.

        :param signature: The signature of this VerifyRequestBody.
        :type signature: str
        """
        self._signature = signature

    @property
    def signing_algorithm(self):
        """Gets the signing_algorithm of this VerifyRequestBody.

        :return: The signing_algorithm of this VerifyRequestBody.
        :rtype: str
        """
        return self._signing_algorithm

    @signing_algorithm.setter
    def signing_algorithm(self, signing_algorithm):
        """Sets the signing_algorithm of this VerifyRequestBody.

        :param signing_algorithm: The signing_algorithm of this VerifyRequestBody.
        :type signing_algorithm: str
        """
        self._signing_algorithm = signing_algorithm

    @property
    def message_type(self):
        """Gets the message_type of this VerifyRequestBody.

        :return: The message_type of this VerifyRequestBody.
        :rtype: str
        """
        return self._message_type

    @message_type.setter
    def message_type(self, message_type):
        """Sets the message_type of this VerifyRequestBody.

        :param message_type: The message_type of this VerifyRequestBody.
        :type message_type: str
        """
        self._message_type = message_type

    @property
    def sequence(self):
        """Gets the sequence of this VerifyRequestBody.

        :return: The sequence of this VerifyRequestBody.
        :rtype: str
        """
        return self._sequence

    @sequence.setter
    def sequence(self, sequence):
        """Sets the sequence of this VerifyRequestBody.

        :param sequence: The sequence of this VerifyRequestBody.
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
        if not isinstance(other, VerifyRequestBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
