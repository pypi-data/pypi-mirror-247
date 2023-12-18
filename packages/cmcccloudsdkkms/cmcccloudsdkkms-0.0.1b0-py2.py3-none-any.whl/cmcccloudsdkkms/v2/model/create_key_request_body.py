# coding: utf-8

import six

from cmcccloudsdkcore.utils.http_utils import sanitize_for_serialization


class CreateKeyRequestBody:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'key_alias': 'str',
        'key_spec': 'str',
        'key_usage': 'str',
        'key_description': 'str',
        'origin': 'str',
        'enterprise_project_id': 'str',
        'sequence': 'str',
        'keystore_id': 'str'
    }

    attribute_map = {
        'key_alias': 'key_alias',
        'key_spec': 'key_spec',
        'key_usage': 'key_usage',
        'key_description': 'key_description',
        'origin': 'origin',
        'enterprise_project_id': 'enterprise_project_id',
        'sequence': 'sequence',
        'keystore_id': 'keystore_id'
    }

    def __init__(self, key_alias=None, key_spec=None, key_usage=None, key_description=None, origin=None, enterprise_project_id=None, sequence=None, keystore_id=None):
        """CreateKeyRequestBody

        The model defined in cmcccloud sdk

        :param key_alias: The param of the CreateKeyRequestBody
        :type key_alias: str
        :param key_spec: The param of the CreateKeyRequestBody
        :type key_spec: str
        :param key_usage: The param of the CreateKeyRequestBody
        :type key_usage: str
        :param key_description: The param of the CreateKeyRequestBody
        :type key_description: str
        :param origin: The param of the CreateKeyRequestBody
        :type origin: str
        :param enterprise_project_id: The param of the CreateKeyRequestBody
        :type enterprise_project_id: str
        :param sequence: The param of the CreateKeyRequestBody
        :type sequence: str
        :param keystore_id: The param of the CreateKeyRequestBody
        :type keystore_id: str
        """
        
        

        self._key_alias = None
        self._key_spec = None
        self._key_usage = None
        self._key_description = None
        self._origin = None
        self._enterprise_project_id = None
        self._sequence = None
        self._keystore_id = None
        self.discriminator = None

        self.key_alias = key_alias
        if key_spec is not None:
            self.key_spec = key_spec
        if key_usage is not None:
            self.key_usage = key_usage
        if key_description is not None:
            self.key_description = key_description
        if origin is not None:
            self.origin = origin
        if enterprise_project_id is not None:
            self.enterprise_project_id = enterprise_project_id
        if sequence is not None:
            self.sequence = sequence
        if keystore_id is not None:
            self.keystore_id = keystore_id

    @property
    def key_alias(self):
        """Gets the key_alias of this CreateKeyRequestBody.

        :return: The key_alias of this CreateKeyRequestBody.
        :rtype: str
        """
        return self._key_alias

    @key_alias.setter
    def key_alias(self, key_alias):
        """Sets the key_alias of this CreateKeyRequestBody.

        :param key_alias: The key_alias of this CreateKeyRequestBody.
        :type key_alias: str
        """
        self._key_alias = key_alias

    @property
    def key_spec(self):
        """Gets the key_spec of this CreateKeyRequestBody.

        :return: The key_spec of this CreateKeyRequestBody.
        :rtype: str
        """
        return self._key_spec

    @key_spec.setter
    def key_spec(self, key_spec):
        """Sets the key_spec of this CreateKeyRequestBody.

        :param key_spec: The key_spec of this CreateKeyRequestBody.
        :type key_spec: str
        """
        self._key_spec = key_spec

    @property
    def key_usage(self):
        """Gets the key_usage of this CreateKeyRequestBody.

        :return: The key_usage of this CreateKeyRequestBody.
        :rtype: str
        """
        return self._key_usage

    @key_usage.setter
    def key_usage(self, key_usage):
        """Sets the key_usage of this CreateKeyRequestBody.

        :param key_usage: The key_usage of this CreateKeyRequestBody.
        :type key_usage: str
        """
        self._key_usage = key_usage

    @property
    def key_description(self):
        """Gets the key_description of this CreateKeyRequestBody.

        :return: The key_description of this CreateKeyRequestBody.
        :rtype: str
        """
        return self._key_description

    @key_description.setter
    def key_description(self, key_description):
        """Sets the key_description of this CreateKeyRequestBody.

        :param key_description: The key_description of this CreateKeyRequestBody.
        :type key_description: str
        """
        self._key_description = key_description

    @property
    def origin(self):
        """Gets the origin of this CreateKeyRequestBody.

        :return: The origin of this CreateKeyRequestBody.
        :rtype: str
        """
        return self._origin

    @origin.setter
    def origin(self, origin):
        """Sets the origin of this CreateKeyRequestBody.

        :param origin: The origin of this CreateKeyRequestBody.
        :type origin: str
        """
        self._origin = origin

    @property
    def enterprise_project_id(self):
        """Gets the enterprise_project_id of this CreateKeyRequestBody.

        :return: The enterprise_project_id of this CreateKeyRequestBody.
        :rtype: str
        """
        return self._enterprise_project_id

    @enterprise_project_id.setter
    def enterprise_project_id(self, enterprise_project_id):
        """Sets the enterprise_project_id of this CreateKeyRequestBody.

        :param enterprise_project_id: The enterprise_project_id of this CreateKeyRequestBody.
        :type enterprise_project_id: str
        """
        self._enterprise_project_id = enterprise_project_id

    @property
    def sequence(self):
        """Gets the sequence of this CreateKeyRequestBody.

        :return: The sequence of this CreateKeyRequestBody.
        :rtype: str
        """
        return self._sequence

    @sequence.setter
    def sequence(self, sequence):
        """Sets the sequence of this CreateKeyRequestBody.

        :param sequence: The sequence of this CreateKeyRequestBody.
        :type sequence: str
        """
        self._sequence = sequence

    @property
    def keystore_id(self):
        """Gets the keystore_id of this CreateKeyRequestBody.

        :return: The keystore_id of this CreateKeyRequestBody.
        :rtype: str
        """
        return self._keystore_id

    @keystore_id.setter
    def keystore_id(self, keystore_id):
        """Sets the keystore_id of this CreateKeyRequestBody.

        :param keystore_id: The keystore_id of this CreateKeyRequestBody.
        :type keystore_id: str
        """
        self._keystore_id = keystore_id

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
        if not isinstance(other, CreateKeyRequestBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
