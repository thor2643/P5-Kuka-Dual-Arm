// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from llm_interfaces:srv/TextToSpeech.idl
// generated code does not contain a copyright notice

#ifndef LLM_INTERFACES__SRV__DETAIL__TEXT_TO_SPEECH__BUILDER_HPP_
#define LLM_INTERFACES__SRV__DETAIL__TEXT_TO_SPEECH__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "llm_interfaces/srv/detail/text_to_speech__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace llm_interfaces
{

namespace srv
{

namespace builder
{

class Init_TextToSpeech_Request_text
{
public:
  Init_TextToSpeech_Request_text()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::llm_interfaces::srv::TextToSpeech_Request text(::llm_interfaces::srv::TextToSpeech_Request::_text_type arg)
  {
    msg_.text = std::move(arg);
    return std::move(msg_);
  }

private:
  ::llm_interfaces::srv::TextToSpeech_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::llm_interfaces::srv::TextToSpeech_Request>()
{
  return llm_interfaces::srv::builder::Init_TextToSpeech_Request_text();
}

}  // namespace llm_interfaces


namespace llm_interfaces
{

namespace srv
{

namespace builder
{

class Init_TextToSpeech_Response_success
{
public:
  Init_TextToSpeech_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::llm_interfaces::srv::TextToSpeech_Response success(::llm_interfaces::srv::TextToSpeech_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return std::move(msg_);
  }

private:
  ::llm_interfaces::srv::TextToSpeech_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::llm_interfaces::srv::TextToSpeech_Response>()
{
  return llm_interfaces::srv::builder::Init_TextToSpeech_Response_success();
}

}  // namespace llm_interfaces

#endif  // LLM_INTERFACES__SRV__DETAIL__TEXT_TO_SPEECH__BUILDER_HPP_
