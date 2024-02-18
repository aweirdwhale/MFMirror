import os
import struct
import wave
from datetime import datetime

import pvporcupine
from pvrecorder import PvRecorder

from dotenv import load_dotenv
from features.Logs.log import Log

load_dotenv("../../../.env.secret")
PiKEY = os.getenv("PORCUPINE_KEY")
console = Log()

console.log(PiKEY, "success")

class PorcupineListener:
    def __init__(self, accessKey, keywordPath, modelPath, outputPath=None, audioDeviceIndex=-1):
        self.access_key = accessKey
        self.keyword_path = keywordPath
        self.model_path = modelPath
        self.output_path = outputPath
        self.audio_device_index = audioDeviceIndex
        self.porcupine = None
        self.recorder = None
        self.wav_file = None
        self.detected = False
        self.stopmsk = False

    def initialize(self):
        self.porcupine = pvporcupine.create(
            access_key=self.access_key,
            keyword_paths=self.keyword_path,
            model_path=self.model_path
        )

        if self.output_path is not None:
            self.wav_file = wave.open(self.output_path, "w")
            self.wav_file.setnchannels(1)
            self.wav_file.setsampwidth(2)
            self.wav_file.setframerate(16000)

        self.recorder = PvRecorder(
            frame_length=self.porcupine.frame_length,
            device_index=self.audio_device_index
        )
        self.recorder.start()

    def start_detection(self):
        print('Listening ...')
        try:
            while True:
                
                

                pcm = self.recorder.read()
                result = self.porcupine.process(pcm)

                if self.wav_file is not None:
                    self.wav_file.writeframes(struct.pack("h" * len(pcm), *pcm))

                
                if result == 0:
                    print('[%s] Detected Hermione' % str(datetime.now()))
                    self.detected = True
                    return
                elif result == 1:
                    print('[%s] Detected Stop Music' % str(datetime.now()))
                    self.stopmsk = True
                    return

        except KeyboardInterrupt:
            print('Stopping ...')
        finally:
            return False


    def cleanup(self):
        if self.recorder:
            self.recorder.delete()
        if self.porcupine:
            self.porcupine.delete()
        if self.wav_file:
            self.wav_file.close()


if __name__ == "__main__":
    access_key = PiKEY
    kpath = "./wake_fr.ppn",  # outre ça
    mpath = "./porcupine_fr.pv",
    opath = "./output.wav"

    listener = PorcupineListener(access_key, kpath, mpath, opath)
    listener.initialize()

    try:
        listener.start_detection()
    finally:
        listener.cleanup()


