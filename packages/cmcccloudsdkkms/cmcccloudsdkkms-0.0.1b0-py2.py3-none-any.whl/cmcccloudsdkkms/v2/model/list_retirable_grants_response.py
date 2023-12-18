# coding: utf-8

import six

from cmcccloudsdkcore.sdk_response import SdkResponse
from cmcccloudsdkcore.utils.http_utils import sanitize_for_serialization


class ListRetirableGrantsResponse(SdkResponse):

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'grants': 'list[Grants]',
        'next_marker': 'str',
        'truncated': 'str'
    }

    attribute_map = {
        'grants': 'grants',
        'next_marker': 'next_marker',
        'truncated': 'truncated'
    }

    def __init__(self, grants=None, next_marker=None, truncated=None):
        """ListRetirableGrantsResponse

        The model defined in cmcccloud sdk

        :param grants: The param of the ListRetirableGrantsResponse
        :type grants: list[:class:`cmcccloudsdkkms.v2.Grants`]
        :param next_marker: The param of the ListRetirableGrantsResponse
        :type next_marker: str
        :param truncated: The param of the ListRetirableGrantsResponse
        :type truncated: str
        """
        
        super(ListRetirableGrantsResponse, self).__init__()

        self._grants = None
        self._next_marker = None
        self._truncated = None
        self.discriminator = None

        if grants is not None:
            self.grants = grants
        if next_marker is not None:
            self.next_marker = next_marker
        if truncated is not None:
            self.truncated = truncated

    @property
    def grants(self):
        """Gets the grants of this ListRetirableGrantsResponse.

        :return: The grants of this ListRetirableGrantsResponse.
        :rtype: list[:class:`cmcccloudsdkkms.v2.Grants`]
        """
        return self._grants

    @grants.setter
    def grants(self, grants):
        """Sets the grants of this ListRetirableGrantsResponse.

        :param grants: The grants of this ListRetirableGrantsResponse.
        :type grants: list[:class:`cmcccloudsdkkms.v2.Grants`]
        """
        self._grants = grants

    @property
    def next_marker(self):
        """Gets the next_marker of this ListRetirableGrantsResponse.

        :return: The next_marker of this ListRetirableGrantsResponse.
        :rtype: str
        """
        return self._next_marker

    @next_marker.setter
    def next_marker(self, next_marker):
        """Sets the next_marker of this ListRetirableGrantsResponse.

        :param next_marker: The next_marker of this ListRetirableGrantsResponse.
        :type next_marker: str
        """
        self._next_marker = next_marker

    @property
    def truncated(self):
        """Gets the truncated of this ListRetirableGrantsResponse.

        :return: The truncated of this ListRetirableGrantsResponse.
        :rtype: str
        """
        return self._truncated

    @truncated.setter
    def truncated(self, truncated):
        """Sets the truncated of this ListRetirableGrantsResponse.

        :param truncated: The truncated of this ListRetirableGrantsResponse.
        :type truncated: str
        """
        self._truncated = truncated

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
        if not isinstance(other, ListRetirableGrantsResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
