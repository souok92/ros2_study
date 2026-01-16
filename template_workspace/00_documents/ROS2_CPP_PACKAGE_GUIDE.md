# ROS2 C++ 패키지 생성 완벽 가이드

이 가이드는 ROS2 C++ 패키지를 처음부터 올바르게 생성하는 방법을 단계별로 설명합니다.

---

## Python vs C++ 패키지 주요 차이점

| 항목 | Python 패키지 | C++ 패키지 |
|------|--------------|-----------|
| **빌드 타입** | `ament_python` | `ament_cmake` |
| **빌드 설정 파일** | `setup.py` | `CMakeLists.txt` |
| **소스 위치** | `<pkg_name>/*.py` | `src/*.cpp`, `include/<pkg_name>/*.hpp` |
| **컴파일 필요** | ❌ (인터프리터) | ✅ (컴파일 언어) |
| **빌드 속도** | 빠름 (복사만) | 느림 (컴파일) |
| **수정 후 재빌드** | 불필요 (symlink 사용 시) | **항상 필요** |
| **실행 성능** | 느림 | 빠름 |
| **주 사용처** | AI/ML, 프로토타입 | 실시간 제어, 센서 처리 |

---

## ROS2 C++ 패키지 개발 순서

### 1. 패키지 골격 생성 (`ros2 pkg create`)
- **목적**: CMake 기반 패키지 구조 자동 생성
- **생성되는 것**: CMakeLists.txt, package.xml, include/, src/, 기본 노드 파일
- **왜 먼저?**: C++ 빌드 시스템 설정이 복잡하므로 자동 생성이 안전

### 2. 코드 작성 및 파일 추가
- **목적**: 실제 로봇 기능 구현
- **작업**: .cpp 파일 작성, .hpp 헤더 작성, launch/config 파일 추가
- **주의**: 헤더는 `include/<package_name>/`, 소스는 `src/`에 작성

### 3. CMakeLists.txt 수정
- **목적**: 새로 추가한 파일들을 빌드 시스템에 등록
- **작업**:
  - `find_package()`로 의존성 선언
  - `add_executable()`로 실행 파일 등록
  - `ament_target_dependencies()`로 링크
  - `install()`로 설치 위치 지정
- **중요**: 등록하지 않으면 컴파일조차 안 됨!

### 4. 빌드 및 테스트
- **목적**: 작성한 코드를 컴파일하고 실행 파일 생성
- **작업**: `colcon build`, `source install/setup.bash`, 실행 및 테스트
- **반복**: 코드 수정 → **재컴파일** → 재테스트 (매번 필요!)

---

## 1단계: 기본 패키지 생성

**이 단계의 목적**: ROS2가 인식할 수 있는 C++ 패키지 구조를 자동으로 생성합니다.

**왜 이 명령어를 사용하나?**
- CMakeLists.txt 설정이 복잡해서 수동 작성 시 실수하기 쉬움
- `ros2 pkg create`는 CMake 템플릿을 자동 생성
- 컴파일러 옵션, 링커 설정 등을 자동으로 구성
- 추후에는 `CMakeLists.txt`, `package.xml` 수정 후 `colcon build`로 업데이트

### 명령어:
```bash
cd <workspace_path>/src
ros2 pkg create --build-type ament_cmake <package_name> \
  --dependencies <dependencies> \
  --node-name <node_name> \
  --maintainer-name "<maintainer_name>" \
  --maintainer-email "<maintainer_email>" \
  --license <license>
```

### 예시:
```bash
cd ~/10_delto_ws/src
ros2 pkg create --build-type ament_cmake my_robot_cpp \
  --dependencies rclcpp std_msgs sensor_msgs geometry_msgs \
  --node-name my_node \
  --maintainer-name "Your Name" \
  --maintainer-email "your@email.com" \
  --license Apache-2.0
```

### 생성되는 폴더 구조:
```
my_robot_cpp/
├── include/
│   └── my_robot_cpp/           # 헤더 파일 (.hpp) 위치
├── src/
│   └── my_node.cpp             # --node-name으로 생성된 소스
├── CMakeLists.txt              # 빌드 설정 (Python의 setup.py 역할)
└── package.xml
```

**Python과 다른 점:**
- ❌ `setup.py`, `setup.cfg` 없음
- ❌ `resource/` 폴더 없음
- ❌ `test/` 폴더 자동 생성 안 됨 (필요 시 수동 생성)
- ✅ `include/` 폴더 생성 (헤더 파일용)
- ✅ `CMakeLists.txt` 사용

### 생성된 파일 내용 예시:

#### `src/my_node.cpp`:
```cpp
#include <memory>
#include "rclcpp/rclcpp.hpp"

class MyNode : public rclcpp::Node
{
public:
  MyNode() : Node("my_node")
  {
    RCLCPP_INFO(this->get_logger(), "Hello from my_node!");
  }
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<MyNode>());
  rclcpp::shutdown();
  return 0;
}
```

#### `CMakeLists.txt` (기본 생성 버전):
```cmake
cmake_minimum_required(VERSION 3.8)
project(my_robot_cpp)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# 의존성 찾기
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)

# 실행 파일 생성
add_executable(my_node src/my_node.cpp)
ament_target_dependencies(my_node
  rclcpp
  std_msgs
  sensor_msgs
  geometry_msgs
)

# 설치 위치 지정
install(TARGETS
  my_node
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
```

#### `package.xml`:
```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>my_robot_cpp</name>
  <version>0.0.0</version>
  <description>TODO: Package description</description>
  <maintainer email="your@email.com">Your Name</maintainer>
  <license>Apache-2.0</license>

  <buildtool_depend>ament_cmake</buildtool_depend>

  <depend>rclcpp</depend>
  <depend>std_msgs</depend>
  <depend>sensor_msgs</depend>
  <depend>geometry_msgs</depend>

  <export>
    <build_type>ament_cmake</build_type>
  </export>
</package>
```

---

## 2단계: 추가 노드 파일 작성

**이 단계의 목적**: 여러 기능을 담은 노드들을 추가합니다.

**C++에서 코드 작성 방식:**
1. **헤더 파일 (.hpp)**: 클래스 선언 → `include/<package_name>/`
2. **소스 파일 (.cpp)**: 구현 → `src/`

### 방법 1: 단일 파일 노드 (간단한 노드)

```bash
cd <workspace_path>/src/<package_name>/src
touch publisher_node.cpp
touch subscriber_node.cpp
```

#### `src/publisher_node.cpp`:
```cpp
#include <chrono>
#include <memory>
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using namespace std::chrono_literals;

class PublisherNode : public rclcpp::Node
{
public:
  PublisherNode() : Node("publisher_node")
  {
    publisher_ = this->create_publisher<std_msgs::msg::String>("topic", 10);
    timer_ = this->create_wall_timer(
      500ms, std::bind(&PublisherNode::timer_callback, this));
  }

private:
  void timer_callback()
  {
    auto message = std_msgs::msg::String();
    message.data = "Hello, ROS2!";
    publisher_->publish(message);
  }

  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
  rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<PublisherNode>());
  rclcpp::shutdown();
  return 0;
}
```

### 방법 2: 헤더 + 소스 분리 (복잡한 노드)

```bash
# 헤더 파일
cd <workspace_path>/src/<package_name>/include/<package_name>
touch robot_controller.hpp

# 소스 파일
cd <workspace_path>/src/<package_name>/src
touch robot_controller.cpp
touch robot_controller_node.cpp
```

#### `include/<package_name>/robot_controller.hpp`:
```cpp
#ifndef MY_ROBOT_CPP__ROBOT_CONTROLLER_HPP_
#define MY_ROBOT_CPP__ROBOT_CONTROLLER_HPP_

#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"

namespace my_robot_cpp
{

class RobotController : public rclcpp::Node
{
public:
  RobotController();
  ~RobotController();

private:
  void control_loop();

  rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr cmd_vel_pub_;
  rclcpp::TimerBase::SharedPtr timer_;
};

}  // namespace my_robot_cpp

#endif  // MY_ROBOT_CPP__ROBOT_CONTROLLER_HPP_
```

#### `src/robot_controller.cpp`:
```cpp
#include "my_robot_cpp/robot_controller.hpp"

namespace my_robot_cpp
{

RobotController::RobotController() : Node("robot_controller")
{
  cmd_vel_pub_ = this->create_publisher<geometry_msgs::msg::Twist>("cmd_vel", 10);
  timer_ = this->create_wall_timer(
    std::chrono::milliseconds(100),
    std::bind(&RobotController::control_loop, this));
}

RobotController::~RobotController() {}

void RobotController::control_loop()
{
  auto msg = geometry_msgs::msg::Twist();
  msg.linear.x = 0.5;
  msg.angular.z = 0.0;
  cmd_vel_pub_->publish(msg);
}

}  // namespace my_robot_cpp
```

#### `src/robot_controller_node.cpp`:
```cpp
#include "my_robot_cpp/robot_controller.hpp"

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<my_robot_cpp::RobotController>());
  rclcpp::shutdown();
  return 0;
}
```

### CMakeLists.txt에 새 노드 등록:

```cmake
# 의존성은 이미 선언되어 있음 (1단계에서)

# 단일 파일 노드
add_executable(publisher_node src/publisher_node.cpp)
ament_target_dependencies(publisher_node rclcpp std_msgs)

add_executable(subscriber_node src/subscriber_node.cpp)
ament_target_dependencies(subscriber_node rclcpp std_msgs)

# 헤더+소스 분리 노드
add_executable(robot_controller_node
  src/robot_controller.cpp
  src/robot_controller_node.cpp
)
ament_target_dependencies(robot_controller_node rclcpp geometry_msgs)

# include 디렉토리 지정 (헤더 파일 사용 시 필수!)
target_include_directories(robot_controller_node PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
)

# 설치 (모든 실행 파일 추가)
install(TARGETS
  my_node
  publisher_node
  subscriber_node
  robot_controller_node
  DESTINATION lib/${PROJECT_NAME}
)
```

### 폴더 구조:
```
my_robot_cpp/
├── include/
│   └── my_robot_cpp/
│       └── robot_controller.hpp    # 헤더 파일
├── src/
│   ├── my_node.cpp
│   ├── publisher_node.cpp          # 단일 파일 노드
│   ├── subscriber_node.cpp
│   ├── robot_controller.cpp        # 구현
│   └── robot_controller_node.cpp   # main 함수
├── CMakeLists.txt
└── package.xml
```

---

## 3단계: Launch 파일 추가

**이 단계의 목적**: 여러 노드를 한 번에 실행하고 설정을 관리합니다.

**Python 패키지와 동일하지만, CMakeLists.txt 설정이 다릅니다.**

### Launch 디렉토리 생성:
```bash
cd <workspace_path>/src/<package_name>
mkdir launch
touch launch/robot.launch.py
```

### `launch/robot.launch.py`:
```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='my_robot_cpp',
            executable='publisher_node',
            name='publisher',
            output='screen',
        ),
        Node(
            package='my_robot_cpp',
            executable='subscriber_node',
            name='subscriber',
            output='screen',
        ),
        Node(
            package='my_robot_cpp',
            executable='robot_controller_node',
            name='robot_controller',
            output='screen',
        ),
    ])
```

### CMakeLists.txt에 launch 파일 등록:

```cmake
# launch 파일 설치
install(DIRECTORY
  launch
  DESTINATION share/${PROJECT_NAME}
)
```

**Python과의 차이:**
- Python: `glob('launch/*.launch.py')` 사용
- C++: `install(DIRECTORY launch ...)` 사용

---

## 4단계: Config 파일 추가

**Python 패키지와 동일합니다.**

### Config 디렉토리 생성:
```bash
cd <workspace_path>/src/<package_name>
mkdir config
touch config/params.yaml
```

### `config/params.yaml`:
```yaml
robot_controller:
  ros__parameters:
    linear_speed: 0.5
    angular_speed: 0.0
    control_frequency: 10.0
```

### CMakeLists.txt에 config 파일 등록:

```cmake
# config 파일 설치
install(DIRECTORY
  config
  DESTINATION share/${PROJECT_NAME}
)
```

---

## 5단계: 라이브러리 생성 (선택사항)

**이 단계의 목적**: 여러 노드에서 공유하는 코드를 라이브러리로 만듭니다.

**언제 필요한가?**
- 여러 노드에서 같은 클래스/함수를 사용할 때
- 다른 패키지에서 이 패키지의 코드를 사용하게 할 때
- 코드 재사용성을 높이고 싶을 때

### 예시: 유틸리티 라이브러리

#### `include/<package_name>/utils.hpp`:
```cpp
#ifndef MY_ROBOT_CPP__UTILS_HPP_
#define MY_ROBOT_CPP__UTILS_HPP_

#include <string>

namespace my_robot_cpp
{

class Utils
{
public:
  static double normalize_angle(double angle);
  static std::string get_timestamp();
};

}  // namespace my_robot_cpp

#endif  // MY_ROBOT_CPP__UTILS_HPP_
```

#### `src/utils.cpp`:
```cpp
#include "my_robot_cpp/utils.hpp"
#include <cmath>
#include <chrono>
#include <sstream>
#include <iomanip>

namespace my_robot_cpp
{

double Utils::normalize_angle(double angle)
{
  while (angle > M_PI) angle -= 2.0 * M_PI;
  while (angle < -M_PI) angle += 2.0 * M_PI;
  return angle;
}

std::string Utils::get_timestamp()
{
  auto now = std::chrono::system_clock::now();
  auto time = std::chrono::system_clock::to_time_t(now);
  std::stringstream ss;
  ss << std::put_time(std::localtime(&time), "%Y-%m-%d %H:%M:%S");
  return ss.str();
}

}  // namespace my_robot_cpp
```

### CMakeLists.txt에 라이브러리 등록:

```cmake
# 라이브러리 생성
add_library(my_robot_cpp_utils src/utils.cpp)
target_include_directories(my_robot_cpp_utils PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
)
ament_target_dependencies(my_robot_cpp_utils rclcpp)

# 노드에서 라이브러리 사용
add_executable(robot_controller_node
  src/robot_controller.cpp
  src/robot_controller_node.cpp
)
target_link_libraries(robot_controller_node my_robot_cpp_utils)
ament_target_dependencies(robot_controller_node rclcpp geometry_msgs)

# 라이브러리 설치 (다른 패키지에서 사용 가능하게)
install(TARGETS
  my_robot_cpp_utils
  EXPORT export_my_robot_cpp_utils
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)

# 헤더 파일 설치
install(DIRECTORY include/
  DESTINATION include
)

# Export 정보 (다른 패키지가 find_package로 찾을 수 있게)
ament_export_targets(export_my_robot_cpp_utils HAS_LIBRARY_TARGET)
ament_export_dependencies(rclcpp)
```

---

## 6단계: Dependencies 추가

**언제든지 추가 가능합니다.**

### 1. package.xml에 추가:
```xml
<depend>rclcpp</depend>
<depend>std_msgs</depend>
<depend>sensor_msgs</depend>
<depend>geometry_msgs</depend>
<depend>tf2</depend>              <!-- 새로 추가 -->
<depend>tf2_ros</depend>           <!-- 새로 추가 -->
```

### 2. CMakeLists.txt에 추가:

```cmake
# find_package 추가
find_package(tf2 REQUIRED)
find_package(tf2_ros REQUIRED)

# 노드에 의존성 추가
ament_target_dependencies(my_node
  rclcpp
  std_msgs
  tf2
  tf2_ros
)
```

**중요:** C++는 Python과 달리 **반드시 두 곳 모두** 추가해야 합니다!
- `package.xml`: ROS2가 의존성을 설치하도록
- `CMakeLists.txt`: 컴파일러가 헤더/라이브러리를 찾도록

---

## 7단계: 빌드 및 실행

**이 단계의 목적**: 작성한 C++ 코드를 컴파일하고 실행 파일을 생성합니다.

**C++ 빌드의 특징:**
- **항상 컴파일 필요**: 코드 수정 시 매번 재빌드
- **빌드 시간**: Python보다 훨씬 오래 걸림 (수초~수분)
- **symlink 무효**: C++는 컴파일 언어라 symlink로 빌드 스킵 불가
- **증분 빌드**: 수정된 파일만 재컴파일 (전체보다 빠름)

### 빌드:
```bash
cd <workspace_path>

# 특정 패키지만 빌드
colcon build --packages-select my_robot_cpp

# 병렬 빌드 (빠름)
colcon build --packages-select my_robot_cpp --parallel-workers 4

# 전체 재빌드 (문제 발생 시)
colcon build --packages-select my_robot_cpp --cmake-clean-cache
```

### 빌드 후 폴더 구조:
```
build/my_robot_cpp/          # 빌드 중간 파일 (object files 등)
install/my_robot_cpp/
├── lib/
│   └── my_robot_cpp/
│       ├── my_node              # 컴파일된 실행 파일
│       ├── publisher_node
│       ├── subscriber_node
│       └── robot_controller_node
└── share/
    └── my_robot_cpp/
        ├── launch/
        │   └── robot.launch.py
        ├── config/
        │   └── params.yaml
        └── package.xml
```

**Python과의 차이:**
- ✅ `lib/` 안에 실행 파일이 **바이너리**로 생성 (Python은 스크립트)
- ✅ `build/` 디렉토리에 컴파일 중간 파일 존재 (Python은 거의 비어있음)

### 소싱 및 실행:
```bash
# 환경 소싱
source install/setup.bash

# 개별 노드 실행
ros2 run my_robot_cpp my_node
ros2 run my_robot_cpp publisher_node
ros2 run my_robot_cpp robot_controller_node

# Launch 파일 실행
ros2 launch my_robot_cpp robot.launch.py

# 파라미터와 함께 실행
ros2 run my_robot_cpp robot_controller_node \
  --ros-args --params-file install/my_robot_cpp/share/my_robot_cpp/config/params.yaml
```

---

## 완성된 CMakeLists.txt 전체 예시

```cmake
cmake_minimum_required(VERSION 3.8)
project(my_robot_cpp)

# 컴파일러 경고 옵션
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# 의존성 찾기
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_ros REQUIRED)

# 라이브러리 생성
add_library(my_robot_cpp_utils src/utils.cpp)
target_include_directories(my_robot_cpp_utils PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
)
ament_target_dependencies(my_robot_cpp_utils rclcpp)

# 실행 파일 생성
add_executable(my_node src/my_node.cpp)
ament_target_dependencies(my_node rclcpp std_msgs)

add_executable(publisher_node src/publisher_node.cpp)
ament_target_dependencies(publisher_node rclcpp std_msgs)

add_executable(subscriber_node src/subscriber_node.cpp)
ament_target_dependencies(subscriber_node rclcpp std_msgs)

add_executable(robot_controller_node
  src/robot_controller.cpp
  src/robot_controller_node.cpp
)
target_include_directories(robot_controller_node PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
)
target_link_libraries(robot_controller_node my_robot_cpp_utils)
ament_target_dependencies(robot_controller_node
  rclcpp
  geometry_msgs
  tf2
  tf2_ros
)

# 설치: 실행 파일
install(TARGETS
  my_node
  publisher_node
  subscriber_node
  robot_controller_node
  DESTINATION lib/${PROJECT_NAME}
)

# 설치: 라이브러리
install(TARGETS
  my_robot_cpp_utils
  EXPORT export_my_robot_cpp_utils
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)

# 설치: 헤더 파일
install(DIRECTORY include/
  DESTINATION include
)

# 설치: launch 파일
install(DIRECTORY
  launch
  DESTINATION share/${PROJECT_NAME}
)

# 설치: config 파일
install(DIRECTORY
  config
  DESTINATION share/${PROJECT_NAME}
)

# Export (다른 패키지에서 사용 가능하게)
ament_export_targets(export_my_robot_cpp_utils HAS_LIBRARY_TARGET)
ament_export_dependencies(
  rclcpp
  std_msgs
  sensor_msgs
  geometry_msgs
  tf2
  tf2_ros
)

ament_package()
```

---

## 체크리스트

### 패키지가 제대로 생성되었는지 확인:

- [ ] `CMakeLists.txt`가 존재하는가?
- [ ] `include/<package_name>/` 디렉토리가 존재하는가?
- [ ] `src/` 디렉토리에 .cpp 파일이 있는가?
- [ ] `CMakeLists.txt`에 모든 노드가 `add_executable()`로 등록되었는가?
- [ ] `CMakeLists.txt`에 모든 의존성이 `find_package()`로 선언되었는가?
- [ ] `CMakeLists.txt`에 `install()`로 설치 위치가 지정되었는가?
- [ ] `package.xml`에 모든 의존성이 선언되었는가?

### 빌드 후 확인:

```bash
# 패키지가 인식되는지 확인
ros2 pkg list | grep my_robot_cpp

# 실행 파일이 있는지 확인
ros2 pkg executables my_robot_cpp

# 실행 파일이 실제로 컴파일되었는지 확인
ls install/my_robot_cpp/lib/my_robot_cpp/

# Launch 파일이 있는지 확인
ros2 launch my_robot_cpp <TAB>
```

---

## 자주 발생하는 오류와 해결법

### 1. "No executable found"
**원인**: `CMakeLists.txt`에 `add_executable()` 또는 `install(TARGETS ...)`가 누락
**해결**:
```cmake
add_executable(my_node src/my_node.cpp)
ament_target_dependencies(my_node rclcpp)

install(TARGETS
  my_node
  DESTINATION lib/${PROJECT_NAME}
)
```

### 2. "fatal error: xxx.hpp: No such file or directory"
**원인**: 헤더 파일을 찾을 수 없음
**해결**:
```cmake
# include 디렉토리 지정
target_include_directories(my_node PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
)

# 또는 의존성 패키지의 헤더가 필요하면
find_package(geometry_msgs REQUIRED)
ament_target_dependencies(my_node geometry_msgs)
```

### 3. "undefined reference to ..."
**원인**: 링커가 함수 구현을 찾을 수 없음 (라이브러리 미링크)
**해결**:
```cmake
# 라이브러리 링크
target_link_libraries(my_node my_robot_cpp_utils)

# 또는 의존성 추가
ament_target_dependencies(my_node rclcpp)
```

### 4. "CMake Error: Cannot find source file: ..."
**원인**: `add_executable()`에 지정한 파일이 실제로 없음
**해결**: 파일 경로 확인 또는 파일 생성
```bash
# 파일 존재 확인
ls src/my_node.cpp
```

### 5. 빌드는 성공했는데 실행 파일이 없음
**원인**: `install(TARGETS ...)`가 누락되어 install 디렉토리로 복사 안 됨
**해결**:
```cmake
install(TARGETS
  my_node
  DESTINATION lib/${PROJECT_NAME}
)
```

### 6. Launch 파일이 안 보임
**원인**: `install(DIRECTORY launch ...)` 누락
**해결**:
```cmake
install(DIRECTORY
  launch
  DESTINATION share/${PROJECT_NAME}
)
```

---

## Python vs C++ 선택 가이드

### Python을 사용해야 할 때:
- ✅ 빠른 프로토타이핑
- ✅ AI/ML 기능 (PyTorch, TensorFlow, OpenCV-Python)
- ✅ 데이터 처리 및 분석
- ✅ 복잡한 로직을 빠르게 구현
- ✅ 실시간 성능이 중요하지 않은 경우

### C++를 사용해야 할 때:
- ✅ 실시간 제어 (로봇 모터 제어, PID 등)
- ✅ 센서 데이터 고속 처리
- ✅ 계산 집약적 작업 (경로 계획, SLAM 등)
- ✅ 기존 C++ 라이브러리 사용 필요
- ✅ 하드웨어와 직접 통신 (드라이버 등)
- ✅ 배터리 수명이 중요한 임베디드 시스템

### 혼합 사용 (권장):
- C++: 실시간 제어 노드, 센서 드라이버
- Python: AI/ML 처리, 의사결정 로직, 모니터링
- 예: C++ 모터 제어 + Python 비전 처리

---

## 빠른 참조 명령어

```bash
# 새 C++ 패키지 생성
ros2 pkg create --build-type ament_cmake <package_name> \
  --dependencies rclcpp std_msgs

# 빌드
colcon build --packages-select <package_name>

# 병렬 빌드
colcon build --parallel-workers 4

# 전체 재빌드
colcon build --packages-select <package_name> --cmake-clean-cache

# 환경 소싱
source install/setup.bash

# 노드 실행
ros2 run <package_name> <node_name>

# Launch 파일 실행
ros2 launch <package_name> <launch_file>.launch.py

# 패키지 정보 확인
ros2 pkg list | grep <package_name>
ros2 pkg executables <package_name>
```

---

## 요약

1. **`ros2 pkg create --build-type ament_cmake`로 기본 템플릿 생성**
2. **헤더는 `include/<package_name>/`, 소스는 `src/`에 작성**
3. **`CMakeLists.txt`에서:**
   - `find_package()`로 의존성 선언
   - `add_executable()`로 실행 파일 등록
   - `ament_target_dependencies()`로 링크
   - `install()`로 설치 위치 지정
4. **`package.xml`에 의존성 추가**
5. **코드 수정 시 항상 재빌드 필요 (C++는 컴파일 언어)**
6. **빌드 후 `source install/setup.bash` 실행**
7. **`ros2 run` 또는 `ros2 launch`로 실행**

C++ 패키지는 Python보다 설정이 복잡하지만, 실행 성능이 중요한 로봇 시스템에서 필수입니다!
