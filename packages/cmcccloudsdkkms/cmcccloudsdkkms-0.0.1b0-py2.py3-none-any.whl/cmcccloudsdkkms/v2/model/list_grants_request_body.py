# coding: utf-8

import six

from cmcccloudsdkcore.utils.http_utils import sanitize_for_serialization


class ListGrantsRequestBody:

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
        'limit': 'str',
        'marker': 'str',
        'sequence': 'str'
    }

    attribute_map = {
        'key_id': 'key_id',
        'limit': 'limit',
        'marker': 'marker',
        'sequence': 'sequence'
    }

    def __init__(self, key_id=None, limit=None, marker=None, sequence=None):
        """ListGrantsRequestBody

        The model defined in cmcccloud sdk

        :param key_id: The param of the ListGrantsRequestBody
        :type key_id: str
        :param limit: The param of the ListGrantsRequestBody
        :type limit: str
        :param marker: The param of the ListGrantsRequestBody
        :type marker: str
        :param sequence: The param of the ListGrantsRequestBody
        :type sequence: str
        """
        
        

        self._key_id = None
        self._limit = None
        self._marker = None
        self._sequence = None
        self.discriminator = None

        self.key_id = key_id
        if limit is not None:
            self.limit = limit
        if marker is not None:
            self.marker = marker
        if sequence is not None:
            self.sequence = sequence

    @property
    def key_id(self):
        """Gets the key_id of this ListGrantsRequestBody.

        :return: The key_id of this ListGrantsRequestBody.
        :rtype: str
        """
        return self._key_id

    @key_id.setter
    def key_id(self, key_id):
        """Sets the key_id of this ListGrantsRequestBody.

        :param key_id: The key_id of this ListGrantsRequestBody.
        :type key_id: str
        """
        self._key_id = key_id

    @property
    def limit(self):
        """Gets the limit of this ListGrantsRequestBody.

        :return: The limit of this ListGrantsRequestBody.
        :rtype: str
        """
        return self._limit

    @limit.setter
    def limit(self, limit):
        """Sets the limit of this ListGrantsRequestBody.

        :param limit: The limit of this ListGrantsRequestBody.
        :type limit: str
        """
        self._limit = limit

    @property
    def marker(self):
        """Gets the marker of this ListGrantsRequestBody.

        :return: The marker of this ListGrantsRequestBody.
        :rtype: str
        """
        return self._marker

    @marker.setter
    def marker(self, marker):
        """Sets the marker of this ListGrantsRequestBody.

        :param marker: The marker of this ListGrantsRequestBody.
        :type marker: str
        """
        self._marker = marker

    @property
    def sequence(self):
        """Gets the sequence of this ListGrantsRequestBody.

        :return: The sequence of this ListGrantsRequestBody.
        :rtype: str
        """
        return self._sequence

    @sequence.setter
    def sequence(self, sequence):
        """Sets the sequence of this ListGrantsRequestBody.

        :param sequence: The sequence of this ListGrantsRequestBody.
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
        if not isinstance(other, ListGrantsRequestBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
