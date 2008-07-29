######################################################################
#
# Copyright 2008 Zenoss, Inc.  All Rights Reserved.
#
######################################################################

import Globals
from Products.ZenModel.migrate.Migrate import Version
from Products.ZenModel.ZenPack import ZenPack

class Menu:
    version = Version(2, 0, 0)

    def migrate(self, pack):
        dmd = pack.__primary_parent__.__primary_parent__
        id = 'falconDeviceDetails'
        try:
            dmd.zenMenus.More.manage_deleteZenMenuItem((id,))
        except (KeyError, AttributeError):
            pass
        dmd.zenMenus.More.manage_addZenMenuItem(
            id,
            action=id,
            description='Falcon Details',
            allowed_classes=('FalconDevice',),
            ordering=5.0)

Menu()
