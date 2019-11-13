"""
Example script of Example_1: Infiltration of Water into a Single-Layered Soil
Profile.

The example is took from: The HYDRUS-1D Software Package for Simulating 
theOne-Dimensional Movement of Water, Heat, and Multiple Solutes in 
Variably-Saturated Media: Tutorial, by David Rassam, Jirka Simunek, 
Dirk Mallants and Martinus Th. van Genuchten.
Version 1.00, July 2018.
    
    
The simulation presents infiltration of water from surface into a 1-m deep
single-layered loam soil. The upper BC is represented as a Constant Pressure 
boundary, by assuming that the pressure head at the soil surface is 1 cm.
The bottom BC is represented with a Free drainage BC, where water drains 
from the bottom of the soil profile by gravity, as the groundwater table is 
at an unspecified point deep in the profile. 

Author: M. Vremec, University of Graz, 2019

"""

import os

import numpy as np
import pandas as pd

import pydrus as ps

ws = "example_1"
exe = os.path.join(os.getcwd(), "../../source/hydrus")

# Create the basic model
desc = "Infiltration of Water into a Single-Layered Soil Profile"

ml = ps.Model(exe_name=exe, ws_name=ws, name="model", description=desc,
              mass_units="mmol", time_unit="days", length_unit="cm")
ml.basic_info["lShort"] = False

ml.time_info["tInit"] = 0  # Initial time of the simulation [T]
ml.time_info["tMax"] = 1  # Final time of the simulation [T]
ml.time_info["MPL"] = 12
ml.time_info["dt"] = 0.001
ml.time_info["dtMin"] = 0.00001
ml.time_info["dtMax"] = 5
ml.time_info["nPrintSteps"] = 1
ml.time_info["tPrintInterval"] = 1

# Define free drainage and dirichlet BC at surface(kodtop = 1),
# initial condition is given in pressure head (lInitW = False)
ml.add_waterflow(free_drainage=True, kodtop=1, linitw=False,
                 ha=1e-006, hb=10000, maxit=10, tolth=0.001, tolh=1)

printtimes = np.linspace(start=ml.time_info["tInit"], \
                         stop=ml.time_info["tMax"], \
                         num=ml.time_info["MPL"] + 1)[1:]

m = pd.DataFrame(data=[[0.078, 0.43, 0.036, 1.56, 24.96, 0.5]],
                 columns=["thr", "ths", "Alfa", "n", "Ks", "l"])
ml.add_material(m)

# Disctretize soil column into n elements
elements = 100

# Depth of the soil column
bottom = -100

# Determine initial Pressure Head
ihead = -100

profile = ps.create_profile(bot=bottom, dx=abs(elements / bottom), h=ihead)

# Define initial Pressure Head at the surface
profile.iloc[0, 1] = 1
# Add the profile

ml.add_profile(profile)

# Add observation nodes at depth

obs = [-20, -40, -60, -80, -100]
ml.add_observations(obs)

# Write input files and run Hydrus
ml.write_input()
rs = ml.simulate()

# Plot profile information
ml.plots.profile_information()
# ml.plots.profile_information("Water Content")
# ml.plots.profile_information("Hydraulic Conductivity")
# ml.plots.profile_information("Water Flux")

# Plot water flow
ml.plots.water_flow(data="Actual Surface Flux")
ml.plots.water_flow(data="Bottom Flux")
ml.plots.water_flow(data="Volume of water in the entire flow domain")

# Plot soil hydraulic properties
ml.plots.shp(data="Water Content")