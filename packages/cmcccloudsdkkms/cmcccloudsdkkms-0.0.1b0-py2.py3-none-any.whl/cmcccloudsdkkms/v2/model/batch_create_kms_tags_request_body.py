# coding: utf-8

import six

from cmcccloudsdkcore.utils.http_utils import sanitize_for_serialization


class BatchCreateKmsTagsRequestBody:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'tags': 'list[TagItem]',
        'action': 'str',
        'sequence': 'str'
    }

    attribute_map = {
        'tags': 'tags',
        'action': 'action',
        'sequence': 'sequence'
    }

    def __init__(self, tags=None, action=None, sequence=None):
        """BatchCreateKmsTagsRequestBody

        The model defined in cmcccloud sdk

        :param tags: The param of the BatchCreateKmsTagsRequestBody
        :type tags: list[:class:`cmcccloudsdkkms.v2.TagItem`]
        :param action: The param of the BatchCreateKmsTagsRequestBody
        :type action: str
        :param sequence: The param of the BatchCreateKmsTagsRequestBody
        :type sequence: str
        """
        
        

        self._tags = None
        self._action = None
        self._sequence = None
        self.discriminator = None

        if tags is not None:
            self.tags = tags
        if action is not None:
            self.action = action
        if sequence is not None:
            self.sequence = sequence

    @property
    def tags(self):
        """Gets the tags of this BatchCreateKmsTagsRequestBody.

        :return: The tags of this BatchCreateKmsTagsRequestBody.
        :rtype: list[:class:`cmcccloudsdkkms.v2.TagItem`]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this BatchCreateKmsTagsRequestBody.

        :param tags: The tags of this BatchCreateKmsTagsRequestBody.
        :type tags: list[:class:`cmcccloudsdkkms.v2.TagItem`]
        """
        self._tags = tags

    @property
    def action(self):
        """Gets the action of this BatchCreateKmsTagsRequestBody.

        :return: The action of this BatchCreateKmsTagsRequestBody.
        :rtype: str
        """
        return self._action

    @action.setter
    def action(self, action):
        """Sets the action of this BatchCreateKmsTagsRequestBody.

        :param action: The action of this BatchCreateKmsTagsRequestBody.
        :type action: str
        """
        self._action = action

    @property
    def sequence(self):
        """Gets the sequence of this BatchCreateKmsTagsRequestBody.

        :return: The sequence of this BatchCreateKmsTagsRequestBody.
        :rtype: str
        """
        return self._sequence

    @sequence.setter
    def sequence(self, sequence):
        """Sets the sequence of this BatchCreateKmsTagsRequestBody.

        :param sequence: The sequence of this BatchCreateKmsTagsRequestBody.
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
        if not isinstance(other, BatchCreateKmsTagsRequestBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
