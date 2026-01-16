// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from my_interfaces:msg/Person.idl
// generated code does not contain a copyright notice

#ifndef MY_INTERFACES__MSG__DETAIL__PERSON__STRUCT_H_
#define MY_INTERFACES__MSG__DETAIL__PERSON__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'name'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/Person in the package my_interfaces.
typedef struct my_interfaces__msg__Person
{
  rosidl_runtime_c__String name;
  int32_t age;
  double height;
  bool is_student;
} my_interfaces__msg__Person;

// Struct for a sequence of my_interfaces__msg__Person.
typedef struct my_interfaces__msg__Person__Sequence
{
  my_interfaces__msg__Person * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} my_interfaces__msg__Person__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MY_INTERFACES__MSG__DETAIL__PERSON__STRUCT_H_
