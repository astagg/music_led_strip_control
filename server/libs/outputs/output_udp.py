from libs.outputs.output import Output  # pylint: disable=E0611, E0401

import logging
import socket
from bagle import BagelThrower
import numpy as np
import socket
import json
from time import sleep
from colorsys import hsv_to_rgb


class OutputUDP(Output):
    def __init__(self, device):
        with open('conf.json', "r") as cfg:
            self.cfg = json.load(cfg)

        self.thrower = BagelThrower(cfg)

    def show(self, output_array):

        print(output_array)

        output_array = output_array * (self._led_brightness / 100)

        # Truncate values and cast to integer
        pixels = np.clip(output_array, 0, 255).astype(int)
        # Optional gamma correction
        p = np.copy(pixels)
        # Read the rgb values
        r = p[0][:].astype(int)
        g = p[1][:].astype(int)
        b = p[2][:].astype(int)
        # Update the pixels
        frame = self.thrower.get_frame_buffer()

        #create array in which we will store the led states
        newstrip = [None]*(int(self._device_config["led_count"])*3)

        for i in range( int(self._device_config["led_count"])):
            newstrip[i*3] = r[i]
            newstrip[i*3+1] = g[i]
            newstrip[i*3+2] = b[i]

        # Typecast the array to int.
        output_array = output_array.clip(0, 255).astype(np.uint8)

        byte_array = output_array.tobytes('F')
        try:
            # self._sock.sendto(byte_array, (self._udp_client_ip, self._udp_client_port))
            self.thrower.send_frame(byte_array)
        except Exception as ex:
            self.logger.exception(f"Could not send to client", ex)
            self.logger.debug(f"Reinit output of {self._udp_client_ip}")
            self.thrower = BagelThrower(self.cfg)