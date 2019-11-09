import socket

class Project:

    def __init__(self, myOp):
        self.MyOp = myOp
        self.Role = myOp.par.Role
        self.MachineName = socket.gethostname()
        self.MachineIp = socket.gethostbyname(self.MachineName)

        # confirm in text port that we've inited the project class
        print("Project init from {}".format(myOp))

    def RoleColor(self, role):
        # color dict
        color = {
            'controller'        : (0.205, 0.0, 0.227),
            'draw'              : (0.0, 0.114, 0.020),
            'mixedController'   : (0.0, 0.169, 0.178),
            'standby'           : (0.108, 0.0, 0.0),
            'default'           : (0.1, 0.105, 0.112)
        }

        # our default color is in the color dict, and is the default bg color of TD
        default = color.get('default')
        return color.get(role, default)

    def ChangeBg(self, role=''):
        # changes the bg of TD based on the role
        color = self.RoleColor(role)
        ui.colors['worksheet.bg'] = color

    def SetMachineGrouping(self):
        role = self.GetCurrentRole()
        if role in ['controller', 'mixedController']:
            op.Project.par.Machinegrouping = 'server'
        
        else:
            op.Project.par.Machinegrouping = 'client'

    def RequestRemoteReload(self, targetOp):
        msg = {
            'messagekind'	: 'ReloadRemoteTox',
            'target'        : 'all',
            'targetOp'		: targetOp,
            'sender'		: op.Project.Role.eval(),
            'output'		: None,
            'value'			: op(targetOp).par.externaltox.eval()
            }

        op.Com.SendMulticast(msg)
        print(targetOp)
        pass

    def RequestParsSync(self, targetOp):
        if 'syncPars' in targetOp.tags:
                
            parsDict = self.ParValsToDict(targetOp)
            msg = {
                'messagekind'   : 'SyncParsToTargetOp',
                'target'        : 'all',
                'targetOp'      : targetOp.path,
                'sender'        : op.Project.Role.eval(),
                'vals'          : parsDict
            }
            op.Com.SendMulticast(msg)
        else:
            pass
        pass

    def ConfigureProject(self, role=None):
        if role == None:
            role = self.GetCurrentRole()
        else:
            role = role
        # this is our configuration order of operations
        self.ChangeBg(role)
        self.SetMachineGrouping()
        #op('container_output').Setup(role)

    def GetCurrentRole(self):
        return self.Role.eval()

    def ActiveParSync(self):
        return True if op.Project.par.Machinegrouping == 'server' else False

    def SetUpParExec(self, fromOp):
        currentOp = self.GetCurrentOp()

        if currentOp.type == 'moviefilein':
            parConstraint = '^index'
        else:
            parConstraint = '*'
        fromOp.par.pars = parConstraint
        return currentOp

    def GetCurrentOp(self):
        networkLocation = ui.panes.current.owner
        return [op for op in networkLocation.findChildren(depth=1) if op.current][0]

    def ParValsToDict(self, targetOp):
        parDict = {}

        for eachPar in targetOp.pars():
            parDict[eachPar.name] = eachPar.eval()

        return parDict

    def UpdateOpPars(self, targetOp, parsDict):
        for eachKey, eachVal in parsDict.items():
            setattr(targetOp.par, eachKey, eachVal)
        pass

    def PageToDict(self, target_op, target_page, ignore_list):
        # create empty par_dict with input name as the preset_name value
        par_dict = {}

        # loop through each parameter in the target_op and capture its name and
        # value only if its custom page matches the input string for target_page, 
        # and the pars are not on the ignore_list
        for each_par in target_op.pars():
            if each_par.isCustom and each_par.page == target_page and each_par.name not in ignore_list:
                par_dict[each_par.name] = each_par.val
        return par_dict

    def UpdateCustomPars(self, target_op, parsDict):
        for each_key, each_val in parsDict.items():
            setattr(target_op.par, each_key, each_val)
        pass

    def UpdateCustomInternalPars(self, target_op, parsDict):
        targetiop = op( target_op.par.iop1.eval() )
        for each_key, each_val in parsDict.items():
            setattr(targetiop.par, each_key, each_val)
        pass