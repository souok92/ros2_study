import rclpy
from rclpy.node import Node
from my_interfaces.msg import Person


class PersonSubscriber(Node):
    def __init__(self):
        super().__init__('person_subscriber')
        self.subscription = self.create_subscription(
            Person,
            'person_info',
            self.person_callback,
            10
        )
        self.get_logger().info('Person Subscriber 시작! 메시지 대기 중...')

    def person_callback(self, msg):
        student_status = '학생' if msg.is_student else '비학생'
        self.get_logger().info(
            f'받음: 이름={msg.name}, 나이={msg.age}세, '
            f'키={msg.height}m, 상태={student_status}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = PersonSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()