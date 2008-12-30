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
    snmpGetMap = GetMap({
        '.1.3.6.1.2.1.1.2.0':      'sysObjectID',

        # On some falcons, input 34 doesn't return
        # proper values during a walk, but does during
        # a get, so we'll get them here
        INPUT_PREFIX + '.34.1.0':  '34.1',
        INPUT_PREFIX + '.34.3.0':  '34.3',
        })

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results

        if not getdata.get('sysObjectID', '').startswith('.1.3.6.1.4.1.3184.1.1'):
            return None

        # Create a data structure
        data = {}
        for key in sorted(tabledata["inputs"][FalconInputs.INPUT_PREFIX]):
            pattern  = '^' + FalconInputs.INPUT_PREFIX.replace('.', '\.')
            pattern += '.([0-9]+)\.([0-9]+)\.0' 
            input, attribute = map(int, re.findall(pattern, key)[0])
            data[input] = data.get(input, {})
            data[input][attribute] = tabledata["inputs"][FalconInputs.INPUT_PREFIX][key]
        for key in sorted(getdata):
            match = re.findall("^([0-9]+)\.([0-9]+)$", key)
            if not match:
                continue
            input, attribute = map(int, match[0])
            data[input] = data.get(input, {})
            data[input][attribute] = getdata[key]

        # Build the model
        id = 0
        rm = self.relMap()
        for i in sorted(data.keys()):
            id            += 1
            om             = self.objectMap()
            om.id          = self.prepId("%d" % id)
            om.type        = data[i].get(1, 0)
            om.snmpindex   = "%d.2.0" % i
            om.description = data[i].has_key(13) and data[i].get(5, "") or data[i].get(3, "")

            # (ABOVE) If we have a 13 column input, the description is in column 5
            # Otherwise we will assume this is a 5 column input (description in column 3)

            rm.append(om)
        return rm
