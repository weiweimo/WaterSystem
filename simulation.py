# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv
import dateutil
import datetime

data = pd.read_csv ("Boston rainfall.csv")
precipitations = data['Precipitation']
#ft
dates = data['Date']

roofarea=80
#inch x inch
#200
fixtures=1
building_height = 5
#m
#4
indoor_use_ratio= 1
electricity_price = 0.116
#$/kWh
water_density=1000
#kg/m3
pump_efficiency = 0.5
#dimensionless
flushing=0
#m3/day
storage = 0
#m3
capacity = 10
#m3
t=0
#date
rate=0.5
#$/gallon
tank_material= 0
#type of material
tank_size=capacity+storage

ETo=15
#inch/day
PF=7
#plant factor, dimensionless
lawnarea=5000
#square feet
#1500
efficiency=0.8
irrigation=ETo*PF*lawnarea*0.62/efficiency
#m3/day
fixture_rate=0.00025236
#m3/s=4pgm

storage_1 = []
supply_1 = []
publicsupply_cost_1 = []
tank_size_1 = []
system_base_cost_1 = []
pumping_energy_cost_1 = []

for tank_size in np.linspace(10, 100, 20):
    

    for (precipitation, date) in zip(precipitations, dates):
        inflow = precipitation * roofarea/1000
        date_parsed = dateutil.parser.parse(date)
        irrigation = 0 # baseline
        
        if date_parsed.month >= 5 and date_parsed.month <= 9 and precipitation==0:
            demand = irrigation + flushing #evapotrapiration
        else:
            demand=flushing
        capacity=tank_size-storage
        storage = min(storage+inflow, capacity)
        outflow = min(demand, storage)
        publicsupply = demand - outflow  
        storage -= outflow 
        storage_1.append(storage)
        supply_1.append(publicsupply)
        publicsupply_cost=publicsupply*rate
        publicsupply_cost_1.append(publicsupply_cost)
        #t = t+1
        pumping_energy = outflow*indoor_use_ratio*water_density*9.8*(building_height/2)/pump_efficiency/3.6e+006
        #kWh/day
        pumping_energy_cost = electricity_price * pumping_energy
        pumping_energy_cost_1.append(pumping_energy_cost)
        
        tank_size_1.append(tank_size)
        #tank_size += 0.1
    
    if tank_material== 0:
        tank_cost=358.77*(tank_size**0.5064)
    else: tank_cost=1292.1*tank_size**0.6771
    
    pump_size_hp = max(0.5,(fixture_rate*fixtures*water_density*9.8)*(building_height/2)*0.00134102/pump_efficiency)
    pump_cost = 100.71*(pump_size_hp**2+1327.7)*pump_size_hp-39.38
    installation_cost = tank_cost * 0.6
    system_base_cost = installation_cost + pump_cost + tank_cost
    system_base_cost_1.append(system_base_cost)
   # net_economic_savings = (outflow*rate)-system_base_cost-maintenance_cost-energy_cost
   # maintenance and constuction costs need PULSE
   
   
  # N = 100 # sample count
  # P = 10  # period
  # D = 5   # width of pulse
  # sig = np.arange(N) % P < D
    
plt.plot (storage_1, 'mo')
plt.show ()
plt.plot (supply_1, 'bx')
plt.show ()
plt.plot  (tank_size_1, system_base_cost_1, 'co')
plt.show ()
plt.plot (pumping_energy_cost_1, 'cx')
plt.show ()

