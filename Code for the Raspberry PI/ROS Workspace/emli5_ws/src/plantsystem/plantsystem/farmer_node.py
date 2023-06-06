import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, Int16

from bs4 import BeautifulSoup 
import urllib.request

class Farmer(Node):

    def __init__(self):
        super().__init__('Farmer')
        
        # Button
        self.buttonPublisher = self.create_publisher(Bool, 'Button', 1)
        button_timer_period = 1
        self.timerButton = self.create_timer(button_timer_period, self.button_callback)
        self.ButtonURL = 'https://10.42.0.222/button/a/count'

        # LED 
        self.subscription = self.create_subscription(Int16,'LED',self.LED_callback,1)
        
        self.Red_on_URL = 'https://10.42.0.222/led/red/on'
        self.Red_off_URL = 'https://10.42.0.222/led/red/off'
        self.Yellow_on_URL = 'https://10.42.0.222/led/yellow/on'
        self.Yellow_off_URL = 'https://10.42.0.222/led/yellow/off'
        self.Green_on_URL = 'https://10.42.0.222/led/green/on'
        self.Green_off_URL = 'https://10.42.0.222/led/green/off'

    def button_callback(self):
        self.response = urllib.request.urlopen(self.ButtonURL)
        html_doc = self.response.read() #http://192.168.0.222/button/a/count
        # Parse the html file
        soup = BeautifulSoup(html_doc, 'html.parser')
        # Format the parsed html file
        strhtml = soup.prettify()
        # Print the first few characters
        msg = Bool()
        if str(strhtml[0]) != '0':
            msg.data = True
            self.buttonPublisher.publish(msg)
    
    def LED_callback(self, input_msg):
        if input_msg.data == 0: # Green
            urllib.request.urlopen(self.Green_on_URL)
            urllib.request.urlopen(self.Yellow_off_URL)
            urllib.request.urlopen(self.Red_off_URL)
        elif input_msg.data == 1: # Yellow
            urllib.request.urlopen(self.Green_off_URL)
            urllib.request.urlopen(self.Yellow_on_URL)
            urllib.request.urlopen(self.Red_off_URL)
        else: # Red
            urllib.request.urlopen(self.Green_off_URL)
            urllib.request.urlopen(self.Yellow_off_URL)
            urllib.request.urlopen(self.Red_on_URL)

def main():
    
    print('Hi from Farmer.')
    rclpy.init()
    farmer = Farmer()
    rclpy.spin(farmer)
    farmer.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()