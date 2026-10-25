import rclpy
import math
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class ObstacleAvoidance(Node):
    def __init__(self):
        super().__init__('obstacle_avoidance_node')
        
        self.subscription = self.create_subscription(
            LaserScan,
            '/bcr_bot/scan', 
            self.scan_callback,
            10)
            
        self.publisher = self.create_publisher(Twist, '/bcr_bot/cmd_vel', 10)
        self.get_logger().info("Obstacle Avoidance Node Started!")

    def scan_callback(self, msg):
        velocity_msg = Twist()
        
        
        clean_ranges = [r if not math.isinf(r) and not math.isnan(r) else 10.0 for r in msg.ranges]
        
        
        front_distances = clean_ranges[:20] + clean_ranges[-20:]
        min_distance = min(front_distances)
        
        
        if min_distance < 1.0:
            self.get_logger().info(f"Obstacle detected at {min_distance:.2f}m! Turning...")
            velocity_msg.linear.x = 0.0
            velocity_msg.angular.z = 0.5  
        else:
            velocity_msg.linear.x = 0.5   
            velocity_msg.angular.z = 0.0
            
        self.publisher.publish(velocity_msg)

def main(args=None):
    rclpy.init(args=args)
    node = ObstacleAvoidance()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
