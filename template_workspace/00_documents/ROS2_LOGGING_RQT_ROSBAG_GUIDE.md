# ROS2 로깅, RQT 도구, Rosbag 가이드

로깅, rqt 도구를 이용한 시각화/디버깅, rosbag을 이용한 데이터 기록/재생에 대한 완벽한 가이드입니다.

---

## 목차
1. [로깅 (Logging)](#로깅-logging)
2. [RQT 도구](#rqt-도구)
3. [Rosbag](#rosbag)

---

## 로깅 (Logging)

### 기본 로깅 레벨

ROS2는 5가지 로깅 심각도 레벨을 제공합니다 (낮은 순서에서 높은 순서로):

```python
# Python
self.get_logger().debug('Debug 메시지')    # 상세한 디버깅 정보
self.get_logger().info('Info 메시지')      # 일반 정보
self.get_logger().warn('Warning 메시지')   # 경고 상황
self.get_logger().error('Error 메시지')    # 에러 상황
self.get_logger().fatal('Fatal 메시지')    # 치명적/심각한 에러
```

```cpp
// C++
RCLCPP_DEBUG(this->get_logger(), "Debug 메시지");
RCLCPP_INFO(this->get_logger(), "Info 메시지");
RCLCPP_WARN(this->get_logger(), "Warning 메시지");
RCLCPP_ERROR(this->get_logger(), "Error 메시지");
RCLCPP_FATAL(this->get_logger(), "Fatal 메시지");
```

### 포맷팅된 로깅

```python
# Python - f-string 사용
count = 42
self.get_logger().info(f'카운터 값: {count}')
self.get_logger().warn(f'온도 {temp}°C가 임계값 {max_temp}°C를 초과했습니다')
```

```cpp
// C++ - printf 스타일 포맷팅 사용
int count = 42;
RCLCPP_INFO(this->get_logger(), "카운터 값: %d", count);
RCLCPP_WARN(this->get_logger(), "온도 %.2f°C가 임계값 %.2f°C를 초과했습니다", temp, max_temp);
```

### 조건부 로깅 (Once, Throttle, Skip)

```python
# Python
# 한 번만 로그 출력
self.get_logger().info('한 번만 출력됩니다', once=True)

# Throttle: N초당 최대 1회만 로그 출력
self.get_logger().info('제한된 메시지', throttle_duration_sec=5.0)

# Skip: N번째 호출마다 로그 출력
self.get_logger().info('10번째 호출마다 출력', skip_first=9)
```

```cpp
// C++
// 한 번만 로그 출력
RCLCPP_INFO_ONCE(this->get_logger(), "한 번만 출력됩니다");

// Throttle: N밀리초당 최대 1회만 로그 출력
RCLCPP_INFO_THROTTLE(this->get_logger(), *this->get_clock(), 5000, "제한된 메시지");

// Skip: N번째 호출마다 로그 출력
RCLCPP_INFO_SKIPFIRST(this->get_logger(), 9, "10번째 호출마다 출력");
```

### 조건식을 사용한 로깅

```python
# Python
# 조건이 참일 때만 로그 출력
if sensor_value > threshold:
    self.get_logger().warn(f'센서 값 {sensor_value}이(가) 임계값을 초과했습니다')

# 조건식 사용
self.get_logger().info(
    f'상태: {"정상" if status else "실패"}'
)
```

```cpp
// C++
// 표현식이 참일 때만 로그 출력
RCLCPP_INFO_EXPRESSION(
    this->get_logger(),
    sensor_value > threshold,
    "센서 값 %f이(가) 임계값을 초과했습니다", sensor_value
);

// Throttle과 결합
RCLCPP_WARN_EXPRESSION_THROTTLE(
    this->get_logger(),
    *this->get_clock(),
    5000,  // 5초
    cpu_usage > 90.0,
    "높은 CPU 사용률: %.1f%%", cpu_usage
);
```

### 런타임에 로그 레벨 설정하기

```bash
# 특정 노드의 로그 레벨 설정
ros2 run <package_name> <node_name> --ros-args --log-level <level>

# 레벨: debug, info, warn, error, fatal
ros2 run my_package my_node --ros-args --log-level debug

# 특정 로거의 로그 레벨 설정
ros2 run my_package my_node --ros-args --log-level my_node:=debug

# 환경 변수를 통한 설정
export RCUTILS_CONSOLE_OUTPUT_FORMAT="[{severity}] [{name}]: {message}"
```

### Launch 파일에서 로깅 설정

```python
# Python launch 파일
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='my_package',
            executable='my_node',
            name='my_node',
            arguments=['--ros-args', '--log-level', 'debug'],
            # 또는 노드별 로깅을 위한 파라미터 사용
            parameters=[{
                'use_sim_time': True
            }]
        )
    ])
```

### 고급 로깅 설정

```python
# Python - 노드에서 커스텀 로거 설정
import rclpy
from rclpy.node import Node

class MyNode(Node):
    def __init__(self):
        super().__init__('my_node')

        # 로거 가져오기
        self.logger = self.get_logger()

        # 현재 로그 레벨 확인
        current_level = self.logger.get_effective_level()
        self.logger.info(f'현재 로그 레벨: {current_level}')

        # 프로그래매틱하게 로그 레벨 설정
        self.logger.set_level(rclpy.logging.LoggingSeverity.DEBUG)
```

### 로깅 모범 사례

1. **적절한 레벨 사용:**
   - `DEBUG`: 상세한 진단 정보
   - `INFO`: 정상 작동 확인
   - `WARN`: 예상치 못한 상황이지만 노드는 계속 실행
   - `ERROR`: 심각한 문제, 기능에 영향
   - `FATAL`: 노드가 계속 실행할 수 없음

2. **메시지에 컨텍스트 포함:**
   ```python
   # 좋음
   self.get_logger().error(f'{ip_address}의 센서 연결 실패: {error}')

   # 덜 유용함
   self.get_logger().error('연결 실패')
   ```

3. **고빈도 로그에는 throttle 사용:**
   ```python
   # 타이머 콜백에서 로그 범람 방지
   self.get_logger().info('데이터 퍼블리싱 중', throttle_duration_sec=1.0)
   ```

4. **민감한 정보는 로그하지 않기:**
   ```python
   # 나쁨 - 비밀번호는 절대 로그하지 마세요
   self.get_logger().info(f'비밀번호로 연결 중: {password}')

   # 좋음
   self.get_logger().info('서버 연결 시도 중')
   ```

### 예제: 완전한 로깅 노드

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

class LoggingExample(Node):
    def __init__(self):
        super().__init__('logging_example')

        # 기본 로깅
        self.get_logger().info('노드가 성공적으로 시작되었습니다')

        # 데모용 파라미터
        self.declare_parameter('update_rate', 1.0)
        self.declare_parameter('threshold', 50.0)

        rate = self.get_parameter('update_rate').value
        self.counter = 0
        self.timer = self.create_timer(1.0 / rate, self.timer_callback)

    def timer_callback(self):
        self.counter += 1

        # 다양한 로그 레벨
        if self.counter % 10 == 0:
            self.get_logger().debug(f'Debug: 카운터가 {self.counter}입니다')

        if self.counter % 5 == 0:
            self.get_logger().info(f'Info: {self.counter}에 도달했습니다')

        if self.counter % 7 == 0:
            self.get_logger().warn('Warning: 행운의 숫자 7 패턴 감지됨')

        if self.counter == 50:
            self.get_logger().error('Error: 에러 임계값에 도달했습니다!')

        # Throttled 로깅 (5초당 최대 1회)
        self.get_logger().info(
            f'주기적 업데이트: {self.counter}',
            throttle_duration_sec=5.0
        )

        # 한 번만 로그
        self.get_logger().info('한 번만 출력됩니다', once=True)

def main(args=None):
    rclpy.init(args=args)
    node = LoggingExample()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('종료 중...')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

---

## RQT 도구

RQT는 ROS의 GUI 개발을 위한 Qt 기반 프레임워크입니다. 시각화와 디버깅을 위한 다양한 플러그인을 제공합니다.

### RQT 설치

```bash
# 모든 rqt 도구 설치
sudo apt install ros-<distro>-rqt*

# Humble의 경우
sudo apt install ros-humble-rqt*
```

### 주요 RQT 도구

#### 1. rqt_graph - 노드와 토픽 시각화

```bash
# 노드와 토픽 시각화
rqt_graph

# 또는 메인 rqt 인터페이스를 통해
rqt
# 그 다음: Plugins > Introspection > Node Graph
```

**기능:**
- 노드는 타원형, 토픽은 사각형으로 표시
- 퍼블리셔와 서브스크라이버 간의 연결 표시
- 토픽 타입별 필터링 또는 특정 노드 숨기기
- 그래프 업데이트를 위한 새로고침

#### 2. rqt_console - 로그 메시지 뷰어

```bash
# 모든 노드의 로그 메시지 보기
rqt_console

# 또는 메인 rqt 인터페이스를 통해
rqt
# 그 다음: Plugins > Logging > Console
```

**기능:**
- 심각도 레벨별 필터링 (Debug, Info, Warn, Error, Fatal)
- 노드 이름 또는 메시지 내용으로 필터링
- 특정 메시지 검색 및 강조
- 로그를 파일로 내보내기
- 심각도 레벨별 색상 코딩

**사용법:**
1. 노드 시작
2. rqt_console 실행
3. 특정 이슈에 집중하기 위한 필터 설정
4. 실시간 로그 출력 모니터링

#### 3. rqt_plot - 실시간 데이터 플로팅

```bash
# 토픽의 숫자 데이터 플로팅
rqt_plot

# 또는 토픽 직접 지정
rqt_plot /my_topic/data

# 여러 토픽
rqt_plot /topic1/field1 /topic2/field2
```

**기능:**
- 숫자 메시지 필드의 실시간 플로팅
- 동일 창에 여러 플롯
- 시간 윈도우 조정 가능
- 플로팅 일시정지/재개
- 플롯 데이터를 CSV로 저장

**예제:**
```bash
# 로봇 속도 플로팅
rqt_plot /cmd_vel/linear/x /cmd_vel/angular/z

# 센서 데이터 플로팅
rqt_plot /sensor/temperature /sensor/humidity
```

#### 4. rqt_topic - 토픽 모니터링

```bash
# 토픽 정보 보기
rqt_topic

# 또는 메인 rqt 인터페이스를 통해
rqt
# 그 다음: Plugins > Topics > Topic Monitor
```

**기능:**
- 활성화된 모든 토픽 나열
- 메시지 타입과 퍼블리싱 속도 표시
- 메시지 내용 보기
- GUI에서 토픽 데이터 에코

#### 5. rqt_publisher - 수동 토픽 퍼블리싱

```bash
# 수동으로 메시지 퍼블리시
rqt_publisher

# 또는 메인 rqt 인터페이스를 통해
rqt
# 그 다음: Plugins > Topics > Message Publisher
```

**기능:**
- 토픽과 메시지 타입 선택
- GUI를 통해 메시지 필드 작성
- 퍼블리싱 속도 설정
- 퍼블리셔 코드 작성 없이 서브스크라이버 테스트에 유용

**예제 사용 사례:**
수동으로 속도 명령을 퍼블리시하여 로봇 컨트롤러 테스트

#### 6. rqt_service_caller - 대화형 서비스 호출

```bash
# GUI에서 서비스 호출
rqt_service_caller

# 또는 메인 rqt 인터페이스를 통해
rqt
# 그 다음: Plugins > Services > Service Caller
```

**기능:**
- 사용 가능한 모든 서비스 나열
- 요청 필드 작성
- 서비스 호출 및 응답 보기
- 서비스 서버 테스트에 유용

#### 7. rqt_reconfigure - 동적 파라미터 설정

```bash
# 노드 파라미터를 동적으로 조정
rqt_reconfigure

# 또는 메인 rqt 인터페이스를 통해
rqt
# 그 다음: Plugins > Configuration > Dynamic Reconfigure
```

**기능:**
- 실시간으로 파라미터 조정
- 숫자 파라미터용 슬라이더 컨트롤
- 불린 파라미터용 체크박스
- 노드 재시작 없이 즉시 적용

**주의:** 노드가 파라미터 변경을 적절히 선언하고 처리해야 합니다

#### 8. rqt_image_view - 이미지 시각화

```bash
# 카메라/이미지 토픽 보기
rqt_image_view

# 또는 메인 rqt 인터페이스를 통해
rqt
# 그 다음: Plugins > Visualization > Image View
```

**기능:**
- 이미지 토픽 표시
- 다양한 인코딩 지원 (RGB, BGR, depth 등)
- 줌 및 팬
- 이미지 저장
- 여러 이미지 창

**예제:**
```bash
# 카메라 피드 보기
ros2 run usb_cam usb_cam_node_exe &
rqt_image_view
# 드롭다운에서 /image_raw 선택
```

#### 9. rqt_bag - Rosbag 시각화 및 재생

```bash
# bag 파일 보기 및 재생
rqt_bag <bag_file>

# 또는 메인 rqt 인터페이스를 통해
rqt
# 그 다음: Plugins > Logging > Bag
```

**기능:**
- bag 내용의 타임라인 시각화
- bag 데이터 재생/일시정지/탐색
- 특정 타임스탬프의 메시지 내용 보기
- 토픽별 필터링

### 커스텀 RQT 플러그인 만들기

```python
# my_rqt_plugin.py
from rqt_gui_py.plugin import Plugin
from python_qt_binding.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel

class MyPlugin(Plugin):
    def __init__(self, context):
        super(MyPlugin, self).__init__(context)
        self.setObjectName('MyPlugin')

        # 위젯 생성
        self._widget = QWidget()
        layout = QVBoxLayout()

        self._label = QLabel('Hello RQT!')
        self._button = QPushButton('클릭하세요')
        self._button.clicked.connect(self.on_button_click)

        layout.addWidget(self._label)
        layout.addWidget(self._button)
        self._widget.setLayout(layout)

        context.add_widget(self._widget)

    def on_button_click(self):
        self._label.setText('버튼이 클릭되었습니다!')

    def shutdown_plugin(self):
        pass
```

### RQT 모범 사례

1. **디버깅에는 rqt_console 사용:** 개발 중 항상 실행해두기
2. **시스템 이해에는 rqt_graph 사용:** 노드 아키텍처 시각화
3. **튜닝에는 rqt_plot 사용:** 실시간 시각화로 파라미터 튜닝
4. **설정 저장:** RQT는 perspective 레이아웃을 저장하여 재사용 가능
5. **여러 플러그인 결합:** 하나의 rqt 창에서 여러 플러그인 열기

---

## Rosbag

Rosbag은 ROS 토픽 데이터를 기록하고 재생합니다. 테스트, 디버깅, 데이터 분석에 필수적입니다.

### 데이터 기록

#### 기본 기록

```bash
# 모든 토픽 기록
ros2 bag record -a

# 특정 토픽 기록
ros2 bag record /topic1 /topic2 /topic3

# 커스텀 이름으로 기록
ros2 bag record -o my_data /topic1 /topic2

# 저장 포맷 지정 (기본값: sqlite3)
ros2 bag record -o my_data -s mcap /topic1
```

#### 고급 기록 옵션

```bash
# 특정 시간 동안 기록 (30초)
ros2 bag record -a --duration 30

# 최대 bag 크기 지정 (100MB)
ros2 bag record -a --max-bag-size 100000000

# 압축과 함께 기록
ros2 bag record -a --compression-mode file --compression-format zstd

# 특정 토픽 제외하고 기록
ros2 bag record -a -x "/camera/.*" "/lidar/points"

# 커스텀 저장 설정으로 기록
ros2 bag record -a --storage sqlite3 --max-cache-size 1000000
```

#### Launch 파일에서 기록

```python
# Python launch 파일
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # 노드 시작
        Node(
            package='my_package',
            executable='my_node',
            name='my_node'
        ),

        # 토픽 기록
        ExecuteProcess(
            cmd=['ros2', 'bag', 'record', '-a', '-o', 'my_recording'],
            output='screen'
        )
    ])
```

### 데이터 재생

#### 기본 재생

```bash
# bag 파일 재생
ros2 bag play my_bag

# 다른 속도로 재생 (0.5x = 절반 속도, 2.0x = 2배 속도)
ros2 bag play my_bag --rate 0.5

# 반복 재생
ros2 bag play my_bag --loop

# 일시정지 상태로 시작
ros2 bag play my_bag --start-paused

# 특정 토픽만 재생
ros2 bag play my_bag --topics /topic1 /topic2
```

#### 고급 재생 옵션

```bash
# 특정 타임스탬프부터 재생
ros2 bag play my_bag --start-offset 10.0  # bag의 10초부터 시작

# 특정 시간까지만 재생
ros2 bag play my_bag --duration 30.0  # 30초만 재생

# 재생 중 토픽 리맵
ros2 bag play my_bag --remap /old_topic:=/new_topic

# 클럭 타임 퍼블리시 (시뮬레이션용)
ros2 bag play my_bag --clock

# 퍼블리싱 전 서브스크라이버 대기
ros2 bag play my_bag --wait-for-all-subscribers
```

### Bag 검사

```bash
# bag 정보 표시
ros2 bag info my_bag

# 출력 내용:
# - 지속 시간
# - 시작/종료 시간
# - 메시지 개수
# - 토픽과 타입
# - 저장 포맷

# 예제 출력:
# Files:             my_bag_0.db3
# Bag size:          5.2 MiB
# Storage id:        sqlite3
# Duration:          30.5s
# Start:             Jan 16 2026 10:30:15.123
# End:               Jan 16 2026 10:30:45.678
# Messages:          1523
# Topic information:
#   Topic: /cmd_vel | Type: geometry_msgs/msg/Twist | Count: 305
#   Topic: /odom | Type: nav_msgs/msg/Odometry | Count: 1218
```

### Bag 변환 및 처리

```bash
# 저장 포맷 간 변환
ros2 bag convert -i input_bag -o output_bag --output-options storage_id=mcap

# bag 재인덱싱 (손상된 인덱스 복구)
ros2 bag reindex my_bag
```

### Python에서 Rosbag 사용

#### 프로그래매틱하게 기록

```python
import rclpy
from rclpy.node import Node
from rosbag2_py import SequentialWriter, StorageOptions, ConverterOptions

class BagRecorder(Node):
    def __init__(self):
        super().__init__('bag_recorder')

        # bag writer 설정
        storage_options = StorageOptions(
            uri='my_bag',
            storage_id='sqlite3'
        )
        converter_options = ConverterOptions(
            input_serialization_format='cdr',
            output_serialization_format='cdr'
        )

        self.writer = SequentialWriter()
        self.writer.open(storage_options, converter_options)

        # 토픽 메타데이터 생성
        from rosbag2_py import TopicMetadata
        from rclpy.serialization import serialize_message

        topic_name = '/my_topic'
        topic_type = 'std_msgs/msg/String'

        topic_metadata = TopicMetadata(
            name=topic_name,
            type=topic_type,
            serialization_format='cdr'
        )
        self.writer.create_topic(topic_metadata)

        # 구독 및 기록
        self.subscription = self.create_subscription(
            String,
            topic_name,
            self.topic_callback,
            10
        )

    def topic_callback(self, msg):
        from rclpy.serialization import serialize_message
        self.writer.write(
            '/my_topic',
            serialize_message(msg),
            self.get_clock().now().nanoseconds
        )
```

#### 프로그래매틱하게 재생

```python
import rclpy
from rosbag2_py import SequentialReader, StorageOptions, ConverterOptions

def read_bag():
    storage_options = StorageOptions(
        uri='my_bag',
        storage_id='sqlite3'
    )
    converter_options = ConverterOptions(
        input_serialization_format='cdr',
        output_serialization_format='cdr'
    )

    reader = SequentialReader()
    reader.open(storage_options, converter_options)

    # 메타데이터 가져오기
    topic_types = reader.get_all_topics_and_types()
    print(f'토픽: {topic_types}')

    # 메시지 읽기
    while reader.has_next():
        (topic, data, timestamp) = reader.read_next()
        print(f'토픽: {topic}, 타임스탬프: {timestamp}')
```

### Rosbag 모범 사례

1. **bag을 설명적으로 명명:**
   ```bash
   ros2 bag record -o 2026_01_16_복도_테스트 /camera/image /lidar/scan
   ```

2. **대용량 데이터셋에는 압축 사용:**
   ```bash
   ros2 bag record -a --compression-mode file --compression-format zstd
   ```

3. **크기 줄이기 위해 토픽 필터링:**
   ```bash
   # 필수 토픽만 기록
   ros2 bag record /odom /cmd_vel /scan

   # 고대역폭 토픽 제외
   ros2 bag record -a -x "/camera/.*"
   ```

4. **기록된 데이터로 테스트:**
   - 테스트 시나리오를 한 번 기록
   - 개발 중 반복적으로 재생
   - 일관된 테스트 조건 보장

5. **bag 아카이브 및 문서화:**
   - 테스트 조건을 설명하는 메타데이터 파일 추가
   - 장기 보관을 위해 bag 압축
   - 각 bag의 내용 인덱스 유지

### 예제 워크플로우: 기록, 분석, 디버그

```bash
# 1. 테스트 중 기록
ros2 bag record -o robot_test /cmd_vel /odom /scan /camera/image

# 2. 기록된 내용 검사
ros2 bag info robot_test

# 3. 시각화와 함께 재생
ros2 bag play robot_test --clock &
rviz2 &
rqt_plot /odom/pose/pose/position/x /odom/pose/pose/position/y &

# 4. 분석을 위해 느린 속도로 재생
ros2 bag play robot_test --rate 0.1

# 5. 다른 노드로 리맵 및 테스트
ros2 bag play robot_test --remap /cmd_vel:=/test_cmd_vel &
ros2 run my_package improved_controller
```

### Rosbag 저장 포맷

**SQLite3 (기본값):**
- 일반적인 용도에 적합
- 광범위한 호환성
- 적당한 성능

**MCAP:**
- 최신 포맷
- 더 나은 성능
- 효율적인 인덱싱
- 채택 증가 중

```bash
# MCAP 포맷 사용
ros2 bag record -a -s mcap -o my_bag
```

---

## 통합 예제: 완전한 디버깅 워크플로우

로깅, rqt, rosbag을 결합한 완전한 예제입니다:

### 1단계: 적절한 로깅이 있는 노드

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class RobotController(Node):
    def __init__(self):
        super().__init__('robot_controller')

        self.get_logger().info('로봇 컨트롤러 시작 중...')

        # 파라미터 선언
        self.declare_parameter('max_speed', 1.0)
        self.declare_parameter('update_rate', 10.0)

        # 퍼블리셔와 서브스크라이버
        self.cmd_pub = self.create_subscription(
            '/cmd_vel',
            Twist,
            10
        )

        self.status_pub = self.create_publisher(String, '/status', 10)

        # 타이머
        rate = self.get_parameter('update_rate').value
        self.timer = self.create_timer(1.0 / rate, self.control_loop)

        self.get_logger().info('로봇 컨트롤러 준비 완료')

    def control_loop(self):
        # 제어 로직
        msg = Twist()

        # 중요한 이벤트 로그
        self.get_logger().debug('제어 루프 실행 중')

        max_speed = self.get_parameter('max_speed').value
        if msg.linear.x > max_speed:
            self.get_logger().warn(
                f'속도 {msg.linear.x}이(가) 최대값 {max_speed}을(를) 초과합니다',
                throttle_duration_sec=1.0
            )

def main(args=None):
    rclpy.init(args=args)
    node = RobotController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### 2단계: 기록과 함께 Launch

```python
# launch/debug_robot.launch.py
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
    return LaunchDescription([
        # 디버그 로깅과 함께 로봇 컨트롤러 시작
        Node(
            package='my_robot',
            executable='robot_controller',
            name='robot_controller',
            output='screen',
            arguments=['--ros-args', '--log-level', 'debug']
        ),

        # 모든 데이터 기록
        ExecuteProcess(
            cmd=['ros2', 'bag', 'record', '-a', '-o', 'debug_session'],
            output='screen'
        )
    ])
```

### 3단계: RQT로 모니터링

```bash
# 터미널 1: 시스템 실행
ros2 launch my_robot debug_robot.launch.py

# 터미널 2: rqt 도구 열기
rqt_console &  # 로그 모니터링
rqt_graph &    # 연결 시각화
rqt_plot /cmd_vel/linear/x &  # 속도 플로팅

# 터미널 3: 시스템과 상호작용
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "..."
```

### 4단계: 기록된 데이터 분석

```bash
# 기록된 내용 확인
ros2 bag info debug_session

# 데이터 재생
ros2 bag play debug_session --clock

# rqt 시각화와 함께 재생
ros2 bag play debug_session --clock &
rqt_plot /cmd_vel/linear/x /odom/twist/twist/linear/x &
```

---

## 요약

**로깅:** 적절한 심각도 레벨 사용, 컨텍스트를 포함한 메시지 포맷팅, 고빈도 로그에 throttling 사용

**RQT 도구:**
- `rqt_console` - 로그 보기
- `rqt_graph` - 노드 연결 시각화
- `rqt_plot` - 실시간 데이터 플로팅
- `rqt_publisher` - 테스트 메시지 퍼블리시
- `rqt_reconfigure` - 파라미터 동적 조정

**Rosbag:**
- `ros2 bag record` - 토픽 기록
- `ros2 bag play` - 데이터 재생
- `ros2 bag info` - bag 내용 검사
- 테스트, 디버깅, 데이터 분석에 사용

이 도구들은 함께 ROS2 시스템 개발, 디버깅, 분석을 위한 완전한 툴킷을 형성합니다.