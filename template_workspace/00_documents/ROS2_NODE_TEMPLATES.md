# ROS2 노드 패턴 템플릿 가이드

이 가이드는 ROS2에서 자주 사용하는 노드 패턴들의 템플릿 코드를 제공합니다.

---

## 목차

1. [Publisher Node (발행자)](#1-publisher-node-발행자)
2. [Subscriber Node (구독자)](#2-subscriber-node-구독자)
3. [Pub-Sub Node (파이프라인)](#3-pub-sub-node-파이프라인)
4. [Timer Node (주기 실행)](#4-timer-node-주기-실행)
5. [Service Server Node](#5-service-server-node)
6. [Service Client Node](#6-service-client-node)
7. [Action Server Node](#7-action-server-node)
8. [Action Client Node](#8-action-client-node)
9. [Parameter Node (설정 가능)](#9-parameter-node-설정-가능)
10. [Lifecycle Node (생명주기 관리)](#10-lifecycle-node-생명주기-관리)

---

## 1. Publisher Node (발행자)

**용도**: 주기적으로 데이터를 토픽으로 발행
**예시**: 센서 데이터 발행, 상태 정보 브로드캐스트

### Python 템플릿

```python
import rclpy
from rclpy.node import Node
from <msg_package>.msg import <MessageType>


class <ClassName>(Node):
    def __init__(self):
        super().__init__('<node_name>')

        # Publisher 생성
        self.publisher = self.create_publisher(
            <MessageType>,
            '<topic_name>',
            <queue_size>)

        # 타이머 생성 (주기: <timer_period> 초)
        timer_period = <timer_period>
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.get_logger().info('<ClassName> started')

    def timer_callback(self):
        """주기적으로 호출되는 콜백 함수"""
        msg = <MessageType>()

        # 메시지 데이터 설정
        msg.<field_name> = <value>

        # 발행
        self.publisher.publish(msg)
        self.get_logger().info(f'Publishing: {msg.<field_name>}')


def main(args=None):
    rclpy.init(args=args)
    node = <ClassName>()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### 구체적 예시: 문자열 발행

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class StringPublisher(Node):
    def __init__(self):
        super().__init__('string_publisher')

        self.publisher = self.create_publisher(String, 'chatter', 10)
        timer_period = 1.0  # 1초마다
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.counter = 0

        self.get_logger().info('StringPublisher started')

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello ROS2: {self.counter}'
        self.publisher.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.counter += 1


def main(args=None):
    rclpy.init(args=args)
    node = StringPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### 실행 방법

```bash
# setup.py에 등록
entry_points={
    'console_scripts': [
        'string_publisher = <package_name>.string_publisher:main',
    ],
}

# 빌드 및 실행
colcon build --packages-select <package_name>
source install/setup.bash
ros2 run <package_name> string_publisher

# 토픽 확인
ros2 topic echo /chatter
```

---

## 2. Subscriber Node (구독자)

**용도**: 토픽에서 데이터를 받아서 처리
**예시**: 센서 데이터 수신, 명령 수신

### Python 템플릿

```python
import rclpy
from rclpy.node import Node
from <msg_package>.msg import <MessageType>


class <ClassName>(Node):
    def __init__(self):
        super().__init__('<node_name>')

        # Subscriber 생성
        self.subscription = self.create_subscription(
            <MessageType>,
            '<topic_name>',
            self.listener_callback,
            <queue_size>)

        self.get_logger().info('<ClassName> started')

    def listener_callback(self, msg):
        """메시지를 받을 때마다 호출되는 콜백 함수"""
        self.get_logger().info(f'Received: {msg.<field_name>}')

        # 여기서 받은 데이터 처리
        self.process_data(msg)

    def process_data(self, msg):
        """받은 데이터를 처리하는 함수"""
        # 실제 처리 로직 구현
        pass


def main(args=None):
    rclpy.init(args=args)
    node = <ClassName>()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### 구체적 예시: 문자열 수신

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class StringSubscriber(Node):
    def __init__(self):
        super().__init__('string_subscriber')

        self.subscription = self.create_subscription(
            String,
            'chatter',
            self.listener_callback,
            10)

        self.get_logger().info('StringSubscriber started')

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')

        # 데이터 처리 예시
        if 'Hello' in msg.data:
            self.get_logger().info('Greeting detected!')


def main(args=None):
    rclpy.init(args=args)
    node = StringSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

---

## 3. Pub-Sub Node (파이프라인)

**용도**: 데이터를 받아서 처리한 후 다시 발행 (데이터 파이프라인)
**예시**: 이미지 필터링, 센서 데이터 변환, 물체 감지

### Python 템플릿

```python
import rclpy
from rclpy.node import Node
from <input_msg_package>.msg import <InputMessageType>
from <output_msg_package>.msg import <OutputMessageType>


class <ClassName>(Node):
    def __init__(self):
        super().__init__('<node_name>')

        # Subscriber 생성 (입력)
        self.subscription = self.create_subscription(
            <InputMessageType>,
            '<input_topic>',
            self.callback,
            <queue_size>)

        # Publisher 생성 (출력)
        self.publisher = self.create_publisher(
            <OutputMessageType>,
            '<output_topic>',
            <queue_size>)

        self.get_logger().info('<ClassName> started')

    def callback(self, input_msg):
        """입력 받아서 처리 후 발행"""
        # 데이터 처리
        processed_data = self.process(input_msg)

        # 출력 메시지 생성
        output_msg = <OutputMessageType>()
        output_msg.<field_name> = processed_data

        # 발행
        self.publisher.publish(output_msg)
        self.get_logger().info(f'Processed and published')

    def process(self, input_msg):
        """실제 데이터 처리 로직"""
        # 처리 로직 구현
        result = input_msg.<field_name>  # 예시
        return result


def main(args=None):
    rclpy.init(args=args)
    node = <ClassName>()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### 구체적 예시: 대문자 변환기

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class UppercaseConverter(Node):
    def __init__(self):
        super().__init__('uppercase_converter')

        self.subscription = self.create_subscription(
            String,
            'input_text',
            self.callback,
            10)

        self.publisher = self.create_publisher(
            String,
            'output_text',
            10)

        self.get_logger().info('UppercaseConverter started')

    def callback(self, input_msg):
        # 대문자로 변환
        uppercase_text = input_msg.data.upper()

        # 결과 발행
        output_msg = String()
        output_msg.data = uppercase_text
        self.publisher.publish(output_msg)

        self.get_logger().info(f'"{input_msg.data}" -> "{uppercase_text}"')


def main(args=None):
    rclpy.init(args=args)
    node = UppercaseConverter()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

---

## 4. Timer Node (주기 실행)

**용도**: Publisher 없이 주기적으로 작업 실행
**예시**: 상태 체크, 로깅, 주기적 계산

### Python 템플릿

```python
import rclpy
from rclpy.node import Node


class <ClassName>(Node):
    def __init__(self):
        super().__init__('<node_name>')

        # 타이머 생성 (주기: <timer_period> 초)
        timer_period = <timer_period>
        self.timer = self.create_timer(timer_period, self.timer_callback)

        # 상태 변수
        self.counter = 0

        self.get_logger().info('<ClassName> started')

    def timer_callback(self):
        """주기적으로 실행되는 작업"""
        self.counter += 1
        self.get_logger().info(f'Timer callback #{self.counter}')

        # 실제 작업 수행
        self.do_work()

    def do_work(self):
        """실제 수행할 작업"""
        # 작업 로직 구현
        pass


def main(args=None):
    rclpy.init(args=args)
    node = <ClassName>()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### 구체적 예시: 시스템 상태 체크

```python
import rclpy
from rclpy.node import Node
import psutil


class SystemMonitor(Node):
    def __init__(self):
        super().__init__('system_monitor')

        # 5초마다 체크
        timer_period = 5.0
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.get_logger().info('SystemMonitor started')

    def timer_callback(self):
        # CPU 사용률 체크
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent

        self.get_logger().info(
            f'CPU: {cpu_percent}%, Memory: {memory_percent}%')

        # 경고 체크
        if cpu_percent > 80:
            self.get_logger().warn('High CPU usage!')


def main(args=None):
    rclpy.init(args=args)
    node = SystemMonitor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

---

## 5. Service Server Node

**용도**: 클라이언트의 요청을 받아서 응답 반환
**예시**: 위치 조회, 계산 수행, 설정 변경

### Python 템플릿

```python
import rclpy
from rclpy.node import Node
from <srv_package>.srv import <ServiceType>


class <ClassName>(Node):
    def __init__(self):
        super().__init__('<node_name>')

        # Service Server 생성
        self.srv = self.create_service(
            <ServiceType>,
            '<service_name>',
            self.service_callback)

        self.get_logger().info('<ClassName> ready')

    def service_callback(self, request, response):
        """서비스 요청 처리"""
        self.get_logger().info(f'Received request: {request.<field_name>}')

        # 요청 처리
        result = self.process_request(request)

        # 응답 설정
        response.<field_name> = result

        self.get_logger().info(f'Sending response: {response.<field_name>}')
        return response

    def process_request(self, request):
        """실제 요청 처리 로직"""
        # 처리 로직 구현
        result = None  # 예시
        return result


def main(args=None):
    rclpy.init(args=args)
    node = <ClassName>()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### 구체적 예시: 두 수 더하기 서비스

```python
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class AdditionServer(Node):
    def __init__(self):
        super().__init__('addition_server')

        self.srv = self.create_service(
            AddTwoInts,
            'add_two_ints',
            self.add_callback)

        self.get_logger().info('Addition service ready')

    def add_callback(self, request, response):
        self.get_logger().info(
            f'Request: {request.a} + {request.b}')

        # 계산 수행
        response.sum = request.a + request.b

        self.get_logger().info(f'Response: {response.sum}')
        return response


def main(args=None):
    rclpy.init(args=args)
    node = AdditionServer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### 테스트 방법

```bash
# 서버 실행
ros2 run <package_name> addition_server

# 다른 터미널에서 서비스 호출
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 5, b: 3}"
```

---

## 6. Service Client Node

**용도**: 서비스 서버에 요청을 보내고 응답 받기
**예시**: 위치 요청, 계산 요청, 설정 변경 요청

### Python 템플릿

```python
import rclpy
from rclpy.node import Node
from <srv_package>.srv import <ServiceType>


class <ClassName>(Node):
    def __init__(self):
        super().__init__('<node_name>')

        # Service Client 생성
        self.client = self.create_client(
            <ServiceType>,
            '<service_name>')

        # 서비스 서버가 준비될 때까지 대기
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for service...')

        self.get_logger().info('<ClassName> ready')

    def send_request(self, <param_name>):
        """서비스 요청 보내기"""
        # 요청 객체 생성
        request = <ServiceType>.Request()
        request.<field_name> = <param_name>

        self.get_logger().info(f'Sending request: {request.<field_name>}')

        # 비동기 요청
        future = self.client.call_async(request)
        return future


def main(args=None):
    rclpy.init(args=args)
    node = <ClassName>()

    # 요청 보내기
    future = node.send_request(<value>)

    # 응답 대기
    rclpy.spin_until_future_complete(node, future)

    if future.result() is not None:
        response = future.result()
        node.get_logger().info(f'Response: {response.<field_name>}')
    else:
        node.get_logger().error('Service call failed')

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### 구체적 예시: 덧셈 요청 클라이언트

```python
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts
import sys


class AdditionClient(Node):
    def __init__(self):
        super().__init__('addition_client')

        self.client = self.create_client(AddTwoInts, 'add_two_ints')

        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for addition service...')

        self.get_logger().info('AdditionClient ready')

    def send_request(self, a, b):
        request = AddTwoInts.Request()
        request.a = a
        request.b = b

        self.get_logger().info(f'Requesting: {a} + {b}')

        future = self.client.call_async(request)
        return future


def main(args=None):
    rclpy.init(args=args)

    # 명령줄 인자로 숫자 받기
    if len(sys.argv) < 3:
        print('Usage: ros2 run <pkg> addition_client <num1> <num2>')
        return

    a = int(sys.argv[1])
    b = int(sys.argv[2])

    node = AdditionClient()
    future = node.send_request(a, b)

    rclpy.spin_until_future_complete(node, future)

    if future.result() is not None:
        response = future.result()
        node.get_logger().info(f'Result: {a} + {b} = {response.sum}')
    else:
        node.get_logger().error('Service call failed')

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### 실행 방법

```bash
# 서버 먼저 실행 (다른 터미널)
ros2 run <package_name> addition_server

# 클라이언트 실행
ros2 run <package_name> addition_client 10 25
```

---

## 7. Action Server Node

**용도**: 장시간 작업 수행 + 진행 상황 피드백
**예시**: 로봇 네비게이션, 파일 다운로드, 복잡한 계산

### Python 템플릿

```python
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from <action_package>.action import <ActionType>
import time


class <ClassName>(Node):
    def __init__(self):
        super().__init__('<node_name>')

        # Action Server 생성
        self._action_server = ActionServer(
            self,
            <ActionType>,
            '<action_name>',
            self.execute_callback)

        self.get_logger().info('<ClassName> ready')

    def execute_callback(self, goal_handle):
        """액션 실행 콜백"""
        self.get_logger().info('Executing goal...')

        # 피드백 객체 생성
        feedback_msg = <ActionType>.Feedback()

        # 작업 수행 (예: 10단계)
        for i in range(1, 11):
            # 작업 수행
            time.sleep(0.5)

            # 피드백 전송
            feedback_msg.<progress_field> = i * 10
            goal_handle.publish_feedback(feedback_msg)
            self.get_logger().info(f'Progress: {i * 10}%')

            # 취소 요청 체크
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal canceled')
                return <ActionType>.Result()

        # 성공
        goal_handle.succeed()

        # 결과 반환
        result = <ActionType>.Result()
        result.<result_field> = <final_value>
        self.get_logger().info('Goal succeeded!')

        return result


def main(args=None):
    rclpy.init(args=args)
    node = <ClassName>()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### 구체적 예시: 피보나치 수열 생성

```python
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from example_interfaces.action import Fibonacci
import time


class FibonacciActionServer(Node):
    def __init__(self):
        super().__init__('fibonacci_action_server')

        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            self.execute_callback)

        self.get_logger().info('Fibonacci action server ready')

    def execute_callback(self, goal_handle):
        self.get_logger().info(f'Executing goal: order={goal_handle.request.order}')

        feedback_msg = Fibonacci.Feedback()
        feedback_msg.sequence = [0, 1]

        # 피보나치 수열 생성
        for i in range(1, goal_handle.request.order):
            # 취소 체크
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                return Fibonacci.Result()

            # 다음 수 계산
            feedback_msg.sequence.append(
                feedback_msg.sequence[i] + feedback_msg.sequence[i - 1])

            # 피드백 전송
            goal_handle.publish_feedback(feedback_msg)
            self.get_logger().info(f'Feedback: {feedback_msg.sequence}')

            time.sleep(0.5)

        # 성공
        goal_handle.succeed()

        result = Fibonacci.Result()
        result.sequence = feedback_msg.sequence
        return result


def main(args=None):
    rclpy.init(args=args)
    node = FibonacciActionServer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

---

## 8. Action Client Node

**용도**: 액션 서버에 작업 요청 + 진행 상황 모니터링
**예시**: 네비게이션 명령, 작업 진행도 확인

### Python 템플릿

```python
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from <action_package>.action import <ActionType>


class <ClassName>(Node):
    def __init__(self):
        super().__init__('<node_name>')

        # Action Client 생성
        self._action_client = ActionClient(
            self,
            <ActionType>,
            '<action_name>')

        self.get_logger().info('<ClassName> ready')

    def send_goal(self, <goal_param>):
        """액션 목표 전송"""
        self.get_logger().info('Waiting for action server...')
        self._action_client.wait_for_server()

        # 목표 생성
        goal_msg = <ActionType>.Goal()
        goal_msg.<goal_field> = <goal_param>

        self.get_logger().info(f'Sending goal: {goal_msg.<goal_field>}')

        # 목표 전송
        send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback)

        send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        """목표 수락/거부 응답 처리"""
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return

        self.get_logger().info('Goal accepted')

        # 결과 대기
        get_result_future = goal_handle.get_result_async()
        get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback_msg):
        """피드백 수신"""
        feedback = feedback_msg.feedback
        self.get_logger().info(f'Feedback: {feedback.<progress_field>}')

    def get_result_callback(self, future):
        """최종 결과 수신"""
        result = future.result().result
        self.get_logger().info(f'Result: {result.<result_field>}')


def main(args=None):
    rclpy.init(args=args)
    node = <ClassName>()
    node.send_goal(<goal_value>)
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### 구체적 예시: 피보나치 클라이언트

```python
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from example_interfaces.action import Fibonacci


class FibonacciActionClient(Node):
    def __init__(self):
        super().__init__('fibonacci_action_client')

        self._action_client = ActionClient(
            self,
            Fibonacci,
            'fibonacci')

    def send_goal(self, order):
        self.get_logger().info('Waiting for action server...')
        self._action_client.wait_for_server()

        goal_msg = Fibonacci.Goal()
        goal_msg.order = order

        self.get_logger().info(f'Sending goal: order={order}')

        send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback)

        send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return

        self.get_logger().info('Goal accepted')

        get_result_future = goal_handle.get_result_async()
        get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(f'Received feedback: {feedback.sequence}')

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Final result: {result.sequence}')
        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    node = FibonacciActionClient()
    node.send_goal(10)  # 10번째까지 피보나치 수열
    rclpy.spin(node)


if __name__ == '__main__':
    main()
```

---

## 9. Parameter Node (설정 가능)

**용도**: 런타임에 설정값 변경 가능한 노드
**예시**: 속도 제한, PID 계수, 임계값 등 동적 조정

### Python 템플릿

```python
import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import ParameterDescriptor


class <ClassName>(Node):
    def __init__(self):
        super().__init__('<node_name>')

        # 파라미터 선언 (기본값과 설명)
        self.declare_parameter(
            '<param_name_1>',
            <default_value_1>,
            ParameterDescriptor(description='<param_description_1>'))

        self.declare_parameter(
            '<param_name_2>',
            <default_value_2>,
            ParameterDescriptor(description='<param_description_2>'))

        # 파라미터 변경 콜백 등록
        self.add_on_set_parameters_callback(self.parameters_callback)

        # 타이머로 주기적으로 파라미터 사용
        self.timer = self.create_timer(1.0, self.timer_callback)

        self.get_logger().info('<ClassName> started')

    def timer_callback(self):
        """파라미터를 사용하는 주기적 작업"""
        # 파라미터 값 가져오기
        param1 = self.get_parameter('<param_name_1>').value
        param2 = self.get_parameter('<param_name_2>').value

        self.get_logger().info(
            f'Using params: {param1}, {param2}')

        # 파라미터를 사용한 작업 수행
        self.do_work(param1, param2)

    def parameters_callback(self, params):
        """파라미터가 변경될 때 호출"""
        for param in params:
            self.get_logger().info(
                f'Parameter changed: {param.name} = {param.value}')

        return rclpy.parameter.SetParametersResult(successful=True)

    def do_work(self, param1, param2):
        """실제 작업 수행"""
        # 작업 로직 구현
        pass


def main(args=None):
    rclpy.init(args=args)
    node = <ClassName>()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### 구체적 예시: 속도 제어 노드

```python
import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import ParameterDescriptor
from geometry_msgs.msg import Twist


class VelocityController(Node):
    def __init__(self):
        super().__init__('velocity_controller')

        # 파라미터 선언
        self.declare_parameter(
            'max_linear_speed',
            1.0,
            ParameterDescriptor(description='Maximum linear speed (m/s)'))

        self.declare_parameter(
            'max_angular_speed',
            1.5,
            ParameterDescriptor(description='Maximum angular speed (rad/s)'))

        # 파라미터 변경 콜백
        self.add_on_set_parameters_callback(self.parameters_callback)

        # Publisher
        self.publisher = self.create_publisher(Twist, 'cmd_vel', 10)

        # Timer
        self.timer = self.create_timer(1.0, self.timer_callback)

        self.get_logger().info('VelocityController started')

    def timer_callback(self):
        # 파라미터 값 가져오기
        max_linear = self.get_parameter('max_linear_speed').value
        max_angular = self.get_parameter('max_angular_speed').value

        # 속도 명령 생성 (예시)
        msg = Twist()
        msg.linear.x = max_linear * 0.5  # 최대 속도의 50%
        msg.angular.z = max_angular * 0.3

        self.publisher.publish(msg)
        self.get_logger().info(
            f'Publishing vel: linear={msg.linear.x:.2f}, angular={msg.angular.z:.2f}')

    def parameters_callback(self, params):
        for param in params:
            if param.name == 'max_linear_speed':
                if param.value <= 0:
                    self.get_logger().error('max_linear_speed must be > 0')
                    return rclpy.parameter.SetParametersResult(successful=False)

            self.get_logger().info(f'{param.name} changed to {param.value}')

        return rclpy.parameter.SetParametersResult(successful=True)


def main(args=None):
    rclpy.init(args=args)
    node = VelocityController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### 파라미터 사용 방법

```bash
# 노드 실행
ros2 run <package_name> velocity_controller

# 파라미터 목록 확인
ros2 param list

# 파라미터 값 확인
ros2 param get /velocity_controller max_linear_speed

# 파라미터 값 변경 (런타임)
ros2 param set /velocity_controller max_linear_speed 2.5

# YAML 파일로 파라미터 설정
ros2 run <package_name> velocity_controller --ros-args --params-file params.yaml
```

### params.yaml 예시

```yaml
velocity_controller:
  ros__parameters:
    max_linear_speed: 2.0
    max_angular_speed: 3.0
```

---

## 10. Lifecycle Node (생명주기 관리)

**용도**: 명확한 상태 전환이 필요한 노드 (초기화, 활성화, 비활성화, 종료)
**예시**: 하드웨어 드라이버, 센서 관리, 복잡한 시스템

### Python 템플릿

```python
import rclpy
from rclpy.lifecycle import Node, State, TransitionCallbackReturn


class <ClassName>(Node):
    def __init__(self, node_name='<node_name>'):
        super().__init__(node_name)
        self.get_logger().info(f'{node_name} created')

    def on_configure(self, state: State) -> TransitionCallbackReturn:
        """Configure 상태로 전환될 때 호출"""
        self.get_logger().info('Configuring...')

        # 초기화 작업 (파라미터 로드, 리소스 할당 등)
        # 예: Publisher/Subscriber 생성

        self.get_logger().info('Configuration complete')
        return TransitionCallbackReturn.SUCCESS

    def on_activate(self, state: State) -> TransitionCallbackReturn:
        """Activate 상태로 전환될 때 호출"""
        self.get_logger().info('Activating...')

        # 활성화 작업 (센서 시작, 타이머 시작 등)

        self.get_logger().info('Activation complete')
        return super().on_activate(state)

    def on_deactivate(self, state: State) -> TransitionCallbackReturn:
        """Deactivate 상태로 전환될 때 호출"""
        self.get_logger().info('Deactivating...')

        # 비활성화 작업 (센서 중지, 타이머 중지 등)

        self.get_logger().info('Deactivation complete')
        return super().on_deactivate(state)

    def on_cleanup(self, state: State) -> TransitionCallbackReturn:
        """Cleanup 상태로 전환될 때 호출"""
        self.get_logger().info('Cleaning up...')

        # 정리 작업 (리소스 해제 등)

        self.get_logger().info('Cleanup complete')
        return TransitionCallbackReturn.SUCCESS

    def on_shutdown(self, state: State) -> TransitionCallbackReturn:
        """Shutdown 상태로 전환될 때 호출"""
        self.get_logger().info('Shutting down...')

        # 종료 작업

        self.get_logger().info('Shutdown complete')
        return TransitionCallbackReturn.SUCCESS


def main(args=None):
    rclpy.init(args=args)
    node = <ClassName>()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### 구체적 예시: 센서 드라이버

```python
import rclpy
from rclpy.lifecycle import Node, State, TransitionCallbackReturn
from std_msgs.msg import String


class SensorDriver(Node):
    def __init__(self):
        super().__init__('sensor_driver')

        self.publisher = None
        self.timer = None
        self.counter = 0

        self.get_logger().info('SensorDriver created')

    def on_configure(self, state: State) -> TransitionCallbackReturn:
        self.get_logger().info('Configuring sensor driver...')

        # Publisher 생성
        self.publisher = self.create_lifecycle_publisher(
            String,
            'sensor_data',
            10)

        self.get_logger().info('Sensor configured')
        return TransitionCallbackReturn.SUCCESS

    def on_activate(self, state: State) -> TransitionCallbackReturn:
        self.get_logger().info('Activating sensor...')

        # 타이머 시작 (센서 읽기)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.counter = 0

        self.get_logger().info('Sensor activated')
        return super().on_activate(state)

    def on_deactivate(self, state: State) -> TransitionCallbackReturn:
        self.get_logger().info('Deactivating sensor...')

        # 타이머 중지
        if self.timer:
            self.timer.cancel()
            self.timer = None

        self.get_logger().info('Sensor deactivated')
        return super().on_deactivate(state)

    def on_cleanup(self, state: State) -> TransitionCallbackReturn:
        self.get_logger().info('Cleaning up sensor...')

        # Publisher 제거
        self.destroy_publisher(self.publisher)
        self.publisher = None

        self.get_logger().info('Cleanup complete')
        return TransitionCallbackReturn.SUCCESS

    def on_shutdown(self, state: State) -> TransitionCallbackReturn:
        self.get_logger().info('Shutting down sensor driver')
        return TransitionCallbackReturn.SUCCESS

    def timer_callback(self):
        """센서 데이터 읽기 및 발행"""
        if self.publisher and self.publisher.is_activated:
            msg = String()
            msg.data = f'Sensor reading #{self.counter}'
            self.publisher.publish(msg)
            self.counter += 1


def main(args=None):
    rclpy.init(args=args)
    node = SensorDriver()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Lifecycle Node 제어 방법

```bash
# 노드 실행
ros2 run <package_name> sensor_driver

# 다른 터미널에서 상태 전환 명령

# Configure
ros2 lifecycle set /sensor_driver configure

# Activate (데이터 발행 시작)
ros2 lifecycle set /sensor_driver activate

# Deactivate (데이터 발행 중지)
ros2 lifecycle set /sensor_driver deactivate

# Cleanup
ros2 lifecycle set /sensor_driver cleanup

# Shutdown
ros2 lifecycle set /sensor_driver shutdown

# 현재 상태 확인
ros2 lifecycle get /sensor_driver
```

---

## 노드 패턴 선택 가이드

| 패턴 | 사용 시기 |
|------|---------|
| **Publisher** | 주기적으로 데이터 발행 (센서, 상태) |
| **Subscriber** | 데이터 수신 및 처리 |
| **Pub-Sub** | 데이터 변환/필터링 파이프라인 |
| **Timer** | 주기적 작업 (발행 없이) |
| **Service Server** | 요청-응답 패턴 (빠른 작업) |
| **Service Client** | 다른 노드에 요청 보내기 |
| **Action Server** | 장시간 작업 + 진행 피드백 |
| **Action Client** | 장시간 작업 요청 |
| **Parameter** | 런타임 설정 변경 필요 |
| **Lifecycle** | 명확한 상태 관리 필요 (드라이버) |

---

## setup.py 등록 예시

모든 노드를 setup.py에 등록해야 실행 가능합니다:

```python
from setuptools import setup

package_name = 'my_robot_pkg'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='your@email.com',
    description='ROS2 node templates',
    license='Apache-2.0',
    extras_require={
        'test': ['pytest'],
    },
    entry_points={
        'console_scripts': [
            'string_publisher = my_robot_pkg.string_publisher:main',
            'string_subscriber = my_robot_pkg.string_subscriber:main',
            'uppercase_converter = my_robot_pkg.uppercase_converter:main',
            'system_monitor = my_robot_pkg.system_monitor:main',
            'addition_server = my_robot_pkg.addition_server:main',
            'addition_client = my_robot_pkg.addition_client:main',
            'fibonacci_server = my_robot_pkg.fibonacci_server:main',
            'fibonacci_client = my_robot_pkg.fibonacci_client:main',
            'velocity_controller = my_robot_pkg.velocity_controller:main',
            'sensor_driver = my_robot_pkg.sensor_driver:main',
        ],
    },
)
```

---

## 다음 단계

- [메시지/서비스/액션 정의 가이드](ROS2_MSG_SRV_ACTION_GUIDE.md)
- [Launch 파일 가이드](ROS2_PACKAGE_TEMPLATE_GUIDE.md#3단계-launch-파일-추가)
- [C++ 노드 템플릿](ROS2_CPP_PACKAGE_GUIDE.md)

이 템플릿들을 복사해서 사용하고, 필요에 맞게 수정하세요!
