import rclpy
from rclpy.node import Node
from std_msgs.msg import Int16, Bool, Float32
from src.plantsystem.plantsystem.msg import FloatList

class Pi(Node):
    def __init__(self):
        super().__init__('pi')
        ## Setup communication with farmer 
        # Listening for button click 
        self.create_subscription(Bool,'Button',self.button_callback,1)
        self.button_counter = 0

        # Writing LED commands
        self.ledPublisher = self.create_publisher(Int16, 'LED', 1)
        led_timer_period = 3
        self.timerLED = self.create_timer(led_timer_period, self.led_callback)
        self.cnt = 0

        ## Setup for communication with Wateringsystem 
        self.pumpPublisher = self.create_publisher(Bool, 'Pump', 1)
        
        # Check if pumping is necessary
        pump_timer_period = 300
        self.hours = 0
        self.wateringTimer = self.create_timer(pump_timer_period, self.timer_callback)

        # Listen for Sensor info
        self.create_subscription(FloatList,'SensorData',self.sensor_callback,1)

        ## Setup communication with FoxGlove
        self.fg_buttonPublisher = self.create_publisher(Int16, 'ButtonFG', 1)
        self.fg_waterAlarmPublisher = self.create_publisher(Bool, 'WaterAlarmFG', 1)
        self.fg_pumpAlarmPublisher = self.create_publisher(Bool, 'PumpAlarmFG', 1)
        self.fg_moisturePublisher = self.create_publisher(Float32, 'moistureFG', 1)
        self.fg_lightPublisher = self.create_publisher(Float32, 'lightFG', 1)
        FG_timer_period = 1
        self.timerLED = self.create_timer(led_timer_period, self.FG_callback)


    def button_callback(self, msg):
        self.button_counter += 1
        # Send Pump Command to WateringSystem
        pumpCommand = Bool()
        pumpCommand.data = True
        self.pumpPublisher.publish(pumpCommand)
        self.get_logger().info("Sending Pump Signal to WateringSystem")

        # Send updated Button Count to FoxGlove
        buttonMsg = Int16()
        buttonMsg.data = self.button_counter()
        self.fg_buttonPublisher.publish(buttonMsg)

    

    def timer_callback(self):
        # Pump every hour if moisture too low or if 12 hours have passed without pumping
        if True or hours == 12: 
            hours = 0
            pumpCommand = Bool()
            pumpCommand.data = True
            self.pumpPublisher.publish(pumpCommand)
            self.get_logger().info("Sending Pump Signal to WateringSystem")
        else: 
            hours += 1


    def led_callback(self):
        msg = Int16()
        msg.data = self.cnt
        self.ledPublisher.publish(msg)
        self.get_logger().info('LED Message: "%i"' % msg.data)

        self.cnt += 1
        if self.cnt == 3:
            self.cnt = 0

    def sensor_callback(self, sensorMsg):
        # Publish Data for Foxglove
        waterAlarmMsg = Bool()
        waterAlarmMsg.data = sensorMsg.data[0]
        self.fg_waterAlarmPublisher.publish(waterAlarmMsg)
        pumpAlarmMsg = Bool()
        pumpAlarmMsg.data = sensorMsg.data[1]
        self.fg_pumpAlarmPublisher.publish(pumpAlarmMsg)
        moistureMsg = Float32()
        moistureMsg.data = sensorMsg.data[2]
        self.fg_moisturePublisher.publish(moistureMsg)
        lightMsg = Float32()
        lightMsg.data = sensorMsg.data[3]
        self.fg_lightPublisher.publish(lightMsg)

    
    def FG_callback(self):
        pass
      

def main():
    print('Hi from Pi.')
    rclpy.init()
    pi = Pi()
    rclpy.spin(pi)
    pi.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()