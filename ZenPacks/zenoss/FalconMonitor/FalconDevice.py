######################################################################
#
# Copyright 2007 Zenoss, Inc.  All Rights Reserved.
#
######################################################################

from Globals import InitializeClass
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.Device import Device


class FalconDevice(Device):
    "A Falcon Environment Monitoring Module"

    _relations = Device._relations + (
        ('inputs', ToManyCont(ToOne,
            'ZenPacks.zenoss.FalconMonitor.Input', 'falcon')),
        )

    def __init__(self, *args, **kw):
        Device.__init__(self, *args, **kw)
        self.buildRelations()

InitializeClass(FalconDevice)
