// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from llm_interfaces:srv/SpeechToText.idl
// generated code does not contain a copyright notice
#include "llm_interfaces/srv/detail/speech_to_text__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

bool
llm_interfaces__srv__SpeechToText_Request__init(llm_interfaces__srv__SpeechToText_Request * msg)
{
  if (!msg) {
    return false;
  }
  // structure_needs_at_least_one_member
  return true;
}

void
llm_interfaces__srv__SpeechToText_Request__fini(llm_interfaces__srv__SpeechToText_Request * msg)
{
  if (!msg) {
    return;
  }
  // structure_needs_at_least_one_member
}

bool
llm_interfaces__srv__SpeechToText_Request__are_equal(const llm_interfaces__srv__SpeechToText_Request * lhs, const llm_interfaces__srv__SpeechToText_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // structure_needs_at_least_one_member
  if (lhs->structure_needs_at_least_one_member != rhs->structure_needs_at_least_one_member) {
    return false;
  }
  return true;
}

bool
llm_interfaces__srv__SpeechToText_Request__copy(
  const llm_interfaces__srv__SpeechToText_Request * input,
  llm_interfaces__srv__SpeechToText_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // structure_needs_at_least_one_member
  output->structure_needs_at_least_one_member = input->structure_needs_at_least_one_member;
  return true;
}

llm_interfaces__srv__SpeechToText_Request *
llm_interfaces__srv__SpeechToText_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  llm_interfaces__srv__SpeechToText_Request * msg = (llm_interfaces__srv__SpeechToText_Request *)allocator.allocate(sizeof(llm_interfaces__srv__SpeechToText_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(llm_interfaces__srv__SpeechToText_Request));
  bool success = llm_interfaces__srv__SpeechToText_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
llm_interfaces__srv__SpeechToText_Request__destroy(llm_interfaces__srv__SpeechToText_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    llm_interfaces__srv__SpeechToText_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
llm_interfaces__srv__SpeechToText_Request__Sequence__init(llm_interfaces__srv__SpeechToText_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  llm_interfaces__srv__SpeechToText_Request * data = NULL;

  if (size) {
    data = (llm_interfaces__srv__SpeechToText_Request *)allocator.zero_allocate(size, sizeof(llm_interfaces__srv__SpeechToText_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = llm_interfaces__srv__SpeechToText_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        llm_interfaces__srv__SpeechToText_Request__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
llm_interfaces__srv__SpeechToText_Request__Sequence__fini(llm_interfaces__srv__SpeechToText_Request__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      llm_interfaces__srv__SpeechToText_Request__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

llm_interfaces__srv__SpeechToText_Request__Sequence *
llm_interfaces__srv__SpeechToText_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  llm_interfaces__srv__SpeechToText_Request__Sequence * array = (llm_interfaces__srv__SpeechToText_Request__Sequence *)allocator.allocate(sizeof(llm_interfaces__srv__SpeechToText_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = llm_interfaces__srv__SpeechToText_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
llm_interfaces__srv__SpeechToText_Request__Sequence__destroy(llm_interfaces__srv__SpeechToText_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    llm_interfaces__srv__SpeechToText_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
llm_interfaces__srv__SpeechToText_Request__Sequence__are_equal(const llm_interfaces__srv__SpeechToText_Request__Sequence * lhs, const llm_interfaces__srv__SpeechToText_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!llm_interfaces__srv__SpeechToText_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
llm_interfaces__srv__SpeechToText_Request__Sequence__copy(
  const llm_interfaces__srv__SpeechToText_Request__Sequence * input,
  llm_interfaces__srv__SpeechToText_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(llm_interfaces__srv__SpeechToText_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    llm_interfaces__srv__SpeechToText_Request * data =
      (llm_interfaces__srv__SpeechToText_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!llm_interfaces__srv__SpeechToText_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          llm_interfaces__srv__SpeechToText_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!llm_interfaces__srv__SpeechToText_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `transcript`
#include "rosidl_runtime_c/string_functions.h"

bool
llm_interfaces__srv__SpeechToText_Response__init(llm_interfaces__srv__SpeechToText_Response * msg)
{
  if (!msg) {
    return false;
  }
  // transcript
  if (!rosidl_runtime_c__String__init(&msg->transcript)) {
    llm_interfaces__srv__SpeechToText_Response__fini(msg);
    return false;
  }
  return true;
}

void
llm_interfaces__srv__SpeechToText_Response__fini(llm_interfaces__srv__SpeechToText_Response * msg)
{
  if (!msg) {
    return;
  }
  // transcript
  rosidl_runtime_c__String__fini(&msg->transcript);
}

bool
llm_interfaces__srv__SpeechToText_Response__are_equal(const llm_interfaces__srv__SpeechToText_Response * lhs, const llm_interfaces__srv__SpeechToText_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // transcript
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->transcript), &(rhs->transcript)))
  {
    return false;
  }
  return true;
}

bool
llm_interfaces__srv__SpeechToText_Response__copy(
  const llm_interfaces__srv__SpeechToText_Response * input,
  llm_interfaces__srv__SpeechToText_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // transcript
  if (!rosidl_runtime_c__String__copy(
      &(input->transcript), &(output->transcript)))
  {
    return false;
  }
  return true;
}

llm_interfaces__srv__SpeechToText_Response *
llm_interfaces__srv__SpeechToText_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  llm_interfaces__srv__SpeechToText_Response * msg = (llm_interfaces__srv__SpeechToText_Response *)allocator.allocate(sizeof(llm_interfaces__srv__SpeechToText_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(llm_interfaces__srv__SpeechToText_Response));
  bool success = llm_interfaces__srv__SpeechToText_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
llm_interfaces__srv__SpeechToText_Response__destroy(llm_interfaces__srv__SpeechToText_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    llm_interfaces__srv__SpeechToText_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
llm_interfaces__srv__SpeechToText_Response__Sequence__init(llm_interfaces__srv__SpeechToText_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  llm_interfaces__srv__SpeechToText_Response * data = NULL;

  if (size) {
    data = (llm_interfaces__srv__SpeechToText_Response *)allocator.zero_allocate(size, sizeof(llm_interfaces__srv__SpeechToText_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = llm_interfaces__srv__SpeechToText_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        llm_interfaces__srv__SpeechToText_Response__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
llm_interfaces__srv__SpeechToText_Response__Sequence__fini(llm_interfaces__srv__SpeechToText_Response__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      llm_interfaces__srv__SpeechToText_Response__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

llm_interfaces__srv__SpeechToText_Response__Sequence *
llm_interfaces__srv__SpeechToText_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  llm_interfaces__srv__SpeechToText_Response__Sequence * array = (llm_interfaces__srv__SpeechToText_Response__Sequence *)allocator.allocate(sizeof(llm_interfaces__srv__SpeechToText_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = llm_interfaces__srv__SpeechToText_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
llm_interfaces__srv__SpeechToText_Response__Sequence__destroy(llm_interfaces__srv__SpeechToText_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    llm_interfaces__srv__SpeechToText_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
llm_interfaces__srv__SpeechToText_Response__Sequence__are_equal(const llm_interfaces__srv__SpeechToText_Response__Sequence * lhs, const llm_interfaces__srv__SpeechToText_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!llm_interfaces__srv__SpeechToText_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
llm_interfaces__srv__SpeechToText_Response__Sequence__copy(
  const llm_interfaces__srv__SpeechToText_Response__Sequence * input,
  llm_interfaces__srv__SpeechToText_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(llm_interfaces__srv__SpeechToText_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    llm_interfaces__srv__SpeechToText_Response * data =
      (llm_interfaces__srv__SpeechToText_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!llm_interfaces__srv__SpeechToText_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          llm_interfaces__srv__SpeechToText_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!llm_interfaces__srv__SpeechToText_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
