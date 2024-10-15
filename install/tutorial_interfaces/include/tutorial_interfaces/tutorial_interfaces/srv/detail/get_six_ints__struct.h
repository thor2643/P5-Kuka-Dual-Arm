// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from tutorial_interfaces:srv/GetSixInts.idl
// generated code does not contain a copyright notice

#ifndef TUTORIAL_INTERFACES__SRV__DETAIL__GET_SIX_INTS__STRUCT_H_
#define TUTORIAL_INTERFACES__SRV__DETAIL__GET_SIX_INTS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/GetSixInts in the package tutorial_interfaces.
typedef struct tutorial_interfaces__srv__GetSixInts_Request
{
  double a;
  double b;
  double c;
  double d;
  double e;
  double f;
  double g;
} tutorial_interfaces__srv__GetSixInts_Request;

// Struct for a sequence of tutorial_interfaces__srv__GetSixInts_Request.
typedef struct tutorial_interfaces__srv__GetSixInts_Request__Sequence
{
  tutorial_interfaces__srv__GetSixInts_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} tutorial_interfaces__srv__GetSixInts_Request__Sequence;


// Constants defined in the message

/// Struct defined in srv/GetSixInts in the package tutorial_interfaces.
typedef struct tutorial_interfaces__srv__GetSixInts_Response
{
  bool succes;
} tutorial_interfaces__srv__GetSixInts_Response;

// Struct for a sequence of tutorial_interfaces__srv__GetSixInts_Response.
typedef struct tutorial_interfaces__srv__GetSixInts_Response__Sequence
{
  tutorial_interfaces__srv__GetSixInts_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} tutorial_interfaces__srv__GetSixInts_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // TUTORIAL_INTERFACES__SRV__DETAIL__GET_SIX_INTS__STRUCT_H_
