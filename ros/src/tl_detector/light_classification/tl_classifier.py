import rospy
from styx_msgs.msg import TrafficLight
import cv2
import numpy as np


class TLClassifier(object):
    def __init__(self):
        self.GREEN_CHANNEL = 1
        self.RED_CHANNEL = 2
        self.area_thr = 80

    def traffic_predict(self, image):
        """
        image: cv2.Image (BGR)
        """
        red_img = image[:,:,self.RED_CHANNEL]
        green_img = image[:,:,self.GREEN_CHANNEL]
        red_area = np.sum(red_img == red_img.max())
        green_area = np.sum(green_img == green_img.max())


        prediction = TrafficLight.UNKNOWN

        if red_area >= self.area_thr and green_area <= self.area_thr:
            prediction = TrafficLight.RED
        elif red_area >= self.area_thr and green_area >= self.area_thr:
            prediction = TrafficLight.YELLOW if 0.8 <= red_area / green_area <= 1.2 else TrafficLight.RED
        elif green_area >= self.area_thr:
            prediction = TrafficLight.GREEN
        else:
            prediction = TrafficLight.UNKNOWN

        if prediction == TrafficLight.RED:
            rospy.logwarn("RED!")
        else:
            rospy.logwarn("No RED")

        return prediction
