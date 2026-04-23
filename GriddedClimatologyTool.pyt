# -*- coding: utf-8 -*-

import arcpy
from arcpy import env
from arcpy.sa import *


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
        
        cell_width = arcpy.Parameter(displayName = "Cell Width",
                        name = "input_cell_width",
                        datatype = "GPLong",
                        parameterType = "Required",
                        direction = "Input")
        
        cell_height = arcpy.Parameter(displayName = "Cell Height",
                        name = "input_cell_height",
                        datatype = "GPLong",
                        parameterType = "Required",
                        direction = "Input")
        
        smoothing = arcpy.Parameter(displayName = "Smoothing",
                        name = "smoothing",
                        datatype = "GPString",
                        parameterType = "Optional",
                        direction = "Input")

        smoothing.filter.type = "ValueList"
        smoothing.filter.list = ["None", "Low", "High"]
        smoothing.value = "None"
        
        smoothing_passes = arcpy.Parameter(displayName = "Filter Passes",
                        name = "smoothing_passes",
                        datatype = "GPLong",
                        parameterType = "Optional",
                        direction = "Input")

        template_layer = arcpy.Parameter(displayName = "Template Layer",
                        name = "template_layer",
                        datatype = "GPRasterLayer",
                        parameterType = "Required",
                        direction = "Output")
        
        output_layer = arcpy.Parameter(displayName = "Output Raster Layer",
                        name = "output_raster_layer",
                        datatype = "GPRasterLayer",
                        parameterType = "Required",
                        direction = "Output")

        params = [input_layer, cell_width, cell_height, smoothing, smoothing_passes, template_layer, output_layer]
        return params

    def isLicensed(self):
        """Set whether the tool is licensed to execute."""
        try:
            if arcpy.CheckExtension("Spatial") == "Available":
                return True

        except:
            return False
        return False

    def updateParameters(self, parameters):
        smoothing = parameters[3]
        smoothing_passes = parameters[4]

        if smoothing.altered:
            if smoothing.value == "None":
                smoothing_passes.enabled = False
            else:
                smoothing_passes.enabled = True
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter. This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        #TO-DO: Take inputs and create Fishnet
        cell_width = parameters[1].valueAsText
        cell_height = parameters[2].valueAsText
        template_layer = parameters[5].valueAsText
        output_location = parameters[6].valueAsText

        arcpy.management.CreateFishnet(
            out_feature_class = "memory\\fishnet",
            origin_coord = "0 1",
            y_axis_coord = "0 1",
            cell_width = cell_width,
            cell_height = cell_height,
            number_rows = "0",
            number_columns = "0",
            corner_coord = "#",
            labels = "NO_LABELS",
            template = template_layer, #overrides origin_coord, y_axis_coord, and auto calculates number_rows, number_columns
            geometry_type = "POLYGON"
        )

        #TO-DO: Create Spatial Join with Fishnet Output and Spatial Input
        arcpy.analysis.SpatialJoin(
            target_features = "memory\\fishnet",
            join_features = template_layer,
            out_feature_class = "memory\\joined",
            match_option = "INTERSECT"
        )

        #TO-DO: Smooth Pass Loop
        # smoothing = parameters[3]
        # smoothing_passes = parameters[4]

        # smooth_raster = None

        # if smoothing.value != "None":
        #     if smoothing.value == "Low":
        #         for i in range(len(smoothing_passes.value)):
        #             arcpy.CheckOutExtension("Spatial")

        #             filter_out = Filter(smooth_raster, "LOW", "DATA")
        #             smooth_raster = filter_out.save()

        #             arcpy.CheckInExtension("Spatial")
        #     else:
        #         for i in range(len(smoothing_passes.value)):
        #             arcpy.CheckOutExtension("Spatial")

        #             filter_out = Filter(smooth_raster, "HIGH", "DATA")
        #             smooth_raster = filter_out.save()

        #             arcpy.CheckInExtension("Spatial")
        #     result = smooth_raster
        # else:
        #     result = None

        #Return Final Product
        result = None
        return result

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
