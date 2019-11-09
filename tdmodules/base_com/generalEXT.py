com = mod('comEXT').Com

class GeneralCom(com):
    def __init__(self, myOp):
        self.MyOp   = myOp

        com.__init__(self, self.MyOp)
        print("GeneralCom init from {}".format(self.MyOp))
    
    def ReloadRemoteTox(self, message):
        '''
            Intended to reload a tox - this assumes that the repo is synced across machines
            or that you're working on machine that has access to the most recent version of 
            a tox
        '''
        role = op.Project.GetCurrentRole()

        if role in ['controller', 'mixedController']:
            pass
        else:
            target = message.get('targetOp')
            externalToxPath = message.get('value')
            op(target).par.externaltox = externalToxPath
            op(target).par.reinitnet.pulse()
            pass

    def SyncParsToTargetOp(self, message):
        role = op.Project.GetCurrentRole()

        targetOp = op( message.get('targetOp') )
        parsDict = message.get('vals')

        if role in ['controller', 'mixedController']:
            pass

        else:
            print("updating")
            op.Project.UpdateOpPars(targetOp, parsDict)
        pass

    def UpdateTargetBase(self, message):
        '''
        Exmample Message

            message = {
                'messagekind'	: 'UpdateTargetBase',
                'target'        : None,
                'targetOp'		: 'base_movie_player_msg_mode',
                'sender'		: op.Project.Role.eval(),
                'output'		: None,
                'pars'		    : dictOfPars,
                'value'			: None
                }
        '''

        role = op.Project.GetCurrentRole()

        if role == 'draw' or role == 'controller' or role == 'mixedController':
            targetOp    = op.Scenes.op(message.get('targetOp'))
            parsDict    = message.get('pars')
            op.Project.UpdateCustomInternalPars(targetOp, parsDict)
        
        else:
            pass