import rclpy
import subprocess
from rclpy.node import Node
from std_msgs.msg import Bool, Int16
from src.plantsystem.plantsystem.msg import FloatList


class WateringSystem(Node):
    def __init__(self):
        super().__init__('wateringsystem')
        # Setup communication with pi
        self.create_subscription(Bool,'Pump',self.pump_callback,1)
        self.sensorPublisher = self.create_publisher(FloatList, 'SensorData', 1)
        sensor_timer_period = 2
        self.timerLED = self.create_timer(sensor_timer_period, self.sensor_callback)
        
    def sensor_callback(self): 
        # Get unpacked data from shell script:
        result = subprocess.run(["sh", "./sensors.sh"], capture_output=True, text=True)
        output = result.stdout.strip()
        values = output.split(",")
        if len(values) > 3:
            print(values[0])
            print(values[1])
            print(values[2])
            print(values[3])

            # Publish data to Pi
            sensorMsg = FloatList()
            sensorMsg.data = [values[0], values[1], values[2], values[3]]
            self.sensorPublisher.publish(sensorMsg)
        

    def pump_callback(self, msg):
        
        if msg.data == True: 
            self.get_logger().info('Start pumping')
            subprocess.run(["sh","./pump.sh"])
        else: 
            self.get_logger().info('Stop pumping')
    

def main(args=None):
    print('Hi from WateringSystem.')
    rclpy.init(args=args)
    ws = WateringSystem()
    rclpy.spin(ws)
    ws.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()