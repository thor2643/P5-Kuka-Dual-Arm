// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from tutorial_interfaces:srv/GetSixInts.idl
// generated code does not contain a copyright notice

#ifndef TUTORIAL_INTERFACES__SRV__DETAIL__GET_SIX_INTS__BUILDER_HPP_
#define TUTORIAL_INTERFACES__SRV__DETAIL__GET_SIX_INTS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "tutorial_interfaces/srv/detail/get_six_ints__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace tutorial_interfaces
{

namespace srv
{

namespace builder
{

class Init_GetSixInts_Request_g
{
public:
  explicit Init_GetSixInts_Request_g(::tutorial_interfaces::srv::GetSixInts_Request & msg)
  : msg_(msg)
  {}
  ::tutorial_interfaces::srv::GetSixInts_Request g(::tutorial_interfaces::srv::GetSixInts_Request::_g_type arg)
  {
    msg_.g = std::move(arg);
    return std::move(msg_);
  }

private:
  ::tutorial_interfaces::srv::GetSixInts_Request msg_;
};

class Init_GetSixInts_Request_f
{
public:
  explicit Init_GetSixInts_Request_f(::tutorial_interfaces::srv::GetSixInts_Request & msg)
  : msg_(msg)
  {}
  Init_GetSixInts_Request_g f(::tutorial_interfaces::srv::GetSixInts_Request::_f_type arg)
  {
    msg_.f = std::move(arg);
    return Init_GetSixInts_Request_g(msg_);
  }

private:
  ::tutorial_interfaces::srv::GetSixInts_Request msg_;
};

class Init_GetSixInts_Request_e
{
public:
  explicit Init_GetSixInts_Request_e(::tutorial_interfaces::srv::GetSixInts_Request & msg)
  : msg_(msg)
  {}
  Init_GetSixInts_Request_f e(::tutorial_interfaces::srv::GetSixInts_Request::_e_type arg)
  {
    msg_.e = std::move(arg);
    return Init_GetSixInts_Request_f(msg_);
  }

private:
  ::tutorial_interfaces::srv::GetSixInts_Request msg_;
};

class Init_GetSixInts_Request_d
{
public:
  explicit Init_GetSixInts_Request_d(::tutorial_interfaces::srv::GetSixInts_Request & msg)
  : msg_(msg)
  {}
  Init_GetSixInts_Request_e d(::tutorial_interfaces::srv::GetSixInts_Request::_d_type arg)
  {
    msg_.d = std::move(arg);
    return Init_GetSixInts_Request_e(msg_);
  }

private:
  ::tutorial_interfaces::srv::GetSixInts_Request msg_;
};

class Init_GetSixInts_Request_c
{
public:
  explicit Init_GetSixInts_Request_c(::tutorial_interfaces::srv::GetSixInts_Request & msg)
  : msg_(msg)
  {}
  Init_GetSixInts_Request_d c(::tutorial_interfaces::srv::GetSixInts_Request::_c_type arg)
  {
    msg_.c = std::move(arg);
    return Init_GetSixInts_Request_d(msg_);
  }

private:
  ::tutorial_interfaces::srv::GetSixInts_Request msg_;
};

class Init_GetSixInts_Request_b
{
public:
  explicit Init_GetSixInts_Request_b(::tutorial_interfaces::srv::GetSixInts_Request & msg)
  : msg_(msg)
  {}
  Init_GetSixInts_Request_c b(::tutorial_interfaces::srv::GetSixInts_Request::_b_type arg)
  {
    msg_.b = std::move(arg);
    return Init_GetSixInts_Request_c(msg_);
  }

private:
  ::tutorial_interfaces::srv::GetSixInts_Request msg_;
};

class Init_GetSixInts_Request_a
{
public:
  Init_GetSixInts_Request_a()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GetSixInts_Request_b a(::tutorial_interfaces::srv::GetSixInts_Request::_a_type arg)
  {
    msg_.a = std::move(arg);
    return Init_GetSixInts_Request_b(msg_);
  }

private:
  ::tutorial_interfaces::srv::GetSixInts_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::tutorial_interfaces::srv::GetSixInts_Request>()
{
  return tutorial_interfaces::srv::builder::Init_GetSixInts_Request_a();
}

}  // namespace tutorial_interfaces


namespace tutorial_interfaces
{

namespace srv
{

namespace builder
{

class Init_GetSixInts_Response_succes
{
public:
  Init_GetSixInts_Response_succes()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::tutorial_interfaces::srv::GetSixInts_Response succes(::tutorial_interfaces::srv::GetSixInts_Response::_succes_type arg)
  {
    msg_.succes = std::move(arg);
    return std::move(msg_);
  }

private:
  ::tutorial_interfaces::srv::GetSixInts_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::tutorial_interfaces::srv::GetSixInts_Response>()
{
  return tutorial_interfaces::srv::builder::Init_GetSixInts_Response_succes();
}

}  // namespace tutorial_interfaces

#endif  // TUTORIAL_INTERFACES__SRV__DETAIL__GET_SIX_INTS__BUILDER_HPP_
