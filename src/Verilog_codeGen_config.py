
import os
import json
from json import JSONEncoder
from pathlib import Path


class Verilog_codeGen_config(JSONEncoder):
    """verilog code generator config"""


    def __init__(self, configFile, searchPaths=[], author="", tabwidth=0):
        """
        :configFile: config file with absolute path which is used for this config object
        :searchPaths: search paths used for module instantiation, passed as iterable containing full absolut path strings
        :author: string used as file author
        :tabwidth: preferred tabwidth used to create global IndentObj
        """

        self.__configFile = configFile
        self.searchPaths = searchPaths
        self.author = author
        self.tabwidth = tabwidth


    def get_configFile(self):
        return self.__configFile


    def __str__(self):
        return "".join( ["configuration file: ", str(self.__configFile), "\n",
                        "search paths: ", str(self.searchPaths), "\n",
                        "author: ", self.author, "\n",
                        "tabwidth: ", str(self.tabwidth) ] )


    def write_config(self):
        """writes the config in json format to self.__configFile
        """
        #### check config file existance ####
        if isinstance(self.__configFile, str) and Path(self.__configFile).is_file():
            # file exists -> query for overwriting
            overwrite = input("Config file '" + self.__configFile + "' exists! Are you sure you want to overwrite it? [y/n]")

            if overwrite == 'y':
                print(self.__configFile + " will be overwritten...")
            else :
                print(self.__configFile + " will not be overwritten. Exiting...")
                return None

        #### write config file ####
        if isinstance(self.__configFile, str):
            with open(self.__configFile, "w") as file_out:
                json.dump( obj=self, fp=file_out, cls=self.__Verilog_codeGen_config_jsonEncoder, indent=4)                        
        else:
            json.dump( obj=self, fp=self.__configFile, cls=self.__Verilog_codeGen_config_jsonEncoder, indent=4)                        


    @classmethod
    def write_template(cls, dir_out):
        """writes an empty configuration file to dir_out, if given, otherwise to $HOME/.config/verilog_codeGen if $HOME/.config exists (->UNIX-system), otherwise just to the top level of this project
        """
        # determine output path
        if not dir_out:
            s_unixConfigPath = os.getenv("HOME") + "/.config"
            if os.path.isdir(s_unixConfigPath):
                dir_out = s_unixConfigPath + "/verilog_codeGen"
                # create dir_out if it does not exist
                try:
                    os.mkdir( dir_out )
                except:
                    pass
            else:
                dir_out = "/".join( os.path.abspath(__file__).split("/")[:-2] )
        
        # create empty config object
        emptyConfig = cls( dir_out + "/config.json", searchPaths=["",""], author="", tabwidth=4 )
        emptyConfig.write_config()
        print("Empty configuration file has been written to: " + dir_out + "/config.json")

    
    @classmethod
    def load(cls):
        """create a Verilog_codeGen_config object from a config file found by cls.find_config
        :returns: Verilog_codeGen_config object
        """
        s_configFile = cls.__find_config()
        if s_configFile:
            # parse json config file
            try:
                with open(s_configFile, "r") as file_in:
                    jsonObj = json.load( file_in )
                    searchPaths = jsonObj["searchPaths"] if jsonObj["searchPaths"] else []
                    author = jsonObj["author"] if jsonObj["author"] else ""
                    tabwidth = int(jsonObj["tabwidth"]) if jsonObj["tabwidth"] else 0
                    return cls(s_configFile, searchPaths, author, tabwidth)
            except Exception as e:
                print("Error while reading configuration from " + s_configFile + "!")
                return None
        else:
            return None


    @staticmethod
    def __find_config():
        """find config files in in $HOME/.config/verilog_codeGen or top-level directory (.config directory has higher priority)
        :returns: string with absolut path of found config, empty string if no config found
        """
        s_configFileName = "config.json"
        # search .config/verilog_codeGen directory
        s_configPath = os.getenv("HOME") + "/" + ".config/verilog_codeGen" 
        try:
            if s_configFileName in os.listdir(s_configPath):
                return s_configPath + "/" + s_configFileName
        except Exception as e:
            # directory s_configPath does not exist
            pass

        # search top level directory
        s_topLevelDir = "/".join( os.path.abspath(__file__).split("/")[:-2] )
        if s_configFileName in os.listdir(s_topLevelDir):
            return s_topLevelDir + "/" + s_configFileName
        
        # no config found
        return ""


    class __Verilog_codeGen_config_jsonEncoder(JSONEncoder):
        """specific json encoder for Verilog_codeGen_config"""

        def default(self, configObj):
            """override default method of JSONEncoder -> return a dictionary containing searchPaths, author and tabwidth 

           :configObj: Verilog_codeGen_config to be serialized
            """
            return { "searchPaths": configObj.searchPaths, "author": configObj.author, "tabwidth": configObj.tabwidth}

            
