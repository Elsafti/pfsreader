__author__ = 'are'

from collections import OrderedDict


class PfsFile:
    """
    Python Wrapper Class for Parsing MIKE ZERO Pfs files. Acts as a Superclass for derived formats.
    """

    ## path to the file
    filename = None
    ## nested dictionary containing the tree structure of the pfs file
    rawdata = None

    ## Constructor
    def __init__(self, filename=None):
        """
        :rtype : object
        """
        self.filename = filename
        self.created = ""
        self.dllid = ""
        self.pfsversion = ""

        if filename:
            self.loadFrom(filename)

    def _loadNestedItem(self, parent, infile):  # recursive function that loads all objects into a tree of dictionaries
        line = infile.readline()  # start recursive action
        while "EndSect" not in line and len(line) > 0:  # abort recursive action if End of Section is reached or EOF
            if len(line.strip()) and line.strip()[0] == "[":
                child_name = line.strip()
                parent[child_name] = OrderedDict()
                self._loadNestedItem(parent[child_name], infile)
            if "=" in line:
                field_name, field_value = line.split("=")
                if field_value[1] == "\'":  # field value is a string
                    while field_value.strip()[-1] != "\'":
                        field_value = field_value + infile.readline()
                    field_value = field_value.strip("\'")
                elif field_value.strip() == "true":
                    field_value = True  # field value is boolean:True
                elif field_value.strip() == "false":
                    field_value = False  # field value is boolean:False
                elif "." in field_value or 'e' in field_value:  # field value might be floating point
                    try:
                        field_value = float(field_value)
                    except ValueError:
                        pass
                else:
                    try:
                        field_value = int(field_value)
                    except ValueError:
                        pass
                field_name = field_name.strip()
                parent[field_name] = field_value
            line = infile.readline()

    ## Parses contents from file into rawdata structure
    def loadFrom(self, filename):
        """Imports the data from a file given by path <filename>
        :param filename: file to be loaded
        :type filename: str
        :type self: object
        """
        self.filename = filename
        infile = open(filename)

        # read metadata
        line = ""
        while "[" not in line:  # iterate until first top level branch
            line = infile.readline()
            if len(line.strip()) < 1:
                continue
            if "// Created" in line:
                self.created = line.strip("//")
                continue
            if "// DLL id" in line or "// DLL" in line:
                self.dllid = line.strip("//")
                continue
            if "// PFS version" in line or "// Version" in line:
                self.pfsversion = line.strip("//")
                continue

        # recursive root for each top level structure
        self.rawdata = OrderedDict()
        while line != "":  # end of file
            if len(line.strip()) and line.strip()[0] == "[": 
                top_level_name = line.strip()
                self.rawdata[top_level_name] = OrderedDict()
                self._loadNestedItem(self.rawdata[top_level_name], infile)
            line = infile.readline()

        # finalize
        infile.close()

    def _saveNestedItem(self, parent, outfile, indentation=0):
        """
        recursive procedure to write a node of the PFS tree
        :param parent: dictionary
        :param outfile: file object of the destination file, in writing access mode
        :param indentation: indentation (number of whitespaces to be written) for better formatting
        :type indentation: int
        :return:
        """
        for itemname in parent.keys():  # iterate through properties and childs
            item = parent[itemname]
            if type(item) == OrderedDict:  # is child
                outfile.write(indentation * ' ' + str(itemname) + '\n')
                self._saveNestedItem(item, outfile, indentation + 3)
                outfile.write(indentation * ' ' + 'EndSect  // ' + str(itemname.strip("[").strip("]")) + '\n\n')
            else:  # is property
                outfile.write(indentation * ' ' + str(itemname) + ' = ' + str(item).strip() + '\n')

    def saveTo(self, filename):
        """
        Saves the data to the file given by <filename>.
        :param filename: path to the file to be written.
        :return:
        """

        # open file and write metadata
        outfile = open(filename, "w")
        outfile.write('//' + self.created)
        outfile.write('//' + self.dllid)
        outfile.write('//' + self.pfsversion)
        outfile.write('\n')

        # start recursion
        self._saveNestedItem(self.rawdata, outfile)

        # finalize
        outfile.close()
