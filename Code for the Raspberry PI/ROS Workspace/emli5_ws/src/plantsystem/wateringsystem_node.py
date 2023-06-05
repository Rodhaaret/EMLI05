import rclpy
import subprocess
from rclpy.node import Node
from std_msgs.msg import Bool, Int16, Float32
from src.plantsystem.msg import FloatList

class WateringSystem(Node):
    def __init__(self):
        super().__init__('wateringsystem')
        # Setup communication with pi
        self.create_subscription(Bool,'Pump',self.pump_callback,1)
        self.waterAlarmPublisher = self.create_publisher(Bool, 'WaterAlarm', 1)
        self.plantAlarmPublisher = self.create_publisher(Bool, 'PlantAlarm', 1)
        self.moisturePublisher = self.create_publisher(Float32, 'moisture', 1)
        self.lightPublisher = self.create_publisher(Float32, 'light', 1)
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
            plantAlarmMsg = Bool()
            plantAlarmMsg.data = values[0]
            self.fg_plantAlarmPublisher.publish(plantAlarmMsg)
            pumpAlarmMsg = Bool()
            pumpAlarmMsg.data = values[1]
            self.fg_pumpAlarmPublisher.publish(pumpAlarmMsg)
            moistureMsg = Float32()
            moistureMsg.data = values[2]
            self.fg_moisturePublisher.publish(moistureMsg)
            lightMsg = Float32()
            lightMsg.data = values[3]
            self.fg_lightPublisher.publish(lightMsg)
        

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