import baseprocess as bp
import yaml
import src.utilities as utl
from plxscripting.easy import new_server
from src.geoplot import GEOPlot
import plotly.graph_objects as go
import pandas as pd
import numpy as np


def flatten_dict(dictionary):
    flattened = []
    for key, value in dictionary.items():
        if isinstance(value, dict):
            flattened.extend(flatten_dict(value))
        else:
            flattened.append(key)
            flattened.append(value)
    return flattened


def post_process(proj, filename):
    df = pd.DataFrame()
    ix = 0
    g_o = proj._g_o
    for phase in g_o.Phases:
        if phase.Name.value == 'InitialPhase':
            continue
        else:
            for step in phase.Steps:
                val = g_o.getcurveresults(
                    g_o.Curvepoints.Nodes[0], step, g_o.ResultTypes.Soil.Utot)
                df.loc[ix, 'y'] = val
                df.loc[ix, 'time'] = step.Reached.Time.value
                ix += 1
    proj._s_o.close()
    fig = GEOPlot.get_figure()
    fig.add_trace(go.Scatter(x=df.time, y=df.y*1000, line=dict(color='black')))
    fig.update_layout(width=800, height=400)
    fig.update_yaxes(range=[200, 0], title='Consolidation Settlement (mm)')
    fig.update_layout(xaxis_type='log')
    df.to_json('./output/'+filename+'.json')
    fig.write_html('./output/'+filename+'.html')
    return df


def build_materials(proj, filename='./material.yaml'):
    g_i = proj._g_i
    proj.delete_all_materials()
    x = utl.read_input_file(filename)

    for material_name in x:
        if material_name[0] == '_': # we don't handle the anchors
            continue

        # material_name = 'Mohr_Coulomb'
        m_sand = x[material_name]
        material = g_i.soilmat()
        mat = material.setproperties(*flatten_dict(m_sand))
        material.Identification = material_name
    
    # Let's also build a dummy structural element here
    m_plate = g_i.platemat()
    m_plate.setproperties('MaterialType','Elastic',
                          'EA1',1e8,
                          'EI',1e8,
                          'StructNu',0.45,
                          'Identification','dummy_plate')


def build_model(proj,
                water_level,
                width,
                seabed,
                thk,
                applied_load,c_h=1.2,interval=1.0,material_name ='Hardening_Soil'):

    mat_dicts = utl.read_input_file('material.yaml')
    g_i = proj._g_i
    g_i.gotosoil()
    proj.delete_all_bh()
    bh = g_i.borehole(0)
    bh.Head = water_level
    width = width
    seabed = seabed
    thk = thk
    applied_load = applied_load
    g_i.SoilContour.initializerectangular(0, seabed-thk, width, seabed)
    dict_soil_sample = mat_dicts[material_name].copy()
    e0 = dict_soil_sample['eInit']
    try:
        Cc = dict_soil_sample['CC']
    except: # if Camclay, CC is not defined, rather by `lambda`
        Cc = dict_soil_sample['lambda']*1.2

    gamma = dict_soil_sample['gammaSat']
    for ix, i in enumerate(np.arange(0,thk,interval)):
        print(ix, i)
        E = 2.3*(1+e0) /Cc*(i+interval/2)*(gamma-10)
        kh = 10*c_h/365/E # convert to days
        mat_name = f"HS_{i+interval/2:02.1f}m".replace('.','_')
        if ix==0:
            g_i.soillayer(-seabed + interval)
            g_i.Soillayers[0].Zones[0].Top=seabed
        else:
            g_i.soillayer(interval)
        material = g_i.soilmat()
        dict_soil_sample['PermHorizontalPrimary'] = kh
        material.setproperties(*flatten_dict(dict_soil_sample))
        material.Identification = mat_name
        g_i.Soillayers[-1].Soil.Material = material

    # ------------Loading-------------------- 
    g_i.gotostructures()
    line_load = g_i.lineload((0, seabed), (width, seabed))
    line_load[-1].q_start = applied_load
    plate = g_i.plate(line_load[-2])
    plate.Material = g_i.dummy_plate
    g_i.drain((0.0331, seabed), (0.0331, seabed-thk))
    g_i.point((width/2,seabed)) # we add a point in the middle for reference
    g_i.gotomesh()
    g_i.mesh(0.05)

    # ------------- set flow condition-----------------
    g_i.gotoflow()
    for drain in g_i.Drains:
        drain.h[g_i.InitialPhase] = 0
        g_i.activate(drain,g_i.InitialPhase)
    for gw_bc in g_i.GWFlowBaseBC:
        if (gw_bc.x_start[g_i.InitialPhase].value==width) and (gw_bc.x_end[g_i.InitialPhase].value==width):
            gw_bc.Behaviour[g_i.InitialPhase] = 'closed'
        else:
            pass
            # gw_bc.Behaviour[g_i.InitialPhase] = 'seepage'

        # g_i.activate(gw_bc,g_i.InitialPhase)
    water_level = g_i.waterlevel((-3,1),(10,1))
    g_i.setglobalwaterlevel(water_level, g_i.InitialPhase)


def build_stages(proj, step_size=3, n_step=12):
    # Construct Stages
    g_i = proj._g_i
    g_i.gotostages()
    n_stage = n_step
    for i in range(1, n_stage):
        this_phase = g_i.phase(g_i.Phases[-1])
        this_phase.Identification = 'Consolidation'
        this_phase.DeformCalcType = 'Consolidation'
        this_phase.TimeInterval = step_size**i
        this_phase.Identification = f'Consolidation at {step_size**i} days'
        g_i.activate(g_i.LineLoads,this_phase)
        g_i.activate(g_i.Drains, this_phase)
        g_i.activate(g_i.GroundwaterFlowBCs, this_phase)
        g_i.activate(g_i.Plates,this_phase)
