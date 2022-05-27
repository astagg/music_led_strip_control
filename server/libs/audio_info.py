from libs.audio_device import AudioDevice  # pylint: disable=E0611, E0401

import logging


class AudioInfo:
    def get_audio_devices(py_audio):
        logger = logging.getLogger(__name__)
        logger.debug("Get audio devices.")
        audio_devices = []

        try:
            audio_device_count = py_audio.get_device_count()
            for i in range(audio_device_count):
                audio_device = py_audio.get_device_info_by_index(i).get('name')
                print (audio_device)
                audio_devices.append(audio_device)

        except Exception as e:
            logger.debug("Could not get device infos.")
            logger.exception(f"Unexpected error in AudioInfo: {e}")

        logger.debug(f"Found {len(audio_devices)} audio devices.")
        return audio_devices

    def get_default_audio_device(py_audio):
        logger = logging.getLogger(__name__)
        default_device = AudioDevice(0, "Error", 44100)
        try:
            raw_default_device = py_audio.get_default_input_device_info()
            default_device = AudioInfo.parse_raw_audio_device_to_audio_device(raw_default_device)

        except Exception as e:
            logger.exception(f"Unexpected error in AudioInfo get_default_audio_device: {e}")

        return default_device

    def parse_raw_audio_device_to_audio_device(raw_audio_device):
        logger = logging.getLogger(__name__)
        id = raw_audio_device["index"]
        name = raw_audio_device["name"]
        defaultSampleRate = raw_audio_device["defaultSampleRate"]
        return AudioDevice(id, name, defaultSampleRate)
