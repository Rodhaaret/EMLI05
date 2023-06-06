import rclpy
from rclpy.node import Node
from std_msgs.msg import Int16, Bool, Float32MultiArray

class Pi(Node):
    def __init__(self):
        super().__init__('Pi')
        ## Setup communication with farmer 
        # Listening for button click 
        self.create_subscription(Bool,'Button',self.button_callback,1)
        self.activation_counter = 0

        # Writing LED commands
        self.ledPublisher = self.create_publisher(Int16, 'LED', 1)

        ## Setup communication with Wateringsystem 
        self.pumpPublisher = self.create_publisher(Bool, 'Pump', 1)
        
        # Listen for Sensor info & check if pumping is necessary once per hour
        self.create_subscription(Float32MultiArray,'SensorData',self.sensor_callback,1)
        self.RedAlarm = False
        self.YellowAlarm = False
        self.EnoughMoisture = True
        pump_timer_period = 60 # Set to one minute instead of one hour for testing purposes
        self.hours = 0
        self.wateringTimer = self.create_timer(pump_timer_period, self.oneHour_callback)

        ## Activation Publisher - Only needed for Visualization Purposes
        self.activationPublisher = self.create_publisher(Int16, 'Activation', 1)

    def button_callback(self, msg):
        self.activation_counter += 1
        # Send Pump Command to WateringSystem
        pumpCommand = Bool()
        pumpCommand.data = True
        self.pumpPublisher.publish(pumpCommand)

        # Send updated Button Count to FoxGlove
        activationMsg = Int16()
        activationMsg.data = self.activation_counter
        self.activationPublisher.publish(activationMsg)

    def oneHour_callback(self):
        # Pump every hour if moisture too low or if 12 hours have passed without pumping
        if (self.YellowAlarm == True) or self.hours == 12: 
            if self.RedAlarm == False: 
                self.hours = 0
                # Update nr of activations
                self.activation_counter += 1
                activationMsg = Int16()
                activationMsg.data = self.activation_counter
                self.activationPublisher.publish(activationMsg)
                # Send Pump Command to WateringSystem
                pumpCommand = Bool()
                pumpCommand.data = True
                self.pumpPublisher.publish(pumpCommand)
                self.YellowAlarm = False
            else: 
                self.hours += 1
        else: 
            self.hours += 1
    
    def sensor_callback(self, msg):
        ledMsg = Int16()
        ledMsg.data = 0
        if (msg.data[1] > 0.5) or (msg.data[2] < 0.5):
            ledMsg.data = 2
            self.RedAlarm = True
            self.ledPublisher.publish(ledMsg)
        elif msg.data[3] < 3: 
            self.RedAlarm = False
            self.YellowAlarm = True
            ledMsg.data = 1
            self.ledPublisher.publish(ledMsg)
        else: 
            self.RedAlarm = False
            self.YellowAlarm = False
            ledMsg.data = 0
            self.ledPublisher.publish(ledMsg)

def main():
    print('Hi from Pi.')
    rclpy.init()
    pi = Pi()
    rclpy.spin(pi)
    pi.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()