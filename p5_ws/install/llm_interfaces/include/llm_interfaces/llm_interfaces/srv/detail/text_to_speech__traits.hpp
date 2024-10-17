// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from llm_interfaces:srv/TextToSpeech.idl
// generated code does not contain a copyright notice

#ifndef LLM_INTERFACES__SRV__DETAIL__TEXT_TO_SPEECH__TRAITS_HPP_
#define LLM_INTERFACES__SRV__DETAIL__TEXT_TO_SPEECH__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "llm_interfaces/srv/detail/text_to_speech__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace llm_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const TextToSpeech_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: text
  {
    out << "text: ";
    rosidl_generator_traits::value_to_yaml(msg.text, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const TextToSpeech_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: text
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "text: ";
    rosidl_generator_traits::value_to_yaml(msg.text, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const TextToSpeech_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace llm_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use llm_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const llm_interfaces::srv::TextToSpeech_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  llm_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use llm_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const llm_interfaces::srv::TextToSpeech_Request & msg)
{
  return llm_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<llm_interfaces::srv::TextToSpeech_Request>()
{
  return "llm_interfaces::srv::TextToSpeech_Request";
}

template<>
inline const char * name<llm_interfaces::srv::TextToSpeech_Request>()
{
  return "llm_interfaces/srv/TextToSpeech_Request";
}

template<>
struct has_fixed_size<llm_interfaces::srv::TextToSpeech_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<llm_interfaces::srv::TextToSpeech_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<llm_interfaces::srv::TextToSpeech_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace llm_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const TextToSpeech_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const TextToSpeech_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const TextToSpeech_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace llm_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use llm_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const llm_interfaces::srv::TextToSpeech_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  llm_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use llm_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const llm_interfaces::srv::TextToSpeech_Response & msg)
{
  return llm_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<llm_interfaces::srv::TextToSpeech_Response>()
{
  return "llm_interfaces::srv::TextToSpeech_Response";
}

template<>
inline const char * name<llm_interfaces::srv::TextToSpeech_Response>()
{
  return "llm_interfaces/srv/TextToSpeech_Response";
}

template<>
struct has_fixed_size<llm_interfaces::srv::TextToSpeech_Response>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<llm_interfaces::srv::TextToSpeech_Response>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<llm_interfaces::srv::TextToSpeech_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<llm_interfaces::srv::TextToSpeech>()
{
  return "llm_interfaces::srv::TextToSpeech";
}

template<>
inline const char * name<llm_interfaces::srv::TextToSpeech>()
{
  return "llm_interfaces/srv/TextToSpeech";
}

template<>
struct has_fixed_size<llm_interfaces::srv::TextToSpeech>
  : std::integral_constant<
    bool,
    has_fixed_size<llm_interfaces::srv::TextToSpeech_Request>::value &&
    has_fixed_size<llm_interfaces::srv::TextToSpeech_Response>::value
  >
{
};

template<>
struct has_bounded_size<llm_interfaces::srv::TextToSpeech>
  : std::integral_constant<
    bool,
    has_bounded_size<llm_interfaces::srv::TextToSpeech_Request>::value &&
    has_bounded_size<llm_interfaces::srv::TextToSpeech_Response>::value
  >
{
};

template<>
struct is_service<llm_interfaces::srv::TextToSpeech>
  : std::true_type
{
};

template<>
struct is_service_request<llm_interfaces::srv::TextToSpeech_Request>
  : std::true_type
{
};

template<>
struct is_service_response<llm_interfaces::srv::TextToSpeech_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // LLM_INTERFACES__SRV__DETAIL__TEXT_TO_SPEECH__TRAITS_HPP_
