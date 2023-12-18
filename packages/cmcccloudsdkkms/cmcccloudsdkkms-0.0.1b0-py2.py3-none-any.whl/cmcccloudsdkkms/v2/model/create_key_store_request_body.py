# coding: utf-8

import six

from cmcccloudsdkcore.utils.http_utils import sanitize_for_serialization


class CreateKeyStoreRequestBody:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'keystore_alias': 'str',
        'hsm_cluster_id': 'str',
        'hsm_ca_cert': 'str'
    }

    attribute_map = {
        'keystore_alias': 'keystore_alias',
        'hsm_cluster_id': 'hsm_cluster_id',
        'hsm_ca_cert': 'hsm_ca_cert'
    }

    def __init__(self, keystore_alias=None, hsm_cluster_id=None, hsm_ca_cert=None):
        """CreateKeyStoreRequestBody

        The model defined in cmcccloud sdk

        :param keystore_alias: The param of the CreateKeyStoreRequestBody
        :type keystore_alias: str
        :param hsm_cluster_id: The param of the CreateKeyStoreRequestBody
        :type hsm_cluster_id: str
        :param hsm_ca_cert: The param of the CreateKeyStoreRequestBody
        :type hsm_ca_cert: str
        """
        
        

        self._keystore_alias = None
        self._hsm_cluster_id = None
        self._hsm_ca_cert = None
        self.discriminator = None

        self.keystore_alias = keystore_alias
        self.hsm_cluster_id = hsm_cluster_id
        self.hsm_ca_cert = hsm_ca_cert

    @property
    def keystore_alias(self):
        """Gets the keystore_alias of this CreateKeyStoreRequestBody.

        :return: The keystore_alias of this CreateKeyStoreRequestBody.
        :rtype: str
        """
        return self._keystore_alias

    @keystore_alias.setter
    def keystore_alias(self, keystore_alias):
        """Sets the keystore_alias of this CreateKeyStoreRequestBody.

        :param keystore_alias: The keystore_alias of this CreateKeyStoreRequestBody.
        :type keystore_alias: str
        """
        self._keystore_alias = keystore_alias

    @property
    def hsm_cluster_id(self):
        """Gets the hsm_cluster_id of this CreateKeyStoreRequestBody.

        :return: The hsm_cluster_id of this CreateKeyStoreRequestBody.
        :rtype: str
        """
        return self._hsm_cluster_id

    @hsm_cluster_id.setter
    def hsm_cluster_id(self, hsm_cluster_id):
        """Sets the hsm_cluster_id of this CreateKeyStoreRequestBody.

        :param hsm_cluster_id: The hsm_cluster_id of this CreateKeyStoreRequestBody.
        :type hsm_cluster_id: str
        """
        self._hsm_cluster_id = hsm_cluster_id

    @property
    def hsm_ca_cert(self):
        """Gets the hsm_ca_cert of this CreateKeyStoreRequestBody.

        :return: The hsm_ca_cert of this CreateKeyStoreRequestBody.
        :rtype: str
        """
        return self._hsm_ca_cert

    @hsm_ca_cert.setter
    def hsm_ca_cert(self, hsm_ca_cert):
        """Sets the hsm_ca_cert of this CreateKeyStoreRequestBody.

        :param hsm_ca_cert: The hsm_ca_cert of this CreateKeyStoreRequestBody.
        :type hsm_ca_cert: str
        """
        self._hsm_ca_cert = hsm_ca_cert

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
        if not isinstance(other, CreateKeyStoreRequestBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
