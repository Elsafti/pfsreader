__author__ = 'are'
___doc___ = '''Python Wrapper Class for Parsing / Writing MSHE wel files.'''

from collections import OrderedDict

from utilities.PFS.PfsFile import PfsFile


class WelFile(PfsFile):
    """
    Python Wrapper Class for Parsing / Writing MSHE wel files.
    """
    defaultwell = OrderedDict(
        [('ID', " 'New well'\n"), ('XCOR', 364016.88104089221), ('YCOR', 6272046.765799256), ('LEVEL', 0),
         ('WELLDEPTH1', 0), ('WELL_FIELD_ID', 0), ('FILTERDATA', OrderedDict([('Touched', 0), ('NoFilters', 1), (
        'FILTERITEM_1', OrderedDict(
            [('Top', 30), ('Bottom', 20), ('AbstrUsed', 1), ('AbstrRedFactor', 1), ('Radius', 0.25), ('Storage', 0), (
            'TIME_SERIES_FILE', OrderedDict(
                [('Touched', 0), ('FILE_NAME', ' |.\\PumpingRate1.dfs0|\n'), ('ITEM_COUNT', 1),
                 ('ITEM_NUMBERS', 1)]))]))])),
         ('LITOGRAFIDATA', OrderedDict([('Touched', 0), ('NoLitografiLayers', 0)]))])

    def getWellInfoByIndex(self, wellindex):
        """
        returns all properties of a well specified by its index as a dictionary structure.
        :param wellindex: index of the well, starting from 1
        :type wellindex: int
        :return: well properties as dictionary structure
        :rtype: dict
        """
        wellitems = self.rawdata['WEL_CFG']['WELLDATA']
        return wellitems['WELLNO_' + str(int(wellindex))].copy()

    def clearAllWells(self):
        """
        removes all wells from file.
        :return:
        """
        wellitems = self.rawdata['WEL_CFG']['WELLDATA']
        for itemname in wellitems.keys():
            item = wellitems[itemname]
            if type(item) == OrderedDict:
                del self.rawdata['WEL_CFG']['WELLDATA'][itemname]
        self.rawdata['WEL_CFG']['WELLDATA']['NoWells'] = 0

    def addWell(self, wellinfo):
        """
        adds a well to the file
        :param wellinfo: a dictionary structure containing the well properties. Use the .defaultwell member as template
        :type wellinfo: dict
        :return:
        """
        wellitems = self.rawdata['WEL_CFG']['WELLDATA']
        nowells =  int(wellitems["NoWells"])+1
        wellitems['WELLNO_'+str(nowells)] = wellinfo
        wellitems['NoWells'] = nowells

