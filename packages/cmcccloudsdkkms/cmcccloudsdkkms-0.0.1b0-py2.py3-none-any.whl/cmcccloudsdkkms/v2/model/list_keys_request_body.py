# coding: utf-8

import six

from cmcccloudsdkcore.utils.http_utils import sanitize_for_serialization


class ListKeysRequestBody:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'limit': 'str',
        'marker': 'str',
        'key_state': 'str',
        'key_spec': 'str',
        'enterprise_project_id': 'str',
        'sequence': 'str'
    }

    attribute_map = {
        'limit': 'limit',
        'marker': 'marker',
        'key_state': 'key_state',
        'key_spec': 'key_spec',
        'enterprise_project_id': 'enterprise_project_id',
        'sequence': 'sequence'
    }

    def __init__(self, limit=None, marker=None, key_state=None, key_spec=None, enterprise_project_id=None, sequence=None):
        """ListKeysRequestBody

        The model defined in cmcccloud sdk

        :param limit: The param of the ListKeysRequestBody
        :type limit: str
        :param marker: The param of the ListKeysRequestBody
        :type marker: str
        :param key_state: The param of the ListKeysRequestBody
        :type key_state: str
        :param key_spec: The param of the ListKeysRequestBody
        :type key_spec: str
        :param enterprise_project_id: The param of the ListKeysRequestBody
        :type enterprise_project_id: str
        :param sequence: The param of the ListKeysRequestBody
        :type sequence: str
        """
        
        

        self._limit = None
        self._marker = None
        self._key_state = None
        self._key_spec = None
        self._enterprise_project_id = None
        self._sequence = None
        self.discriminator = None

        if limit is not None:
            self.limit = limit
        if marker is not None:
            self.marker = marker
        if key_state is not None:
            self.key_state = key_state
        if key_spec is not None:
            self.key_spec = key_spec
        if enterprise_project_id is not None:
            self.enterprise_project_id = enterprise_project_id
        if sequence is not None:
            self.sequence = sequence

    @property
    def limit(self):
        """Gets the limit of this ListKeysRequestBody.

        :return: The limit of this ListKeysRequestBody.
        :rtype: str
        """
        return self._limit

    @limit.setter
    def limit(self, limit):
        """Sets the limit of this ListKeysRequestBody.

        :param limit: The limit of this ListKeysRequestBody.
        :type limit: str
        """
        self._limit = limit

    @property
    def marker(self):
        """Gets the marker of this ListKeysRequestBody.

        :return: The marker of this ListKeysRequestBody.
        :rtype: str
        """
        return self._marker

    @marker.setter
    def marker(self, marker):
        """Sets the marker of this ListKeysRequestBody.

        :param marker: The marker of this ListKeysRequestBody.
        :type marker: str
        """
        self._marker = marker

    @property
    def key_state(self):
        """Gets the key_state of this ListKeysRequestBody.

        :return: The key_state of this ListKeysRequestBody.
        :rtype: str
        """
        return self._key_state

    @key_state.setter
    def key_state(self, key_state):
        """Sets the key_state of this ListKeysRequestBody.

        :param key_state: The key_state of this ListKeysRequestBody.
        :type key_state: str
        """
        self._key_state = key_state

    @property
    def key_spec(self):
        """Gets the key_spec of this ListKeysRequestBody.

        :return: The key_spec of this ListKeysRequestBody.
        :rtype: str
        """
        return self._key_spec

    @key_spec.setter
    def key_spec(self, key_spec):
        """Sets the key_spec of this ListKeysRequestBody.

        :param key_spec: The key_spec of this ListKeysRequestBody.
        :type key_spec: str
        """
        self._key_spec = key_spec

    @property
    def enterprise_project_id(self):
        """Gets the enterprise_project_id of this ListKeysRequestBody.

        :return: The enterprise_project_id of this ListKeysRequestBody.
        :rtype: str
        """
        return self._enterprise_project_id

    @enterprise_project_id.setter
    def enterprise_project_id(self, enterprise_project_id):
        """Sets the enterprise_project_id of this ListKeysRequestBody.

        :param enterprise_project_id: The enterprise_project_id of this ListKeysRequestBody.
        :type enterprise_project_id: str
        """
        self._enterprise_project_id = enterprise_project_id

    @property
    def sequence(self):
        """Gets the sequence of this ListKeysRequestBody.

        :return: The sequence of this ListKeysRequestBody.
        :rtype: str
        """
        return self._sequence

    @sequence.setter
    def sequence(self, sequence):
        """Sets the sequence of this ListKeysRequestBody.

        :param sequence: The sequence of this ListKeysRequestBody.
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
        if not isinstance(other, ListKeysRequestBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
