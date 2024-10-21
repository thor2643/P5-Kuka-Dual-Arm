// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from llm_interfaces:srv/SpeechToText.idl
// generated code does not contain a copyright notice

#ifndef LLM_INTERFACES__SRV__DETAIL__SPEECH_TO_TEXT__BUILDER_HPP_
#define LLM_INTERFACES__SRV__DETAIL__SPEECH_TO_TEXT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "llm_interfaces/srv/detail/speech_to_text__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace llm_interfaces
{

namespace srv
{


}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::llm_interfaces::srv::SpeechToText_Request>()
{
  return ::llm_interfaces::srv::SpeechToText_Request(rosidl_runtime_cpp::MessageInitialization::ZERO);
}

}  // namespace llm_interfaces


namespace llm_interfaces
{

namespace srv
{

namespace builder
{

class Init_SpeechToText_Response_transcript
{
public:
  Init_SpeechToText_Response_transcript()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::llm_interfaces::srv::SpeechToText_Response transcript(::llm_interfaces::srv::SpeechToText_Response::_transcript_type arg)
  {
    msg_.transcript = std::move(arg);
    return std::move(msg_);
  }

private:
  ::llm_interfaces::srv::SpeechToText_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::llm_interfaces::srv::SpeechToText_Response>()
{
  return llm_interfaces::srv::builder::Init_SpeechToText_Response_transcript();
}

}  // namespace llm_interfaces

#endif  // LLM_INTERFACES__SRV__DETAIL__SPEECH_TO_TEXT__BUILDER_HPP_
