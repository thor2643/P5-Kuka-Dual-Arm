# generated from rosidl_generator_py/resource/_idl.py.em
# with input from moveit_msgs:srv/SetPlannerParams.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_SetPlannerParams_Request(type):
    """Metaclass of message 'SetPlannerParams_Request'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('moveit_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'moveit_msgs.srv.SetPlannerParams_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__set_planner_params__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__set_planner_params__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__set_planner_params__request
            cls._TYPE_SUPPORT = module.type_support_msg__srv__set_planner_params__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__set_planner_params__request

            from moveit_msgs.msg import PlannerParams
            if PlannerParams.__class__._TYPE_SUPPORT is None:
                PlannerParams.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class SetPlannerParams_Request(metaclass=Metaclass_SetPlannerParams_Request):
    """Message class 'SetPlannerParams_Request'."""

    __slots__ = [
        '_pipeline_id',
        '_planner_config',
        '_group',
        '_params',
        '_replace',
    ]

    _fields_and_field_types = {
        'pipeline_id': 'string',
        'planner_config': 'string',
        'group': 'string',
        'params': 'moveit_msgs/PlannerParams',
        'replace': 'boolean',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['moveit_msgs', 'msg'], 'PlannerParams'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.pipeline_id = kwargs.get('pipeline_id', str())
        self.planner_config = kwargs.get('planner_config', str())
        self.group = kwargs.get('group', str())
        from moveit_msgs.msg import PlannerParams
        self.params = kwargs.get('params', PlannerParams())
        self.replace = kwargs.get('replace', bool())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.pipeline_id != other.pipeline_id:
            return False
        if self.planner_config != other.planner_config:
            return False
        if self.group != other.group:
            return False
        if self.params != other.params:
            return False
        if self.replace != other.replace:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def pipeline_id(self):
        """Message field 'pipeline_id'."""
        return self._pipeline_id

    @pipeline_id.setter
    def pipeline_id(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'pipeline_id' field must be of type 'str'"
        self._pipeline_id = value

    @builtins.property
    def planner_config(self):
        """Message field 'planner_config'."""
        return self._planner_config

    @planner_config.setter
    def planner_config(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'planner_config' field must be of type 'str'"
        self._planner_config = value

    @builtins.property
    def group(self):
        """Message field 'group'."""
        return self._group

    @group.setter
    def group(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'group' field must be of type 'str'"
        self._group = value

    @builtins.property
    def params(self):
        """Message field 'params'."""
        return self._params

    @params.setter
    def params(self, value):
        if __debug__:
            from moveit_msgs.msg import PlannerParams
            assert \
                isinstance(value, PlannerParams), \
                "The 'params' field must be a sub message of type 'PlannerParams'"
        self._params = value

    @builtins.property
    def replace(self):
        """Message field 'replace'."""
        return self._replace

    @replace.setter
    def replace(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'replace' field must be of type 'bool'"
        self._replace = value


# Import statements for member types

# already imported above
# import rosidl_parser.definition


class Metaclass_SetPlannerParams_Response(type):
    """Metaclass of message 'SetPlannerParams_Response'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('moveit_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'moveit_msgs.srv.SetPlannerParams_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__set_planner_params__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__set_planner_params__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__set_planner_params__response
            cls._TYPE_SUPPORT = module.type_support_msg__srv__set_planner_params__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__set_planner_params__response

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class SetPlannerParams_Response(metaclass=Metaclass_SetPlannerParams_Response):
    """Message class 'SetPlannerParams_Response'."""

    __slots__ = [
    ]

    _fields_and_field_types = {
    }

    SLOT_TYPES = (
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)


class Metaclass_SetPlannerParams(type):
    """Metaclass of service 'SetPlannerParams'."""

    _TYPE_SUPPORT = None

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('moveit_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'moveit_msgs.srv.SetPlannerParams')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__srv__set_planner_params

            from moveit_msgs.srv import _set_planner_params
            if _set_planner_params.Metaclass_SetPlannerParams_Request._TYPE_SUPPORT is None:
                _set_planner_params.Metaclass_SetPlannerParams_Request.__import_type_support__()
            if _set_planner_params.Metaclass_SetPlannerParams_Response._TYPE_SUPPORT is None:
                _set_planner_params.Metaclass_SetPlannerParams_Response.__import_type_support__()


class SetPlannerParams(metaclass=Metaclass_SetPlannerParams):
    from moveit_msgs.srv._set_planner_params import SetPlannerParams_Request as Request
    from moveit_msgs.srv._set_planner_params import SetPlannerParams_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')
