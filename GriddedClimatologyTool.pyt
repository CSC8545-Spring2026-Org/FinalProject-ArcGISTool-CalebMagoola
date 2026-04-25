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
        
        cell_size = arcpy.Parameter(displayName = "Cell Size",
                        name = "cell_size",
                        datatype = "GPDouble",
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

        smoothing_passes.value = 1

        template_layer = arcpy.Parameter(displayName = "Template Layer (for Extent & Cell Alignment)",
                        name = "template_layer",
                        datatype = "GPRasterLayer",
                        parameterType = "Required",
                        direction = "Input")
        
        output_layer = arcpy.Parameter(displayName = "Output Raster Layer",
                        name = "output_raster_layer",
                        datatype = "DERasterDataset"
                        parameterType = "Required",
                        direction = "Output")

        params = [input_layer, cell_size, smoothing, smoothing_passes, template_layer, output_layer]
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
        config = self._build_config(parameters)

        fishnet = self.create_fishnet(config)
        joined = self.spatial_join(config, fishnet)
        raster = self.to_raster(config, joined)
        
        climatology = raster
        if config["smoothing_type"] != "None" and config["smoothing_passes"] > 0:
            climatology = self.smooth(config, raster)

        climatology.save(config["output"])

        return climatology

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return

"""
Execute Step Helper Methods Below
"""
    def _build_config(self, parameters):
        return {
            "input_layer": parameters[0].valueAsText,
            "cell_size": float(parameters[1].value),
            "smoothing_type": parameters[2].valueAsText,
            "smoothing_passes": int(parameters[3].value) if parameters[3].value else 0,
            "template_layer": parameters[4].value,
            "output_layer": parameters[5].valueAsText
        }
    
    def create_fishnet(config):
        cell_size = config["cell_size"]
        template = config["template_layer"]

        return arcpy.management.CreateFishnet(
            out_feature_class="in_memory/fishnet",
            origin_coord="0 0",
            y_axis_coord="0 1",
            cell_width=cell_size,
            cell_height=cell_size,
            number_rows="0",
            number_columns="0",
            corner_coord="#",
            labels="NO_LABELS",
            template=template,
            geometry_type="POLYGON"
        )
    
    def spatial_join(config):
        input_layer = config["input_layer"]

        return arcpy.analysis.SpatialJoin(
            target_features = "in_memory/fishnet",
            join_features = input_layer,
            out_feature_class = "in_memory/joined",
            match_option = "INTERSECT"
        )

    def convert_to_raster():

    def smooth_climatology(gridded_raster, smooth_type):
        if smooth_type != "None" and smooth_passes > 0:
            for i in range(smooth_passes):
                climatology = smooth_climatology(climatology, smooth_type)

        arcpy.CheckOutExtension("Spatial")
        filter_out = Filter(gridded_raster, smooth_type, "DATA")
        smooth_raster = filter_out.save()
        arcpy.CheckInExtension("Spatial")
        return smooth_raster