// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from llm_interfaces:srv/SpeechToText.idl
// generated code does not contain a copyright notice

#ifndef LLM_INTERFACES__SRV__DETAIL__SPEECH_TO_TEXT__STRUCT_HPP_
#define LLM_INTERFACES__SRV__DETAIL__SPEECH_TO_TEXT__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__llm_interfaces__srv__SpeechToText_Request __attribute__((deprecated))
#else
# define DEPRECATED__llm_interfaces__srv__SpeechToText_Request __declspec(deprecated)
#endif

namespace llm_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct SpeechToText_Request_
{
  using Type = SpeechToText_Request_<ContainerAllocator>;

  explicit SpeechToText_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->structure_needs_at_least_one_member = 0;
    }
  }

  explicit SpeechToText_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->structure_needs_at_least_one_member = 0;
    }
  }

  // field types and members
  using _structure_needs_at_least_one_member_type =
    uint8_t;
  _structure_needs_at_least_one_member_type structure_needs_at_least_one_member;


  // constant declarations

  // pointer types
  using RawPtr =
    llm_interfaces::srv::SpeechToText_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const llm_interfaces::srv::SpeechToText_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<llm_interfaces::srv::SpeechToText_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<llm_interfaces::srv::SpeechToText_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      llm_interfaces::srv::SpeechToText_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<llm_interfaces::srv::SpeechToText_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      llm_interfaces::srv::SpeechToText_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<llm_interfaces::srv::SpeechToText_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<llm_interfaces::srv::SpeechToText_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<llm_interfaces::srv::SpeechToText_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__llm_interfaces__srv__SpeechToText_Request
    std::shared_ptr<llm_interfaces::srv::SpeechToText_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__llm_interfaces__srv__SpeechToText_Request
    std::shared_ptr<llm_interfaces::srv::SpeechToText_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const SpeechToText_Request_ & other) const
  {
    if (this->structure_needs_at_least_one_member != other.structure_needs_at_least_one_member) {
      return false;
    }
    return true;
  }
  bool operator!=(const SpeechToText_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct SpeechToText_Request_

// alias to use template instance with default allocator
using SpeechToText_Request =
  llm_interfaces::srv::SpeechToText_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace llm_interfaces


#ifndef _WIN32
# define DEPRECATED__llm_interfaces__srv__SpeechToText_Response __attribute__((deprecated))
#else
# define DEPRECATED__llm_interfaces__srv__SpeechToText_Response __declspec(deprecated)
#endif

namespace llm_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct SpeechToText_Response_
{
  using Type = SpeechToText_Response_<ContainerAllocator>;

  explicit SpeechToText_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->transcript = "";
    }
  }

  explicit SpeechToText_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : transcript(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->transcript = "";
    }
  }

  // field types and members
  using _transcript_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _transcript_type transcript;

  // setters for named parameter idiom
  Type & set__transcript(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->transcript = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    llm_interfaces::srv::SpeechToText_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const llm_interfaces::srv::SpeechToText_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<llm_interfaces::srv::SpeechToText_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<llm_interfaces::srv::SpeechToText_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      llm_interfaces::srv::SpeechToText_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<llm_interfaces::srv::SpeechToText_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      llm_interfaces::srv::SpeechToText_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<llm_interfaces::srv::SpeechToText_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<llm_interfaces::srv::SpeechToText_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<llm_interfaces::srv::SpeechToText_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__llm_interfaces__srv__SpeechToText_Response
    std::shared_ptr<llm_interfaces::srv::SpeechToText_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__llm_interfaces__srv__SpeechToText_Response
    std::shared_ptr<llm_interfaces::srv::SpeechToText_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const SpeechToText_Response_ & other) const
  {
    if (this->transcript != other.transcript) {
      return false;
    }
    return true;
  }
  bool operator!=(const SpeechToText_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct SpeechToText_Response_

// alias to use template instance with default allocator
using SpeechToText_Response =
  llm_interfaces::srv::SpeechToText_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace llm_interfaces

namespace llm_interfaces
{

namespace srv
{

struct SpeechToText
{
  using Request = llm_interfaces::srv::SpeechToText_Request;
  using Response = llm_interfaces::srv::SpeechToText_Response;
};

}  // namespace srv

}  // namespace llm_interfaces

#endif  // LLM_INTERFACES__SRV__DETAIL__SPEECH_TO_TEXT__STRUCT_HPP_
