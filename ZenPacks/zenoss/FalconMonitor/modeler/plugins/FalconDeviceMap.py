######################################################################
#
# Copyright 2008 Zenoss, Inc.  All Rights Reserved.
#
######################################################################

__doc__="""FalconDeviceMap

FalconDeviceMap maps the device level information for Falcon Environmental monitors.

$ID: $"""

__version__ = '$Revision: $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap

class FalconDeviceMap(SnmpPlugin):

    maptype = "FalconDeviceMap"

    snmpGetMap = GetMap({
        '.1.3.6.1.2.1.1.2.0': 'sysObjectID',
        '.1.3.6.1.4.1.3184.1.1.1.1.1.0': 'manufacturer',
        '.1.3.6.1.4.1.3184.1.1.1.1.2.0': 'model',
        '.1.3.6.1.4.1.3184.1.1.1.1.3.0': 'firmwareVersion',
        })

    def process(self, device, results, log):
        log.info("processing %s for device %s", self.name(), device.id)
        getdata, tabledata = results
        if not getdata['sysObjectID'].startswith('.1.3.6.1.4.1.3184.1.1'):
            return None
            
        om = self.objectMap()
        om.setHWProductKey = getdata['manufacturer'] + " " + getdata['model']
        om.setOSProductKey = 'Falcon OS ' + getdata['firmwareVersion']
        return om
