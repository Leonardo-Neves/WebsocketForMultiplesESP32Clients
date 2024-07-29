import numpy as np
import warnings

from utils.websocket import WebSocket

warnings.simplefilter("ignore")

web_socket = WebSocket('0.0.0.0', 5000)

web_socket.startWebSocket()