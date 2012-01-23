######################################################################
#
# Copyright 2008 Zenoss, Inc.  All Rights Reserved.
#
######################################################################

__doc__="""Input

Input is an installed sensor on a Falcon environment monitoring device

$Id: $"""

__version__ = "$Revision: $"[11:-2]

import locale

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenUtils.Utils import convToUnits
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenUtils.Utils import prepId

class Input(DeviceComponent, ManagedEntity):
    """Falcon Input"""

    portal_type = meta_type = 'Input'
    
    description  = ""
    type        = 0

    _properties = (
        {'id':'description',  'type':'string',  'mode':''},
        {'id':'type',  'type':'int', 'mode':''},
        )

    _relations = (
        ("falcon", ToOne(ToManyCont,
            "ZenPacks.zenoss.FalconMonitor.FalconDevice", "inputs")),
        )

    factory_type_information = ( 
        { 
            'id'             : 'Input',
            'meta_type'      : 'Input',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'Input_icon.gif',
            'product'        : 'FalconMonitor',
            'factory'        : 'manage_addInput',
            'immediate_view' : 'viewInput',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewInput'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Template'
                , 'action'        : 'objTemplates'
                , 'permissions'   : (ZEN_CHANGE_SETTINGS, )
                },                
                { 'id'            : 'viewHistory'
                , 'name'          : 'Modifications'
                , 'action'        : 'viewHistory'
                , 'permissions'   : (ZEN_VIEW, )
                },
            )
          },
        )

    def device(self):
        return self.falcon()

    def getTypeDescription(self):
        return ("not installed", "not installed", "analog", "digital", "digital")[self.type]

    def primarySortKey(self):
        return int(self.id)

InitializeClass(Input)
