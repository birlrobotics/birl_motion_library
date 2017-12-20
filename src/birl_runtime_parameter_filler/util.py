import rospy
import threading

received_msg = None
receive_evt = threading.Event() 
def topic_cb(data):
    global received_msg, receive_evt
    received_msg = data
    receive_evt.set()

def get_topic_message_once(topic_name, topic_type):
    global received_msg, receive_evt
    
    receive_evt.clear()
    sub = rospy.Subscriber(topic_name, topic_type, topic_cb)
    received = receive_evt.wait(2)
    sub.unregister()
    if received:
        return received_msg 
    else:
        return None
        

