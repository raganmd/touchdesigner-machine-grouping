import json

class Com:
    '''
        This class handles sending and receiving multicast data in a TouchDesigner network
            Usually sent as a dict containing keys
            message = {
                'messagekind'	: ,
                'target'		: ,
                'targetOp'      : ,
                'sender'		: ,
                'output'		: ,
                'pars'		    : ,
                'value'			:
                }
    '''

    def __init__(self, myOp):

        self.MyOp = myOp
        self.MultiCastOutDAT = op('base_udp_multicast/udpout_multicast')
        print("Com init from {}".format(self.MyOp))

    def SendMulticast(self, pyObj):
        message = json.dumps(pyObj).encode('utf-8')
        self.MultiCastOutDAT.sendBytes(message)
        pass

    def ReceiveMulticast(self, message):
        message = json.loads(message.decode('utf-8'))

        if message.get('target') == None:
            print("Missing Target for Communication")
        else:
            self.ProcessMessage(message)
        pass

    def ProcessMessage(self, message):
        if hasattr(self.MyOp, message.get('messagekind', None)):
            function = getattr(self.MyOp, message.get('messagekind', None))
            function(message)
        else:
            print('Invalid Call')
        pass