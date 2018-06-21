# -*- coding: utf-8 -*-
import os
import json

class LayerMap(object):

    def __init__(self, configFile = None):
        # isConfigured when initing is false
        self.isConfigured = False
        self.layerMap = None
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
                self.layerMap = json.load(jsonConfig)
        except IOError as e:
            print("Specified file: " + configFile + " cannot be found.")
            print("Layer map configuration aborted.")
            return

        self.isConfigured = True

    '''
    getMap:
    I : N/A
    O : self.layerMap
    Wrapper function to get data. Writing layerMap.layerMap is kind of ugly though.
    '''
    def getMap(self):
        return self.layerMap