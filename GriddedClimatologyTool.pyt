# -*- coding: utf-8 -*-

import arcpy
from arcpy import env
import arcpy.sa


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
        
        smoothing = arcpy.Parameter(displayName = "Raster Smoothing",
                        name = "smoothing",
                        datatype = "GPString",
                        parameterType = "Optional",
                        direction = "Input")

        smoothing.filter.type = "ValueList"
        smoothing.filter.list = ["None", "Low", "High"]
        smoothing.value = "None"
        
        smoothing_passes = arcpy.Parameter(displayName = "Smoothing Passes",
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
                        datatype = "DERasterDataset",
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

    def updateParameters(self, parameters):
        smoothing = parameters[2]
        smoothing_passes = parameters[3]

        if smoothing.altered:
            if smoothing.value == "None":
                smoothing_passes.enabled = False
                smoothing_passes.value = 0
            else:
                smoothing_passes.enabled = True

        return

    def updateMessages(self, parameters):
        input_layer = parameters[0]
        cell_size = parameters[1]
        smoothing = parameters[2]
        smoothing_passes = parameters[3]
        template_layer = parameters[4]
        output_layer = parameters[5]

        if not input_layer.value:
            input_layer.setErrorMessage("Input Feature Layer is required.")

        if not cell_size.value:
            cell_size.setErrorMessage("Cell Size is required.")
        else:
            try:
                if float(cell_size.value) <= 0:
                    cell_size.setErrorMessage("Cell Size must be greater than 0.")
            except:
                cell_size.setErrorMessage("Cell Size must be numeric.")

        if template_layer.value:
            try:
                _ = template_layer.value.extent
            except AttributeError:
                template_layer.setErrorMessage("Template Layer must be a valid spatial dataset.")

        if smoothing.value == "None":
            smoothing_passes.setWarningMessage("Ignored since smoothing is currently disabled")
        else:
            if smoothing_passes.value is None or smoothing_passes.value < 1:
                smoothing_passes.setErrorMessage("Smoothing Passes must be 1+ when Smoothing is enabled.")

        if not output_layer.value:
            output_layer.setErrorMessage("Output Raster Layer is required.")

        return

    def execute(self, parameters, messages):
        config = self._build_config(parameters)

        fishnet = self.create_fishnet(config)
        joined = self.spatial_join(config, fishnet)
        raster = self.to_raster(config, joined)
        climatology = self.smooth(config, raster)

        climatology.save(config["output"])
        return climatology

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return

    def _build_config(self, parameters):
        return {
            "input_layer": parameters[0].valueAsText,
            "cell_size": float(parameters[1].value),
            "smoothing_type": parameters[2].valueAsText,
            "smoothing_passes": int(parameters[3].value) if parameters[3].value else 0,
            "template_layer": parameters[4].value,
            "output_layer": parameters[5].valueAsText
        }
    
    def create_fishnet(self, config):
        return arcpy.management.CreateFishnet(
            out_feature_class="in_memory/fishnet",
            origin_coord="0 0",
            y_axis_coord="0 1",
            cell_width=config["cell_size"],
            cell_height=config["cell_size"],
            number_rows="0",
            number_columns="0",
            corner_coord="#",
            labels="NO_LABELS",
            template=config["template_layer"],
            geometry_type="POLYGON"
        )
    
    def spatial_join(self, config):
        return arcpy.analysis.SpatialJoin(
            target_features = "in_memory/fishnet",
            join_features = config["input_layer"],
            out_feature_class = "in_memory/joined",
            match_option = "INTERSECT",
            join_operation="JOIN_ONE_TO_ONE"
        )

    def to_raster(self, config, joined_fc):
        return arcpy.conversion.PolygonToRaster(
            in_features=joined_fc,
            value_field="Join_Count",
            out_rasterdataset="in_memory/raster",
            cell_assignment="MAXIMUM_AREA",
            priority_field="NONE",
            cellsize=config["cell_size"]
        )

    def smooth(self, config, raster):
        if config["smoothing_type"] == "None" or config["smoothing_passes"] <= 0:
            return raster

        arcpy.CheckOutExtension("Spatial")
        result = raster

        for _ in range(config["smoothing_passes"]):
            result = arcpy.sa.FocalStatistics(
                in_raster = result,
                neighborhood = arcpy.sa.NbrRectangle(3, 3, "CELL"),
                statistics_type = "MEAN"
            )

        arcpy.CheckInExtension("Spatial")
        return result