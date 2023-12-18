# coding: utf-8

import six

from cmcccloudsdkcore.utils.http_utils import sanitize_for_serialization


class ImportKeyMaterialRequestBody:

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
        'import_token': 'str',
        'encrypted_key_material': 'str',
        'encrypted_privatekey': 'str',
        'expiration_time': 'int',
        'sequence': 'str'
    }

    attribute_map = {
        'key_id': 'key_id',
        'import_token': 'import_token',
        'encrypted_key_material': 'encrypted_key_material',
        'encrypted_privatekey': 'encrypted_privatekey',
        'expiration_time': 'expiration_time',
        'sequence': 'sequence'
    }

    def __init__(self, key_id=None, import_token=None, encrypted_key_material=None, encrypted_privatekey=None, expiration_time=None, sequence=None):
        """ImportKeyMaterialRequestBody

        The model defined in cmcccloud sdk

        :param key_id: The param of the ImportKeyMaterialRequestBody
        :type key_id: str
        :param import_token: The param of the ImportKeyMaterialRequestBody
        :type import_token: str
        :param encrypted_key_material: The param of the ImportKeyMaterialRequestBody
        :type encrypted_key_material: str
        :param encrypted_privatekey: The param of the ImportKeyMaterialRequestBody
        :type encrypted_privatekey: str
        :param expiration_time: The param of the ImportKeyMaterialRequestBody
        :type expiration_time: int
        :param sequence: The param of the ImportKeyMaterialRequestBody
        :type sequence: str
        """
        
        

        self._key_id = None
        self._import_token = None
        self._encrypted_key_material = None
        self._encrypted_privatekey = None
        self._expiration_time = None
        self._sequence = None
        self.discriminator = None

        self.key_id = key_id
        self.import_token = import_token
        self.encrypted_key_material = encrypted_key_material
        if encrypted_privatekey is not None:
            self.encrypted_privatekey = encrypted_privatekey
        if expiration_time is not None:
            self.expiration_time = expiration_time
        if sequence is not None:
            self.sequence = sequence

    @property
    def key_id(self):
        """Gets the key_id of this ImportKeyMaterialRequestBody.

        :return: The key_id of this ImportKeyMaterialRequestBody.
        :rtype: str
        """
        return self._key_id

    @key_id.setter
    def key_id(self, key_id):
        """Sets the key_id of this ImportKeyMaterialRequestBody.

        :param key_id: The key_id of this ImportKeyMaterialRequestBody.
        :type key_id: str
        """
        self._key_id = key_id

    @property
    def import_token(self):
        """Gets the import_token of this ImportKeyMaterialRequestBody.

        :return: The import_token of this ImportKeyMaterialRequestBody.
        :rtype: str
        """
        return self._import_token

    @import_token.setter
    def import_token(self, import_token):
        """Sets the import_token of this ImportKeyMaterialRequestBody.

        :param import_token: The import_token of this ImportKeyMaterialRequestBody.
        :type import_token: str
        """
        self._import_token = import_token

    @property
    def encrypted_key_material(self):
        """Gets the encrypted_key_material of this ImportKeyMaterialRequestBody.

        :return: The encrypted_key_material of this ImportKeyMaterialRequestBody.
        :rtype: str
        """
        return self._encrypted_key_material

    @encrypted_key_material.setter
    def encrypted_key_material(self, encrypted_key_material):
        """Sets the encrypted_key_material of this ImportKeyMaterialRequestBody.

        :param encrypted_key_material: The encrypted_key_material of this ImportKeyMaterialRequestBody.
        :type encrypted_key_material: str
        """
        self._encrypted_key_material = encrypted_key_material

    @property
    def encrypted_privatekey(self):
        """Gets the encrypted_privatekey of this ImportKeyMaterialRequestBody.

        :return: The encrypted_privatekey of this ImportKeyMaterialRequestBody.
        :rtype: str
        """
        return self._encrypted_privatekey

    @encrypted_privatekey.setter
    def encrypted_privatekey(self, encrypted_privatekey):
        """Sets the encrypted_privatekey of this ImportKeyMaterialRequestBody.

        :param encrypted_privatekey: The encrypted_privatekey of this ImportKeyMaterialRequestBody.
        :type encrypted_privatekey: str
        """
        self._encrypted_privatekey = encrypted_privatekey

    @property
    def expiration_time(self):
        """Gets the expiration_time of this ImportKeyMaterialRequestBody.

        :return: The expiration_time of this ImportKeyMaterialRequestBody.
        :rtype: int
        """
        return self._expiration_time

    @expiration_time.setter
    def expiration_time(self, expiration_time):
        """Sets the expiration_time of this ImportKeyMaterialRequestBody.

        :param expiration_time: The expiration_time of this ImportKeyMaterialRequestBody.
        :type expiration_time: int
        """
        self._expiration_time = expiration_time

    @property
    def sequence(self):
        """Gets the sequence of this ImportKeyMaterialRequestBody.

        :return: The sequence of this ImportKeyMaterialRequestBody.
        :rtype: str
        """
        return self._sequence

    @sequence.setter
    def sequence(self, sequence):
        """Sets the sequence of this ImportKeyMaterialRequestBody.

        :param sequence: The sequence of this ImportKeyMaterialRequestBody.
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
        if not isinstance(other, ImportKeyMaterialRequestBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
