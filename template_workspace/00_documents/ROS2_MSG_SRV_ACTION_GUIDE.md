# ROS2 메시지/서비스/액션 정의 가이드

이 가이드는 ROS2에서 커스텀 메시지, 서비스, 액션을 정의하는 방법을 설명합니다.

---

## 목차

1. [개요](#개요)
2. [메시지 (Message) 정의](#메시지-message-정의)
3. [서비스 (Service) 정의](#서비스-service-정의)
4. [액션 (Action) 정의](#액션-action-정의)
5. [패키지 설정](#패키지-설정)
6. [빌드 및 사용](#빌드-및-사용)

---

## 개요

### 언제 커스텀 타입이 필요한가?

**기본 제공 타입으로 충분한 경우:**
```python
from std_msgs.msg import String, Int32, Float64, Bool
from geometry_msgs.msg import Twist, Pose, Point
from sensor_msgs.msg import Image, LaserScan
from example_interfaces.srv import AddTwoInts
from example_interfaces.action import Fibonacci
```

**커스텀 타입이 필요한 경우:**
- 기본 타입에 없는 복잡한 데이터 구조
- 여러 데이터를 하나로 묶어서 전송
- 프로젝트 특화 데이터 타입

### 메시지 vs 서비스 vs 액션

| 타입 | 통신 방식 | 응답 | 피드백 | 사용 예시 |
|------|----------|------|--------|---------|
| **메시지** | 단방향 (Pub/Sub) | ❌ | ❌ | 센서 데이터, 상태 정보 |
| **서비스** | 양방향 (요청-응답) | ✅ | ❌ | 계산, 조회, 설정 변경 |
| **액션** | 양방향 (목표-피드백-결과) | ✅ | ✅ | 네비게이션, 긴 작업 |

---

## 메시지 (Message) 정의

### 기본 구조

메시지는 `.msg` 파일로 정의합니다.

**폴더 구조:**
```
my_interfaces/
├── msg/
│   └── <MessageName>.msg
├── CMakeLists.txt
└── package.xml
```

**중요:** 메시지/서비스/액션 패키지는 **항상 CMake** (`ament_cmake`) 사용!

### 데이터 타입

```
# 기본 타입
bool
int8, int16, int32, int64
uint8, uint16, uint32, uint64
float32, float64
string
time, duration

# 배열
int32[] dynamic_array          # 크기 가변
int32[5] fixed_array           # 고정 크기
string[] string_list

# 다른 메시지 타입
geometry_msgs/Point position
std_msgs/Header header
```

### 예시 1: 간단한 메시지

**`msg/Person.msg`:**
```
string name
int32 age
float64 height
bool is_student
```

### 예시 2: 중첩 메시지

**`msg/Address.msg`:**
```
string street
string city
string zipcode
```

**`msg/PersonWithAddress.msg`:**
```
string name
int32 age
Address address              # 커스텀 메시지 사용
```

### 예시 3: 배열 사용

**`msg/SensorData.msg`:**
```
std_msgs/Header header       # 타임스탬프, 프레임 ID
float64[] temperature_readings
int32[] error_codes
string[] sensor_names
```

### 예시 4: 고정 크기 배열

**`msg/RobotState.msg`:**
```
float64[3] position          # [x, y, z]
float64[4] orientation       # [x, y, z, w] quaternion
float64[6] joint_angles      # 6개 관절
```

### 예시 5: 상수 정의

**`msg/RobotStatus.msg`:**
```
# 상태 상수
uint8 STATUS_IDLE = 0
uint8 STATUS_MOVING = 1
uint8 STATUS_ERROR = 2
uint8 STATUS_CHARGING = 3

# 실제 데이터
uint8 current_status
string status_message
float64 battery_level
```

### 예시 6: 복잡한 실전 메시지

**`msg/DetectedObject.msg`:**
```
std_msgs/Header header

# 물체 정보
string object_class          # "person", "car", "bicycle" 등
float32 confidence           # 0.0 ~ 1.0

# 바운딩 박스 (이미지 좌표)
int32 x
int32 y
int32 width
int32 height

# 3D 위치 (월드 좌표)
geometry_msgs/Point position
geometry_msgs/Vector3 dimensions

# 추가 정보
string[] attributes          # 속성 리스트
float32[] attribute_scores   # 각 속성의 확률
```

---

## 서비스 (Service) 정의

### 기본 구조

서비스는 `.srv` 파일로 정의합니다.

**폴더 구조:**
```
my_interfaces/
├── srv/
│   └── <ServiceName>.srv
├── CMakeLists.txt
└── package.xml
```

**`.srv` 파일 형식:**
```
# 요청 (Request)
<request_field_type> <request_field_name>
---
# 응답 (Response)
<response_field_type> <response_field_name>
```

**중요:** `---` 구분선으로 요청과 응답 분리!

### 예시 1: 간단한 서비스

**`srv/SetSpeed.srv`:**
```
# 요청
float64 linear_speed
float64 angular_speed
---
# 응답
bool success
string message
```

### 예시 2: 조회 서비스

**`srv/GetRobotPosition.srv`:**
```
# 요청 (빈 요청도 가능)
---
# 응답
float64 x
float64 y
float64 z
float64 yaw
bool is_valid
```

### 예시 3: 복잡한 요청/응답

**`srv/ProcessImage.srv`:**
```
# 요청
sensor_msgs/Image image
bool apply_filter
string filter_type
float32 threshold
---
# 응답
bool success
sensor_msgs/Image processed_image
int32 num_objects_detected
DetectedObject[] detected_objects
string error_message
```

### 예시 4: 데이터베이스 조회

**`srv/QueryDatabase.srv`:**
```
# 요청
string query_type            # "all", "by_id", "by_name"
int32 id
string name
---
# 응답
bool found
Person[] results
int32 total_count
```

### 예시 5: 로봇 제어

**`srv/MoveToPosition.srv`:**
```
# 요청
geometry_msgs/Point target_position
float64 max_speed
bool avoid_obstacles
---
# 응답
bool success
float64 estimated_time
float64 actual_distance
string error_code
```

---

## 액션 (Action) 정의

### 기본 구조

액션은 `.action` 파일로 정의합니다.

**폴더 구조:**
```
my_interfaces/
├── action/
│   └── <ActionName>.action
├── CMakeLists.txt
└── package.xml
```

**`.action` 파일 형식:**
```
# Goal (목표)
<goal_field_type> <goal_field_name>
---
# Result (최종 결과)
<result_field_type> <result_field_name>
---
# Feedback (진행 상황)
<feedback_field_type> <feedback_field_name>
```

**중요:** `---`로 3개 섹션 분리!

### 예시 1: 네비게이션

**`action/NavigateToPoint.action`:**
```
# Goal
geometry_msgs/Point target_position
float64 max_speed
---
# Result
bool success
float64 total_distance
float64 total_time
string message
---
# Feedback
geometry_msgs/Point current_position
float64 distance_remaining
float64 progress_percentage
float64 estimated_time_remaining
```

### 예시 2: 파일 다운로드

**`action/DownloadFile.action`:**
```
# Goal
string url
string destination_path
---
# Result
bool success
int64 file_size
float64 download_time
string error_message
---
# Feedback
int64 bytes_downloaded
int64 total_bytes
float64 progress_percentage
float64 download_speed
```

### 예시 3: 로봇 작업

**`action/PickAndPlace.action`:**
```
# Goal
geometry_msgs/Point pick_position
geometry_msgs/Point place_position
string object_name
---
# Result
bool success
float64 execution_time
string final_status
---
# Feedback
string current_stage          # "approaching", "grasping", "lifting", "moving", "placing"
float64 stage_progress
geometry_msgs/Point current_position
```

### 예시 4: 데이터 수집

**`action/CollectData.action`:**
```
# Goal
int32 num_samples
float64 sample_interval
string[] sensor_types
---
# Result
bool success
int32 samples_collected
float64 total_time
string data_file_path
---
# Feedback
int32 samples_so_far
float64 time_elapsed
string current_sensor
float64 progress_percentage
```

### 예시 5: 배터리 충전

**`action/ChargeBattery.action`:**
```
# Goal
float64 target_battery_level  # 0.0 ~ 100.0
bool fast_charge
---
# Result
bool success
float64 final_battery_level
float64 charging_time
int32 charge_cycles_used
---
# Feedback
float64 current_battery_level
float64 charging_rate
float64 estimated_time_remaining
float64 temperature
```

---

## 패키지 설정

### 1. 패키지 생성

```bash
# 인터페이스 패키지는 항상 ament_cmake
ros2 pkg create --build-type ament_cmake my_interfaces
```

### 2. 폴더 구조

```
my_interfaces/
├── msg/
│   ├── Person.msg
│   ├── Address.msg
│   ├── DetectedObject.msg
│   └── RobotStatus.msg
├── srv/
│   ├── SetSpeed.srv
│   ├── GetRobotPosition.srv
│   └── ProcessImage.srv
├── action/
│   ├── NavigateToPoint.action
│   ├── DownloadFile.action
│   └── PickAndPlace.action
├── CMakeLists.txt
└── package.xml
```

### 3. package.xml 설정

```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>my_interfaces</name>
  <version>0.0.1</version>
  <description>Custom interfaces for my robot</description>
  <maintainer email="your@email.com">Your Name</maintainer>
  <license>Apache-2.0</license>

  <buildtool_depend>ament_cmake</buildtool_depend>

  <!-- 메시지 생성 도구 -->
  <build_depend>rosidl_default_generators</build_depend>
  <exec_depend>rosidl_default_runtime</exec_depend>
  <member_of_group>rosidl_interface_packages</member_of_group>

  <!-- 사용하는 다른 메시지 패키지 -->
  <depend>std_msgs</depend>
  <depend>geometry_msgs</depend>
  <depend>sensor_msgs</depend>

  <export>
    <build_type>ament_cmake</build_type>
  </export>
</package>
```

### 4. CMakeLists.txt 설정

```cmake
cmake_minimum_required(VERSION 3.8)
project(my_interfaces)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# 의존성 찾기
find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)

# 메시지/서비스/액션 파일 등록
rosidl_generate_interfaces(${PROJECT_NAME}
  # 메시지
  "msg/Person.msg"
  "msg/Address.msg"
  "msg/DetectedObject.msg"
  "msg/RobotStatus.msg"

  # 서비스
  "srv/SetSpeed.srv"
  "srv/GetRobotPosition.srv"
  "srv/ProcessImage.srv"

  # 액션
  "action/NavigateToPoint.action"
  "action/DownloadFile.action"
  "action/PickAndPlace.action"

  # 의존성
  DEPENDENCIES
    std_msgs
    geometry_msgs
    sensor_msgs
)

ament_package()
```

---

## 빌드 및 사용

### 1. 빌드

```bash
cd <workspace>
colcon build --packages-select my_interfaces
source install/setup.bash
```

### 2. 생성된 인터페이스 확인

```bash
# 메시지 확인
ros2 interface show my_interfaces/msg/Person
ros2 interface show my_interfaces/msg/DetectedObject

# 서비스 확인
ros2 interface show my_interfaces/srv/SetSpeed

# 액션 확인
ros2 interface show my_interfaces/action/NavigateToPoint

# 모든 인터페이스 목록
ros2 interface list | grep my_interfaces
```

### 3. Python에서 사용

**의존성 추가 (package.xml):**
```xml
<depend>my_interfaces</depend>
```

**코드에서 import:**
```python
# 메시지
from my_interfaces.msg import Person, DetectedObject, RobotStatus

# 서비스
from my_interfaces.srv import SetSpeed, GetRobotPosition

# 액션
from my_interfaces.action import NavigateToPoint, DownloadFile

# 사용 예시
def create_person():
    person = Person()
    person.name = "John"
    person.age = 30
    person.height = 1.75
    person.is_student = False
    return person
```

### 4. C++에서 사용

**CMakeLists.txt:**
```cmake
find_package(my_interfaces REQUIRED)

add_executable(my_node src/my_node.cpp)
ament_target_dependencies(my_node
  rclcpp
  my_interfaces
)
```

**코드에서 include:**
```cpp
#include "my_interfaces/msg/person.hpp"
#include "my_interfaces/srv/set_speed.hpp"
#include "my_interfaces/action/navigate_to_point.hpp"

// 사용 예시
auto person = my_interfaces::msg::Person();
person.name = "John";
person.age = 30;
person.height = 1.75;
person.is_student = false;
```

---

## 실전 예시: 전체 워크플로우

### 시나리오: 물체 감지 시스템

**1. 메시지 정의 (`msg/DetectedObject.msg`):**
```
std_msgs/Header header
string object_class
float32 confidence
int32 x
int32 y
int32 width
int32 height
geometry_msgs/Point position
```

**2. 서비스 정의 (`srv/GetObjectInfo.srv`):**
```
# 요청
int32 object_id
---
# 응답
bool found
DetectedObject object
```

**3. 액션 정의 (`action/TrackObject.action`):**
```
# Goal
int32 object_id
float64 max_tracking_time
---
# Result
bool success
float64 total_tracking_time
int32 frames_tracked
---
# Feedback
geometry_msgs/Point current_position
float64 tracking_confidence
int32 frames_so_far
```

**4. 빌드:**
```bash
colcon build --packages-select my_interfaces
source install/setup.bash
```

**5. Publisher 노드 작성:**
```python
from my_interfaces.msg import DetectedObject
from std_msgs.msg import Header

class ObjectDetector(Node):
    def __init__(self):
        super().__init__('object_detector')
        self.publisher = self.create_publisher(
            DetectedObject, 'detected_objects', 10)
        self.timer = self.create_timer(1.0, self.detect)

    def detect(self):
        msg = DetectedObject()
        msg.header = Header()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.object_class = "person"
        msg.confidence = 0.95
        msg.x = 100
        msg.y = 200
        msg.width = 50
        msg.height = 120

        self.publisher.publish(msg)
```

---

## 자주 발생하는 오류

### 1. "Could not find interface"
**원인**: 인터페이스 패키지가 빌드되지 않았거나 소싱 안 함
**해결**:
```bash
colcon build --packages-select my_interfaces
source install/setup.bash
```

### 2. "No module named 'my_interfaces'"
**원인**: Python에서 패키지를 못 찾음
**해결**:
- `package.xml`에 `<depend>my_interfaces</depend>` 추가
- 워크스페이스 재빌드

### 3. 빌드 시 "No such file or directory"
**원인**: CMakeLists.txt에 파일이 잘못 등록됨
**해결**:
- 파일 경로 확인 (msg/srv/action 디렉토리)
- 파일명 확인 (대소문자 구분)

### 4. "dependency 'xxx_msgs' not found"
**원인**: 의존하는 메시지 패키지가 선언 안 됨
**해결**:
- `package.xml`에 `<depend>xxx_msgs</depend>` 추가
- `CMakeLists.txt`에 `find_package(xxx_msgs REQUIRED)` 추가

---

## 베스트 프랙티스

### 1. 네이밍 컨벤션
- **메시지**: PascalCase (예: `DetectedObject.msg`)
- **필드**: snake_case (예: `object_class`)
- **상수**: UPPER_SNAKE_CASE (예: `STATUS_IDLE`)

### 2. 패키지 구성
- 인터페이스만 모아놓은 별도 패키지 생성 권장
- 패키지명: `<project_name>_interfaces`

### 3. 문서화
```
# msg/Person.msg
# 사람 정보를 담는 메시지

string name           # 이름
int32 age            # 나이 (0 이상)
float64 height       # 키 (미터)
bool is_student      # 학생 여부
```

### 4. 버전 관리
- 메시지 구조 변경 시 버전 업데이트
- 하위 호환성 고려

---

## 요약

| 타입 | 파일 | 용도 | 예시 |
|------|------|------|------|
| **메시지** | `.msg` | 단방향 데이터 전송 | 센서 데이터, 상태 |
| **서비스** | `.srv` | 요청-응답 | 조회, 계산 |
| **액션** | `.action` | 장시간 작업 + 피드백 | 네비게이션, 작업 |

**빌드 체크리스트:**
- [ ] `.msg` / `.srv` / `.action` 파일 작성
- [ ] `CMakeLists.txt`에 파일 등록
- [ ] `package.xml`에 의존성 추가
- [ ] `colcon build` 실행
- [ ] `source install/setup.bash`
- [ ] `ros2 interface show` 로 확인

이제 커스텀 인터페이스를 자유롭게 만들 수 있습니다!
