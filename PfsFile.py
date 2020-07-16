__author__ = 'are'


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


    def getItemValue(self,parent,key,order=None):
        indecies=[i for i, e in enumerate(parent) if e == key]
        if(len(indecies)==0):
            raise Exception("Error: Key: "+str(key)+" is not a key in the given target/section!")
        if(len(indecies)>1 and order==None):
            print("WARNING: key "+str(key)+" is not unique in the given target/section! Please provide an order for the key!")
            return parent[indecies[0]+1]
        elif (order!=None and order>=len(indecies)):
            raise Exception("Error: key "+str(key)+" was not found at the given order or key not found!")
        else:
            if(order==None): order=0
            return parent[indecies[order]+1]

    def getItemIndex(self,parent,key,order=None):
        indecies=[i for i, e in enumerate(parent) if e == key]
        if(len(indecies)==0):
            raise Exception("Error: Key: "+str(key)+" is not a key in the given target/section!")
        if(len(indecies)>1 and order==None):
            print("WARNING: key "+str(key)+" is not unique in the given target/section! Please provide an order for the key!")
            return parent[indecies[0]]
        elif (order!=None and order>=len(indecies)):
            print("Error: key "+str(key)+" was not found at the given order or key not found!")
        else:
            if(order==None): order=0
            return (indecies[order]+1)
        
    def getItemString(self, parent,indentation=0):
        string=''
        if (type(parent) != list):
            return parent
        for index in range(0,len(parent),2):
            itemname = parent[index]
            item     = parent[index+1]
            if type(item) == list:
                string+=(indentation * ' ' + str(itemname) + '\n')
                string+=self.getItemString(item, indentation + 3)
                string+=(indentation * ' ' + 'EndSect  // ' + str(itemname.strip("[").strip("]")) + '\n\n')
            else:
                if str(item).strip() == "True":
                    item = "true"
                if str(item).strip() == "False":
                    item = "false"

                string+=(indentation * ' ' + str(itemname) + ' = ' + str(item).strip() + '\n')
        return string
                
    def __getitem__(self, key):
        reqRawdata=self.rawdata
        for i, e in enumerate(key):
            if(i<(len(key)-1) and type(key[i+1])==int ):
                reqRawdata=self.getItemValue(reqRawdata,e,key[i+1])
            elif(type(e)!=int):
                reqRawdata=self.getItemValue(reqRawdata,e)
        return self.getItemString(reqRawdata)

    def __setitem__(self, key, value):
        dummy=self.__getitem__(key)
        if(type(dummy)!=type(value)):
            raise Exception("Error: type of given value does not match type of referred item!")
        
        index=[]
        accSections=[self.rawdata]
        order=0
        if(type(key[1])==int):
            order=key[1]
        else:
            order=0
        indecies=[i for i, e in enumerate(self.rawdata) if e == key[0]]
        index.append(indecies[order])
        for i, aKey in enumerate(key):
            if(i<(len(key)-1) and type(key[i+1])==int):
                order=key[i+1]
            else:
                order=0
            if(type(aKey)!=int):
                index.append(self.getItemIndex(accSections[-1],aKey,order))
                accSections.append(accSections[-1][index[-1]])
        for i, section in enumerate(accSections):
            if(i==0):
                accSections[-1]=value
            else:
                accSections[len(accSections)-1-i][index[len(index)-i]]=accSections[len(accSections)-i]
                
        self.rawdata = accSections[0]

    # TODO (please don't remove)

    #def copy(self):
    #    make new subsections as copy of existing 
    
    #def __delitem__(self, key):
    #    del self.__dict__[key]

    #def __contains__(self, key):
    #    return key in self.__dict__

    #def __len__(self):
    #    return len(self.__dict__)

    def _loadNestedItem(self, parent, infile):  # recursive function that loads all objects into a tree of dictionaries
        line = infile.readline()  # start recursive action
        while "EndSect" not in line and len(line) > 0:  # abort recursive action if End of Section is reached or EOF
            if len(line.strip()) and line.strip()[0] == "[":
                child_name = line.strip()
                parent.append(child_name)
                parent.append([])
                self._loadNestedItem(parent[-1], infile)
            elif "=" in line:
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
                parent.append(field_name) 
                parent.append(field_value)
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
        # TODO Change to one variable called header containing all lines starting with // 
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
        self.rawdata = [] 
        while line != "":  # end of file
            if len(line.strip()) and line.strip()[0] == "[": 
                top_level_name = line.strip()
                self.rawdata.append(top_level_name) 
                self.rawdata.append([]) 
                self._loadNestedItem(self.rawdata[-1], infile)
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
        for index in range(0,len(parent),2): # iterate through properties and children
            itemname = parent[index]
            item     = parent[index+1]
            if type(item) == list: # is child
                outfile.write(indentation * ' ' + str(itemname) + '\n')
                self._saveNestedItem(item, outfile, indentation + 3)
                outfile.write(indentation * ' ' + 'EndSect  // ' + str(itemname.strip("[").strip("]")) + '\n\n')
            else:  # is property

                if str(item).strip() == "True":
                    item = "true"
                if str(item).strip() == "False":
                    item = "false"

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
