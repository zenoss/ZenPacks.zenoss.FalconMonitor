######################################################################
#
# Copyright 2008 Zenoss, Inc.  All Rights Reserved.
#
######################################################################

__doc__="""FalconInputs

FalconInputs map Falcon devices to their installed sensors

$Id: $"""

__version__ = '$Revision: $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, \
        GetMap
from Products.DataCollector.plugins.DataMaps import ObjectMap
import re
import itertools

class WalkTree(object):

    def __init__(self, name, tableoid):
        self.name = name
        self.tableoid = tableoid
        self.colmap = {}
        self._oids = { tableoid: "all" }

    def getoids(self):
        """Return the raw oids used to get this table.
        """
        return self._oids.keys()

    def mapdata(self, results):
	return results


class FalconInputs(SnmpPlugin):

    INPUT_PREFIX = '.1.3.6.1.4.1.3184.1.1.1.3'

    relname = "inputs"
    modname = "ZenPacks.zenoss.FalconMonitor.Input"

    snmpGetTableMaps = (WalkTree("inputs", INPUT_PREFIX),)
    snmpGetMap = GetMap({'.1.3.6.1.2.1.1.2.0': 'sysObjectID',})

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results

        if not getdata['sysObjectID'].startswith('.1.3.6.1.4.1.3184.1.1'):
            return None

        # Create a data structure
        data = {}
        for key in tabledata["inputs"][FalconInputs.INPUT_PREFIX]:
            pattern  = '^' + FalconInputs.INPUT_PREFIX.replace('.', '\.')
            pattern += '.([0-9]+)\.([0-9]+)\.0' 
            input, attribute = map(int, re.findall(pattern, key)[0])
            data[input] = data.get(input, {})
            data[input][attribute] = tabledata["inputs"][FalconInputs.INPUT_PREFIX][key]

        # Build the model
        counter = itertools.count()
        counter.next()
        rm = self.relMap()
        for i in sorted(data.keys()):
            om              = self.objectMap()
            om.id           = self.prepId("%d" % counter.next())

            if   len(data[i]) == 13:
                om.type        = data[i][1]
                om.snmpindex   = "%d.2.0" % i
                om.description = data[i][5]
            elif len(data[i]) == 5:
                om.type        = data[i][1]
                om.snmpindex   = "%d.2.0" % i
                om.description = data[i][3]
            else:
                continue

            rm.append(om)
        return rm
