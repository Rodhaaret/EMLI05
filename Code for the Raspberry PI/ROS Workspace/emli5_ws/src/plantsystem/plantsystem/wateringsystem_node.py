import rclpy
import subprocess
from rclpy.node import Node
from std_msgs.msg import Bool, Int16, Float32MultiArray

class WateringSystem(Node):
    def __init__(self):
        super().__init__('Wateringsystem')
        self.PlantNr = 0.

        # Setup communication with pi
        self.create_subscription(Bool,'Pump',self.pump_callback,1)
        self.sensorPublisher = self.create_publisher(Float32MultiArray, 'SensorData', 1)
        sensor_timer_period = 1
        self.timerLED = self.create_timer(sensor_timer_period, self.sensor_callback)
        
    def sensor_callback(self): 
        # Get unpacked data from shell script:
        result = subprocess.run(["sh", "/home/pi/emli_WS/sensors.sh"], capture_output=True, text=True)
        subprocess.call(['/bin/bash', '/home/pi/emli_WS/WriteData.sh'])
        output = result.stdout.strip()
        values = output.split()
        
        if len(values) > 3:
            sensorMSg = Float32MultiArray()
            sensorMSg.data = [self.PlantNr,float(values[0]),float(values[1]),float(values[2]),float(values[3])]
            self.sensorPublisher.publish(sensorMSg)
        
    def pump_callback(self, msg):
        subprocess.run(["sh","./pump.sh"])
        

def main(args=None):
    print('Hi from WateringSystem.')
    rclpy.init(args=args)
    ws = WateringSystem()
    rclpy.spin(ws)
    ws.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()