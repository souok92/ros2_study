# ROS2 Study Repository

ROS2 학습 및 개발을 위한 포괄적인 템플릿, 가이드, 예제 패키지 모음입니다.

## 저장소 구조

```
ros2_study/
├── template_workspace/          # 메인 ROS2 워크스페이스
│   ├── 00_documents/           # 문서 및 가이드
│   ├── src/                    # ROS2 패키지들
│   ├── build/                  # 빌드 결과물 (자동 생성)
│   ├── install/                # 설치 공간 (자동 생성)
│   └── log/                    # 빌드 로그 (자동 생성)
└── README.md                   # 이 파일
```

## 문서

[`00_documents`](template_workspace/00_documents/) 폴더에는 ROS2 개발을 위한 포괄적인 가이드가 포함되어 있습니다:

### 핵심 가이드
- **[ROS2_PACKAGE_TEMPLATE_GUIDE.md](template_workspace/00_documents/ROS2_PACKAGE_TEMPLATE_GUIDE.md)** - ROS2 Python 패키지 생성 및 구조화에 대한 완벽한 가이드
- **[ROS2_CPP_PACKAGE_GUIDE.md](template_workspace/00_documents/ROS2_CPP_PACKAGE_GUIDE.md)** - ROS2 C++ 패키지 생성 가이드
- **[ROS2_NODE_TEMPLATES.md](template_workspace/00_documents/ROS2_NODE_TEMPLATES.md)** - 일반적인 ROS2 노드 패턴을 위한 즉시 사용 가능한 템플릿 (퍼블리셔, 서브스크라이버, 서비스, 액션, 라이프사이클 노드)
- **[ROS2_MSG_SRV_ACTION_GUIDE.md](template_workspace/00_documents/ROS2_MSG_SRV_ACTION_GUIDE.md)** - 커스텀 메시지, 서비스, 액션 생성 가이드

### 도구 & 디버깅
- **[ROS2_LOGGING_RQT_ROSBAG_GUIDE.md](template_workspace/00_documents/ROS2_LOGGING_RQT_ROSBAG_GUIDE.md)** - 로깅, RQT 도구, rosbag 사용에 대한 완벽한 가이드

## 예제 패키지

[`src`](template_workspace/src/) 디렉토리에는 다양한 ROS2 개념을 보여주는 예제 패키지들이 포함되어 있습니다:

### 템플릿 패키지
- **`template_python`** - 기본 Python 패키지 템플릿
- **`template_python_step_2`** - 여러 노드가 있는 템플릿
- **`template_python_step_3_launch`** - launch 파일이 있는 템플릿
- **`template_python_step_4_config`** - 설정 파일이 있는 템플릿
- **`template_python_step_5_include_data`** - 데이터 파일이 있는 템플릿

### 커스텀 패키지
- **`my_python_pkg`** - Python 패키지 예제
- **`my_interfaces`** - 커스텀 메시지, 서비스, 액션 정의

## 시작하기

### 필수 조건

- ROS2 설치 (Humble, Iron, 또는 Jazzy 권장)
- Python 3.8+ 또는 C++ 컴파일러
- colcon 빌드 도구

```bash
# colcon이 설치되지 않은 경우 설치
sudo apt install python3-colcon-common-extensions
```

### 워크스페이스 빌드

```bash
# 워크스페이스로 이동
cd template_workspace

# 모든 패키지 빌드
colcon build

# 워크스페이스 소싱
source install/setup.bash
```

### 특정 패키지 빌드

```bash
# 특정 패키지만 빌드
colcon build --packages-select my_python_pkg

# 심볼릭 링크 설치로 빌드 (Python용 - 코드 변경 시 재빌드 불필요)
colcon build --symlink-install
```

## 빠른 시작 예제

### 새 패키지 생성

```bash
# src 디렉토리로 이동
cd template_workspace/src

# Python 패키지 생성
ros2 pkg create --build-type ament_python my_new_package \
  --dependencies rclpy std_msgs

# C++ 패키지 생성
ros2 pkg create --build-type ament_cmake my_cpp_package \
  --dependencies rclcpp std_msgs
```

자세한 내용은 [ROS2_PACKAGE_TEMPLATE_GUIDE.md](template_workspace/00_documents/ROS2_PACKAGE_TEMPLATE_GUIDE.md)를 참조하세요.

### 예제 노드 실행

```bash
# 먼저 워크스페이스 소싱
source template_workspace/install/setup.bash

# 노드 실행
ros2 run my_python_pkg my_node

# launch 파일 실행
ros2 launch my_python_pkg my_launch_file.launch.py
```

### 템플릿 사용

1. [노드 템플릿](template_workspace/00_documents/ROS2_NODE_TEMPLATES.md) 탐색
2. 사용 사례에 맞는 템플릿 복사
3. 플레이스홀더 교체 (예: `<ClassName>`, `<package_name>`)
4. `setup.py`를 업데이트하여 노드 등록
5. 빌드 및 테스트

## 자주 사용하는 명령어

### 패키지 관리
```bash
# 모든 패키지 나열
ros2 pkg list

# 패키지 정보 가져오기
ros2 pkg prefix <package_name>

# 패키지의 실행 파일 나열
ros2 pkg executables <package_name>
```

### 노드 작업
```bash
# 실행 중인 노드 나열
ros2 node list

# 노드 정보 가져오기
ros2 node info <node_name>
```

### 토픽 작업
```bash
# 토픽 나열
ros2 topic list

# 토픽 데이터 에코
ros2 topic echo <topic_name>

# 토픽 정보 가져오기
ros2 topic info <topic_name>

# 토픽에 퍼블리시
ros2 topic pub <topic_name> <msg_type> "<data>"
```

### 서비스 작업
```bash
# 서비스 나열
ros2 service list

# 서비스 호출
ros2 service call <service_name> <srv_type> "<request>"
```

### 기록 및 재생
```bash
# 모든 토픽 기록
ros2 bag record -a

# 특정 토픽 기록
ros2 bag record /topic1 /topic2

# 재생
ros2 bag play <bag_file>
```

자세한 rosbag 사용법은 [ROS2_LOGGING_RQT_ROSBAG_GUIDE.md](template_workspace/00_documents/ROS2_LOGGING_RQT_ROSBAG_GUIDE.md)를 참조하세요.

## 디버깅 도구

### RQT 도구
```bash
# 로그를 위한 rqt console 열기
rqt_console

# 노드 그래프 시각화
rqt_graph

# 토픽 데이터 플로팅
rqt_plot /topic_name/field

# 이미지 보기
rqt_image_view
```

### 로깅
```bash
# 디버그 로깅으로 노드 실행
ros2 run <package> <node> --ros-args --log-level debug

# 실시간으로 로그 보기
ros2 run <package> <node> 2>&1 | tee logfile.txt
```

## 개발 워크플로우

1. **계획**: 관련 가이드 및 템플릿 검토
2. **생성**: `ros2 pkg create`로 패키지 구조 생성
3. **개발**: 템플릿을 참조하여 노드 코드 작성
4. **설정**: `setup.py`, `package.xml`, launch 파일 업데이트
5. **빌드**: `colcon build` 실행 (Python의 경우 `--symlink-install` 사용)
6. **테스트**: 워크스페이스 소싱 후 노드 테스트
7. **디버그**: rqt 도구와 로깅을 사용하여 문제 해결
8. **기록**: rosbag을 사용하여 테스트 데이터 기록
9. **반복**: 테스트 결과를 바탕으로 개선

## 모범 사례

### 패키지 구성
- 로봇 기능/하위 시스템당 하나의 패키지
- 관련 노드를 동일한 패키지에 유지
- 인터페이스 정의를 전용 패키지로 분리
- 설명적인 패키지 및 노드 이름 사용

### 코드 품질
- ROS2 코딩 표준 준수
- 적절한 로그 레벨 사용 (debug, info, warn, error, fatal)
- 함수와 클래스에 docstring 추가
- 예외를 우아하게 처리
- 파라미터와 입력 검증

### 버전 관리
- `src/` 디렉토리 내용 커밋
- `build/`, `install/`, `log/`를 `.gitignore`에 추가
- 코드 변경과 함께 문서 포함
- 의미 있는 커밋 메시지 사용

### 테스트
- 복잡한 로직에 대한 단위 테스트 작성
- 일관성을 위해 기록된 bag으로 테스트
- 통합 테스트를 위한 launch 테스트 사용
- 파라미터 범위와 엣지 케이스 검증

## 학습 경로

### 초급
1. [ROS2_PACKAGE_TEMPLATE_GUIDE.md](template_workspace/00_documents/ROS2_PACKAGE_TEMPLATE_GUIDE.md) 읽기
2. 간단한 퍼블리셔/서브스크라이버 패키지 생성
3. `ros2` CLI 명령어 연습
4. rqt 도구 실험

### 중급
1. [ROS2_NODE_TEMPLATES.md](template_workspace/00_documents/ROS2_NODE_TEMPLATES.md) 학습
2. 서비스와 액션 구현
3. 파라미터가 있는 launch 파일 생성
4. 커스텀 메시지와 서비스 정의
5. 테스트를 위한 rosbag 사용

### 고급
1. 라이프사이클 노드 구현
2. 파라미터와 동적 재설정 사용
3. 커스텀 rqt 플러그인 생성
4. 포괄적인 launch 파일 작성
5. 성능 최적화 및 이슈 디버그
6. 오픈소스 ROS2 패키지에 기여

## 문제 해결

### 빌드 이슈
```bash
# 빌드 결과물 정리
rm -rf build/ install/ log/

# 처음부터 재빌드
colcon build

# 누락된 의존성 확인
rosdep install --from-paths src --ignore-src -r -y
```

### 런타임 이슈
- 워크스페이스가 소싱되었는지 확인: `source install/setup.bash`
- 노드가 `setup.py`에 등록되었는지 확인
- 토픽/서비스 이름이 일치하는지 확인
- `ros2 node list`와 `ros2 topic list`로 디버그
- `rqt_console`로 로그 확인

### 패키지를 찾을 수 없음
- 패키지가 `src/` 디렉토리에 있는지 확인
- `package.xml`이 존재하고 유효한지 확인
- 패키지가 빌드되었는지 확인: `colcon build --packages-select <package_name>`
- 빌드 후 워크스페이스 소싱

## 추가 자료

### 공식 문서
- [ROS2 문서](https://docs.ros.org/)
- [ROS2 튜토리얼](https://docs.ros.org/en/humble/Tutorials.html)
- [ROS2 API 레퍼런스](https://docs.ros.org/en/humble/p/rclpy/)

### 커뮤니티
- [ROS Discourse](https://discourse.ros.org/)
- [ROS Answers](https://answers.ros.org/)
- [ROS GitHub](https://github.com/ros2)

## 기여

이 저장소에 더 많은 템플릿, 가이드, 예제를 자유롭게 추가하세요. 기여 시:

1. 기존 문서 구조를 따르기
2. 커밋 전 모든 코드 예제 테스트
3. 새 섹션 추가 시 이 README 업데이트
4. 명확하고 설명적인 명명 규칙 사용
5. 복잡한 개념을 설명하는 주석 포함

## 라이선스

이 저장소는 교육 목적입니다. 개별 패키지는 자체 라이선스를 가질 수 있습니다.

---

**최종 업데이트**: 2026-01-16

**테스트된 ROS2 배포판**: Humble, Iron, Jazzy

질문이나 이슈가 있는 경우 [`00_documents/`](template_workspace/00_documents/)의 문서를 참조하거나 공식 ROS2 문서를 확인하세요.