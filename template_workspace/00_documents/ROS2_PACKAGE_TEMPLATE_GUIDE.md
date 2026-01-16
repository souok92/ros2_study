# ROS2 Python 패키지 생성 완벽 가이드

이 가이드는 ROS2 Python 패키지를 처음부터 올바르게 생성하는 방법을 단계별로 설명합니다.

---

## ROS2 패키지 개발 순서

ROS2 패키지는 다음 순서로 개발합니다:

### 1. 패키지 골격 생성 (`ros2 pkg create`)
- **목적**: 기본 폴더 구조와 설정 파일을 자동으로 생성
- **생성되는 것**: setup.py, package.xml, setup.cfg, resource/, test/, 기본 노드 파일
- **왜 먼저?**: ROS2가 인식할 수 있는 올바른 구조를 자동으로 만들어줌

### 2. 코드 작성 및 파일 추가
- **목적**: 실제 로봇 기능을 구현
- **작업**: 노드 파일 작성/수정, launch 파일 추가, config 파일 추가
- **주의**: 생성된 패키지 **안에서** 작업해야 함

### 3. 설정 파일 수정 (setup.py)
- **목적**: 새로 추가한 파일들을 ROS2가 인식하도록 등록
- **작업**: entry_points에 노드 등록, data_files에 launch/config 파일 등록
- **중요**: 등록하지 않으면 빌드해도 실행 안 됨!

### 4. 빌드 및 테스트
- **목적**: 작성한 코드를 실행 가능한 형태로 변환
- **작업**: `colcon build`, `source install/setup.bash`, 실행 및 테스트
- **반복**: 문제 발견 → 수정 → 재빌드 → 재테스트

### 왜 이 순서가 중요한가?
- `ros2 pkg create`가 만들어주는 기본 구조는 ROS2 규칙에 맞춰져 있음
- 처음부터 올바른 구조에서 시작하면 실수를 줄일 수 있음
- setup.py의 설정이 복잡하므로 자동 생성된 것을 수정하는 게 안전함

---

## 1단계: 기본 패키지 생성

**이 단계의 목적**: ROS2가 인식할 수 있는 올바른 패키지 구조를 자동으로 생성합니다.

**왜 이 명령어를 사용하나?**
- 수동으로 만들면 폴더 구조나 설정 파일에서 실수하기 쉬움
- `ros2 pkg create`는 ROS2 규칙에 맞는 템플릿을 자동 생성
- setup.py, package.xml 등의 복잡한 설정을 자동으로 작성
- 추후에는 `package.xml`, `setup.py` 에 추가한 후 `colcon build`를 통해서 의존성, 노드 업데이트 가능
### 명령어:
```bash
cd <workspace_path>/src
ros2 pkg create --build-type ament_python <package_name> \
  --dependencies <dependencies> \
  --node-name <node_name> \
  --maintainer-name "<maintainer_name>" \
  --maintainer-email "<maintainer_email>" \
  --license <license>
```

### 예시:
```bash
cd ~/10_delto_ws/src
ros2 pkg create --build-type ament_python my_robot_pkg \
  --dependencies rclpy std_msgs sensor_msgs geometry_msgs \
  --node-name my_node \
  --maintainer-name "Your Name" \
  --maintainer-email "your@email.com" \
  --license Apache-2.0
```

### 생성되는 폴더 구조:
```
<package_name>/
├── <package_name>/
│   ├── __init__.py
│   └── <node_name>.py          # --node-name으로 생성된 노드
├── resource/
│   └── <package_name>          # 빈 파일 (패키지 마커)
├── test/
│   ├── test_copyright.py
│   ├── test_flake8.py
│   └── test_pep257.py
├── package.xml
├── setup.cfg
└── setup.py
```

### 생성된 파일 내용 예시:

#### `setup.py`:
```python
from setuptools import setup

package_name = '<package_name>'

setup(
    name=package_name,
    version='<version>',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='<maintainer_name>',
    maintainer_email='<maintainer_email>',
    description='<package_description>',
    license='<license>',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            '<node_name> = <package_name>.<node_name>:main'
        ],
    },
)
```

#### `<package_name>/__init__.py`:
```python
# 비어있음 (또는 패키지 초기화 코드)
```

#### `<package_name>/<node_name>.py`:
```python
def main():
    print('Hi from <package_name>.')


if __name__ == '__main__':
    main()
```

---

## 2단계: 추가 노드 파일 작성

**이 단계의 목적**: 실제 로봇 기능을 구현하는 노드들을 추가합니다.

**언제 필요한가?**
- 1단계에서 만든 기본 노드만으로는 부족할 때
- Publisher, Subscriber, Service 등 여러 역할의 노드가 필요할 때
- 기능별로 노드를 분리하고 싶을 때

**주의사항**:
- 노드 파일은 반드시 `<package_name>/` 디렉토리 안에 작성
- 파일을 만들기만 하면 안 되고, setup.py에 **반드시 등록**해야 함

### 새 노드 파일 생성:
```bash
cd <workspace_path>/src/<package_name>/<package_name>
touch <node_name_2>.py
touch <node_name_3>.py
```

### 폴더 구조:
```
<package_name>/
├── <package_name>/
│   ├── __init__.py
│   ├── <node_name>.py
│   ├── <node_name_2>.py    # 새로 추가
│   └── <node_name_3>.py    # 새로 추가
├── resource/
├── test/
├── package.xml
├── setup.cfg
└── setup.py
```

### `setup.py`에 새 노드 등록:
```python
entry_points={
    'console_scripts': [
        '<node_name> = <package_name>.<node_name>:main',
        '<node_name_2> = <package_name>.<node_name_2>:main',
        '<node_name_3> = <package_name>.<node_name_3>:main',
    ],
},
```

```bash
ros2 run <package_name> <node_name> // 노드 실행
```

---

## 3단계: Launch 파일 추가

**이 단계의 목적**: 여러 노드를 한 번에 실행하고 설정을 관리합니다.

**왜 필요한가?**
- 노드를 하나씩 `ros2 run`으로 실행하면 번거로움
- Launch 파일로 여러 노드를 한 번에 실행 가능
- 노드별 파라미터, 네임스페이스 등을 중앙에서 관리

**중요**:
- Launch 파일은 `launch/` 디렉토리에 작성 (패키지 루트에)
- setup.py의 `data_files`에 등록해야 빌드 후 사용 가능
- 등록 안 하면 `ros2 launch`로 찾을 수 없음!

### Launch 디렉토리 생성:
```bash
cd <workspace_path>/src/<package_name>
mkdir launch
touch launch/<launch_file_name>.launch.py
```

### 폴더 구조:
```
<package_name>/
├── <package_name>/
├── launch/
│   └── <launch_file_name>.launch.py  # 새로 추가
├── resource/
├── test/
├── package.xml
├── setup.cfg
└── setup.py
```

### `setup.py`에 launch 파일 등록:
```python
import os
from glob import glob

setup(
    # ... 기존 내용 ...
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Launch 파일 추가
        ('share/' + package_name + '/launch',
            glob('launch/*.launch.py')),
    ],
    # ... 나머지 내용 ...
)
```

### `launch/<launch_file_name>.launch.py` 예시:
```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='<package_name>',
            executable='<node_name_2>',
            name='<node_instance_name_1>',
            output='screen',
        ),
        Node(
            package='<package_name>',
            executable='<node_name_3>',
            name='<node_instance_name_2>',
            output='screen',
        ),
    ])
```

---

## 4단계: Config 파일 추가 (파라미터)

**이 단계의 목적**: 노드의 설정값(파라미터)을 외부 파일로 관리합니다.

**왜 필요한가?**
- 코드를 수정하지 않고 파라미터 값만 변경 가능
- 환경별(개발/테스트/운영)로 다른 설정 사용 가능
- 여러 노드의 설정을 한 곳에서 관리

**언제 사용?**
- 노드에서 조정 가능한 값이 있을 때 (속도, 주기, 임계값 등)
- 같은 코드로 다른 설정을 사용해야 할 때
- 하드코딩을 피하고 싶을 때

**주의**:
- Config 파일도 setup.py에 등록 필수
- YAML 문법 주의 (들여쓰기, 콜론 뒤 공백)

### Config 디렉토리 생성:
```bash
cd <workspace_path>/src/<package_name>
mkdir config
touch config/<config_file_name>.yaml
```

### 폴더 구조:
```
<package_name>/
├── <package_name>/
├── launch/
├── config/
│   └── <config_file_name>.yaml          # 새로 추가
├── resource/
├── test/
├── package.xml
├── setup.cfg
└── setup.py
```

### `setup.py`에 config 파일 등록:
```python
data_files=[
    ('share/ament_index/resource_index/packages',
        ['resource/' + package_name]),
    ('share/' + package_name, ['package.xml']),
    ('share/' + package_name + '/launch',
        glob('launch/*.launch.py')),
    # Config 파일 추가
    ('share/' + package_name + '/config',
        glob('config/*.yaml')),
],
```

### `config/<config_file_name>.yaml` 예시:
```yaml
<node_name>:
  ros__parameters:
    <param_name_1>: <param_value_1>
    <param_name_2>: <param_value_2>
    <param_name_3>: "<param_value_3>"
```

### 노드 코드에서 파라미터 사용:

파라미터를 사용하려면 노드의 `__init__`에서 파라미터를 선언하고 값을 가져와야 합니다.

```python
class MyNode(Node):
    def __init__(self):
        super().__init__('<node_name>')

        # 파라미터 선언 (이름, 기본값)
        self.declare_parameter('<param_name_1>', <default_value>)
        self.declare_parameter('<param_name_2>', <default_value>)

        # 파라미터 값 가져오기
        param1 = self.get_parameter('<param_name_1>').get_parameter_value().double_value  # float
        param2 = self.get_parameter('<param_name_2>').get_parameter_value().string_value  # string
        param3 = self.get_parameter('<param_name_3>').get_parameter_value().integer_value # int

        # 가져온 값으로 초기화
        self.publisher = self.create_publisher(String, param2, 10)
        self.timer = self.create_timer(1.0 / param1, self.callback)
```

**파라미터 타입별 접근 방법:**
- **float/double**: `.get_parameter_value().double_value`
- **string**: `.get_parameter_value().string_value`
- **int**: `.get_parameter_value().integer_value`
- **bool**: `.get_parameter_value().bool_value`

### Launch 파일에서 config 로드:

Launch 파일에서 config 파일을 노드에 전달해야 합니다.

```python
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    # Config 파일 경로 가져오기
    config_dir = get_package_share_directory('<package_name>')
    config_file = os.path.join(config_dir, 'config', '<config_file_name>.yaml')

    return LaunchDescription([
        Node(
            package='<package_name>',
            executable='<node_name>',
            name='<node_instance_name>',
            output='screen',
            parameters=[config_file],  # Config 파일 전달
        ),
    ])
```

### 런타임 파라미터 변경 (선택사항 - 고급):

기본적으로 파라미터는 **노드 시작 시에만** 로드됩니다. 런타임에 파라미터를 변경하고 즉시 반영하려면 **파라미터 콜백**을 등록해야 합니다.

#### 필요한 import:

```python
from rclpy.parameter import Parameter
from rcl_interfaces.msg import SetParametersResult
```

#### 전체 예시 코드 (템플릿):

```python
class <DynamicNodeClass>(Node):
    def __init__(self):
        super().__init__('<node_name>')

        # 파라미터 선언
        self.declare_parameter('<param_name_1>', <default_value_1>)
        self.declare_parameter('<param_name_2>', <default_value_2>)

        # 초기값 가져오기
        self.<param_var_1> = self.get_parameter('<param_name_1>').get_parameter_value().<type_value_1>
        self.<param_var_2> = self.get_parameter('<param_name_2>').get_parameter_value().<type_value_2>

        # 리소스 생성 (예: timer, publisher 등)
        self.<resource> = self.<create_resource>(self.<param_var_1>)

        # 파라미터 콜백 등록 (런타임 변경 감지)
        self.add_on_set_parameters_callback(self.parameter_callback)

    def parameter_callback(self, params):
        """
        런타임에 파라미터가 변경되면 호출됩니다.
        노드 재시작 없이 파라미터 변경을 즉시 반영할 수 있습니다.
        """
        for param in params:
            # 파라미터 이름과 타입 확인
            if param.name == '<param_name_1>' and param.type_ == Parameter.Type.<PARAM_TYPE>:
                new_value = param.value

                # 유효성 검사 (선택사항)
                if not self.validate_<param_name>(new_value):
                    self.get_logger().error(f'Invalid value: {new_value}')
                    return SetParametersResult(successful=False)

                # 리소스 재생성 또는 업데이트
                self.<resource>.cancel()  # 기존 리소스 해제
                self.<resource> = self.<create_resource>(new_value)  # 새 값으로 재생성
                self.<param_var_1> = new_value

                self.get_logger().info(f'Updated <param_name_1> to {new_value}')

            elif param.name == '<param_name_2>' and param.type_ == Parameter.Type.<PARAM_TYPE>:
                # 단순 변수 업데이트 (리소스 재생성 불필요한 경우)
                self.<param_var_2> = param.value
                self.get_logger().info(f'Updated <param_name_2> to {param.value}')

        return SetParametersResult(successful=True)
```

#### 런타임 파라미터 변경 명령어:

```bash
# 노드 실행
ros2 run <package_name> <node_name>

# 다른 터미널에서 파라미터 변경 (즉시 반영!)
ros2 param set /<node_name> <param_name> <new_value>
ros2 param set /dynamic_talker publish_frequency 5.0

# 현재 파라미터 확인
ros2 param list /<node_name>
ros2 param get /<node_name> <param_name>
```

#### 파라미터 타입 참조:

| ROS2 타입 | Python 타입 | 값 접근 | Parameter.Type |
|-----------|-------------|---------|----------------|
| double | float | `.double_value` | `Parameter.Type.DOUBLE` |
| integer | int | `.integer_value` | `Parameter.Type.INTEGER` |
| string | str | `.string_value` | `Parameter.Type.STRING` |
| bool | bool | `.bool_value` | `Parameter.Type.BOOL` |

---

## 5단계: 데이터/모델 파일 추가 (AI/ML 프로젝트)

**이 단계의 목적**: AI/ML 모델, 학습 데이터, 이미지 등 추가 파일을 패키지에 포함시킵니다.

**왜 필요한가?**
- AI 모델 파일(.pth, .onnx 등)을 패키지와 함께 배포
- 테스트용 데이터나 샘플 이미지를 포함
- 설정 파일, 맵 데이터 등 정적 리소스 관리

**언제 사용?**
- 머신러닝/딥러닝 노드를 사용할 때
- 이미지 처리에 필요한 샘플 데이터가 있을 때
- 시뮬레이션용 맵, 환경 데이터가 필요할 때

**중요**:
- 큰 파일(모델 가중치 등)은 Git에 올리지 말고 별도 관리 권장
- setup.py에 glob 패턴으로 등록
- 빌드 후 `install/<package_name>/share/<package_name>/` 경로에 복사됨

### 디렉토리 생성:
```bash
cd <workspace_path>/src/<package_name>
mkdir models
mkdir data
```

### 폴더 구조:
```
<package_name>/
├── <package_name>/
├── launch/
├── config/
├── models/
│   ├── <model_definition_file>.py       # 모델 정의
│   └── <model_weights_file>.pth         # 학습된 가중치
├── data/
│   ├── <data_file>.csv
│   └── images/
│       ├── <image_file_1>.png
│       └── <image_file_2>.png
├── resource/
├── test/
├── package.xml
├── setup.cfg
└── setup.py
```

### `setup.py`에 데이터 파일 등록:
```python
data_files=[
    ('share/ament_index/resource_index/packages',
        ['resource/' + package_name]),
    ('share/' + package_name, ['package.xml']),
    # Include launch files
    ('share/' + package_name + '/launch',
        glob('launch/*.launch.py')),
    # Include config files
    ('share/' + package_name + '/config',
        glob('config/*.yaml')),
    # Include data files
    ('share/' + package_name + '/data',
        glob('data/*')),
    # Include AI model files
    ('share/' + package_name + '/models',
        glob('models/*')),
],
```

---

## 6단계: 빌드 및 실행

**이 단계의 목적**: 작성한 코드를 실행 가능한 형태로 변환하고 테스트합니다.

**빌드가 하는 일**:
1. Python 파일들을 `install/` 디렉토리로 복사
2. setup.py의 `entry_points`를 보고 실행 파일 생성
3. launch, config 등 data_files를 `share/` 디렉토리로 복사
4. 의존성 검사 및 패키지 등록

**중요한 개념**:
- **빌드는 필수**: 코드를 수정하면 항상 재빌드 필요
- **소싱 필수**: 빌드 후 `source install/setup.bash` 실행해야 ROS2가 인식
- **개발 팁**: `--symlink-install` 사용하면 Python 파일은 재빌드 없이 반영

**자주 하는 실수**:
- 코드 수정 후 빌드를 안 함 → 변경사항이 반영 안 됨
- source를 안 함 → "패키지를 찾을 수 없음" 에러
- 터미널마다 source를 해야 함 (각 터미널은 독립적인 환경)

### 빌드:
```bash
cd <workspace_path>
colcon build --packages-select <package_name>
```

### 빌드 후 폴더 구조 (install 디렉토리):
```
install/<package_name>/
├── lib/
│   ├── <package_name>/
│   │   ├── <node_name>           # 실행 파일
│   │   ├── <node_name_2>
│   │   └── <node_name_3>
│   └── python3.10/
│       └── site-packages/
│           └── <package_name>/
│               ├── __init__.py
│               ├── <node_name>.py
│               ├── <node_name_2>.py
│               └── <node_name_3>.py
└── share/
    └── <package_name>/
        ├── launch/
        │   └── <launch_file_name>.launch.py
        ├── config/
        │   └── <config_file_name>.yaml
        ├── models/
        │   ├── <model_definition_file>.py
        │   └── <model_weights_file>.pth
        ├── data/
        │   ├── <data_file>.csv
        │   └── images/
        ├── package.xml
        └── ...
```

### 소싱 및 실행:
```bash
# 환경 소싱
source install/setup.bash

# 개별 노드 실행
ros2 run <package_name> <node_name>
ros2 run <package_name> <node_name_2>

# Launch 파일 실행
ros2 launch <package_name> <launch_file_name>.launch.py

# 파라미터와 함께 실행
ros2 run <package_name> <node_name> --ros-args --params-file install/<package_name>/share/<package_name>/config/<config_file_name>.yaml
```

---

## 완성된 setup.py 전체 예시

```python
from setuptools import setup
import os
from glob import glob

package_name = '<package_name>'

setup(
    name=package_name,
    version='<version>',
    packages=[package_name],
    data_files=[
        # ROS2 패키지 등록 (필수)
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),

        # Launch 파일
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.py')),

        # Config 파일
        (os.path.join('share', package_name, 'config'),
            glob('config/*.yaml')),

        # 모델 파일
        (os.path.join('share', package_name, 'models'),
            glob('models/*.py')),
        (os.path.join('share', package_name, 'models'),
            glob('models/*.pth')),

        # 데이터 파일
        (os.path.join('share', package_name, 'data'),
            glob('data/*.csv')),
        (os.path.join('share', package_name, 'data', 'images'),
            glob('data/images/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='<maintainer_name>',
    maintainer_email='<maintainer_email>',
    description='<package_description>',
    license='<license>',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            '<node_name> = <package_name>.<node_name>:main',
            '<node_name_2> = <package_name>.<node_name_2>:main',
            '<node_name_3> = <package_name>.<node_name_3>:main',
        ],
    },
)
```

---

## 체크리스트

### 패키지가 제대로 생성되었는지 확인:

- [ ] `resource/<package_name>` 파일이 존재하는가?
- [ ] `<package_name>/__init__.py` 파일이 존재하는가?
- [ ] `setup.py`의 `packages=[package_name]` 항목이 올바른가?
- [ ] `setup.py`의 `entry_points`에 모든 노드가 등록되었는가?
- [ ] `setup.py`의 `data_files`에 launch, config, data 파일이 모두 포함되었는가?
- [ ] `package.xml`에 모든 의존성이 선언되었는가?

### 빌드 후 확인:

```bash
# 패키지가 인식되는지 확인
ros2 pkg list | grep my_robot_pkg

# 실행 파일이 있는지 확인
ros2 pkg executables my_robot_pkg

# Launch 파일이 있는지 확인
ros2 launch my_robot_pkg <TAB>
```

---

## 자주 발생하는 오류와 해결법

### 1. "No executable found"
**원인**: `setup.py`의 `entry_points`에 노드가 등록되지 않았거나, 빌드가 제대로 안 됨
**해결**:
```bash
# setup.py 확인 후
cd ~/10_delto_ws
rm -rf build/<package_name> install/<package_name>
colcon build --packages-select <package_name>
source install/setup.bash
```

### 2. "libexec directory does not exist"
**원인**: Python 패키지는 `lib/<package_name>/`에 실행 파일을 만드는데, `setup.cfg`가 잘못됨
**해결**: `setup.py`의 `packages=[<package_name>]`를 확인 (`find_packages()` 대신)

### 3. "FileNotFoundError: Model/Data not found"
**원인**: `setup.py`의 `data_files`에 파일이 등록되지 않음
**해결**: `setup.py`의 `data_files`에 해당 파일 패턴 추가 후 재빌드

### 4. Launch 파일이 안 보임
**원인**: `setup.py`에 launch 파일이 등록되지 않음
**해결**:
```python
(os.path.join('share', package_name, 'launch'),
    glob('launch/*.launch.py')),
```

---

## 빠른 참조 명령어

```bash
# 새 패키지 생성
ros2 pkg create --build-type ament_python <package_name> --dependencies <dependencies>

# 빌드
colcon build --packages-select <package_name>

# 심볼릭 링크 빌드 (개발 중)
colcon build --symlink-install

# 전체 빌드
colcon build

# 특정 패키지만 재빌드
colcon build --packages-select <package_name> --cmake-clean-cache

# 환경 소싱
source install/setup.bash

# 노드 실행
ros2 run <package_name> <node_name>

# Launch 파일 실행
ros2 launch <package_name> <launch_file_name>.launch.py

# 패키지 정보 확인
ros2 pkg list
ros2 pkg executables <package_name>
ros2 pkg prefix <package_name>
```

---

## 요약

1. **`ros2 pkg create`로 기본 템플릿 생성**
2. **노드 파일을 `<package_name>/` 디렉토리에 작성**
3. **`setup.py`의 `entry_points`에 노드 등록**
4. **launch, config, data 파일은 별도 디렉토리에 작성**
5. **`setup.py`의 `data_files`에 추가 파일 등록**
6. **빌드 후 `source install/setup.bash` 실행**
7. **`ros2 run` 또는 `ros2 launch`로 실행**

이 가이드를 따라하면 ROS2 패키지를 올바르게 생성할 수 있습니다!
