// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from llm_interfaces:srv/SpeechToText.idl
// generated code does not contain a copyright notice

#ifndef LLM_INTERFACES__SRV__DETAIL__SPEECH_TO_TEXT__STRUCT_H_
#define LLM_INTERFACES__SRV__DETAIL__SPEECH_TO_TEXT__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/SpeechToText in the package llm_interfaces.
typedef struct llm_interfaces__srv__SpeechToText_Request
{
  uint8_t structure_needs_at_least_one_member;
} llm_interfaces__srv__SpeechToText_Request;

// Struct for a sequence of llm_interfaces__srv__SpeechToText_Request.
typedef struct llm_interfaces__srv__SpeechToText_Request__Sequence
{
  llm_interfaces__srv__SpeechToText_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} llm_interfaces__srv__SpeechToText_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'transcript'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/SpeechToText in the package llm_interfaces.
typedef struct llm_interfaces__srv__SpeechToText_Response
{
  rosidl_runtime_c__String transcript;
} llm_interfaces__srv__SpeechToText_Response;

// Struct for a sequence of llm_interfaces__srv__SpeechToText_Response.
typedef struct llm_interfaces__srv__SpeechToText_Response__Sequence
{
  llm_interfaces__srv__SpeechToText_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} llm_interfaces__srv__SpeechToText_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // LLM_INTERFACES__SRV__DETAIL__SPEECH_TO_TEXT__STRUCT_H_
