# -*- coding: utf-8 -*-

import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [Tool]

class Tool(object):
    def __init__(self):
        #Define the tool (tool name is the name of the class)
        self.label = "Tool"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        input_layer = arcpy.Parameter(displayName = "Input Feature Layer",
                        name = "input_feature_layer",
                        datatype = "GPFeatureLayer",
                        parameterType = "Required",
                        direction = "Input")
        
        cell_height = arcpy.Parameter(displayName = "Cell Height",
                        name = "input_cell_height",
                        datatype = "GPLong",
                        parameterType = "Required",
                        direction = "Input")
        
        cell_width = arcpy.Parameter(displayName = "Cell Width",
                        name = "input_cell_width",
                        datatype = "GPLong",
                        parameterType = "Required",
                        direction = "Input")
        
        smoothing = arcpy.Parameter(displayName = "Smoothing",
                        name = "input_feature_layer",
                        datatype = "GPString",
                        parameterType = "Optional",
                        direction = "Input")

        smoothing.filter.type = "ValueList"
        smoothing.filter.list = ["none", "low", "high"]
        smoothing.value = "none"
        
        smoothing_passes = arcpy.Parameter(displayName = "Filter Passes",
                        name = "input_feature_layer",
                        datatype = "GPLong",
                        parameterType = "Optional",
                        direction = "Input")
        
        output_layer = arcpy.Parameter(displayName = "Output Raster Layer",
                        name = "output_raster_layer",
                        datatype = "GPRasterLayer",
                        parameterType = "Required",
                        direction = "Output")



        params = [input_layer, cell_height, cell_width, smoothing, smoothing_passes, output_layer]
        return params

    def isLicensed(self):
        """Set whether the tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter. This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
