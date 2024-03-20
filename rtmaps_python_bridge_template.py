import rtmaps.core as rt
import rtmaps.types
from rtmaps.base_component import BaseComponent
import cv2
import numpy as np

class rtmaps_python(BaseComponent):
    def __init__(self):
        BaseComponent.__init__(self)
        self.camera = None
        self.max_can_payload = 8  # Classical CAN frame payload size

    def Dynamic(self):
        self.add_output("out", rtmaps.types.AUTO)

    def Birth(self):
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            raise Exception("Could not open video device")

    def Core(self):
        ret, frame = self.camera.read()
        if ret:
            # Simplified example: Convert the frame to grayscale to reduce data size
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Serialize the grayscale image to a bytes object
            image_bytes = gray_frame.tobytes()

            # Split the bytes object into CAN frame-sized chunks
            for i in range(0, len(image_bytes), self.max_can_payload):
                can_frame_payload = image_bytes[i:i+self.max_can_payload]
                
                # Construct a CAN frame with the chunk of image data
                can_frame = {
                    "id": 0x123,  # Example CAN ID
                    "data": can_frame_payload,
                    "size": len(can_frame_payload)
                }
                
                # Output the CAN frame
                self.write("out", can_frame)

    def Death(self):
        if self.camera:
            self.camera.release()
            print("Video capture released")
