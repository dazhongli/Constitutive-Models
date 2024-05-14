# Import Python libraries
import csv
import logging
import math
import os
import re
import socket
import subprocess
import time
import yaml
import numpy as np
import pandas as pd
import collections
# import xlwing as xw
try:
    import geopandas as gpd
    from shapely.geometry import Point, LineString, Polygon
except ImportError:
    print('geopandas not installed!')
from pathlib import Path

__version__ = 1.0


class BaseProject:
    '''
    Class that provides a way to quickly set_up a project for base cases
    '''

    def __init__(self, host='localhost', openplaxis=False, plaxis_visible=True,
                 loggername=__name__, password='', plaxis_path=''):
        from plxscripting.easy import new_server
        self._localhost = host
        self._new_server = new_server
        self.logger = self.logger(loggername)
        self.password = password
        if openplaxis:
            self.logger.info('Launching Plaxis, it may take a minute...')
            try:
                args = [os.path.join(plaxis_path, "Plaxis2DXInput.exe"),
                        "--AppserverPort={}".format(10000)]
                self._input_process = subprocess.Popen(args)
                self._s_i, self._g_i = self._new_server(host, 10000,password=password, timeout=0)
                self._s_o, self._g_o = self._new_server(host, 10001,password=password,timeout=0)
            except Exception as e:
                print(e)
        else:
            self._s_i, self._g_i = self._new_server(host, 10000,password=password,timeout=0)
            self._s_o, self._g_o = self._new_server(host, 10001,password=password,timeout=0)
            self.logger.info('Plaxis connection established...')
        self._model_geometry = {}
        self._model_phases = pd.DataFrame(dict(name=[], ID=[], plxobj=[]))
        self.plx_file_path = ''
        # Define a namedtuple for solvertype
        SolverType = collections.namedtuple('SolverType','Picos, Pardiso, Classic')
        self.solver_type = SolverType(Picos  = 'Picos (multicore iterative)',
                                      Pardiso = 'Pardiso (multicore direct)',
                                      Classic = 'Classic (single core iterative)' )
        #test

#================================================================================================================================================================
#   PROJECT FILE FUNCTIONS
#================================================================================================================================================================

    def new_2Dproject(self, xmin_ip, xmax_ip, ymax_ip, ymin_ip,
                      project_title,usr_comment,model_type='Plane strain'):
        '''
        Creates a new 2D Plaxis Project with the extent defined.
        Param:
            xmin_ip:       leftmost boundary
            xmax_ip:       rightmost boundary
            ymax_ip:       top boundary
            ymin_ip:       bottom boundary
            project_title: project title
            usr_comment:   user comments
        Return:
            None
         '''
        self._s_i.new()
        self._g_i.Project.setproperties('Title', project_title, 'Comments', usr_comment, 
                                        'UnitForce', "kN", 'UnitLength', "m", 'UnitTime', "day", 
                                        'ModelType', model_type,
                                        'ElementType', "15-Noded")
        self._g_i.SoilContour.initializerectangular(
            xmin_ip, ymin_ip, xmax_ip, ymax_ip)

    def restore(self, dirname, filename, suffix):
        '''
        Opens a Plaxis file.
        Param:
            dirname:  directory where file is stored, e.g r'C:\PlaxisFiles'
            filename: name of plaxis file in text quotations, e.g. "Testing123"
            suffix:   suffix of plaxis file, i.e. ".p3D" or ".p2dx", and the dot should be included
        Return:
            None
        '''
        basename   = str(filename)
        pathformat = Path(dirname, basename).with_suffix(suffix)
        fileloc    = str(pathformat)
        self._s_i.open(fileloc)
        self.logger.info("Plaxis file opened: " + fileloc)
        return

    def savecopy(self, dirname, filename, suffix):
        '''
        Saves the file into specified directory
        Param:
            dirname:  directory where file is stored, e.g r'C:\PlaxisFiles'
            filename: name of plaxis file in text quotations, e.g. "Testing123"
            suffix:   suffix of plaxis file, i.e. ".p3D" or ".p2dx", and the dot should be included
        Return:
            None
        '''
        basename   = str(filename)
        pathformat = Path(dirname, basename).with_suffix(suffix)
        fileloc    = str(pathformat)
        self._g_i.save(fileloc)
        self.logger.info("Plaxis file saved in " + fileloc)
        return

    def _get_usr_info(self):
        '''
        FOR PASSWORD PROTECTED CONNECTION TO PLAXIS - TO BE DEVELOPED
        Param:
            None
        Return:
            None
        '''
        import getpass
        file_path = os.path.dirname(__file__)
        user_name = getpass.getuser()
        users = yaml.load(open(os.path.join(file_path, 'user_info.yml')))
        for user in users:
            if user['name'] == user_name:
                return user

    def read_user_profile(self, filename='user_info.yml'):
        '''
        FOR PASSWORD PROTECTED CONNECTION TO PLAXIS - TO BE DEVELOPED
        Param:
            None
        Return:
            None
        '''
        machine_ID = socket.gethostname()
        import getpass
        this_user = getpass.getuser()
        file_path = os.path.dirname(__file__)
        filename = os.path.join(file_path, filename)
        with open(filename, 'r') as fin:
            user_info = fin.read()
        users = yaml.load(user_info)
        return users[this_user][machine_ID]

    def logger(self, filename, level=logging.DEBUG, stream=True):
        '''
        Logs the Plaxis command that are executed.
        Param:
            None
        Return:
            None
        '''
        logger = logging.getLogger(__name__)
        logFormatter = logging.Formatter(
            "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
        fileHandler = logging.FileHandler(filename + '-debug.log', mode='w')
        fileHandler.setFormatter(logFormatter)
        logger.addHandler(fileHandler)
        if stream is True:
            consoleHandler = logging.StreamHandler()
            consoleHandler.setFormatter(logFormatter)
            logger.addHandler(consoleHandler)
        logger.setLevel(logging.DEBUG)
        return logger

    def save_temp_files():
        pass

    def load_temp_files():
        pass

#================================================================================================================================================================
#   'SOIL' TAB FUNCTIONS
#================================================================================================================================================================

#   Soil Materials Related

    def mat_read_para(self, filename, soilmat_sheet = 'PP_MC_SFormat'):
        '''
        Reads soil material information from different formats.
        Creates soil materials in Plaxis based on the read properties. 
        Note: Definition of Stiffness of Mohr-Coulomb Material is by Shear Modulus (G).
              Converted to Young's Modulus (E) via Poisson's Ratio (v)
        Param:
            filename:      full file name of material data, including path
            soilmat_sheet: name of standard input worksheet for different material models
                           i.e. PP_MC_SFormat  = Mohr-Coloumb
                                PP_HS_SFormat  = Hardening Soil
                                PP_MCC_SFormat = Modified Cam Clay
                                PP_SS_SFormat  = Soft Soft
                                PP_SSC_SFormat = Soft Soft Creep
        Return:
            dfgv_Soil_Para: viewable dataframe of soil materials
        '''
        if filename.endswith('.xlsm'):
            self.dfgv_Soil_Para = self._mat_read_para_excel(filename, soilmat_sheet)
        self._mat_input_para()
        return self.dfgv_Soil_Para

    def _mat_read_para_excel(self, filename, soilmat_sheet):
        '''
        An interface reading standard excel file of soil material properties.
        Param:
            filename:      full file name of material data, including path
            soilmat_sheet: name of standard input worksheet for different material models
                           i.e. PP_MC_SFormat  = Mohr-Coloumb
                                PP_HS_SFormat  = Hardening Soil
                                PP_MCC_SFormat = Modified Cam Clay
                                PP_SS_SFormat  = Soft Soft
                                PP_SSC_SFormat = Soft Soft Creep
        Return:
            self._dfg_Soil_Para: a dataframe of soil materials
        '''
        # User to specify soilmat_sheet depending on material model, 
        df_Soil_Para = pd.read_excel(filename, sheet_name=soilmat_sheet)
        # Drops the last row of data if it's incomplete "NaN" entry.
        df_Soil_Para.dropna(inplace=True)
        # Sets column named 'Soil' as the index of rows
        df_Soil_Para.set_index('Soil', inplace=True)
        # Cast specified properties as integer
        df_Soil_Para = df_Soil_Para.astype({"MaterialNumber":  int,
                                            "SoilModel": int,
                                            "DrainageType": int,
                                            "Colour": int,
                                            "InterfaceStrength": int,
                                            "CrossPermeability": int})
        if (soilmat_sheet is "PP_SS_SFormat") or (soilmat_sheet is "PP_SSC_SFormat"):
            # Additions for Soft Soil and Soft Soil Creep Models
            df_Soil_Para.UseAlternatives   = df_Soil_Para.UseAlternatives.astype('bool')
        self._dfg_Soil_Para = df_Soil_Para
        # print(self._dfg_Soil_Para)
        self.logger.info("Nos. of Soil Materials Read = " +
                         str(len(self._dfg_Soil_Para)))
        return self._dfg_Soil_Para

    def _mat_input_para(self):
        '''
        Inputs soil materials in dataframe into Plaxis.
        Note: This function should be called after '_dfg_Soil_Para' has been initialised.
        Param:
            None
        Return:
            self._plx_mat: a dictionary of soil materials for inputting pairs of attributes and values into Plaxis
        '''
        if not hasattr(self, '_dfg_Soil_Para'):
            self.logger.error("Material data not read in. _dfg_Soil_Para dataframe not available.")
            return None
        material = {}
        for ix, row in self._dfg_Soil_Para.iterrows():
            # Creates a new empty list and stores as 'temp'
            temp = []
            # Iterates over two lists in parallel
            for key, value in zip(row.index, row.values):
                # Appends pair of key and value into the 'temp' list
                temp.append(key)
                temp.append(value)
            # Creates a new soil material set
            new_material = self._g_i.soilmat()
            new_material.setproperties(*temp)
            material[row['MaterialName']] = new_material
            self._plx_mat = material                     # Keeps a record of material
            # print(self._plx_mat)
        self.logger.info(
            "Nos. of Soil Materials Imported into Plaxis = " + str(len(self._plx_mat)))
        return self._plx_mat

    def copy_from_a_material(self, material_source='',
                             material_name_target='default'):
        '''
        Creates a new soil material from a copy of an old one.
        Param:
            material_source:      string, the idendification of the old material
            material_name_target: string, the identification of the new material
        Param:
            None
        Return:
            The plxobject of the new material
        '''
        if material_source == '':  # if source not specified, create new a soil material.
            mat_target = self.g_i.soilmat()
        else:
            mat_source = getattr(self.g_i, material_source)
            property_list = []
            for attr in dir(mat_source):
                try:
                    if isinstance(getattr(mat_source, attr).value, int) or \
                       isinstance(getattr(mat_source, attr).value, float):
                        property_list.append(attr)
                        property_list.append(getattr(mat_source, attr).value)
                except:  # this should be avoided, will be fixed later
                    pass  # we do nothing here, as the exceptions will be some plxmethods
            mat_target = self.g_i.soilmat(*property_list)
        mat_target.MaterialName = material_name_target
        mat_target.Name = material_name_target
        return mat_target

    def mat_extract_para(self):
        '''
        Extracts existing soil material information in Plaxis to a dictionary.
        Param:
            None
        Return:
            A dictionary of soil materials in an existing Plaxis model
        '''
        self._plx_mat = {}
        self._plx_mat = self._extract_mat_property('SoilMat')
        return self._plx_mat

    def mat_extract_excel(self, filename='Arup_PP_Soil_Para_Input_rev00.xlsm',
                                sheetname='MC_Extracted'):
        '''
        Extracts existing Plaxis soil materials into excel via dataframe and dictionary.
        Param:
            None
        Return:
            None
        '''
        wb = xw.Book(filename)
        wb.sheets[sheetname].activate()
        # Define column headers and set-up dataframe
        columns = ['MaterialNumber', 'MaterialName', 'SoilModel', 'DrainageType',
                   'gammaUnsat', 'gammaSat', 'cref', 'phi', 'cinc', 'nu', 'Eref',
                   'Einc', 'verticalref', 'perm_primary_horizontal_axis', 'perm_vertical_axis',
                   'InterfaceStrength', 'Rinter', 'CrossPermeability', 'HydraulicResistance',
                   'DrainageConductivity', 'K0Determination', 'K0Primary', 'K0Secondary']
        df_soil_param = pd.DataFrame(columns=columns)
        soils = self.mat_extract_para()
        # Extract soil property here
        for soil_name in soils:
            soil = soils[soil_name]
            for prop in columns:
                df_soil_param.loc[soil_name, prop] = getattr(soil, prop).value
        drainage_type = {0: 'Drained',
                         1: 'Undrained (A)',
                         2: 'Undrained (B)',
                         3: 'Undrained (C)',
                         4: 'Non-porous'}
        material_type = {1: 'Linear Elastic',
                         2: 'Mohr-Coulomb'}
        start_row = 13
        xw.Range('A13:AB100').clear_contents()
        for iMat in range(len(soils)):
            xw.Range(
                (start_row+iMat, 1)).value = df_soil_param.loc[iMat, "MaterialNumber"].value
            xw.Range(
                (start_row+iMat, 2)).value = df_soil_param.loc[iMat, "MaterialName"].value

            if df_soil_param.loc[iMat, "SoilModel"].value is 1:
                temp = "Linear Elastic"
            elif df_soil_param.loc[iMat, "SoilModel"].value is 2:
                temp = "Mohr-Coulomb"
            xw.Range((start_row+iMat, 3)).value = temp

            if df_soil_param.loc[iMat, "DrainageType"].value is 0:
                temp = "Drained"
            elif df_soil_param.loc[iMat, "DrainageType"].value is 1:
                temp = "Undrained (A)"
            elif df_soil_param.loc[iMat, "DrainageType"].value is 2:
                temp = "Undrained (B)"
            elif df_soil_param.loc[iMat, "DrainageType"].value is 3:
                temp = "Undrained (C)"
            elif df_soil_param.loc[iMat, "DrainageType"].value is 4:
                temp = "Non-porous"
            xw.Range((start_row+iMat, 4)).value = temp

            xw.Range(
                (start_row+iMat, 5)).value = df_soil_param.loc[iMat, "gammaUnsat"]
            xw.Range(
                (start_row+iMat, 6)).value = df_soil_param.loc[iMat, "gammaSat"]

            if df_soil_param.loc[iMat, "DrainageType"].value is 0:
                xw.Range(
                    (start_row+iMat, 7)).value = df_soil_param.loc[iMat, "cref"]
                xw.Range((start_row+iMat, 8)
                         ).value = df_soil_param.loc[iMat, "phi"]
            elif df_soil_param.loc[iMat, "DrainageType"].value is 1:
                xw.Range(
                    (start_row+iMat, 9)).value = df_soil_param.loc[iMat, "cref"]
                xw.Range((start_row+iMat, 10)
                         ).value = df_soil_param.loc[iMat, "cinc"]
            elif df_soil_param.loc[iMat, "DrainageType"].value is 2:
                xw.Range(
                    (start_row+iMat, 9)).value = df_soil_param.loc[iMat, "cref"]
                xw.Range((start_row+iMat, 10)
                         ).value = df_soil_param.loc[iMat, "cinc"]
            elif df_soil_param.loc[iMat, "DrainageType"].value is 3:
                xw.Range(
                    (start_row+iMat, 9)).value = df_soil_param.loc[iMat, "cref"]
                xw.Range((start_row+iMat, 10)
                         ).value = df_soil_param.loc[iMat, "cinc"]
            elif df_soil_param.loc[iMat, "DrainageType"].value is 4:
                xw.Range(
                    (start_row+iMat, 7)).value = df_soil_param.loc[iMat, "cref"]
                xw.Range((start_row+iMat, 8)
                         ).value = df_soil_param.loc[iMat, "phi"]

            xw.Range((start_row+iMat, 11)
                     ).value = df_soil_param.loc[iMat, "nu"]
            xw.Range((start_row+iMat, 13)
                     ).value = df_soil_param.loc[iMat, "Eref"]
            xw.Range((start_row+iMat, 14)
                     ).value = df_soil_param.loc[iMat, "Einc"]
            xw.Range((start_row+iMat, 15)
                     ).value = df_soil_param.loc[iMat, "verticalref"]
            xw.Range(
                (start_row+iMat, 16)).value = df_soil_param.loc[iMat, "perm_primary_horizontal_axis"]
            xw.Range((start_row+iMat, 17)
                     ).value = df_soil_param.loc[iMat, "perm_vertical_axis"]

            if df_soil_param.loc[iMat, "InterfaceStrength"].value is 0:
                temp = "Rigid"
            elif df_soil_param.loc[iMat, "InterfaceStrength"].value is 1:
                temp = "Manual"
            xw.Range((start_row+iMat, 18)).value = temp

            xw.Range((start_row+iMat, 19)
                     ).value = df_soil_param.loc[iMat, "Rinter"]
            
            if df_soil_param.loc[iMat, "CrossPermeability"].value is 0:
                temp = "Impermeable"
            elif df_soil_param.loc[iMat, "CrossPermeability"].value is 1:
                temp = "Semi-impermeable"
            elif df_soil_param.loc[iMat, "CrossPermeability"].value is 2:
                temp = "Fully permeable"
            xw.Range((start_row+iMat, 20)).value = temp

            xw.Range((start_row+iMat, 21)
                     ).value = df_soil_param.loc[iMat, "HydraulicResistance"]
            xw.Range(
                (start_row+iMat, 22)).value = df_soil_param.loc[iMat, "DrainageConductivity"]

            if df_soil_param.loc[iMat, "K0Determination"].value is 0:
                temp = "Manual"
            elif df_soil_param.loc[iMat, "K0Determination"].value is 1:
                temp = "Automatic"
            xw.Range((start_row+iMat, 23)).value = temp

            xw.Range((start_row+iMat, 24)
                     ).value = df_soil_param.loc[iMat, "K0Primary"]
            xw.Range((start_row+iMat, 25)
                     ).value = df_soil_param.loc[iMat, "K0Secondary"]
        return

    def get_soil_slice_results(self, phase, type_of_result, points):
        '''
        Returns plaxis results at a list of points defined in Points
        Param: 
            Points: 2D array containing coordinates of the points to be extracted
            Phase: str of the phase name
            type_of_results: type of results of interested, e.g., X, Y, etc, refer to Plaxis command for details
        '''
        g_o = self._g_o
        phase = getattr(g_o, phase)
        results = []
        for point in points:
            result = float(g_o.getsingleresult(phase, getattr(
                g_o.ResultTypes.Soil, type_of_result), point[0], point[1]))
            results.append(result)
        return np.array(results)

#   Borehole Related

    def _borehole_slay(self, BH_name, BH_slay_num, BH_slay_btm, BH_layer, BH_slay_mat):
        '''
        Creates new soil layers in a new borehole
        Param:
            BH_name:        borehole name
            BH_xcoord:      x-coordinate of borehole
            BH_sum_slay:    total number of soil layers in all boreholes (this should be the same for all boreholes)
            BH_head:        groundwater level (i.e. head level)
            BH_slay_num_00: soil layer ID, starting at 0
            BH_slay_btm_00: bottom elevation of the above soil layer ID
            BH_layer:       layer being assigned to
            BH_slay_mat:    soil layer material
        Return:
            None
        '''
        # Sets the bottom level of a soil layer of specified borehole
        self._g_i.setsoillayerlevel(BH_name, BH_slay_num, BH_slay_btm)
        # Assigns soil material to a specified layer, other than the top (0) layer
        if BH_slay_num is not 0:
            self._g_i.set(BH_layer.Soil.Material, BH_slay_mat)

    def _bh_data_input(self):
        '''
        Runs '_borehole_slay' function mutliple times to create all BHs in standard excel file.
        Added soil layer is added to all boreholes. 
        Its thickness should be specified as zero if it does not exist at a specific borehole location.
        Param:
            None
        Return:
            None
        '''
        self._g_i.gotosoil()
        # Re-reads dictionary of soil materials from Plaxis
        self.mat_extract_para()
        # Loops over iterable with automatic counter assigned
        for ix, col_name in enumerate(self._dfg_BH_Data):
            if 'MaterialName' in col_name:           # To escape the last column, where material ID is saved
                continue
            # Gets pandas series using column name
            BH_i = self._dfg_BH_Data[col_name]
            # Gets the indices with "BH_slay" in it
            layer_index = [ix for ix in BH_i.index if 'BH_slay' in ix]
            # Makes sure index is an even number
            assert(len(layer_index) % 2 == 0)
            # It will pop up an error messeage if number is odd
            # Calculates the total number of soil layers
            nsoillayer = int(len(layer_index)/2)
            # Variable for x-coordinate of BH
            plx_soillayers = []
            x_coord = BH_i['BH_xcoord']
            if 'BH_ycoord' in BH_i.index:                         # check if it's 3D case
                y_coord = BH_i['BH_ycoord']
                plx_BH = self._g_i.borehole(
                                            x_coord, y_coord)     # Adds a new 3D borehole
            else:
                plx_BH = self._g_i.borehole(x_coord)              # Adds a new 2D borehole
            # Variable for groundwater level at BH
            BH_head = BH_i['BH_head']
            # Allocates a list for holding soil layer information
            # Sets the water level inside the borehole
            self._g_i.Boreholes[-1].Head.set(BH_head)
            # Renames new borehole with column name
            plx_BH.rename(col_name)
            # Adds the total number of soil layers
            if ix == 0:
                for i in np.arange(nsoillayer):
                    plx_soillayers.append(self._g_i.soillayer(0))
            # Generates a dictionary of soil layers generated in Plaxis
            plx_soillayer = {}
            for x in self._g_i.Soillayers[:]:
                plx_soillayer[str(x.Name)] = x
            # Slices the dataFrame to get the soil layering info only
            soil_layer = BH_i[layer_index]
            # print(soil_layer)
            # Loops over the soil layers, special handling for the top layer
            for i in np.arange(nsoillayer):          
                if i == 0:                             
                    self._borehole_slay(plx_BH, int(
                        soil_layer[0]), soil_layer[1], 0, 0)
                else:
                    mat_index = soil_layer.index[2*i]
                    Mat_Name = self._dfg_BH_Data.loc[mat_index, 'MaterialName']
                    self._borehole_slay(plx_BH, int(soil_layer[2*i]), soil_layer[2*i+1],
                                       plx_soillayer['Soillayer_'+str(i)],
                                       self._plx_mat[Mat_Name])
        self._plx_soillayer = plx_soillayer
        # print(self._plx_soillayer)
        self.logger.info(
            str(ix) + " Nos. of Soil Materials Imported into Plaxis")
        return

    def bh_extract_data(self):
        '''
        Extracts the Plaxis borehole information and saves to a local copy in 'self._plx_BHdata'
        Param:
            None
        Return:
            A dictionary containing the BH information in an existing Plaxis model.
        '''
        self._plx_BHdata = {}
        self._g_i.gotosoil()
        for BH in self._g_i.Boreholes:
            name = BH.Name.value
            self._plx_BHdata[name] = BH
        self.logger.info(
            "Nos. of Boreholes Extracted into Dictionary = " + str(len(self._plx_BHdata)))
        return self._plx_BHdata

    def bh_read_data(self, filename):
        '''
        Reads borehole information from different formats.
        Creates boreholes in Plaxis based on the read properties.
        Param:
            filename: full file name of material data, including path
        Return:
            None    
        '''
        if filename.endswith('.xlsm'):
            self._bh_read_data_excel(filename)
        else:
            self.logger.error('Filetype not implemented!!!')
        self._bh_data_input()

    def delete_all_bh(self):
        '''
        Deletes all boreholes (if any) in the model
        Param:
            None
        Return:
            None            
        '''
        if len(self.g_i.Boreholes) == 0:  # if no borehole in Plaxis, just return Ture
            self.logger.info("No BH information in Plaxis Model")
            return
        self._g_i.gotosoil()
        for x in self._g_i.Boreholes[:]:
            self._g_i.delete(x)
        self.logger.debug("{} BHs has been deleted".format(
            len(self.g_i.Boreholes)))

#================================================================================================================================================================
#   'STRUCTURES' TAB FUNCTIONS
#================================================================================================================================================================

#   Plate Material Related 

    def plate_read_prop(self, filename):
        '''
        Reads plate material information from different formats.
        Creates plate materials in Plaxis based on the read properties.
        Note: The ratios of E, EA, EA2, EI, nu, d and Gref need to be exact in terms of bd^3/12 and G = E/(2*(1+nu)) etc. 
              otherwise the imported Plaxis values maybe incorrect. Although it may be possible to change
              specific parameters by "setproperties" function.
        Param:
            filename: full file name of material data, including path
        Return:
            dfgv_Plate_Prop: viewable dataframe of plate materials
        '''
        if filename.endswith('.xlsm') or filename.endswith('.xlsx'):
            self.dfgv_Plate_Prop = self._plate_read_prop_excel(filename)
        else:
            self.logger.error('Filetype not implemented yet!')
        self._plate_input_prop()
        return self.dfgv_Plate_Prop

    def _plate_read_prop_excel(self, filename, sheetname="PP_Plate_SFormat"):
        '''
        An interface reading standard excel file of plate properties.
        Param:
            filename: full file name of material data, including path
        Return:
            self._dfg_Plate_Prop: a dataframe containing plate information
        '''
        df_Plate_Prop = pd.read_excel(filename, sheet_name=sheetname)
        # Drops the last row of data if it's incomplete "NaN" entry.
        df_Plate_Prop.dropna(inplace=True)
        # Sets column named 'Plate_ID' as index of rows
        df_Plate_Prop.set_index('Plate_ID', inplace=True)
        df_Plate_Prop = df_Plate_Prop.loc[~(df_Plate_Prop == 0).all(
            axis=1)]     # Remove rows with all zeros
        df_Plate_Prop.IsIsotropic = df_Plate_Prop.IsIsotropic.astype(
            'bool')      # Cast specified objects as boolean
        df_Plate_Prop.IsEndBearing = df_Plate_Prop.IsEndBearing.astype('bool')
        # Drops Rows with Plate_ID equal to 0, i.e. unused rows
        self._dfg_Plate_Prop = df_Plate_Prop[df_Plate_Prop.MaterialName != 0]
        return self._dfg_Plate_Prop

    def _plate_input_prop(self):
        '''
        Inputs plate materials in dataframe into Plaxis.
        Note: This function should be called after '_dfg_Plate_Prop' has been initialised.
        Param:
            None
        Return:
            self._plx_plate: a dictionary of plate materials for inputting pairs of attributes and values into Plaxis
        '''
        material = {}
        for ix, row in self._dfg_Plate_Prop.iterrows():
            # Creates a new empty list and stores as 'temp'
            temp = []
            # Iterates over two lists in parallel
            for key, value in zip(row.index, row.values):
                # Appends pair of key and value into the 'temp' list
                temp.append(key)
                temp.append(value)
            # Creates a new plate material set
            new_material = self._g_i.platemat()
            new_material.setproperties(*temp)
            material[row['MaterialName']] = new_material
            self._plx_plate = material                   # Keeps a record of material
            # print(self._plx_plate)
        self.logger.info("Nos. of Plate Materials Imported into Plaxis = " +
                         str(len(self._plx_plate)))
        return self._plx_plate
    
    def _extract_mat_property(self, material_type):
        '''
        Generic function that extracts properties of different materials in Plaxis.
        Param:
            material_type: string, indicating type of materials/structure elements
                           'PlateMat2D'  = 2D plate elements
                           'AnchorMat2D' = 2D anchor elements
                           'SoilMat'     = soil materials
        Return: 
            A dictionary of Plaxis objects of the specified materials
        '''
        # mats = self.g_i.Materials.filter(material_type)
        mats = self.g_i.filter(self.g_i.Materials, material_type)
        dict_mats = {}
        for mat in mats:
            dict_mats[mat.MaterialName.value] = mat
        return dict_mats

    def plate_extract_prop(self):
        '''
        Extracts existing plate information in Plaxis to a dictionary
        Param:
            None
        Return:
            A dictionary of plate materials in an existing Plaxis model
        '''
        self._plx_plate = self._extract_mat_property('PlateMat2D')
        self.logger.info(
            '{} Plate material information extracted!'.format(len(self._plx_plate)))
        return self._plx_plate

    def plate_extract_df(self):
        '''
        Extracts existing Plaxis plate materials into a dataFrame via a dictionary
        Param:
            None
        Return:
            df_plate_extract_para:  Dataframe of plate properties extracted from existing Plaxis model
        '''
        columns = ['MaterialNumber', 'MaterialName', 'Elasticity', 'IsIsotropic',
                   'IsEndBearing', 'EA', 'EA2', 'EI', 'nu', 'd', 'w', 'Mp', 'Np',
                   'Np2', 'RayleighAlpha', 'RayleighBeta', 'Gref', 'Colour']
        df_plate_extract_para = pd.DataFrame(columns=columns)
        plate_dict            = self.plate_extract_prop()
        for plate_name in plate_dict:
            plate = plate_dict[plate_name]
            for prop in columns:
                df_plate_extract_para.loc[plate_name,
                                          prop] = getattr(plate, prop).value
        return df_plate_extract_para

#   Anchor Material Related 

    def anchor_read_prop(self, filename):
        '''
        Reads anchor material information from different formats.
        Creates anchor materials in Plaxis based on the read properties.
        Param:
            filename: full file name of material data, including path
        Return:
            dfgv_Anchor_Prop: viewable dataframe of anchor materials
        '''
        if filename.endswith('.xlsm') or filename.endswith('.xlsx'):
            self.dfgv_Anchor_Prop = self._anchor_read_prop_excel(filename)
        else:
            self.logger.error('Filetype not implemented yet!')
        self._anchor_input_prop()
        return self.dfgv_Anchor_Prop

    def _anchor_read_prop_excel(self, filename, sheetname="PP_Anchor_SFormat"):
        '''
        An interface reading standard excel file of anchor properties.
        Param:
            filename: full file name of material data, including path
        Return:
            self._dfg_Anchor_Prop: a dataframe containing plate information
        '''
        df_Anchor_Prop = pd.read_excel(filename, sheet_name=sheetname)
        df_Anchor_Prop.dropna(inplace=True)
        df_Anchor_Prop.set_index('Anchor_ID', inplace=True)
        # Remove rows with all zeros
        df_Anchor_Prop = df_Anchor_Prop.loc[~(df_Anchor_Prop == 0).all(axis=1)]
        # Drops Rows with Anchor_ID equal to 0, i.e. unused rows
        self._dfg_Anchor_Prop = df_Anchor_Prop[df_Anchor_Prop.MaterialName != 0]
        return self._dfg_Anchor_Prop

    def _anchor_input_prop(self):
        '''
        Inputs anchor materials in dataframe into Plaxis.
        Note: This function should be called after '_dfg_Anchor_Prop' has been initialised.
        Param:
            None
        Return:
           self._plx_anchor: a dictionary of anchor materials for inputting pairs of attributes and values into Plaxis
        '''        
        material = {}
        for ix, row in self._dfg_Anchor_Prop.iterrows():
            # Creates a new empty list and stores as 'temp'
            temp = []
            # Iterates over two lists in parallel
            for key, value in zip(row.index, row.values):
                # Appends pair of key and value into the 'temp' list
                temp.append(key)
                temp.append(value)
            # Creates a new anchor material set
            material_01 = self._g_i.anchormat()
            material_01.setproperties(*temp)
            material[row['MaterialName']] = material_01
            self._plx_anchor = material                  # Keeps a record of material
            # print(self._plx_anchor)
        self.logger.info("Nos. of Anchor Materials Imported into Plaxis = " +
                         str(len(self._plx_anchor)))
        return self._plx_anchor

    def anchor_extract_prop(self):
        '''
        Extracts existing anchor information in Plaxis to a dictionary
        Param:
            None
        Return:
            A dictionary of anchor materials in an existing Plaxis model
        '''
        self._plx_anchor = self._extract_mat_property('AnchorMat2D')
        self.logger.info(
            '{} Anchor material information extracted!'.format(len(self._plx_anchor)))
        return self._plx_anchor

#   Embedded Beam Material Related 


#   Geogrid Material Related 

    def phase_extract(self):
        '''
        Extracts phases into dictionary
        '''
        self._plx_phase = {}
        for phase in self.g_i.Phases:
            self._plx_phase[phase.Identification.value] = phase
        return self._plx_phase

#   Geometry Extraction Related 

    def _soilpoly_extract(self):
        '''
        Extracts existing SoilPolygons into a dictionary.
        Param:
            None
        Return:
            self._plx_soilpoly: a dictionary of SoilPolygons
        '''        
        self._plx_soilpoly = {}     # Clears existing dictionary to be refreshed
        geometry = []
        geometry_key = []
        self._g_i.gotostages()
        # Create a list of SoilPolygon Names as key (index) for the dictionary of Plaxis objects
        sort_geo0 = self._g_i.tabulate(self._g_i.SoilPolygons)
        sort_geo1 = re.split('\n', sort_geo0)
        sort_geo2 = [re.split('\t', x)[0]
                     for x in sort_geo1 if 'N/A' not in x][1:]
        geometry_key = sort_geo2
        # Converts the counter of nos. of SoilPolygons to integer
        read_nos_geo = self._g_i.count(self._g_i.SoilPolygons)
        nos_geo  = int(read_nos_geo[:read_nos_geo.rfind(" items")])
        geometry = self._g_i.SoilPolygons[:]

        for igeo in range(nos_geo):
            Read_Geom_Name = geometry_key[igeo]
            Read_Geom_Code = geometry[igeo]
            self._plx_soilpoly[Read_Geom_Name] = Read_Geom_Code
        # print(self._plx_soilpoly)
        print("Nos. of SoilPolygons Extracted into Dictionary = " +
              str(len(self._plx_soilpoly)))
        if len(self._plx_soilpoly) == nos_geo:
            print("Nos. of Items in Dictionary Match Plaxis File")
        else:
            print("Error: Nos. of Items in Dictionary DO NOT Match Plaxis File!")
        return self._plx_soilpoly

    def poly_extract(self):
        '''
        Extracts existing polygons into a dictionary.
        Param:
            None
        Return:
            self._plx_poly: a dictionary of SoilPolygons     
        '''
        self._plx_poly = {}     # Clears existing dictionary to be refreshed
        geometry = []
        geometry_key = []
        self._g_i.gotostages()
        # Create a list of Polygon Names as key (index) for the dictionary of Plaxis objects
        sort_geo0 = self._g_i.tabulate(self._g_i.Polygons)
        sort_geo1 = re.split('\n', sort_geo0)
        sort_geo2 = [re.split('\t', x)[0]
                     for x in sort_geo1 if 'N/A' not in x][1:]
        geometry_key = sort_geo2
        # Converts the counter of nos. of Polygons to integer
        read_nos_geo = self._g_i.count(self._g_i.Polygons)
        nos_geo = int(read_nos_geo[:read_nos_geo.rfind(" items")])
        geometry = self._g_i.Polygons[:]
        for igeo in range(nos_geo):
            Read_Geom_Name = geometry_key[igeo]
            Read_Geom_Code = geometry[igeo]
            self._plx_poly[Read_Geom_Name] = Read_Geom_Code
        # print(self._plx_poly)
        print("Nos. of Polygons Extracted into Dictionary = " +
              str(len(self._plx_poly)))
        if len(self._plx_poly) == nos_geo:
            print("Nos. of Items in Dictionary Match Plaxis File")
        else:
            print("Error: Nos. of Items in Dictionary DO NOT Match Plaxis File!")
        return

    def get_soil_bounding_box(self, soilpoly_name):
        '''
        Returns a bounding box of a soil polygon given the name of the polygon
        Param:
            soilpoly_name: string, soil polygon name, e.g., "Soil_12_3"
        Return:
            A shapely.Polygon object
        '''
        soil = getattr(self.g_i, soilpoly_name)
        m    = re.search(r'.*\((.*);(.*);(.*)\).*\((.*);(.*);(.*)\)',
                         str(soil.Parent.BoundingBox))
        point1 = (eval(m.group(1)), eval(m.group(2)))
        point2 = (eval(m.group(4)), eval(m.group(2)))
        point3 = (eval(m.group(1)), eval(m.group(5)))
        point4 = (eval(m.group(4)), eval(m.group(5)))
        bounding_box = Polygon([point1, point2, point4, point3])
        return bounding_box

    def soilpoly_extract_df(self):
        '''
        Extracts existing Plaxis SoilPolygons into an dataFrame via dictionary
        Param:
            None
        Return:
            self._dfg_Poly_Extract_BB: a dataFrame of SoilPolygons
        '''        
        self._soilpoly_extract()
        # Define column headers and set-up dataframe
        columns = {'PolygonName':[],
                   'Area':[],
                   'BB_xmin':[],'BB_xmax':[],
                   'BB_ymax':[],'BB_ymin':[],
                   'CoarsenessFactor':[],
                   'BoundingBox':[], 'echoinfo':[]}
        df_Poly_Extract_BB = pd.DataFrame(columns=columns)
        # Populate dataframe
        for igeo, iName in enumerate(self._plx_soilpoly):
            # Converts 'plxscripting.plxproxy.PlxProxyIPText' into string
            df_Poly_Extract_BB.loc[igeo,"PolygonName"] = str(self._plx_soilpoly[iName].Name)  
            df_Poly_Extract_BB.loc[igeo,"Area"]        = self._plx_soilpoly[iName].Area
            mm = re.search('min: \((.*); (.*); .*\) max: \((.*); (.*); .*\)', \
                           str(self._plx_soilpoly[iName].BoundingBox))  
            # Converts BoundingBox output into string first
            if mm is not None:
                data =  {'xmin': float(mm.group(1)),
                         'ymin': float(mm.group(2)),
                         'xmax': float(mm.group(3)),
                         'ymax': float(mm.group(4))}
            df_Poly_Extract_BB.loc[igeo,"BB_xmin"] = data['xmin']
            df_Poly_Extract_BB.loc[igeo,"BB_xmax"] = data['xmax']
            df_Poly_Extract_BB.loc[igeo,"BB_ymax"] = data['ymax']
            df_Poly_Extract_BB.loc[igeo,"BB_ymin"] = data['ymin']
            df_Poly_Extract_BB.loc[igeo,"CoarsenessFactor"] = self._plx_soilpoly[iName].CoarsenessFactor
            self._dfg_Poly_Extract_BB = df_Poly_Extract_BB
            # print(self._dfg_Poly_Extract_BB)
        self.logger.info("Nos. of SoilPolygons Extracted into Dataframe = " + str(len(self._plx_soilpoly)))
        return self._dfg_Poly_Extract_BB

    def construct_soil_geom(self, path=''):
        '''
            Construct the geometries of Plaxis2D Model from the file path provided. If the path is left as defualt, 
            the model will be saved first in order to get the path of the Plaxis folder
            Param: 
                Path : path to the Plaxis 2D folder
            Return: 
                A Pandas dataframe holding the soil name ID and shapely polygons. 
        '''
        if self.plx_file_path == '':
            str_path = self.g_i.save()
            m = re.search(r'.*: (.*).p2dx', str_path)
            path = m.group(1)+'.p2dxdat'
            self.plx_file_path = path
        self.soils = BaseProject.polygon_from_meshinfo(path)
        for soil in self.g_i.soils:
            name = soil.Name.value
            results = self.soils[abs(np.array(
                (self.soils.area - soil.Parent.Area.value))) < 1e-4]  # check the area first
            if results.shape[0] > 1:  # if more polygons have the same area.
                box = self.get_soil_bounding_box(name)
                # lets check the centroid first
                results_further = results[results.centroid.within(box)]
                if results_further.shape[0] == 1:
                    ix = results_further.index[0]
                    self.soils.loc[ix, 'soil_ID'] = name
                else:                                                   # centroid provide more choices
                    # neet to check in a hard way, to go over all vertices and make sure all within the bounding box
                    for ix, row in results_further.iterrows():
                        polygon = row.geometry
                        the_polygon = True
                        for pt in polygon.exterior.coords[:]:
                            x, y = round(pt[0], 3), round(pt[1], 3)
                            if Point((x, y)).disjoint(box):
                                the_polygon = False
                                break
                        if the_polygon:
                            self.soils.loc[ix, 'soil_ID'] = name
                            break
            elif results.shape[0] == 1:
                ix = results.index[0]
                self.soils.loc[ix, 'soil_ID'] = name
            else:
                print('It is likely that the model has not been saved!')
            return self.soils

    def construct_soil_material_table(self):
        '''
        Param:
            None
        Return:
            None
        '''
        self.soil_material = pd.DataFrame()
        for phase in self.g_i.Phases:
            for soil in self.g_i.Soils:
                self.soil_material.loc[soil.Name.value, phase.Name.value] = (
                    soil.Material[phase].Name, soil.Active[phase])

    def get_soil_by_material_name(self, phase, material_name, plot=False):
        '''
        Param:
            None
        Return:
            None
        '''
        results = self.soil_material[self.soil_material[phase]
                                     == material_name].index
        if plot:
            ax = self.soils.plot(alpha=0.5, figsize=(10, 10), edgecolor='k')
            self.soils[results].plot(ax=ax)

    def get_soil_by_bounding_box():
        pass

#----------------------------------------------------------------------------------------------------------------------------------------------------------------
#  ELS PACKAGE FUNCTIONS
#----------------------------------------------------------------------------------------------------------------------------------------------------------------

    def draw_plate(self, filename, sheetname="PP_PlateCoord_SFormat"):
        '''
        Draws plate elements from excel.
        Param:
            filename:  full file name of plate coordinate information, including path
            sheetname: name of worksheet that contains the data
        Return:
            plx_plate_ele:  a dictionary of plates
            plx_plate_line: a dictionary of lines of plates
        '''
        self.plx_plate_ele = {}; self.plx_plate_line = {}; self._plx_plate_pts = {}
        self._plx_plate_negintf = {}; self._plx_plate_posintf = {}
        self.plate_extract_prop()
        df_Plate_Coord = pd.read_excel(filename, sheet_name=sheetname)
        df_Plate_Coord.dropna(inplace = True)
        df_Plate_Coord = df_Plate_Coord.loc[~(df_Plate_Coord==0).all(axis=1)]
        df_Plate_Coord.set_index('MaterialName', inplace = True)
        # print(df_Plate_Coord)
        # Cycles through rows in dataframe
        for ix, row in df_Plate_Coord.iterrows():
            Pts = []
            for key,value in zip(row.index,row.values):
                Pts.append(value)               # Adds coordinates as a list
            self._g_i.gotostructures()
            element_01 = self._g_i.plate(*Pts)  # Inserts coordinates without brackets into Plaxis to draw Plate
            element_02 = element_01[-1]         # Split list to retain Plate element entry
            element_03 = element_01[2]          # Split list to retain Line entry
            element_04 = []
            element_04.append(element_01[0]); element_04.append(element_01[1]) # Split list to retain Points entry
            plate_materialname = str(ix)
            # print(plate_materialname)
            # plx_Plate_Mat[plate_materialname] Reads the detailed Plaxis ID for named plate/anchor material
            # e.g. 'S1': <AnchorMat2D {816D907F-D41F-422A-9BAE-24F3203E24BC}>
            element_02.setmaterial(self._plx_plate[plate_materialname])  # Assigns Plate material
            line_name = "Line_"+str(ix)
            element_03.rename(line_name)            # Renames Line
            plate_name = "Plate_"+str(ix)
            element_02.rename(plate_name)           # Renames Plate
            self.plx_plate_ele[plate_materialname]  =  element_02   # Keep Dictionary of Plates
            self.plx_plate_line[plate_materialname] =  element_03   # Keep Dictionary of Lines of Plates
            self._plx_plate_pts[plate_materialname]  =  element_04  # Keep Dictionary of Points of Plates
            for i, item in enumerate(element_04):
                pt_name = "Point_"+str(plate_name)+"_"+str(i+1)     # Renames Points
                item.rename(pt_name)
            # Adds interfaces
            element_05 = self._g_i.neginterface(element_03)    
            element_06 = self._g_i.posinterface(element_03)  
            neginterface_name = "NegInterface_"+str(ix)
            element_05.rename(neginterface_name)                    # Renames Interfaces
            posinterface_name = "PosInterface_"+str(ix)
            element_06.rename(posinterface_name) 
            self._plx_plate_negintf = element_05                    # Keep Dictionary of Negative Interfaces
            self._plx_plate_posintf = element_06                    # Keep Dictionary of Positive Interfaces
        # Draws line at toe
        Pts_toe = [(df_Plate_Coord.iloc[0,2], df_Plate_Coord.iloc[0,3]), (df_Plate_Coord.iloc[1,2], df_Plate_Coord.iloc[1,3])]
        print(Pts_toe)
        self._g_i.line(*Pts_toe)
        self._g_i.rename(self._g_i.Lines[-1], "Line_WallToe")
        self.logger.info("Nos. of Plate Elements Imported into Plaxis = " + str(len(self.plx_plate_ele)))
        return self.plx_plate_ele, self.plx_plate_line

    def delete_all_plates(self):
        '''
        Delete all existing plates
        Param:
            None
        Return:
            None
        '''
        self._g_i.gotostructures()
        for x in self._g_i.plates[:]:
            self._g_i.delete(x)
        return

    def draw_anchor(self, filename, sheetname="PP_AnchorCoord_SFormat"):
        '''
        Draws n2n anchor elements from excel
        Param:
            filename:  full file name of anchor coordinate information, including path
            sheetname: name of worksheet that contains the data
        Return:
            plx_anchor_ele:  a dictionary of n2n anchors
            plx_anchor_line: a dictionary of lines of n2n anchors
        '''        
        self.plx_anchor_ele = {}; self.plx_anchor_line = {}; self._plx_anchor_pts = {}
        self.anchor_extract_prop()
        df_Anchor_Coord = pd.read_excel(filename, sheet_name=sheetname)
        df_Anchor_Coord.dropna(inplace = True)
        df_Anchor_Coord = df_Anchor_Coord.loc[~(df_Anchor_Coord==0).all(axis=1)]
        df_Anchor_Coord.set_index('MaterialName', inplace = True)
        # Cycles through rows in dataframe
        for ix, row in df_Anchor_Coord.iterrows():
            Pts = []
            for key,value in zip(row.index,row.values):
                Pts.append(value)                   # Adds coordinates as a list
            self._g_i.gotostructures()
            element_01 = self._g_i.n2nanchor(*Pts)  # Inserts coordinates without brackets into Plaxis to draw Anchor
            element_02 = element_01[-1]             # Split list to retain NodeToNodeAnchor element entry
            element_03 = element_01[2]              # Split list to retain Line entry
            element_04 = []
            element_04.append(element_01[0]); element_04.append(element_01[1]) # Split list to retain Points entry
            anchor_materialname = str(ix)
            # print(anchor_materialname)
            element_02.setmaterial(self._plx_anchor[anchor_materialname])      # Assigns Anchor material
            line_name   = "Line_"+str(ix)
            element_03.rename(line_name)                            # Renames Line
            anchor_name = "Anchor_"+str(ix)
            element_02.rename(anchor_name)                          # Renames Anchor
            for i, item in enumerate(element_04):
                pt_name = "Point_"+str(anchor_name)+"_"+str(i+1)    # Renames Points
                item.rename(pt_name)
            self.plx_anchor_ele[anchor_materialname]  = element_02   # Keep Dictionary of N2NAnchors
            self.plx_anchor_line[anchor_materialname] = element_03   # Keep Dictionary of Lines of N2NAnchors
            self._plx_anchor_pts[anchor_materialname]  = element_04  # Keep Dictionary of Points of N2NAnchors
        self.logger.info("Nos. of Anchor Elements Imported into Plaxis = " + str(len(self.plx_anchor_ele)))
        return self.plx_anchor_ele, self.plx_anchor_line

    def delete_all_anchors(self):
        '''
        Delete all existing anchors
        Param:
            None
        Return:
            None
        '''
        self._g_i.gotostructures()
        for x in self._g_i.n2nanchor[:]:
            self._g_i.delete(x)

    def draw_lineload(self, filename, sheetname="PP_LineLoad_SFormat", lineload_value=-20.0):
        '''
        Draws lineload from excel
        Param:
            filename:       full file name of lineload coordinate information, including path
            sheetname:      name of worksheet that contains the data
            lineload_value: magnitude of lineload. Default, qy_start = -20.0[kPa]
        Return:
            plx_lineload_ele:  a dictionary of lineloads
            plx_lineload_line: a dictionary of lines of lineloads
        '''        
        self.plx_lineload_ele = {}; self.plx_lineload_line = {}; self._plx_lineload_pts = {}  
        df_LineLoad_Coord = pd.read_excel(filename, sheet_name=sheetname)
        df_LineLoad_Coord.dropna(inplace = True)
        df_LineLoad_Coord = df_LineLoad_Coord.loc[~(df_LineLoad_Coord==0).all(axis=1)]
        df_LineLoad_Coord.set_index('LineLoadName', inplace = True)
        # Cycles through rows in dataframe
        for ix, row in df_LineLoad_Coord.iterrows():
            Pts = []
            for key,value in zip(row.index,row.values):
                Pts.append(value)                   # Adds coordinates as a list
            self._g_i.gotostructures()
            element_01 = self._g_i.lineload(*Pts)   # Inserts coordinates without brackets into Plaxis to draw LineLoad
            element_02 = element_01[-1]             # Split list to retain LineLoad entry
            element_03 = element_01[2]              # Split list to retain Line entry
            element_04 = []
            element_04.append(element_01[0]); element_04.append(element_01[1])  # Split list to retain Points entry
            lineload_name = str(ix)
            # print(element_01, element_02, element_03, element_04, lineload_name)
            self._g_i.set(element_02.qy_start, lineload_value)                  # Assigns Lineload value
            line_name     = "Line_"+str(ix)
            element_03.rename(line_name)                             # Renames Line
            lineload_name = "LineLoad_"+str(ix)
            element_02.rename(lineload_name)                         # Renames Lineload
            for i, item in enumerate(element_04):
                pt_name = "Point_"+str(lineload_name)+"_"+str(i+1)   # Renames Points
                item.rename(pt_name)
            self.plx_lineload_ele[lineload_name]  = element_02  # Keep dictionary of Lineload
            self.plx_lineload_line[lineload_name] = element_03  # Keep dictionary of Lines of Lineload
            self._plx_lineload_pts[lineload_name] = element_04  # Keep dictionary of Points of Lineload
        # print(self.plx_lineload_ele)
        group_line = [*self.plx_lineload_ele.values()]
        group_name = str(lineload_name)
        group_name = "Group_"+str(group_name[:group_name.index("_")])+"s"
        # print(group_line, group_name)
        self._g_i.group(group_line).rename(group_name)
        self.logger.info("Nos. of LineLoads Imported into Plaxis = " + str(len(self.plx_lineload_ele)))
        return self.plx_lineload_ele, self.plx_lineload_line

    def delete_all_lineloads(self):
        '''
        Delete all existing lineloads
        Param:
            None
        Return:
            None
        '''
        self._g_i.gotostructures()
        for x in self._g_i.lineloads[:]:
            self._g_i.delete(x)

    def draw_rect_poly(rect_dep, rect_wid, ref_x, ref_y):
        '''
        Draws a rectangular polygon   
            rect_dep:    depth of polygon
            rect_wid:    width of polygon
            ref_x:       x-coordinate of reference point (leftmost side of polygon)
            ref_y:       y-coordinate of reference point (top level of polygon in mPD)
        Param:
            None
        Return:
            None
        '''
        coord_tl = (ref_x, ref_y)
        coord_tr = (ref_x + rect_wid, ref_y)
        coord_bl = (ref_x, ref_y - rect_dep)
        coord_br = (ref_x + rect_wid, ref_y - rect_dep)
        self._g_i.gotostructures()
        self._g_i.polygon(coord_bl, coord_br, coord_tr, coord_tl)
        return

    def draw_exc_lvl(self, filename, sheetname="PP_ExcCoord_SFormat"):
        '''
        Draws excavation level from excel
        Param:
            filename:  full file name of excavation levels, including path
            sheetname: name of worksheet that contains the coordinate data
        Return:
            None
        '''
        self._plx_exc_line = {}; self._plx_exc_pts = {}
        df_Exc_Coord = pd.read_excel(filename, sheet_name=sheetname)
        df_Exc_Coord.dropna(inplace = True)
        df_Exc_Coord = df_Exc_Coord.loc[~(df_Exc_Coord==0).all(axis=1)]
        df_Exc_Coord.set_index('ExcavationLevel', inplace = True)
        # Cycles through rows in dataframe
        for ix, row in df_Exc_Coord.iterrows():
            Pts = []
            for key,value in zip(row.index,row.values):
                Pts.append(value)              # Adds coordinates as a list
            self._g_i.gotostructures()
            element_01 = self._g_i.line(*Pts)  # Inserts coordinates without brackets into Plaxis to draw Line
            element_02 = element_01[-1]        # Split list to retain Line entry
            element_03 = []
            element_03.append(element_01[0]); element_03.append(element_01[1]) # Split list to retain Points entry
            exc_ID = str(ix)
            # print(exc_ID)
            line_name   = "Line_"+str(ix)
            element_02.rename(line_name)                             # Renames Line
            for i, item in enumerate(element_03):
                pt_name = "Point_"+str(line_name)+"_"+str(i+1)   # Renames Points
                item.rename(pt_name)
            self._plx_exc_line[exc_ID] =  element_02  # Keep Dictionary of Lines of Line
            self._plx_exc_pts[exc_ID]  =  element_03  # Keep Dictionary of Points of Lines
        self.logger.info("Nos. of Excavation Levels Imported into Plaxis = " + str(len(self._plx_exc_line)))
        return

    def draw_dewtr_lvl(self, filename, sheetname="PP_DewtrCoord_SFormat"):
        '''
        Draws dewater level from excel
        Param:
            filename:  full file name of dewater levels, including path
            sheetname: name of worksheet that contains the coordinate data
        Return:
            None
        '''
        self._plx_dewtr_line = {}
        df_Dewtr_Coord = pd.read_excel(filename, sheet_name=sheetname)
        df_Dewtr_Coord.dropna(inplace = True)
        df_Dewtr_Coord = df_Dewtr_Coord.loc[~(df_Dewtr_Coord==0).all(axis=1)]
        df_Dewtr_Coord.set_index('DewaterLevel', inplace = True)
        # Cycles through rows in dataframe
        for ix, row in df_Dewtr_Coord.iterrows():
            Pts = []
            for key,value in zip(row.index,row.values):
                Pts.append(value)                    # Adds coordinates as a list
            self._g_i.gotoflow()
            element_01 = self._g_i.waterlevel(*Pts)  # Inserts coordinates to draw water level
            dewtr_ID = str(ix)
            # print(dewtr_ID)
            dewtr_name   = "UserWaterLvl_"+str(ix)
            element_01.rename(dewtr_name)            # Renames UserWaterLevel
            self._plx_dewtr_line[dewtr_ID] =  element_01  # Keep Dictionary of UserWaterLevel
        # print(self._plx_dewtr_line)
        self.logger.info("Nos. of UserWaterLevels Imported into Plaxis = " + str(len(self._plx_dewtr_line)))
        return

#================================================================================================================================================================
#   'MESH' TAB FUNCTIONS
#================================================================================================================================================================

    def mesh2D(self, mesh_factor=0.06):
        '''
        This function goes to the 'Mesh' Tab and meshes 2D model. 
        Unless otherwise specified, mesh_factor = 0.06, i.e. Medium element distribution.
        Param:
            mesh_factor: 0.10000 = Very Coarse, 0.07500 = Coarse, 0.06000 = Medium, 0.04002 = Fine, 0.03000 = Very Fine
        Return:
            None
        '''
        mesh_factor = 0.06
        self._g_i.gotomesh()
        self._g_i.mesh(mesh_factor)     # Generates mesh
        self.logger.info("2D Meshing Successful")
        return

    @staticmethod
    def points_from_meshinfo(path, plot=False):
        '''
        This function parse  Points information from the 'meshinfo file'
        Return:
            A dataframe containing point IDs and coodinates
        Param:
            path - path to the data of plaxis
            b_plot: True - plot a graph of points; False - no plot
        example:
        >>> ponits_from_meshinfo('data.meshinfo',b_plot=True)
        '''
        with open(os.path.join(path, 'data.meshinfo')) as fin:
            meshdata = fin.read()
        points_block = re.findall(r'POINTS((.|\n)*?)CURVES', meshdata)[0][0]
        points_str_list = points_block.strip().split('\n')
        df_points = pd.DataFrame(dict(x=[], y=[], z=[]))
        geometry = []
        for point_str in points_str_list:
            m = re.search(r'(P.*) =.*\((.*),(.*),(.*)\)', point_str)
            df_points.loc[m.group(1), 'x'] = float(m.group(2))
            df_points.loc[m.group(1), 'y'] = float(m.group(3))
            df_points.loc[m.group(1), 'z'] = float(m.group(4))
            geometry.append(Point(float(m.group(2)), float(m.group(3))))
        gdf = gpd.GeoDataFrame(df_points, geometry=geometry)
        if plot:
            gdf.plot(figsize=(10, 10), color='k', marker='o', markersize=3)
        return gdf

    @staticmethod
    def curve_from_meshinfo(path, plot=False):
        '''
        This function parse Curve information from the 'meshinfo file'
        Return:
            A dataframe containing point IDs and coodinates
        Param:
            path - path to the data of plaxis
            b_plot: True - plot a graph of curve; False - no plot
        example:
        >>> curve_from_meshinfo('data.meshinfo',b_plot=True)
        '''
        points_gdf = BaseProject.ponits_from_meshinfo(path)
        import pandas as pd
        with open(os.path.join(path, 'data.meshinfo')) as fin:
            meshdata = fin.read()
        curves_block = re.findall(r'CURVES((.|\n)*?)SURFACES', meshdata)[0][0]
        curve_str_list = curves_block.strip().split('\n')
        df_curves = pd.DataFrame(dict(pt1=[], pt2=[]))
        for curve_str in curve_str_list:
            m = re.search(r'(C.*) =.*\((.*),(.*)\)', curve_str)
            df_curves.loc[m.group(1), 'pt1'] = m.group(2).strip()
            df_curves.loc[m.group(1), 'pt2'] = m.group(3).strip()
        # form the curve below
        geometry = []
        for ix, row in df_curves.iterrows():
            pt1_ix, pt2_ix = row['pt1'], row['pt2']
            pt1 = points_gdf.loc[pt1_ix, 'geometry']
            pt2 = points_gdf.loc[pt2_ix, 'geometry']
            geometry.append(LineString([pt1, pt2]))
        curves_gdf = gpd.GeoDataFrame(df_curves, geometry=geometry)
        if plot is True:
            ax = points_gdf.plot(figsize=(20, 20), color='b',
                                 marker='o', markersize=5)
            curves_gdf.plot(ax=ax, color='k')
        return curves_gdf

    def delete_all_materials(self):
        for mat in self.g_i.materials:
            self.g_i.delete(mat)

    @staticmethod
    def polygon_from_meshinfo(path, plot=True):
        '''
        This function parse surface information from the 'meshinfo file'
        Return:
            A dataframe containing point IDs and coodinates
        Param:
            path - path to the data of plaxis
            b_plot: True - plot a graph of curve; False - no plot
        example:
        >>> polygon_from_meshinfo('data.meshinfo',b_plot=True)
        '''
        curves_gdf = BaseProject.curve_from_meshinfo(path)
        with open(os.path.join(path, 'data.meshinfo')) as fin:
            meshdata = fin.read()
        surface_block = re.findall(
            r'SURFACES((.|\n)*?)INTERFACE_ELEMENTS', meshdata)[0][0]
        surface_str_list = surface_block.strip().split('\n')
        polygon_ID = []
        geometry = []
        for surface in surface_str_list:
            m = re.search(r'(S.*) =.*\((.*)\)', surface)
            polygon_ID.append(m.group(1))
            list = m.group(2).strip().split(',')
            list = [x.strip() for x in list]
            # let's form the polygon here
            polygon_vertices = []
            for ix, line in enumerate(list):
                if '-' in line:
                    line_ends = curves_gdf.loc[line[1:]
                                               ]['geometry'].coords[:][::-1]
                else:
                    line_ends = curves_gdf.loc[line]['geometry'].coords[:]
                if ix == 0:
                    polygon_vertices.append(line_ends[0])
                    polygon_vertices.append(line_ends[1])
                else:
                    polygon_vertices.append(line_ends[1])
            geometry.append(Polygon(polygon_vertices))
        #     print(list)
        polygon_gdf = gpd.GeoDataFrame(dict(ID=polygon_ID, geometry=geometry))
        polygon_gdf['area'] = polygon_gdf.area
        polygon_gdf['centroid'] = polygon_gdf.centroid
        polygon_gdf.set_index('ID', inplace=True)
        return polygon_gdf

#================================================================================================================================================================
#   'FLOW CONDITIONS' TAB FUNCTIONS
#================================================================================================================================================================

    def _dewtr_poly(self, dewtr_xmin, dewtr_xmax, dewtr_ymax, dewtr_ymin, exc_lvl, dewtr_uwlvl, Phase_exc):
        '''
        Set Water Levels/Conditions of Polygons for excavation
            dewtr_xmin:   set leftmost extent of dewatering zone (m)
            dewtr_xmax:   set rightmost extent of dewatering zone (m)
            dewtr_ymax:   set top extent of dewatering zone (m)
            dewtr_ymin:   set bottom extent of dewatering zone (m)
            exc_lvl:      set excavation level (m)
            dewtr_uwlvl:  set UserWaterLevel of dewatering zone
            Phase_exc:    set excavation phase
        Param:
            None
        Return:
            None
        '''
        dewtr_extX  = (self._dfg_Poly_Extract_BB['BB_xmin']>=dewtr_xmin) & \
                      (self._dfg_Poly_Extract_BB['BB_xmax']<=dewtr_xmax)
        df_poly01   = self._dfg_Poly_Extract_BB.loc[dewtr_extX]
        # Set Clusters above dewtr_uwlvl to Dry
        dry_extY      = (df_poly01['BB_ymax']<=dewtr_ymax) & (df_poly01['BB_ymin']>=exc_lvl)
        df_dewtr_poly = df_poly01.loc[dry_extY]
        self._g_i.gotowater()
        for ix, row in df_dewtr_poly.iterrows():
            if row['PolygonName'] in self._plx_soilpoly.keys():
                self._g_i.setwaterdry(self._plx_soilpoly[row['PolygonName']], Phase_exc)
        # Set Clusters above dewtr_uwlvl to Dry
        dewtr_extY    = (df_poly01['BB_ymax']<=exc_lvl) & (df_poly01['BB_ymin']>=dewtr_ymin)
        df_dewtr_poly = []
        df_dewtr_poly = df_poly01.loc[dewtr_extY]
        self._g_i.gotowater()
        for ix, row in df_dewtr_poly.iterrows():
            if row['PolygonName'] in self._plx_soilpoly.keys():
                self._g_i.setwaterlevel(self._plx_soilpoly[row['PolygonName']], Phase_exc, dewtr_uwlvl)
        self.logger.info("Dewatering Set in Plaxis Model Phase: ")
        return

#================================================================================================================================================================
#   'STAGED CONSTRUCTION' TAB FUNCTIONS
#================================================================================================================================================================

#   Phase Related 

    def add_plastic(self, PhaseName, PhaseStart, PhaseNew, PwpCalcType="Phreatic", SolverType="Picos (multicore iterative)",
                    ResetDispl0=False):
        '''
        Adds a Plastic type Phase with standard setting, unless otherwise specified.
        Param:
            PhaseName:   text description of new phase to be entered into ID
            PhaseStart:  sequential Phase No. that new phase will be added after
            PhaseNew:    sequentual No. of new Phase
            PwpCalcType: set pore pressure calculation type. Default = "Phreatic"
                         options: "Use pressures from previous phase" or "Steady state groundwater flow"
            SolverType:  set solver type. Default = "Picos (multicore iterative)"
                         options: "Pardiso (multicore direct)" or "Classic (single core iterative)"
            ResetDispl0: RESETS DISPLACEMENTS TO ZERO! Default = False
        Return:
            None
        '''
        self._g_i.gotostages()
        self._g_i.phase(self._g_i.Phases[PhaseStart])     # Create extra Phase
        self._g_i.set(self._g_i.Phases[PhaseNew].Identification, PhaseName)
        self._g_i.set(self._g_i.Phases[PhaseNew].PorePresCalcType, PwpCalcType)
        self._g_i.set(self._g_i.Phases[PhaseNew].Deform.ResetDisplacementsToZero, False)     # RESET DISPLACEMENTS!
        self._g_i.set(self._g_i.Phases[PhaseNew].Deform.UseCavitationCutOff, True)
        self._g_i.set(self._g_i.Phases[PhaseNew].Solver, SolverType)
        self.logger.info("Plastic Calculation Type [Phase_"+str(PhaseNew)+"] Added: "+str(PhaseName))
        return

    def add_consolidation(self, PhaseName, PhaseStart, PhaseNew, LoadType="Staged construction", ConsParam=1,
                          SolverType="Picos (multicore iterative)"):
        '''
        Adds a Consolidation type Phase with standard setting, unless otherwise specified.
        Param:
            PhaseName:  text description of new phase to be entered into ID
            PhaseStart: sequential Phase No. that new phase will be added after
            PhaseNew:   sequentual No. of new Phase
            LoadType:   set loading type. Default = "Staged construction"
                        options: "Minimum excess pore pressure" or "Degree of consolidation"
            ConsParam:  attribute depends on loading type
                        consolidation time interval in days (Default = 1 day)
                        min. excess pore pressure (Default = 1 kPa)
                        degree of consolidation (Default = 1 %)
            SolverType: solver type Default = "Picos (multicore iterative)"
                        options: "Pardiso (multicore direct)" or "Classic (single core iterative)"
        Return:
            None
        '''
        self._g_i.gotostages()
        self._g_i.phase(self._g_i.Phases[PhaseStart])     # Create extra Phase
        self._g_i.set(self._g_i.Phases[PhaseNew].DeformCalcType, "Consolidation")     # Set to consolidation calculation
        self._g_i.set(self._g_i.Phases[PhaseNew].Deform.LoadingType, LoadType)
        self._g_i.set(self._g_i.Phases[PhaseNew].Identification, PhaseName)
        self._g_i.set(self._g_i.Phases[PhaseNew].Deform.UseCavitationCutOff, True)
        self._g_i.set(self._g_i.Phases[PhaseNew].Solver, SolverType)
        if LoadType == "Staged construction":
            self._g_i.set(self._g_i.Phases[PhaseNew].TimeInterval, ConsParam)
        elif LoadType == "Minimum excess pore pressure":
            self._g_i.set(self._g_i.Phases[PhaseNew].Deform.Loading.PStop, ConsParam)
        elif LoadType == "Degree of consolidation":
            self._g_i.set(self._g_i.Phases[PhaseNew].Deform.Loading.ConsolidDegree, ConsParam)
        self.logger.info("Consolidation Calculation Type [Phase_"+str(PhaseNew)+"] Added: "+str(PhaseName))
        return
    
    def add_safety(self, PhaseName, PhaseStart, PhaseNew, 
                   IterPara=True, MaxStep=100, SolverType="Picos (multicore iterative)"):
        '''
        Adds a Safety type Phase with standard setting unless otherwise specified.
        Param:
            PhaseName:  text description of new phase to be entered into ID
            PhaseStart: sequential Phase No. that new phase will be added after
            PhaseNew:   sequentual No. of new Phase
            IterPara:   use default iteration parameters. Default = True
            MaxStep:    set maximum nos. of steps if default iteration parameters are not used
            SolverType: solver type Default = "Picos (multicore iterative)"
                        options: "Pardiso (multicore direct)" or "Classic (single core iterative)"
        Return:
            None
        '''
        self._g_i.gotostages()
        self._g_i.phase(self._g_i.Phases[PhaseStart])     # Create extra Phase
        self._g_i.set(self._g_i.Phases[PhaseNew].DeformCalcType, "Safety")     # Set to phi-c calculation
        self._g_i.set(self._g_i.Phases[PhaseNew].Identification, PhaseName)
        self._g_i.set(self._g_i.Phases[PhaseNew].Deform.UseCavitationCutOff, True)
        self._g_i.set(self._g_i.Phases[PhaseNew].Solver, SolverType)
        self._g_i.set(self._g_i.Phases[PhaseNew].Deform.UseDefaultIterationParams, IterPara)
        if IterPara == False:
            self._g_i.set(self._g_i.Phases[PhaseNew].Deform.MaxSteps, MaxStep)     # Set maximum number of steps
        self.logger.info("Safety Calculation Type [Phase_"+str(PhaseNew)+"] Added: "+str(PhaseName))
        return

    def phase_extract(self):
        '''
        Extracts phases into a dictionary.
        Return:
            self._plx_phase: a dictionary of construction phases
        '''
        self._plx_phase = {}
        stage           = []
        stage_key       = []
        stage = self._g_i.Phases[:]                     # List out Phases, and saves Plaxis code to a list
        for iStage in range(len(stage)):
            iName = str(stage[iStage].Identification)   # Converts Plaxis Code (PlxProxyIPText) into string
            stage_key.append(iName)
            self._plx_phase[stage_key[iStage]] = stage[iStage]
        return self._plx_phase

    def rename_phases(self):
        '''
        Renames the phase to an increasing order, where 'Initial_Phase' is called "Phase_0"
        Param:
            None
        Return:
            None
        '''
        for ix, phase in enumerate(self._g_i.Phases):
            try:
                phase.Name = 'Phase_' + str(ix)
            except:
                # If the name is already in the list, we rename the conflicing name to a temporary name
                getattr(self._g_i, 'Phase_' + str(ix)).Name = 'Phase_temp_' + str(ix)
                phase.Name = 'Phase_' + str(ix)

    def same_all_plates(self, refplate):
        '''
        Making all plates in all phases have identical settings in staged construction
        Param:
            refplate: reference plate
        Return:
            None
        '''
        self._g_i.gotostages()
        otherplates = self._g_i.Plates[1:]
        for iStage in self._g_i.Phases[:]:
            if refplate.Active[iStage] is None: # Phase not yet initialised
                continue
            for otherplate in otherplates:
                otherplate.Material[iStage] = refplate.Material[iStage]
                otherplate.Material[iStage] = refplate.Material[iStage]
        return

#----------------------------------------------------------------------------------------------------------------------------------------------------------------
#  ELS PACKAGE FUNCTIONS
#----------------------------------------------------------------------------------------------------------------------------------------------------------------

    def stages_exc_nopreload(self, exc_start, filename, exc_sheetname="PP_ExcCoord_SFormat"):
        '''
        Creates excavation phases without preload and activate preceding anchors.
        Param:
            exc_start: phase index of 1st (NEW) excavation stage
            filename:  full file name of dewater levels, including path
            sheetname: name of worksheet that contains the coordinate data
        Return:
            None
        '''
        # Read excavation levels
        df_Exc_Coord = pd.read_excel(filename, sheet_name=exc_sheetname)
        df_Exc_Coord.dropna(inplace=True)
        df_Exc_Coord = df_Exc_Coord.loc[~(df_Exc_Coord == 0).all(axis=1)]
        df_Exc_Coord.set_index('ExcavationLevel', inplace=True)
        # Get total number of excavation phases
        total_exc = len(df_Exc_Coord)
        # Get last excavation phase
        exc_end = exc_start + total_exc

        self._g_i.gotostages()
        for x in range(total_exc):
            if x == 0 and exc_start == 1:
                self._g_i.phase(self._g_i.InitialPhase)
                self._g_i.set(
                    self._g_i.Phases[-1].Identification, str(df_Exc_Coord.index[x]))
            elif x == 0:
                self._g_i.phase(self._g_i.Phases[exc_start-1])
                self._g_i.set(
                    self._g_i.Phases[-1].Identification, str(df_Exc_Coord.index[x]))
            else:
                # Plural (phases) for index reference
                self._g_i.phase(self._g_i.Phases[-1])
                self._g_i.set(
                    self._g_i.Phases[-1].Identification, str(df_Exc_Coord.index[x]))
        return

    def _exc_poly(self, exc_xmin, exc_xmax, exc_ymax, exc_ymin, Phase_exc):
        '''
        Deactivate Polygons for excavation
            exc_xmin:     set rightmost extent of excavation (m)
            exc_xmax:     set leftmost extent of excavation (m)
            exc_ymax:     set top extent of excavation (m)
            exc_ymin:     set bottom extent of excavation (m)
            Phase_exc:    set excavation phase
        Param:
            None
        Return:
            None
        '''
        exc_extX    = (self._dfg_Poly_Extract_BB['BB_xmin']>=exc_xmin) & \
                      (self._dfg_Poly_Extract_BB['BB_xmax']<=exc_xmax)
        df_poly01   = self._dfg_Poly_Extract_BB.loc[exc_extX]
        
        exc_extY    = (df_poly01['BB_ymax']<=exc_ymax) & (df_poly01['BB_ymin']>=exc_ymin)
        df_exc_poly = df_poly01.loc[exc_extY]
        
        self._g_i.gotostages()
        for ix, row in df_exc_poly.iterrows():
            if row['PolygonName'] in self._plx_soilpoly.keys():
                self._g_i.deactivate(self._plx_soilpoly[row['PolygonName']], Phase_exc)
        self.logger.info("Excavation Added to Plaxis Model Phase: ")
        return

    def stage_deact_dewtr(self, max_gl, grouttoe, filename, exc_sheetname="PP_ExcCoord_SFormat",
                          anchor_sheetname="PP_AnchorCoord_SFormat", dewtr_sheetname="PP_DewtrCoord_SFormat", 
                          dewatr_delta=0.500):
        '''
        Deactive SoilPolygons, Activate Anchors and Set Water Levels/Conditions
        Param:
            filename:     full file name of dewater levels, including path
            sheetname:    name of worksheet that contains the coordinate data
            max_gl:       maximum ground level
            grouttoe:     grout toe level
            dewatr_delta: depth of dewatering level below excavation level. Default = 0.500m
        Return:
            None
        '''
        self.phase_extract()
        self.soilpoly_extract_df()
        # Read excavation levels
        df_Exc_Coord = pd.read_excel(filename, sheet_name=exc_sheetname)
        df_Exc_Coord.dropna(inplace = True)
        df_Exc_Coord = df_Exc_Coord.loc[~(df_Exc_Coord==0).all(axis=1)]
        df_Exc_Coord.set_index('ExcavationLevel', inplace = True)
        # print(df_Exc_Coord, df_Exc_Coord.drop(df_Exc_Coord.index[[0]]))
        # Read anchor levels
        df_Anchor_Coord = pd.read_excel(filename, sheet_name=anchor_sheetname)
        df_Anchor_Coord.dropna(inplace = True)
        df_Anchor_Coord = df_Anchor_Coord.loc[~(df_Anchor_Coord==0).all(axis=1)]
        df_Anchor_Coord.set_index('MaterialName', inplace = True)    
        # print(df_Anchor_Coord)    
        # Read dewater levels
        df_Dewtr_Coord = pd.read_excel(filename, sheet_name=dewtr_sheetname)
        df_Dewtr_Coord.dropna(inplace = True)
        df_Dewtr_Coord = df_Dewtr_Coord.loc[~(df_Dewtr_Coord==0).all(axis=1)]
        df_Dewtr_Coord.set_index('DewaterLevel', inplace = True)
        # print(df_Dewtr_Coord)

        self._g_i.gotostages()
        # Cycles through rows in dataframe to deactivate excavation levels
        for iStage, row in df_Exc_Coord.iterrows():
            # print(iStage, self._plx_phase[iStage])
            self._g_i.setcurrentphase(self._plx_phase[iStage])
            exc_xmin     = df_Exc_Coord.loc[iStage,"Exc_x1"]  
            exc_xmax     = df_Exc_Coord.loc[iStage,"Exc_x2"]    
            exc_ymax     = max_gl 
            exc_ymin     = min(df_Exc_Coord.loc[iStage,"Exc_y1"], df_Exc_Coord.loc[iStage,"Exc_y2"])   
            Phase_exc    = self._plx_phase[iStage]
            self._exc_poly(exc_xmin, exc_xmax, exc_ymax, exc_ymin, Phase_exc)
            # Cycles through rows in dataframe to activate anchors
            # First map anchors and excavation stages. Define column headers and set-up dataframe
            columns = ['ExcavationLevelName','AnchorMaterialName']
            df_Map_Anchnexc = pd.DataFrame(columns=columns)
            df_Map_Exc = df_Exc_Coord.drop(df_Exc_Coord.index[0]).copy()
            df_Map_Anchnexc.loc[:,'ExcavationLevelName'] = df_Map_Exc.index     # 1st Strut installed before 2nd excavaton stage
            df_Map_Anchnexc.loc[:,'AnchorMaterialName']  = df_Anchor_Coord.index
            df_Map_Anchnexc.set_index('ExcavationLevelName', inplace = True)
            # print(df_Map_Exc, df_Map_Anchnexc, df_Exc_Coord, df_Exc_Coord.index[0])
            if iStage != df_Exc_Coord.index[0]:                                # 1st Strut installed before 2nd excavaton stage
               iStrut = df_Map_Anchnexc.loc[iStage,'AnchorMaterialName']
               self._g_i.activate(self.plx_anchor_line[iStrut], self._plx_phase[iStage])
               self.logger.info("Anchors Added to Plaxis Model Phase: "+str(iStage))
        # Cycles through rows in dataframe to deactivate dewatering levels
        for iStage, row in df_Dewtr_Coord.iterrows():
            # print(iStage)
            dewtr_xmin   = df_Dewtr_Coord.loc[iStage,"Dewtr_x1"] 
            dewtr_xmax   = df_Dewtr_Coord.loc[iStage,"Dewtr_x2"]  
            dewtr_ymax   = max_gl
            dewtr_ymin   = grouttoe  
            exc_lvl      = min(df_Dewtr_Coord.loc[iStage,"Dewtr_y1"], \
                               df_Dewtr_Coord.loc[iStage,"Dewtr_y2"]) + dewatr_delta
            dewtr_uwlvl  = self._plx_dewtr_line[iStage]
            Phase_exc    = self._plx_phase[iStage]
            # print(dewtr_uwlvl)
            self._dewtr_poly(dewtr_xmin, dewtr_xmax, dewtr_ymax, dewtr_ymin, exc_lvl, dewtr_uwlvl, Phase_exc)
        self.logger.info("All Excavations, Anchors & Dewatering Incorporated into Plaxis Model")
        return

#   Calculation Related 

    def numctrlparam(self, PhaseNo, MaxStep=1000, MaxUnloadStep=5, MaxIter=60, DesMinIter=6, DesMaxIter=15, 
                     LineSearch=False, GradualError=False, SolverType="Picos (multicore iterative)"):
        '''
        Adjusts numerical control parameters of specified sequential Phase No.
        Param:
            PhaseNo:       sequential Phase No. 
            MaxStep:       max. nos. of steps. Default = 1000
            MaxUnloadStep: max. nos. of unloading steps. Default = 5
            MaxIter:       max. nos. of iterations. Default = 60
            DesMinIter:    desired min. nos. of iterations. Default = 6
            DesMaxIter:    desired max. nos. of iterations. Default = 15
            LineSearch:    whether to use line search function.  Default = False
            GradualError:  whether to use gradual error reduction function.  Default = False
            SolverType:    solver type Default = "Picos (multicore iterative)"
                           options: "Pardiso (multicore direct)" or "Classic (single core iterative)"
        Return:
            None
        '''
        self._g_i.gotostages()
        self._g_i.set(self._g_i.Phases[PhaseNo].Solver, SolverType)
        self._g_i.set(self._g_i.Phases[PhaseNo].Deform.UseDefaultIterationParams, False)
        self._g_i.set(self._g_i.Phases[PhaseNo].Deform.MaxSteps, MaxStep)                    # Set maximum number of steps
        self._g_i.set(self._g_i.Phases[PhaseNo].Deform.MaxUnloadingSteps, MaxUnloadStep)     # Set maximum unloading steps
        self._g_i.set(self._g_i.Phases[PhaseNo].Deform.MaxIterations, MaxIter)               # Set maximum number of iterations
        self._g_i.set(self._g_i.Phases[PhaseNo].Deform.DesiredMinIterations, DesMinIter)
        self._g_i.set(self._g_i.Phases[PhaseNo].Deform.DesiredMaxIterations, DesMaxIter)
        self._g_i.set(self._g_i.Phases[PhaseNo].Deform.UseLineSearch, LineSearch)
        self._g_i.set(self._g_i.Phases[PhaseNo].Deform.UseGradualError, GradualError)
        self.logger.info("Numerical Control Parameters Adjusted for [Phase_"+str(PhaseNo)+"]")
        return

    def allshouldcalc(self):
        '''
        Sets all phases to be calculated.
        '''
        self._g_i.gotostages()
        for phase in self.g_i.Phases:
            phase.ShouldCalculate = True
        return

    def runcalc(self):
        '''
        Runs Calculate.
        '''
        self._g_i.gotostages()
        t0 = time.time()
        self._g_i.calculate()
        t1 = time.time()
        self.logger.info("Calculation Runtime (mins): "+str(round((t1 - t0)/60, 2)))
        return

#================================================================================================================================================================
#   OUPUT FUNCTIONS
#================================================================================================================================================================

    def get_anchor_force(self, phase):
        '''
        This function get the anchor force in a certain phase
        Param: 
            phase - string of the phase name
        Return: 
            Pandas DataFrame containing information of anchor force 
        '''
        phase = getattr(self._g_o, phase)
        F = np.array(self.g_o.getresults(phase,
                                         self.g_o.ResultTypes.NodeToNodeAnchor.AnchorForce2D, 'node'))
        Fmax = np.array(self.g_o.getresults(phase,
                                            self.g_o.ResultTypes.NodeToNodeAnchor.AnchorForceMax2D, 'node'))
        x = np.array(self.g_o.getresults(
            phase, self.g_o.ResultTypes.NodeToNodeAnchor.X, 'node'))
        y = np.array(self.g_o.getresults(
            phase, self.g_o.ResultTypes.NodeToNodeAnchor.Y, 'node'))
        df = pd.DataFrame(dict(x=[], y=[], F=[], Fmax=[]))
        df.x = x
        df.y = y
        df.F = F
        df.Fmax = Fmax
        # put the two end points at the same row
        df_start = df.iloc[0:-1:2, :]
        df_end = df.iloc[1:-1:2, :]
        ix = 0
        df_anchor = pd.DataFrame(
            dict(xa=[], ya=[], xb=[], yb=[], F=[], Fmax=[]))
        for xa, ya, xb, yb, fa, fb, fmax in zip(df_start.x, df_start.y, df_end.x, df_end.y, df_start.F, df_end.F, df_start.Fmax):
            #import pdb; pdb.set_trace()
            # we always put the left point as xa
            if xa > xb:
                xa, xb = xb, xa
                ya, yb = yb, ya
            # we want make sure the two points form the same anchor by checking the force.
            assert(abs(fa-fb) < 1e-6)
            df_anchor.loc[ix] = [xa, ya, xb, yb, fa, fmax]
            ix += 1
        return df_anchor.sort_values(by='ya', ascending=False)

    #----Private Method-----------------------------#

    def _bh_read_data_excel(self, filename="Arup_PP_Borehole_Input_rev00.xlsm",
                            sheetname="PP_BHData_SFormat"):
        '''
        Reads in the data from excel and saves as a global copy of data
        Param:
            filename:  name of the excel file
            sheetname: name of worksheet that contains the BH information
        '''
        df_BH_Data = pd.read_excel(filename, sheet_name=sheetname)
        # Column named 'BH_name' as the index of rows
        df_BH_Data.set_index('BH_name', inplace=True)
        df_BH_Data1 = df_BH_Data.drop(df_BH_Data.columns[df_BH_Data.columns.str.contains('Unnamed',
                                                                                         case=False)], axis=1)
        # Drops rows with MaterialName equal to 0, i.e. unused rows
        self._dfg_BH_Data = df_BH_Data1[df_BH_Data1.MaterialName != 0]
        return self._dfg_BH_Data

    #--------Properties--------------------------------------------------

    @property
    def g_i(self):
        return self._g_i

    @property
    def s_i(self):
        return self._s_i

    @property
    def g_o(self):
        return self._g_o
