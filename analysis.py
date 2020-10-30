import numpy as np
import socketIO_client
from keras.models import model_from_json
from socketIO_client import SocketIO, LoggingNamespace
import json

from socketIO_client.transports import get_response
from socketIO_client.parsers import get_byte, _read_packet_text, parse_packet_text

from requests.exceptions import ConnectionError

# extra function to support XHR1 style protocol
def _new_read_packet_length(content, content_index):
    packet_length_string = ''
    while get_byte(content, content_index) != ord(':'):
        byte = get_byte(content, content_index)
        packet_length_string += chr(byte)
        content_index += 1
    content_index += 1
    return content_index, int(packet_length_string)


def new_decode_engineIO_content(content):
    content_index = 0
    content_length = len(content)
    while content_index < content_length:
        try:
            content_index, packet_length = _new_read_packet_length(
                content, content_index)
        except IndexError:
            break
        content_index, packet_text = _read_packet_text(
            content, content_index, packet_length)
        engineIO_packet_type, engineIO_packet_data = parse_packet_text(
            packet_text)
        yield engineIO_packet_type, engineIO_packet_data


def new_recv_packet(self):
    params = dict(self._params)
    params['t'] = self._get_timestamp()
    response = get_response(
        self.http_session.get,
        self._http_url,
        params=params,
        **self._kw_get)
    for engineIO_packet in new_decode_engineIO_content(response.content):
        engineIO_packet_type, engineIO_packet_data = engineIO_packet
        yield engineIO_packet_type, engineIO_packet_data


setattr(socketIO_client.transports.XHR_PollingTransport, 'recv_packet', new_recv_packet)

def on_aaa_response(*args):
    splitData = str(args).split('\'')
    print(str(splitData[1]))
    tensorData = make_numpy("C:\\Users\\zmzmd\\Desktop\\test\\analysis_test.json")
    SData = tensorData / 100

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    # 해당 값을 소켓 통신으로 보내면 됨
    analysisData = ""

    for k in range(len(SData)):
        analysisData += str(np.argmax(model.predict(SData[k].reshape(1, 34)))) + ","

    push_data(analysisData[0:-1])

def My_connect():
    print('connect')

def make_numpy(path):
    Sdata = read_file(path)

    return np.array(Sdata[0:-1])

def read_file(path):
    with open(path) as json_file:
        json_data = json.load(json_file)

    return json_data

def learn_load():
    json_file = open('C:\\node_searver\\src\\python\\model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)

    return loaded_model

def read_model():
    global model

    model = learn_load()

    model.load_weights("C:\\Users\\zmzmd\\Desktop\\test\\Action_model.h5")
    print("Loaded model Complete")

def push_data(data):
    socketIO.emit('add ActionData', data)
    print('Push Complete')

read_model()
socketIO = SocketIO('http://49.50.172.88', 4000, LoggingNamespace)
socketIO.on("connect", My_connect)
socketIO.on('push PoseData', on_aaa_response)
socketIO.wait()