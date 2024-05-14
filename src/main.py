import baseprocess as bp
import json
import yaml
import src.utilities as utl
from plxscripting.easy import new_server
from src.geoplot import GEOPlot
import  plotly.graph_objects as go
from pathlib import Path
from model import *
from consolidation import consolidation_settlement, DoC_Barren_avg
import socket

def main():
    water_level=1.0
    width = 0.63
    # material_names = ['Soft_Soil','Soft_Soil_Creep']
    material_names = ['Cam_Clay','Soft_Soil','Hardening_Soil','Soft_Soil_Creep']
    material_names = ['Hardening_Soil']
    intervals = [10/2,10/4,10/10]
    thks = [10]
    # applied_loads=[20,40,80]
    seabed = -3
    #material_names = ['Soft_Soil_Creep']
    #thks = [4]
    applied_loads = [200]
    Cc = 1.2
    e0 = 2.0
    ch = 1.2 #m^2/year
    user_name = socket.gethostname()
    user_profile = utl.read_input_file('userprofile.yaml')[user_name]

    for material_name in material_names:
        for thk in thks:
            for applied_load in applied_loads:
                for interval in intervals:
                    filename = f'{material_name}-thk={thk}-width={width}-q={applied_load:.0f}kPa-{interval :.2f}'.replace('.','_')
                    print(f'processing - {filename}')
                    proj = bp.BaseProject(openplaxis=False,plaxis_path=user_profile['PLX_EXE_PATH'],password=user_profile['PLX_PASSWORD'])
                    proj.new_2Dproject(xmin_ip=0,xmax_ip=1,ymin_ip=-8,ymax_ip=0,project_title="Consolidation Analysis",usr_comment='',model_type='Axisymmetry')
                    g_i = proj.g_i
                    build_materials(proj)
                    build_model(proj,water_level=water_level,
                                width=width,
                                seabed=seabed,
                                thk=thk,
                                applied_load=applied_load,
                                material_name=material_name,interval=interval,c_h=ch)
                    build_stages(proj,step_size=10,n_step=5)
                    output_port = g_i.selectmeshpoints()
                    s_o, g_o = new_server('localhost', output_port, password=proj.password)
                    proj._g_o = g_o
                    proj._s_o = s_o
                    g_o.addcurvepoint('node',(width/2, seabed),(0,1))
                    g_o.update()
                    g_i.calculate()
                    proj.savecopy(user_profile['PLX_OUTPUT_PATH'],filename,suffix='.p2dx')
                    output_port = g_i.view(g_i.Phases[-1])
                    df = post_process(proj,filename)
                    # settlement_infinity = consolidation_settlement(thk,applied_load,gamma=6,Cc=Cc, e0=e0)
                    # df['Barron'] = DoC_Barren_avg(c_h =0.869, t = df.time/365, d=0.064, D_e=1.133)*settlement_infinity
                    df.to_json('output/'+filename+'.json')

    #do the post process
    # fig = GEOPlot.get_figure()
    # output_path = Path('output')
    # for file in output_path.glob('*.json'):
    #     with open(file) as fin:
    #         data = json.load(fin)
    #         df = pd.DataFrame(data)
    #     fig.add_trace(go.Scatter(x=df.time, y=df.y,name=file.stem))
    #     fig.add_trace(go.Scatter(x=df.time, y=df.Barron, name=file.stem+'(Barron)'))
    # fig.update_xaxes(type='log',title='Time(days)')
    # fig.update_yaxes(range=[df.y.max()*1.1, 0],title = 'Settlement(m)')
    # fig.update_layout(width=1000,height=600,legend=dict(orientation='h'))
    # fig.write_html('output/combined.html')
                # proj.s_i.close()
if __name__ == "__main__":
    main()
