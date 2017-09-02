import functools
import queue
import threading
import logging
import os
import subprocess
import uuid
from yandex_speech import TTS


logging.basicConfig(level="INFO", format="%(name)s : %(levelname)s : %(message)s")


@functools.total_ordering
class TaskGenerateText:
    def __init__(self, priority, data, key):
        self.priority = int(priority)
        self.data = data
        self.key = key
        logging.info('Create task with: %s' % self.data)

    def play(self):
        try:
            if self.data.get('text'):
                filename = str(uuid.uuid4())
                tts = TTS(self.data.get('speaker', 'jane'),
                          'mp3',
                          self.key,
                          lang=self.data.get('lang', 'ru‑RU'),
                          emotion=self.data.get('emotion', 'neutral'),
                          speed=float(self.data.get('speed', 1.0)),
                          )
                tts.generate(self.data.get('text'))
                tts.save(filename)

                subprocess.call(['ffplay', '-nodisp', '-autoexit', '%s.mp3' % filename])
                os.remove('%s.mp3' % filename)
        except Exception as e:
            logging.exception("Erorr by play sound!")

    def __eq__(self, other):
        try:
            return self.priority == other.priority
        except AttributeError:
            return NotImplemented

    def __lt__(self, other):
        try:
            return self.priority < other.priority
        except AttributeError:
            return NotImplemented
