# coding: utf-8

import six

from cmcccloudsdkcore.utils.http_utils import sanitize_for_serialization


class ScheduleKeyDeletionRequestBody:

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
        'pending_days': 'str',
        'sequence': 'str'
    }

    attribute_map = {
        'key_id': 'key_id',
        'pending_days': 'pending_days',
        'sequence': 'sequence'
    }

    def __init__(self, key_id=None, pending_days=None, sequence=None):
        """ScheduleKeyDeletionRequestBody

        The model defined in cmcccloud sdk

        :param key_id: The param of the ScheduleKeyDeletionRequestBody
        :type key_id: str
        :param pending_days: The param of the ScheduleKeyDeletionRequestBody
        :type pending_days: str
        :param sequence: The param of the ScheduleKeyDeletionRequestBody
        :type sequence: str
        """
        
        

        self._key_id = None
        self._pending_days = None
        self._sequence = None
        self.discriminator = None

        self.key_id = key_id
        self.pending_days = pending_days
        if sequence is not None:
            self.sequence = sequence

    @property
    def key_id(self):
        """Gets the key_id of this ScheduleKeyDeletionRequestBody.

        :return: The key_id of this ScheduleKeyDeletionRequestBody.
        :rtype: str
        """
        return self._key_id

    @key_id.setter
    def key_id(self, key_id):
        """Sets the key_id of this ScheduleKeyDeletionRequestBody.

        :param key_id: The key_id of this ScheduleKeyDeletionRequestBody.
        :type key_id: str
        """
        self._key_id = key_id

    @property
    def pending_days(self):
        """Gets the pending_days of this ScheduleKeyDeletionRequestBody.

        :return: The pending_days of this ScheduleKeyDeletionRequestBody.
        :rtype: str
        """
        return self._pending_days

    @pending_days.setter
    def pending_days(self, pending_days):
        """Sets the pending_days of this ScheduleKeyDeletionRequestBody.

        :param pending_days: The pending_days of this ScheduleKeyDeletionRequestBody.
        :type pending_days: str
        """
        self._pending_days = pending_days

    @property
    def sequence(self):
        """Gets the sequence of this ScheduleKeyDeletionRequestBody.

        :return: The sequence of this ScheduleKeyDeletionRequestBody.
        :rtype: str
        """
        return self._sequence

    @sequence.setter
    def sequence(self, sequence):
        """Sets the sequence of this ScheduleKeyDeletionRequestBody.

        :param sequence: The sequence of this ScheduleKeyDeletionRequestBody.
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
        if not isinstance(other, ScheduleKeyDeletionRequestBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
