import atexit
import logging
import threading
import time
from abc import abstractmethod
from enum import Enum

import msgpack_numpy as msgpack
import numpy as np
import zmq
from zmq.utils import jsonapi


class Protocol(Enum):
    TCP = 1
    IPC = 2


class Tracker:

    def __init__(self, name: str, color: tuple, debug=False):

        self._name = name
        self._color = color

        self._client_socket = None
        self._fps = 0

        self.debug = debug
        self.logger = self._setup_logger()

        atexit.register(self._close)

    @abstractmethod
    def initialize(self, frame: np.ndarray, init_bbox: list):
        """

        :param frame: Image as a numpy array of dimensions [W,H,C]
        :param init_bbox: Init bbox rectangle coordinates [x,y,w,h]

         :return: State dict [Optional]
        """
        pass

    @abstractmethod
    def track(self, frame: np.ndarray, state_dict=None) -> tuple:
        """

        :param frame: Image as a numpy array of dimensions [W,H,C]
        :param state_dict: State from the previous track, if necessary

        :return: Rectangle coordinates of the recognized object and confidence ([x,y,w,h], p)
        """
        pass

    def setup(self,
              protocol: Protocol,
              socket_address: str = "/tmp/server_socket",
              host: str = "127.0.0.1",
              port: str = "8080"):
        """

        :param protocol:
        :param socket_address:
        :param host:
        :param port:
        """
        context = zmq.Context()
        self._client_socket = context.socket(zmq.DEALER)
        self._client_socket.setsockopt_string(zmq.IDENTITY, self._name)
        if protocol == Protocol.IPC:
            self._client_socket.connect(f"ipc://{socket_address}")
            self.logger.info(f"Connected to {socket_address}")
        elif protocol == Protocol.TCP:
            self._client_socket.connect(f"tcp://{host}:{port}")
            self.logger.info(f"Connected to {host}:{port}")

    def start(self):
        try:
            while True:
                self._client_socket.send_multipart([b"info", jsonapi.dumps({
                    'color': self._color,
                })])

                self.logger.info("The tracker is ready for use")

                thread = threading.Thread(target=self._accept)
                thread.start()
                thread.join()
        except Exception as e:
            self.logger.error(f"An error occurred in start method: {str(e)}")

    def _accept(self):
        try:
            while True:

                message = self._client_socket.recv()
                message = jsonapi.loads(message)
                init_frame = np.array(message['init_frame'], dtype=np.uint8)
                init_bbox = message['init_bbox']

                self.logger.info("Tracker initialized")
                self.logger.debug("Initial Bbox: %s", init_bbox)

                state_dict = self.initialize(init_frame, list(init_bbox))

                self.logger.info("Tracking...")

                while True:
                    status, message = self._client_socket.recv_multipart()
                    status = status.decode()

                    if status == "stop":
                        self.logger.info("Tracking stopped")
                        break

                    frame = msgpack.unpackb(message)

                    self.logger.debug("Frame shape: %s", frame.shape)

                    if frame is None:
                        break

                    t1 = time.time()
                    bbox, confidence = self.track(frame, state_dict)
                    t2 = time.time()
                    delay = str((t2 - t1))
                    result = {"delay": delay, "confidence": confidence, "bbox": bbox}

                    self.logger.debug("Bbox: %s", bbox)
                    self.logger.debug("Confidence: %s", confidence)

                    self._client_socket.send_multipart([b"data", jsonapi.dumps(result)])
                time.sleep(1)
        except Exception as e:
            self.logger.error(f"An error occurred in _accept method: {str(e)}")

    def _close(self):
        try:
            self._client_socket.send_multipart([b"close", jsonapi.dumps({})])
            print("Connection closed")
        except zmq.ZMQError as e:
            print(f"Close failed {e}")

    def _setup_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG if self.debug else logging.INFO)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG if self.debug else logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)

        logger.addHandler(ch)

        return logger
