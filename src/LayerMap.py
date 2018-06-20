# -*- coding: utf-8 -*-
import os
import json

class LayerMap(object):

    def __init__(self, configFile = None):
        # isConfigured when initing is false
        self.isConfigured = False
        if configFile:
            self.config(configFile)

    '''
    config:
    I : configFile, json configuration file. It is specified as follows:
    O : N/A
    Configure the layer map. After configuration, isConfigured will be set to true,
    giving meaningful returns for the following functions:
    '''
    def config(self, configFile):
        try:
            with open(configFile) as jsonConfig:
                _configs = json.load(jsonConfig)
        except IOError as e:
            print("Specified file: " + configFile + " cannot be found.")
            print("Layer map configuration aborted.")
            return

        self.isConfigured = True