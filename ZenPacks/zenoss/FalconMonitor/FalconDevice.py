##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2007, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


from Globals import InitializeClass
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.Device import Device
from Products.ZenModel.ZenossSecurity import ZEN_VIEW
from copy import deepcopy


class FalconDevice(Device):
    "A Falcon Environment Monitoring Module"

    _relations = Device._relations + (
        ('inputs', ToManyCont(ToOne,
            'ZenPacks.zenoss.FalconMonitor.Input', 'falcon')),
        )
    
    
    factory_type_information = deepcopy(Device.factory_type_information)
    custom_actions = []
    custom_actions.extend(factory_type_information[0]['actions'])
    custom_actions.insert(2,
           { 'id'              : 'falconDeviceDetails'
           , 'name'            : 'Inputs'
           , 'action'          : 'falconDeviceDetails'
           , 'permissions'     : (ZEN_VIEW, ) },
           )
    factory_type_information[0]['actions'] = custom_actions
    

    def __init__(self, *args, **kw):
        Device.__init__(self, *args, **kw)
        self.buildRelations()

InitializeClass(FalconDevice)
