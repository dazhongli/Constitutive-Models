# Import Python libraries
import csv
import collections
import enum
import imp
import logging
import math
import matplotlib.pyplot as plt
import os
import re
import socket
import subprocess
import time
import yaml
import numpy as np
import pandas as pd
# import xlwing as xw
try:
    import geopandas as gpd
    from shapely.geometry import Point, LineString, Polygon
except ImportError:
    print('geopandas not installed!')
from pathlib import Path
from plxscripting.plx_scripting_exceptions import PlxScriptingError


__version__ = 1.0
__author__ = 'Ove Arup & Partners Hong Kong Ltd. - Dazhong Li & Victor Shea'


class OutputBase:
    '''
    Class that provides a way to quickly set_up a project for base cases
    '''

    def __init__(self, host='localhost', openplaxis=False, plaxis_visible=True,
                 loggername=__name__):
        # Get user profile
        # user_profile    = self.read_user_profile()
        # plaxis_exe_path = user_profile['plaxis_exe_path']
        # plaxis_path     = user_profile['plaxis_path']
        # found_module    = imp.find_module('plxscripting', [plaxis_path])
        # imp.load_module('plxscripting', *found_module)
        from plxscripting.easy import new_server
        self._localhost = host
        self._new_server = new_server
        self.logger = self.logger(loggername)
        if not openplaxis:
            self._s_i, self._g_i = self._new_server(host, 10000)
            self._s_o, self._g_o = self._new_server(host, 10001)
            self.logger.info('Plaxis connection established...')
        else:
            self.logger.info('Launching Plaxis, it may takes a while...')
            args = [os.path.join(plaxis_exe_path, "Plaxis2DXInput.exe"),
                    "--AppserverPort={}".format(10000)]
            self._input_process = subprocess.Popen(args)
            self._s_i, self._g_i = self._new_server(host, 10000)
        self._s_i, self._g_i = self._new_server(host, 10000)
        self._s_o, self._g_o = self._new_server(host, 10001)
        self._model_geometry = {}
        self._model_phases = pd.DataFrame(dict(name=[], ID=[], plxobj=[]))
        self.plx_file_path = ''
        # Define a namedtuple for solvertype
        SolverType = collections.namedtuple('SolverType','Picos, Pardiso, Classic')
        self.solver_type = SolverType(Picos  = 'Picos (multicore iterative)',
                                      Pardiso = 'Pardiso (multicore direct)',
                                      Classic = 'Classic (single core iterative)' )

#================================================================================================================================================================
#   PROJECT FILE FUNCTIONS
#================================================================================================================================================================

    def joinfileloc(self, dirname, filename, suffix):
        '''
        Joins directory name and filename to create file location
        Param:
            dirname:  directory where file is stored, e.g r'C:\PlaxisFiles'
            filename: name of plaxis file in text quotations, e.g. "Testing123"
            suffix:   suffix of plaxis file, i.e. ".p3D" or ".p2dx", and the dot should be included
        Return:
            fileloc
        '''
        basename   = str(filename)
        pathformat = Path(dirname, basename).with_suffix(suffix)
        fileloc    = str(pathformat)
        return fileloc
    
    def restore_o(self, dirname, filename, suffix):
        '''
        Opens a Plaxis file in Plaxis Output
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
        self._s_o.open(fileloc)
        self.logger.info("Plaxis file opened: " + fileloc)
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
#   OUPUT FUNCTIONS
#================================================================================================================================================================

# ANCHOR OUTPUTS

    def get_n2nanchor_forces(self, phases):
        if isinstance(phases, list):
            dict_n2n = {}
            for ix, phase in enumerate(phases, start=0): 
                dict_n2n[ix] = pd.DataFrame()
                dict_n2n[ix] = self._get_n2nanchor_forces_one_phase(phase)
            return self._sort_anchor_force_by_phases(dict_n2n)
        else:
            return self._get_n2nanchor_forces_one_phase(phases)

    def get_material_df(self, phase) -> pd.DataFrame:
        '''
        Returns a dataframe of materials used in a particular phase specified by the 'phase'
        Param: 
            phase - name of the phase
        '''
        g_o = self.g_o
        pass

    def plot_n2nanchor_forces(self, dict_n2n):
        '''
        Plots anchor forces in dictionary as a Matlab plot and saves as .pdf
        Param: 
            dict_n2n: dictionary of anchor forces
        Return: 
            .pdf file of anchor force vs. phase ID
        '''
        # Creates a Matlab Plot
        fig_1, ax_1 = plt.subplots(1,1) # This is the overall Figure and the Axes object
        # Plotting the data...
        for ia in dict_n2n:
        #     print(ia)
            seriesname = "Anchor at Elevation: "+str(dict_n2n[ia].iloc[0,1])+"m"
            ax_1.plot(dict_n2n[ia].index, dict_n2n[ia]["F"], color = 'green', linewidth = 2, linestyle = "-", marker = "^",
                    label = seriesname)
        plt.xticks(rotation=90, verticalalignment='top')
        plt.gca().invert_yaxis()
        # Add labels
        ax_1.set_xlabel("Phase")
        ax_1.set_ylabel("Anchor Axial Force [kN]\n (-ve means compression)")
        ax_1.set_title("Plot of Development of Anchor Axial Force")
        # Add legend
        ax_1.legend()
        fig_1.show()    
        plot_name   = "N2N_Anchor_Results"
        plot_suffix = ".pdf"
        plt.savefig(plot_name + plot_suffix, bbox_inches="tight", pad_inches=1)
        return

# -------Private functions ---------------------------------------
    def _get_n2nanchor_forces_one_phase(self, phase):
        '''
        Gets the anchor forces in a certain phase.
        Param: 
            phase: phase name, e.g. g_o.Phases[-1]
        Return: 
            Pandas dataframe containing information of anchor forces
        '''
        anchor_name = np.array(self.g_o.getresults(
                                phase, self.g_o.ResultTypes.NodeToNodeAnchor.MaterialID, 'node'))
        F    = np.array(self.g_o.getresults(
                        phase, self.g_o.ResultTypes.NodeToNodeAnchor.AnchorForce2D, 'node'))
        Fmin = np.array(self.g_o.getresults(
                        phase, self.g_o.ResultTypes.NodeToNodeAnchor.AnchorForceMin2D, 'node'))
        Fmax = np.array(self.g_o.getresults(
                        phase, self.g_o.ResultTypes.NodeToNodeAnchor.AnchorForceMax2D, 'node'))
        x    = np.array(self.g_o.getresults(
                        phase, self.g_o.ResultTypes.NodeToNodeAnchor.X, 'node'))
        y    = np.array(self.g_o.getresults(
                        phase, self.g_o.ResultTypes.NodeToNodeAnchor.Y, 'node'))
        df   = pd.DataFrame(dict(anchor_name=[], x=[], y=[], F=[], Fmin=[], Fmax=[]))
        df.anchor_name = anchor_name
        df.x = x ; df.y = y
        df.F = F; df.Fmin = Fmin; df.Fmax = Fmax
        # print(df)
        # Put the two end points at the same row
        df_start = df.iloc[0::2, :]
        df_end   = df.iloc[1::2, :]
        ix = 0
        # print(df_start)
        # print(df_end)
        df_anchor_o = pd.DataFrame(dict(anchor_name=[], xa=[], ya=[], xb=[], yb=[], F=[], Fmin=[], Fmax=[]))
        for anchor_name, xa, ya, xb, yb, fa, fb, fmin, fmax in zip(df_start.anchor_name, df_start.x, df_start.y, 
                        df_end.x, df_end.y, df_start.F, df_end.F, df_start.Fmin, df_start.Fmax):
            # We always put the left point as xa
            if xa > xb:
                xa, xb = xb, xa
                ya, yb = yb, ya
            # We want make sure the two points form the same anchor by checking the force.
            assert(abs(fa-fb) < 1e-6)
            df_anchor_o.loc[ix] = [anchor_name, xa, ya, xb, yb, fa, fmin, fmax]
            ix += 1
        df_anchor_o.sort_values(by='ya', ascending=False)
        df_anchor_o.set_index("anchor_name", inplace = True)
        return df_anchor_o

    def _sort_anchor_force_by_phases(self, dict_n2n: dict) -> pd.DataFrame: 
        '''
        Groups the anchor forces by anchor name
        Param:
            dict_n2n: a dictionary holding the force information in a format {phase_ID: df_forces}
        Return: 
            anchor_results in a format {anchor_id: df_forces}
        '''
        anchor_results = {}
        for key in dict_n2n: #looping over phases
            anchor_result = dict_n2n[key]
        #     import pdb; pdb.set_trace()
            for index, row in anchor_result.iterrows(): #loop over anchors
                data = row.to_frame().transpose()
                data['Phase'] = key
                data.set_index('Phase', inplace=True)
                if index in anchor_results.keys():
                    anchor_results[index] = anchor_results[index].append(data)
                else:
                    anchor_results[index] = data
        return anchor_results

#================================================================================================================================================================
# DISPLACEMENT OUTPUTS
#================================================================================================================================================================

    def get_displ_one_phase(self, xmin, xmax, ycut, phase, cut_name):
        '''
        Gets the displacement along a horizontal cut section in a certain phase
        Param:
            xmin:     leftmost extent of cut section
            xmax:     rightmost extent of cut section
            ycut:     elevation (y-coordinate) of cut section
            phase:    phase name, e.g. g_o.Phases[-1]
            cut_name: name of cut section
        Return: 
            Pandas dataframe containing displacement information
        '''
        # Extract displacement info at nodes as arrays
        soilX  = np.array(self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.X, 'node'))
        soilY  = np.array(self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.Y, 'node'))
        soilUy = np.array(self.g_o.getresults(phase, self.g_o.ResultTypes.Soil.Uy, 'node'))
        # Define column headers and set-up dataframe
        columns = ['x', 'y', 'Uy']
        df = pd.DataFrame(columns=columns)
        for i, (x, y, Uy) in enumerate(zip(soilX, soilY, soilUy)):
            if xmin < x < xmax: 
                if abs(y - ycut) < 1E-6: 
                    df.loc[i,'x']  = x
                    df.loc[i,'y']  = y
                    df.loc[i,'Uy'] = Uy*1000  # Convert settlement into mm
        df_settle_o = df.sort_values(by='x', ascending=True)
        self.logger.info("Settlement Data Extracted.")
        return df_settle_o
    
    def plot_displ_hsect(self, df):
        '''
        Plots anchor forces in dictionary as a Matlab plot and saves as .pdf
        Param: 
            df: dataframe containing displacement information
        Return: 
            .pdf file of settlement along a horizontal cut section
        '''
        # Creates a Matlab Plot
        fig_1, ax_1 = plt.subplots(1,1) # This is the overall Figure and the Axes object
        # Plotting the data...
        seriesname = "Settlement along section: "
        ax_1.plot(df["x"], df["Uy"], color = 'green', linewidth = 2, linestyle = "-", marker = "^",
                label = seriesname)
        plt.xticks(rotation=90, verticalalignment='top')
        # Add labels
        ax_1.set_xlabel("X-Coordinate [m]")
        ax_1.set_ylabel("Settlement [m]\n (-ve means settlement)")
        ax_1.set_title("Plot of Settlement along a Horizontal Cut Section")
        # Add legend
        ax_1.legend()
        fig_1.show()    
        plot_name   = "Settlement_Results"
        plot_suffix = ".pdf"
        plt.savefig(plot_name + plot_suffix, bbox_inches="tight", pad_inches=1)
        return

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

    @property
    def s_o(self):
        return self._s_o

