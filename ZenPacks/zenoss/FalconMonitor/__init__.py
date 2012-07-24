##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2007, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


import Globals
import os
from Products.CMFCore.DirectoryView import registerDirectory

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())


from Products.ZenModel.ZenPack import ZenPack as Base

class ZenPack(Base):
    def install(self, app):
        Base.install(self, app)
        self.migrate()

    def upgrade(self, app):
        Base.upgrade(self, app)
        self.migrate()
