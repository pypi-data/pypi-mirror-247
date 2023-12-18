# coding: utf-8

import six

from cmcccloudsdkcore.utils.http_utils import sanitize_for_serialization


class CreateGrantRequestBody:

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
        'grantee_principal': 'str',
        'operations': 'list[str]',
        'name': 'str',
        'retiring_principal': 'str',
        'grantee_principal_type': 'str',
        'sequence': 'str'
    }

    attribute_map = {
        'key_id': 'key_id',
        'grantee_principal': 'grantee_principal',
        'operations': 'operations',
        'name': 'name',
        'retiring_principal': 'retiring_principal',
        'grantee_principal_type': 'grantee_principal_type',
        'sequence': 'sequence'
    }

    def __init__(self, key_id=None, grantee_principal=None, operations=None, name=None, retiring_principal=None, grantee_principal_type=None, sequence=None):
        """CreateGrantRequestBody

        The model defined in cmcccloud sdk

        :param key_id: The param of the CreateGrantRequestBody
        :type key_id: str
        :param grantee_principal: The param of the CreateGrantRequestBody
        :type grantee_principal: str
        :param operations: The param of the CreateGrantRequestBody
        :type operations: list[str]
        :param name: The param of the CreateGrantRequestBody
        :type name: str
        :param retiring_principal: The param of the CreateGrantRequestBody
        :type retiring_principal: str
        :param grantee_principal_type: The param of the CreateGrantRequestBody
        :type grantee_principal_type: str
        :param sequence: The param of the CreateGrantRequestBody
        :type sequence: str
        """
        
        

        self._key_id = None
        self._grantee_principal = None
        self._operations = None
        self._name = None
        self._retiring_principal = None
        self._grantee_principal_type = None
        self._sequence = None
        self.discriminator = None

        self.key_id = key_id
        self.grantee_principal = grantee_principal
        self.operations = operations
        if name is not None:
            self.name = name
        if retiring_principal is not None:
            self.retiring_principal = retiring_principal
        if grantee_principal_type is not None:
            self.grantee_principal_type = grantee_principal_type
        if sequence is not None:
            self.sequence = sequence

    @property
    def key_id(self):
        """Gets the key_id of this CreateGrantRequestBody.

        :return: The key_id of this CreateGrantRequestBody.
        :rtype: str
        """
        return self._key_id

    @key_id.setter
    def key_id(self, key_id):
        """Sets the key_id of this CreateGrantRequestBody.

        :param key_id: The key_id of this CreateGrantRequestBody.
        :type key_id: str
        """
        self._key_id = key_id

    @property
    def grantee_principal(self):
        """Gets the grantee_principal of this CreateGrantRequestBody.

        :return: The grantee_principal of this CreateGrantRequestBody.
        :rtype: str
        """
        return self._grantee_principal

    @grantee_principal.setter
    def grantee_principal(self, grantee_principal):
        """Sets the grantee_principal of this CreateGrantRequestBody.

        :param grantee_principal: The grantee_principal of this CreateGrantRequestBody.
        :type grantee_principal: str
        """
        self._grantee_principal = grantee_principal

    @property
    def operations(self):
        """Gets the operations of this CreateGrantRequestBody.

        :return: The operations of this CreateGrantRequestBody.
        :rtype: list[str]
        """
        return self._operations

    @operations.setter
    def operations(self, operations):
        """Sets the operations of this CreateGrantRequestBody.

        :param operations: The operations of this CreateGrantRequestBody.
        :type operations: list[str]
        """
        self._operations = operations

    @property
    def name(self):
        """Gets the name of this CreateGrantRequestBody.

        :return: The name of this CreateGrantRequestBody.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this CreateGrantRequestBody.

        :param name: The name of this CreateGrantRequestBody.
        :type name: str
        """
        self._name = name

    @property
    def retiring_principal(self):
        """Gets the retiring_principal of this CreateGrantRequestBody.

        :return: The retiring_principal of this CreateGrantRequestBody.
        :rtype: str
        """
        return self._retiring_principal

    @retiring_principal.setter
    def retiring_principal(self, retiring_principal):
        """Sets the retiring_principal of this CreateGrantRequestBody.

        :param retiring_principal: The retiring_principal of this CreateGrantRequestBody.
        :type retiring_principal: str
        """
        self._retiring_principal = retiring_principal

    @property
    def grantee_principal_type(self):
        """Gets the grantee_principal_type of this CreateGrantRequestBody.

        :return: The grantee_principal_type of this CreateGrantRequestBody.
        :rtype: str
        """
        return self._grantee_principal_type

    @grantee_principal_type.setter
    def grantee_principal_type(self, grantee_principal_type):
        """Sets the grantee_principal_type of this CreateGrantRequestBody.

        :param grantee_principal_type: The grantee_principal_type of this CreateGrantRequestBody.
        :type grantee_principal_type: str
        """
        self._grantee_principal_type = grantee_principal_type

    @property
    def sequence(self):
        """Gets the sequence of this CreateGrantRequestBody.

        :return: The sequence of this CreateGrantRequestBody.
        :rtype: str
        """
        return self._sequence

    @sequence.setter
    def sequence(self, sequence):
        """Sets the sequence of this CreateGrantRequestBody.

        :param sequence: The sequence of this CreateGrantRequestBody.
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
        if not isinstance(other, CreateGrantRequestBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
