""" This node polls the e-stop button and publishes an estop topic. 


Publishes: 
    /estop (Bool) - False if no e-stop condition, True if e-stop condition. 

Subscribes:
    None.

Services:
    None. 

Parameters:
    None. 
"""


from .submodules.teensy_hal import *
import rclpy
from rclpy.node import Node

from std_msgs.msg import Bool
import time

class EstopPublisher(Node):
    def __init__(self):
        super().__init__('estop_driver')
        self.publisher_ = self.create_publisher(Bool, 'estop', 10)
        timer_period = 0.1 #TODO: make this a parameter and share with other node
        estop_id = b'STP'
        self.period = 1 # Period for lED sin wave. 
        self.brightness = 200 # LED brightness out of 255
        
        ## Find the e-stop ##
        result = find_comport(estop_id)
        
        self.port = []
        if result['success']:
            self.port = result['port']
            self.get_logger().info('Found port {} for device with ID {}'.format(self.port, estop_id))
        else:
            self.get_logger().error('Unable to find port for device with ID: ', estop_id)
            self.destroy_node()
            rclpy.shutdown()

        self.timer = self.create_timer(timer_period, self.poll_estop) 

    def poll_estop(self):


        # Check E-stop Status.
        msg = Bool()
        result = get_button(self.port)
        if not result[0]: self.get_logger().warn("Failed to poll teensy")
        if result[1] == b'\x01':
            msg.data = True
        else:
            msg.data = False
        print(result) 
        self.publisher_.publish(msg)

        # Make LED change. 
        period = self.period
        if msg.data == False: period *= 0.25
        value = (np.sin(time.time()*2*np.pi*period)/2 + 0.5)*self.brightness   
        set_light(1, int(value), self.port) 
        
def main(args = None):
    rclpy.init(args = args)
    estop_driver = EstopPublisher()
    rclpy.spin(estop_driver)
    
    estop_driver.destroy_node()
    rclpy.shutdown()    


if __name__ == '__main__':
   main() 
