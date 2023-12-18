# coding: utf-8

import six

from cmcccloudsdkcore.utils.http_utils import sanitize_for_serialization


class ListRetirableGrantsRequestBody:

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
        'sequence': 'str'
    }

    attribute_map = {
        'limit': 'limit',
        'marker': 'marker',
        'sequence': 'sequence'
    }

    def __init__(self, limit=None, marker=None, sequence=None):
        """ListRetirableGrantsRequestBody

        The model defined in cmcccloud sdk

        :param limit: The param of the ListRetirableGrantsRequestBody
        :type limit: str
        :param marker: The param of the ListRetirableGrantsRequestBody
        :type marker: str
        :param sequence: The param of the ListRetirableGrantsRequestBody
        :type sequence: str
        """
        
        

        self._limit = None
        self._marker = None
        self._sequence = None
        self.discriminator = None

        if limit is not None:
            self.limit = limit
        if marker is not None:
            self.marker = marker
        if sequence is not None:
            self.sequence = sequence

    @property
    def limit(self):
        """Gets the limit of this ListRetirableGrantsRequestBody.

        :return: The limit of this ListRetirableGrantsRequestBody.
        :rtype: str
        """
        return self._limit

    @limit.setter
    def limit(self, limit):
        """Sets the limit of this ListRetirableGrantsRequestBody.

        :param limit: The limit of this ListRetirableGrantsRequestBody.
        :type limit: str
        """
        self._limit = limit

    @property
    def marker(self):
        """Gets the marker of this ListRetirableGrantsRequestBody.

        :return: The marker of this ListRetirableGrantsRequestBody.
        :rtype: str
        """
        return self._marker

    @marker.setter
    def marker(self, marker):
        """Sets the marker of this ListRetirableGrantsRequestBody.

        :param marker: The marker of this ListRetirableGrantsRequestBody.
        :type marker: str
        """
        self._marker = marker

    @property
    def sequence(self):
        """Gets the sequence of this ListRetirableGrantsRequestBody.

        :return: The sequence of this ListRetirableGrantsRequestBody.
        :rtype: str
        """
        return self._sequence

    @sequence.setter
    def sequence(self, sequence):
        """Sets the sequence of this ListRetirableGrantsRequestBody.

        :param sequence: The sequence of this ListRetirableGrantsRequestBody.
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
        if not isinstance(other, ListRetirableGrantsRequestBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
