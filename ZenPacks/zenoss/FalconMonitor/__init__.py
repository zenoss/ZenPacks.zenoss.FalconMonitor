######################################################################
#
# Copyright 2007 Zenoss, Inc.  All Rights Reserved.
#
######################################################################

import Globals
from Products.CMFCore.DirectoryView import registerDirectory
registerDirectory("skins", globals())

from Products.ZenModel.ZenPack import ZenPack as Base

class ZenPack(Base):
    def install(self, app):
        Base.install(self, app)
        self.migrate()

    def upgrade(self, app):
        Base.upgrade(self, app)
        self.migrate()
