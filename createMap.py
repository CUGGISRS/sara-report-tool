#-------------------------------------------------------------------------------
# Name:        Create SARA Facility Map and PNG Export
#
# Summary:     Creates a project MXD file from a template file.  Adds the SARA
#              facility and risk radii layers to project map.  Saves the map
#              and exports as PNG file.
#
# Author:      Patrick McKinney
#
# Created:     4/25/19
#
# Updated:     5/30/19
#-------------------------------------------------------------------------------

# Import modules
import arcpy, os, errorLogger, datetime

def saveLayerFile(layer,name,out_dir):
        # create a feature layer
        arcpy.MakeFeatureLayer_management(layer,name)
        # directory and name of layer file
        out_layer_file = r'{}\{}.lyr'.format(out_dir, name)
        # save as a layer file
        arcpy.SaveToLayerFile_management(name,out_layer_file,"RELATIVE")
        # get access to layer file
        return out_layer_file

def createSaraMap(sara_site, risk_radii, sara_name, sara_address, patts, chem_info, output_dir):
    try:
        # create a layer file to disk for SARA Facility
        sara_lyr = saveLayerFile(sara_site,'SARA Site',output_dir)
        # create a layer file to disk for Risk Radii
        risk_radii_lyr = saveLayerFile(risk_radii,'Risk Radii',output_dir)

        # create map document object from template map
        mxd_template = arcpy.mapping.MapDocument(r'C:\GIS\Scripts\SARA\Templates\SARA Radius Map Template.mxd')
        # create a copy of the template map document
        project_mxd_file = os.path.join(output_dir, 'SARA_Project_Map.mxd')
        # save a copy of template map
        mxd_template.saveACopy(project_mxd_file)
        # add message
        arcpy.AddMessage('\nCreated a project map document')
        # create a map document object for project map
        project_mxd = arcpy.mapping.MapDocument(project_mxd_file)
        # create data frame object (so you can add a layer to a map)
        data_frame = arcpy.mapping.ListDataFrames(project_mxd)[0]
        # gain access to legend element
        map_legend = arcpy.mapping.ListLayoutElements(project_mxd, "LEGEND_ELEMENT", "Legend")[0]
        # if a layer is added to map, add it to map legend
        map_legend.autoAdd = True

        # add SARA Facility to map document
        # sara layer file on disk - this represents a layer file, not the layer as it is added to the map document
        sara_temp = arcpy.mapping.Layer(sara_lyr)
        # add layer to map document
        arcpy.mapping.AddLayer(data_frame,sara_temp,'TOP')
        # create object reference streams layer within map document
        sara_of_interest = arcpy.mapping.ListLayers(project_mxd,'*SARA*',data_frame)[0]
        # add symbology layer
        sara_symbol_file = arcpy.mapping.Layer(r'C:\GIS\Scripts\SARA\Templates\SARA of Interest.lyr')
        # update symbology
        arcpy.mapping.UpdateLayer(data_frame,sara_of_interest,sara_symbol_file,True)

        # add risk radii to map
        # risk radii layer file on disk - this represents a layer file, not the layer as it is added to the map document
        risk_radii_temp = arcpy.mapping.Layer(risk_radii_lyr)
        # add layer to map document
        arcpy.mapping.AddLayer(data_frame,risk_radii_temp,'TOP')
        # create object reference streams layer within map document
        risk_radii_of_interest = arcpy.mapping.ListLayers(project_mxd,'*Risk*',data_frame)[0]
        # add symbology layer
        risk_radii_symbol_file = arcpy.mapping.Layer(r'C:\GIS\Scripts\SARA\Templates\Risk Radii.lyr')
        # update symbology
        arcpy.mapping.UpdateLayer(data_frame,risk_radii_of_interest,risk_radii_symbol_file,True)

        # set map extent
        data_frame.extent = risk_radii_of_interest.getExtent(True)
        # set scale a little larger to add padding
        data_frame.scale = data_frame.scale * 1.1

        # update SARA Name for map
        sara_name_text = arcpy.mapping.ListLayoutElements(project_mxd,'TEXT_ELEMENT','SARA_Title_Text')[0]
        sara_name_text.text = str(sara_name)

        # update SARA Address for map
        sara_address_text = arcpy.mapping.ListLayoutElements(project_mxd,'TEXT_ELEMENT','SARA_Address_Text')[0]
        sara_address_text.text = str(sara_address)

        # update SARA PATTS for map
        sara_patts_text = arcpy.mapping.ListLayoutElements(project_mxd,'TEXT_ELEMENT','SARA_PATTS_Text')[0]
        sara_patts_text.text = sara_patts_text.text.replace('x', str(patts))

        # update chemical information
        sara_chem_text = arcpy.mapping.ListLayoutElements(project_mxd,'TEXT_ELEMENT','SARA_Chem_Text')[0]
        sara_chem_text.text = str('Chemical: {}'.format(chem_info))

        # update risk radii information
        # container for risk radii information
        risk_radii_info = ''
        # fields for cursor
        risk_radii_fields = ['BUFFDIST','UNITS']
        # perform search cursor on risk radii layer to get risk radii information
        with arcpy.da.SearchCursor(risk_radii,risk_radii_fields) as cursor:
            for row in cursor:
                risk_radii_info += '{}-{}; '.format(row[0],row[1])
            # end for in
        # end cursor
        # get map layout element
        risk_radii_text = arcpy.mapping.ListLayoutElements(project_mxd,'TEXT_ELEMENT','SARA_Radii_Text')[0]
        risk_radii_text.text = str('Risk Radii Distances: {}'.format(risk_radii_info))

        # update date text element with current date
        # get current date
        date_today = datetime.date.today()
        # reformat date
        date_formatted = date_today.strftime("%m-%d-%Y")
        # create object reference to date text element
        date_text = arcpy.mapping.ListLayoutElements(project_mxd,'TEXT_ELEMENT','Date_Text')[0]
        # update text
        date_text.text = str(date_formatted)

        # save map
        project_mxd.save()
        # add message
        arcpy.AddMessage('\nSaved the project map document')

        # export map to pdf using current date in file name
        # file name
        pdf_name = r'{} Risk Radius Map {}.pdf'.format(sara_name,date_formatted)
        # export map to pdf using default settings
        arcpy.mapping.ExportToPDF(project_mxd,os.path.join(output_dir,pdf_name),'PAGE_LAYOUT', resolution=300)
        # add message
        arcpy.AddMessage('\nExported project map to .pdf format.  File is named {}'.format(pdf_name))
    # If an error occurs running geoprocessing tool(s) capture error and write message
    # handle error outside of Python system
    except EnvironmentError as e:
            arcpy.AddError('\nAn error occured running this tool. Please provide the GIS Department the following error messages:')
            # call error logger method
            errorLogger.PrintException(e)
        # handle exception error
    except Exception as e:
            arcpy.AddError('\nAn error occured running this tool. Please provide the GIS Department the following error messages:')
            # call error logger method
            errorLogger.PrintException(e)
    finally:
        try:
            # delete variables to release locks on map documents (.mxd) and layer files (.lyr)
            del mxd_template, project_mxd, sara_lyr, sara_temp, sara_symbol_file, risk_radii_lyr, risk_radii_temp, risk_radii_symbol_file
            arcpy.AddMessage('\nReleased locks on map documents and layer files')
            arcpy.AddMessage('\nCompleted running tool')
        except:
            arcpy.AddWarning('\nLocks may still exist on map documents and layer files')
            arcpy.AddMessage('\nCompleted running tool')