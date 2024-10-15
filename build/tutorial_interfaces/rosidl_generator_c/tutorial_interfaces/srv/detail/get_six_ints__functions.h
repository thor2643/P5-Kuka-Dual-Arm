// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from tutorial_interfaces:srv/GetSixInts.idl
// generated code does not contain a copyright notice

#ifndef TUTORIAL_INTERFACES__SRV__DETAIL__GET_SIX_INTS__FUNCTIONS_H_
#define TUTORIAL_INTERFACES__SRV__DETAIL__GET_SIX_INTS__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "tutorial_interfaces/msg/rosidl_generator_c__visibility_control.h"

#include "tutorial_interfaces/srv/detail/get_six_ints__struct.h"

/// Initialize srv/GetSixInts message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * tutorial_interfaces__srv__GetSixInts_Request
 * )) before or use
 * tutorial_interfaces__srv__GetSixInts_Request__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_tutorial_interfaces
bool
tutorial_interfaces__srv__GetSixInts_Request__init(tutorial_interfaces__srv__GetSixInts_Request * msg);

/// Finalize srv/GetSixInts message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_tutorial_interfaces
void
tutorial_interfaces__srv__GetSixInts_Request__fini(tutorial_interfaces__srv__GetSixInts_Request * msg);

/// Create srv/GetSixInts message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * tutorial_interfaces__srv__GetSixInts_Request__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_tutorial_interfaces
tutorial_interfaces__srv__GetSixInts_Request *
tutorial_interfaces__srv__GetSixInts_Request__create();

/// Destroy srv/GetSixInts message.
/**
 * It calls
 * tutorial_interfaces__srv__GetSixInts_Request__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_tutorial_interfaces
void
tutorial_interfaces__srv__GetSixInts_Request__destroy(tutorial_interfaces__srv__GetSixInts_Request * msg);

/// Check for srv/GetSixInts message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_tutorial_interfaces
bool
tutorial_interfaces__srv__GetSixInts_Request__are_equal(const tutorial_interfaces__srv__GetSixInts_Request * lhs, const tutorial_interfaces__srv__GetSixInts_Request * rhs);

/// Copy a srv/GetSixInts message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_tutorial_interfaces
bool
tutorial_interfaces__srv__GetSixInts_Request__copy(
  const tutorial_interfaces__srv__GetSixInts_Request * input,
  tutorial_interfaces__srv__GetSixInts_Request * output);

/// Initialize array of srv/GetSixInts messages.
/**
 * It allocates the memory for the number of elements and calls
 * tutorial_interfaces__srv__GetSixInts_Request__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_tutorial_interfaces
bool
tutorial_interfaces__srv__GetSixInts_Request__Sequence__init(tutorial_interfaces__srv__GetSixInts_Request__Sequence * array, size_t size);

/// Finalize array of srv/GetSixInts messages.
/**
 * It calls
 * tutorial_interfaces__srv__GetSixInts_Request__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_tutorial_interfaces
void
tutorial_interfaces__srv__GetSixInts_Request__Sequence__fini(tutorial_interfaces__srv__GetSixInts_Request__Sequence * array);

/// Create array of srv/GetSixInts messages.
/**
 * It allocates the memory for the array and calls
 * tutorial_interfaces__srv__GetSixInts_Request__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_tutorial_interfaces
tutorial_interfaces__srv__GetSixInts_Request__Sequence *
tutorial_interfaces__srv__GetSixInts_Request__Sequence__create(size_t size);

/// Destroy array of srv/GetSixInts messages.
/**
 * It calls
 * tutorial_interfaces__srv__GetSixInts_Request__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_tutorial_interfaces
void
tutorial_interfaces__srv__GetSixInts_Request__Sequence__destroy(tutorial_interfaces__srv__GetSixInts_Request__Sequence * array);

/// Check for srv/GetSixInts message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_tutorial_interfaces
bool
tutorial_interfaces__srv__GetSixInts_Request__Sequence__are_equal(const tutorial_interfaces__srv__GetSixInts_Request__Sequence * lhs, const tutorial_interfaces__srv__GetSixInts_Request__Sequence * rhs);

/// Copy an array of srv/GetSixInts messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_tutorial_interfaces
bool
tutorial_interfaces__srv__GetSixInts_Request__Sequence__copy(
  const tutorial_interfaces__srv__GetSixInts_Request__Sequence * input,
  tutorial_interfaces__srv__GetSixInts_Request__Sequence * output);

/// Initialize srv/GetSixInts message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * tutorial_interfaces__srv__GetSixInts_Response
 * )) before or use
 * tutorial_interfaces__srv__GetSixInts_Response__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_tutorial_interfaces
bool
tutorial_interfaces__srv__GetSixInts_Response__init(tutorial_interfaces__srv__GetSixInts_Response * msg);

/// Finalize srv/GetSixInts message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_tutorial_interfaces
void
tutorial_interfaces__srv__GetSixInts_Response__fini(tutorial_interfaces__srv__GetSixInts_Response * msg);

/// Create srv/GetSixInts message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * tutorial_interfaces__srv__GetSixInts_Response__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_tutorial_interfaces
tutorial_interfaces__srv__GetSixInts_Response *
tutorial_interfaces__srv__GetSixInts_Response__create();

/// Destroy srv/GetSixInts message.
/**
 * It calls
 * tutorial_interfaces__srv__GetSixInts_Response__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_tutorial_interfaces
void
tutorial_interfaces__srv__GetSixInts_Response__destroy(tutorial_interfaces__srv__GetSixInts_Response * msg);

/// Check for srv/GetSixInts message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_tutorial_interfaces
bool
tutorial_interfaces__srv__GetSixInts_Response__are_equal(const tutorial_interfaces__srv__GetSixInts_Response * lhs, const tutorial_interfaces__srv__GetSixInts_Response * rhs);

/// Copy a srv/GetSixInts message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_tutorial_interfaces
bool
tutorial_interfaces__srv__GetSixInts_Response__copy(
  const tutorial_interfaces__srv__GetSixInts_Response * input,
  tutorial_interfaces__srv__GetSixInts_Response * output);

/// Initialize array of srv/GetSixInts messages.
/**
 * It allocates the memory for the number of elements and calls
 * tutorial_interfaces__srv__GetSixInts_Response__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_tutorial_interfaces
bool
tutorial_interfaces__srv__GetSixInts_Response__Sequence__init(tutorial_interfaces__srv__GetSixInts_Response__Sequence * array, size_t size);

/// Finalize array of srv/GetSixInts messages.
/**
 * It calls
 * tutorial_interfaces__srv__GetSixInts_Response__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_tutorial_interfaces
void
tutorial_interfaces__srv__GetSixInts_Response__Sequence__fini(tutorial_interfaces__srv__GetSixInts_Response__Sequence * array);

/// Create array of srv/GetSixInts messages.
/**
 * It allocates the memory for the array and calls
 * tutorial_interfaces__srv__GetSixInts_Response__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_tutorial_interfaces
tutorial_interfaces__srv__GetSixInts_Response__Sequence *
tutorial_interfaces__srv__GetSixInts_Response__Sequence__create(size_t size);

/// Destroy array of srv/GetSixInts messages.
/**
 * It calls
 * tutorial_interfaces__srv__GetSixInts_Response__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_tutorial_interfaces
void
tutorial_interfaces__srv__GetSixInts_Response__Sequence__destroy(tutorial_interfaces__srv__GetSixInts_Response__Sequence * array);

/// Check for srv/GetSixInts message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_tutorial_interfaces
bool
tutorial_interfaces__srv__GetSixInts_Response__Sequence__are_equal(const tutorial_interfaces__srv__GetSixInts_Response__Sequence * lhs, const tutorial_interfaces__srv__GetSixInts_Response__Sequence * rhs);

/// Copy an array of srv/GetSixInts messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_tutorial_interfaces
bool
tutorial_interfaces__srv__GetSixInts_Response__Sequence__copy(
  const tutorial_interfaces__srv__GetSixInts_Response__Sequence * input,
  tutorial_interfaces__srv__GetSixInts_Response__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // TUTORIAL_INTERFACES__SRV__DETAIL__GET_SIX_INTS__FUNCTIONS_H_
