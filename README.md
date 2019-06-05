# Introduction

This repository contains the set of Python scripts that were developed to create a custom [ArcGIS geoprocessing tool](https://desktop.arcgis.com/en/arcmap/10.5/analyze/main/geoprocessing-tools.htm) to assit the Cumberland County (Pennsylvania) Department of Public Safety with their [SARA Tier II](https://www.epa.gov/epcra/state-tier-ii-reporting-requirements-and-procedures) reporting.

The goal of this repository to is to provide a starting point for other government agencies that perform SARA Tier II reports.  As your organization may use different datasets in your analysis, the tool would need to be updated to reflect those changes.  

While this tool was created for a specific purpose, the scripts could be refactored to perform a proximity analysis for a location that is defined by latitude/longitude.

# Analysis Summary

1. Create a projected point feature from the user provided latitude/longitude coordinates.<br>
2. Create a multi-ring buffer feature class around the point feature.  The user provides the buffer distance(s) and units.<br>
3. Perform an analysis to see if any building polygon features that intersect the point feature intersect a FEMA floodplain.<br>
4. For each ring in the multi-ring buffer feature class, clip a U.S. Census Block dataset.  A proportional population and number of households is calculated for each ring in the multi-ring buffer feature class.<br>
5. For each ring in the multi-ring buffer feature class, select any vulnerable facilties that intersect the multi-ring buffer feature.  If any features are selected, they are exported to a Microsoft Excel file.<br>
6. A project map (.mxd) is created from a template file. The point feature and multi-ring buffer feature are added to the map.  The map is saved, and exported to a .pdf file.

# Summary of Tool

This tool consists of eight (8) Python scripts.  `SARAReportTool.py` is the script that the custom tool is built from.  The other seven scripts are modules which are imported into `SARAReportTool.py` or other modules.

#### SARAReportTool.py

This tool collects parameters from the ArcGIS tool's form using the `arcpy.GetParameterAsText()` [method](http://pro.arcgis.com/en/pro-app/arcpy/functions/getparameterastext.htm).  All inputs are required.

1. SARA Name (string) - the name of the SARA facility.<br>
2. SARA Address (sring) - the street address of the SARA facility.<br>
3. PATTS ID (string) - an unique identifier for each SARA facility.<br>
4. Chemical Info (string) - information about the chemical(s) being used for the analysis
5. Latitude (double) - the latitude in decimal degrees of the SARA facility.<br>
6. Longitude (double) - the longitude in decimal degrees of the SARA facility.<br>
7. Distances for Risk Radius (double; multiple values allowed) - the distance(s) for each risk radius buffer.<br>
8. Risk Radius Units (string) - the units for the risk radius buffers<br>
9. Output Directory (folder) - the folder location where the data and files for the analysis are generated.

#### errorLogger.py

A helper module that handles reporting errors to the user.  It lists the error message, line number, and file in which the error occurs.  It is based upon a [custom geoprocessing tool](https://community.esri.com/docs/DOC-6496-download-arcgis-online-feature-service-or-arcgis-server-featuremap-service) developed by Esri's Jake Skinner.  

#### riskRadius.py

I will update this later.

#### floodplainAnalysis.py

A helper module which tests whether a building polygon feature related to the user submitted latitude/longitude coordinates intersect a FEMA floodplain.  It is used within the `riskRadius.py` module.  A Select By Location analysis is performed between the point feature class (generated in `riskRadius.py`) and a building polygon layer.  If the building polygon layer contains the poin feature class, then the selected building polygon layer participates in a select by location analysis against the FEMA floodplain layer.  A message is written to an output text file as to whether the site intersects or does not intersect a floodplain.

#### populationEstimate.py

I will update this later.

#### exportLayersToExcel.py

A helper module which converts a feature class to a Microsof Excel file.  It is used within the `vulnerableFacilities.py` module.  It performs a select by location between the `featureLayer` and `intersectLayer` parameters.  If records from the `featureLayer` are selected, the layer is exported to Excel.  If not features are selected, a warning message is provided to the user.

#### vulnerableFacilities.py

I will update this later.

#### createMap.py

I will update this later.
