import rclpy
from rclpy.node import Node
from my_interfaces.msg import Person


class PersonPublisher(Node):
    def __init__(self):
        super().__init__('person_publisher')
        self.publisher = self.create_publisher(Person, 'person_info', 10)
        self.timer = self.create_timer(1.0, self.publish_person)
        self.counter = 0
        self.get_logger().info('Person Publisher 시작!')

    def publish_person(self):
        msg = Person()
        msg.name = f'홍길동{self.counter}'
        msg.age = 25 + self.counter
        msg.height = 1.75
        msg.is_student = (self.counter % 2 == 0)
        
        self.publisher.publish(msg)
        self.get_logger().info(
            f'발행: {msg.name}, {msg.age}세, {msg.height}m, '
            f'학생: {msg.is_student}'
        )
        self.counter += 1


def main(args=None):
    rclpy.init(args=args)
    node = PersonPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()