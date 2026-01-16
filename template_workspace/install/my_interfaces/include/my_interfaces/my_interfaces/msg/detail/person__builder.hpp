// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from my_interfaces:msg/Person.idl
// generated code does not contain a copyright notice

#ifndef MY_INTERFACES__MSG__DETAIL__PERSON__BUILDER_HPP_
#define MY_INTERFACES__MSG__DETAIL__PERSON__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "my_interfaces/msg/detail/person__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace my_interfaces
{

namespace msg
{

namespace builder
{

class Init_Person_is_student
{
public:
  explicit Init_Person_is_student(::my_interfaces::msg::Person & msg)
  : msg_(msg)
  {}
  ::my_interfaces::msg::Person is_student(::my_interfaces::msg::Person::_is_student_type arg)
  {
    msg_.is_student = std::move(arg);
    return std::move(msg_);
  }

private:
  ::my_interfaces::msg::Person msg_;
};

class Init_Person_height
{
public:
  explicit Init_Person_height(::my_interfaces::msg::Person & msg)
  : msg_(msg)
  {}
  Init_Person_is_student height(::my_interfaces::msg::Person::_height_type arg)
  {
    msg_.height = std::move(arg);
    return Init_Person_is_student(msg_);
  }

private:
  ::my_interfaces::msg::Person msg_;
};

class Init_Person_age
{
public:
  explicit Init_Person_age(::my_interfaces::msg::Person & msg)
  : msg_(msg)
  {}
  Init_Person_height age(::my_interfaces::msg::Person::_age_type arg)
  {
    msg_.age = std::move(arg);
    return Init_Person_height(msg_);
  }

private:
  ::my_interfaces::msg::Person msg_;
};

class Init_Person_name
{
public:
  Init_Person_name()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Person_age name(::my_interfaces::msg::Person::_name_type arg)
  {
    msg_.name = std::move(arg);
    return Init_Person_age(msg_);
  }

private:
  ::my_interfaces::msg::Person msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::my_interfaces::msg::Person>()
{
  return my_interfaces::msg::builder::Init_Person_name();
}

}  // namespace my_interfaces

#endif  // MY_INTERFACES__MSG__DETAIL__PERSON__BUILDER_HPP_
