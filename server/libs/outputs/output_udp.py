from libs.outputs.output import Output  # pylint: disable=E0611, E0401

import numpy as np
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


        # # Truncate values and cast to integer
        # pixels = np.clip(pixels, 0, 255).astype(int)
        # # Optional gamma correction
        # p = np.copy(pixels)
        # # Read the rgb values
        # r = p[0][:].astype(int)
        # g = p[1][:].astype(int)
        # b = p[2][:].astype(int)
        # # Update the pixels
        # frame = thrower.get_frame_buffer()

        # #create array in which we will store the led states
        # newstrip = [None]*(config.N_PIXELS*3)

        # for i in range(config.N_PIXELS):
        #     newstrip[i*3] = r[i]
        #     newstrip[i*3+1] = g[i]
        #     newstrip[i*3+2] = b[i]



        output_array = output_array * (self._led_brightness / 100)

        output_array = self.map_channels(output_array)
        # Typecast the array to int.
        output_array = output_array.clip(0, 255).astype(np.uint8)

        byte_array = output_array.tobytes('F')
        try:
            # self._sock.sendto(byte_array, (self._udp_client_ip, self._udp_client_port))
            self.thrower.send_frame(byte_array)
        except Exception as ex:
            self.logger.exception(f"Could not send to client", ex)
            self.logger.debug(f"Reinit output of {self._udp_client_ip}")
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def map_channels(self, output_array_in):
        if "SK6812" in self._led_strip:
            if len(output_array_in[:]) == 4:
                return self.map_four_channels_sk(output_array_in)
            else:
                return self.map_three_channels_sk(output_array_in)
        else:
            return self.map_three_channels_ws(output_array_in)

    def map_three_channels_ws(self, output_array_in):
        r = output_array_in[0]
        g = output_array_in[1]
        b = output_array_in[2]

        output_array_out = np.zeros((3, len(r)))

        if self._led_strip == "ws2811_strip_bgr":
            output_array_out[0] = b
            output_array_out[1] = g
            output_array_out[2] = r
            return output_array_out
        elif self._led_strip == "ws2811_strip_brg":
            output_array_out[0] = b
            output_array_out[1] = r
            output_array_out[2] = g
            return output_array_out
        elif self._led_strip == "ws2811_strip_gbr":
            output_array_out[0] = g
            output_array_out[1] = b
            output_array_out[2] = r
            return output_array_out
        elif self._led_strip == "ws2811_strip_grb":
            output_array_out[0] = g
            output_array_out[1] = r
            output_array_out[2] = b
            return output_array_out
        elif self._led_strip == "ws2811_strip_rbg":
            output_array_out[0] = r
            output_array_out[1] = b
            output_array_out[2] = g
            return output_array_out
        else:
            return output_array_in

    def map_three_channels_sk(self, output_array_in):
        r = output_array_in[0]
        g = output_array_in[1]
        b = output_array_in[2]

        output_array_out = np.zeros((3, len(r)))

        if self._led_strip == "sk6812_strip_bgrw":
            output_array_out[0] = b
            output_array_out[1] = g
            output_array_out[2] = r
            return output_array_out
        elif self._led_strip == "sk6812_strip_brgw":
            output_array_out[0] = b
            output_array_out[1] = r
            output_array_out[2] = g
            return output_array_out
        elif self._led_strip == "sk6812_strip_gbrw":
            output_array_out[0] = g
            output_array_out[1] = b
            output_array_out[2] = r
            return output_array_out
        elif self._led_strip == "sk6812_strip_grbw":
            output_array_out[0] = g
            output_array_out[1] = r
            output_array_out[2] = b
            return output_array_out
        elif self._led_strip == "sk6812_strip_rbgw":
            output_array_out[0] = r
            output_array_out[1] = b
            output_array_out[2] = g
            return output_array_out
        else:
            return output_array_in

    def map_four_channels_sk(self, output_array_in):
        r = output_array_in[0]
        g = output_array_in[1]
        b = output_array_in[2]
        w = output_array_in[3]

        output_array_out = np.zeros((4, len(r)))

        if self._led_strip == "sk6812_strip_bgrw":
            output_array_out[0] = b
            output_array_out[1] = g
            output_array_out[2] = r
            output_array_out[3] = w
            return output_array_out
        elif self._led_strip == "sk6812_strip_brgw":
            output_array_out[0] = b
            output_array_out[1] = r
            output_array_out[2] = g
            output_array_out[3] = w
            return output_array_out
        elif self._led_strip == "sk6812_strip_gbrw":
            output_array_out[0] = g
            output_array_out[1] = b
            output_array_out[2] = r
            output_array_out[3] = w
            return output_array_out
        elif self._led_strip == "sk6812_strip_grbw":
            output_array_out[0] = g
            output_array_out[1] = r
            output_array_out[2] = b
            output_array_out[3] = w
            return output_array_out
        elif self._led_strip == "sk6812_strip_rbgw":
            output_array_out[0] = r
            output_array_out[1] = b
            output_array_out[2] = g
            output_array_out[3] = w
            return output_array_out
        else:
            return output_array_in