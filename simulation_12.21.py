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

data = pd.read_csv ("Boston_rainfall.csv")
precipitations = data['Precipitation']  #mm
dates = data['Date']

roofarea=100  #m^2
number_of_tenants_per_fixture= 2  # tenants
tenant_number = 6 #number of people living in the household
fixtures= tenant_number / number_of_tenants_per_fixture  #number of toilets
building_height = 10  #m
electricity_price = 0.216  #$/kWh
water_density=1000  #kg/m3
pump_efficiency = 0.5  #dimensionless
t=0  #date
rate=1.82  #$/m^3 water price from public supply
tank_material= 0  #type of material, 0 denotes plastic and 1 denotes steel
fixture_rate= 0.072 #m3/person/day rate of toilet flushing
flushing=tenant_number*fixture_rate  #m3/day daily total flushing 


ETo=0.05 #inch/day evapotranspiration in Boston
PF=1.0  #plant factor, dimensionless
lawnarea=5000 #square feet
efficiency=0.8
irrigation=ETo*PF*lawnarea*0.62*0.00378541/efficiency  #m3/day

storage_1 = []
supply_1 = []
publicsupply_cost_1 = []
tank_size_1 = []
system_base_cost_1 = []
pumping_energy_cost_1 = []
pumping_energy_cost_cum_1 = []
cost_saving_cum_1 = []
net_saving_1 = []
outflow_1 = []
demand_1 = []
outflow_cum_1 = []

for tank_size in np.linspace(0, 20, 20):

    if tank_material== 0:
        tank_cost=358.77*(tank_size**0.5064)
    else: tank_cost=1292.1*tank_size**0.6771
    
    pump_size_hp = 0.5
    #max(0.5,(fixture_rate*fixtures*water_density*9.8)*(building_height/2)*0.00134102/pump_efficiency)
   
    if pump_size_hp <= 7:
        #pump_cost = -31.2*pump_size_hp**2 + 486.33*pump_size_hp + 205.68
        pump_cost = -100.71*pump_size_hp**2 + 1327.7*pump_size_hp - 39.38 #$
    else: pump_cost = 4320
    
    installation_cost = tank_cost * 0.6 #$
    annual_maint_cost = 100  #$ annual maintenance cost
    total_maint_cost = annual_maint_cost*30 #$ total maintenance cost over 30 years of life span
    system_base_cost = installation_cost + pump_cost + tank_cost + total_maint_cost
    system_base_cost_1.append(system_base_cost)
    tank_size_1.append(tank_size) 
    pumping_energy_cost_cum = 0 #$
    cost_saving_cum = 0 #$
    outflow_cum = 0 #m3
    storage = 0  #m3 initial storage in the tank

    for (precipitation, date) in zip(precipitations, dates):
        inflow = precipitation * roofarea/1000 #m^3/day 
        date_parsed = dateutil.parser.parse(date)
        
        if date_parsed.month >= 5 and date_parsed.month <= 9 and precipitation==0:
            demand = irrigation + flushing #evapotrapiration
        else:
            demand=flushing
        demand_1.append(demand)
        capacity=tank_size-storage
        storage = min(storage+inflow, tank_size)
        outflow = min(demand, storage)
        outflow_1.append(outflow)
        outflow_cum += outflow
        publicsupply = demand - outflow  
        storage -= outflow 
        storage_1.append(storage)
        supply_1.append(publicsupply)
        publicsupply_cost=publicsupply*rate
        publicsupply_cost_1.append(publicsupply_cost)
        cost_saving = outflow*rate #$
        cost_saving_cum += cost_saving #$
        if outflow > 0:
            indoor_use_ratio=flushing/outflow  #ratio of toilet flushing over total outflow
        else:
            indoor_use_ratio=0
        pumping_energy = outflow*indoor_use_ratio*water_density*9.8*(building_height/2)*.000000278/pump_efficiency  #kWh/day
        pumping_energy_cost = electricity_price * pumping_energy
        pumping_energy_cost_cum += pumping_energy_cost
        pumping_energy_cost_1.append(pumping_energy_cost)
    
    outflow_cum_1.append(outflow_cum)  #m3
    cost_saving_cum_1.append(cost_saving_cum)   #$
    pumping_energy_cost_cum_1.append(pumping_energy_cost_cum)    #$    
    net_saving = cost_saving_cum - system_base_cost - pumping_energy_cost_cum    #$
    net_saving_1.append(net_saving)
  
   
    
plt.plot (tank_size_1, cost_saving_cum_1, 'mo')
plt.show ()
plt.plot (tank_size_1, pumping_energy_cost_cum_1, 'bx')
plt.show ()
plt.plot (tank_size_1, net_saving_1, 'co')
plt.show ()
plt.plot (tank_size_1, system_base_cost_1, 'gx')
plt.show ()

