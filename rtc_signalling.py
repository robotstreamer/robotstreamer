from ws4py.client.threadedclient import WebSocketClient
import json
import sys
import os

class SFUClient(WebSocketClient):


    def init(self, streamKey, videoCodec, videoSSRC, audioSSRC):
        self.videoEndpoint = False
        self.audioEndpoint = False

        self.streamKey = streamKey
        self.videoSSRC = videoSSRC
        self.audioSSRC = audioSSRC
        self.videoCodec = videoCodec

    def opened(self):
        self.send(json.dumps({  'request':True,
                                'id': 0,
                                'method'  : 'join',   
                                'data'    : {'rtpCapabilities' : {'dummy': 'dummy'}}   
                            }))


    def getRouterRtpCapabilities(self):
        self.send(json.dumps({  'request':True,
                                'id': 1,
                                'method'  : 'getRouterRtpCapabilities',   
                                'data'    : {}   
                            }))


    def requestPlainTransportVideo(self):
        self.send(json.dumps({  'request':True,
                                'id': 20,
                                'method'  : 'createPlainRtcTransport',   
                                'data'    : {'producing' : True,
                                             'consuming' : False,
                                             'streamkey' : self.streamKey}   
                            }))

    def requestPlainTransportAudio(self):
        self.send(json.dumps({  'request':True,
                                'id': 21,
                                'method'  : 'createPlainRtcTransport',   
                                'data'    : {'producing' : True,
                                             'consuming' : False,
                                             'streamkey' : self.streamKey}   
                            }))

    def requestCreateProducerVideo(self, transportId):
        self.send(json.dumps({  'request':True,
                                'id': 3,
                                'method'  : 'produce',   
                                'data'    : {
                                            'transportId' : transportId,
                                            'kind' : 'video',
                                            'rtpParameters' : {
                                                    'codecs': [{'mimeType' : str(self.videoCodec), 
                                                                'payloadType': 101, 
                                                                'parameters': 
                                                                    {'packetization-mode': 1,
                                                                     'profile-level-id': '42e01f',
                                                                     'level-asymmetry-allowed': 1},
                                                                'clockRate':90000 }],
                                                                'encodings': [{ 'ssrc': self.videoSSRC }] 
                                                              }           
                                            }   
                            }))

    def requestCreateProducerAudio(self, transportId):
        self.send(json.dumps({  
                            'request':True,
                            'id': 4,
                            'method'  : 'produce',   
                            'data'    : {
                                        'transportId' : transportId,
                                        'kind' : 'audio',
                                        'rtpParameters' : {'codecs': [{'mimeType' :"audio/opus", 
                                                                       'payloadType': 100, 
                                                                       'channels': 2, 
                                                                       'clockRate':48000,
                                                                       'parameters':{ 'sprop-stereo':1 } }],
                                                                       'encodings': [{ 'ssrc': self.audioSSRC }] 
                                                          }           
                                        }   
                            }))

    def closed(self, code, reason=None):
        print ("Websocket closed:", reason)
        #os.system("killall ffmpeg")
        #os._exit(0)

    def received_message(self, m):
        message = json.loads(str(m))

        #join room
        if message['id'] == 0:
            print('join response:')
            print(message)

        #getRouterRtpCapabilities
        if message['id'] == 1:
            print('getRouterRtpCapabilities response:')
            #print(json.dumps(message, indent=2)) 

        #createPlainRtcTransport 20 = video
        if message['id'] == 20:
            print('createPlainRtcTransport video response:', message)
            self.requestCreateProducerVideo(message['data']['id'])
            self.videoEndpoint = message['data']['tuple']

        #createPlainRtcTransport 21 = audio
        if message['id'] == 21:
            print('createPlainRtcTransport audio response:', message)
            self.requestCreateProducerAudio(message['data']['id'])
            self.audioEndpoint = message['data']['tuple']

        if message['id'] == 3:
            print('requestCreateProducerVideo response:', message)
        
        if message['id'] == 4:
            print('requestCreateProducerAudio response:', message)
