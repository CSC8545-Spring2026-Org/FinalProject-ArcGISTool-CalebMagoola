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
        """Define the tool (tool name is the name of the class)."""
        self.label = "Tool"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define the tool parameters."""
        params = [
            #Input Feature Layer
            arcpy.Parameter(displayName = "Input Feature Layer",
                            name = "input_feature_layer",
                            datatype = "GPFeatureLayer",
                            parameterType = "Required",
                            direction = "Input"),
            #Cell Height
            arcpy.Parameter(displayName = "Input Cell Height",
                            name = "input_cell_height",
                            datatype = "GPLong",
                            parameterType = "Required",
                            direction = "Input"),
            #Cell Width
            arcpy.Parameter(displayName = "Input Cell Width",
                            name = "input_cell_width",
                            datatype = "GPLong",
                            parameterType = "Required",
                            direction = "Input"),
            #Smoothing Type
            arcpy.Parameter(displayName = "Input Smoothing Type",
                            name = "input_feature_layer",
                            datatype = "GPString",
                            parameterType = "Optional",
                            direction = "Input"),
            #Passes
            arcpy.Parameter(displayName = "Input Number of Filter Passes",
                            name = "input_feature_layer",
                            datatype = "GPLong",
                            parameterType = "Optional",
                            direction = "Input"),
            #Output Raster
            arcpy.Parameter(displayName = "Output Raster Layer",
                            name = "output_raster_layer",
                            datatype = "GPRasterLayer",
                            parameterType = "Required",
                            direction = "Output")
        ]
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
