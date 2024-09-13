import pydeck as pdk
import pandas as pd
import os
import geopandas as gpd
import json
import numpy as np

cwd = os.getcwd()

dataloc = os.path.join("data","SA1_2021_AUST_SHP_GDA2020","SA1_2021_AUST_GDA2020.shp")


sa1 = gpd.read_file(dataloc)
sa1popdata = pd.read_csv("data/2021_GCP_SA1_for_NSW_short-header/2021 Census GCP Statistical Area 1 for NSW/2021Census_G01_NSW_SA1.csv")




sa1 = sa1[sa1.SA4_NAME21.astype(str).str.contains('Sydney')]
sa1 = pd.merge(sa1[["SA1_CODE21","SA2_NAME21","AREASQKM21","geometry"]],sa1popdata[["Tot_P_P"]], left_index=True, right_index=True, how='left')
sa1["SA1_NAME"] = sa1.apply(lambda row: str(row["SA2_NAME21"]) + str(row["SA1_CODE21"])[-2:],axis=1)

tot_area = sum(1/np.sqrt(sa1[~pd.isnull(sa1.geometry)].AREASQKM21))
length = sa1.shape[0]
def reducegeo(case):
    tolerance = (1/np.sqrt(case.AREASQKM21))/tot_area*sa1.shape[0]*0.002
    return case.geometry.simplify(tolerance)
# sa1.geometry = sa1[~pd.isnull(sa1.geometry)].apply(reducegeo,axis=1)
# sa1.geometry = sa1.geometry.simplify(tolerance=0.001)

sa1reducedjson = json.loads(sa1.to_json())

INITIAL_VIEW_STATE = pdk.ViewState(latitude=-32.90232731500082, longitude=144.82657825047986, zoom=11, max_zoom=16, pitch=45, bearing=0)


geojson = pdk.Layer(
    "GeoJsonLayer",
    sa1reducedjson,
    opacity=0.8,
    pickable=True,
    stroked=False,
    filled=True,
    extruded=True,
    wireframe=True,
    get_elevation="properties.Tot_P_P * 20",
    get_fill_color="[255, 255, properties.AREASQKM21 * 255]",
    get_line_color=[255, 255, 255],
)
tooltip = {"html": "<b>Area:</b> {SA1_NAME} <b>Total Population:</b> {Tot_P_P} <br />"}

r = pdk.Deck(layers=[geojson], initial_view_state=INITIAL_VIEW_STATE,    tooltip=tooltip,
)

r.to_html("geojson_layer.html")


