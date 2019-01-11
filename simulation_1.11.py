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

energy_conversion_factor= 3.6 #MJ/kWh
treatment_energy_intensity = 0.19 #MJ/m3
friction_loss_coefficient = 34 #m/km
foot_of_head_conversion = 2.31 
distance = 20 #(km)
plant_elevation = 93 #m
home_elevation = 20 #m
central_pump_efficiency = 0.7
distance_from_plant = 40 #km
operating_pressure = 160 #psi
maint_energy_intensity = 9.41 #MJ/$
pump_embodied_energy_intensity = 8.49 #MJ/$
tank_embodied_energy_intensity = 14.8 #MJ/$
installation_energy_intensity = 6.21 #MJ/$

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
avoided_pumping_energy_1 = []
centralized_pumping_energy_1 = []
treatment_energy_1 = []
treatment_energy_cum_1 = []
centralized_pumping_energy_cum_1 = []
avoided_pumping_energy_cum_1 = []
pumping_energy_cum_1 = []
operation_energy_1 = []
pump_manufacture_energy_1= []
tank_manufacture_energy_1 = []
installation_energy_1 = []
construction_energy_1 = []
net_embodied_energy_saving_1 = []

for tank_size in np.linspace(0, 30, 20):

    if tank_material== 0:
        tank_cost=358.77*(tank_size**0.5064)
    else: tank_cost=1292.1*tank_size**0.6771
    
    pump_size_hp = max(0.5,(fixture_rate*fixtures*water_density*9.8)*(building_height/2)/745.7/86400/pump_efficiency)
   
    if pump_size_hp <= 7:
        pump_cost = -31.2*pump_size_hp**2 + 486.33*pump_size_hp + 205.68
        #pump_cost = -100.71*pump_size_hp**2 + 1327.7*pump_size_hp - 39.38 #$
    else: pump_cost = 2100
    
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
    treatment_energy_cum = 0
    centralized_pumping_energy_cum = 0 #kwH
    avoided_pumping_energy_cum = 0
    pumping_energy_cum = 0
    total_maint_energy = total_maint_cost * maint_energy_intensity #MJ
    pump_manufacture_energy = pump_embodied_energy_intensity * pump_cost #MJ
    pump_manufacture_energy_1.append(pump_manufacture_energy) #MJ
    tank_manufacture_energy = tank_embodied_energy_intensity *tank_cost #MJ
    tank_manufacture_energy_1.append(tank_manufacture_energy) #MJ
    installation_energy = installation_energy_intensity * installation_cost #MJ
    installation_energy_1.append(installation_energy) #MJ
    construction_energy = pump_manufacture_energy + tank_manufacture_energy + installation_energy #MJ
    construction_energy_1.append(construction_energy) #MJ

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
        treatment_energy = treatment_energy_intensity * outflow #(MJ/Day)
        treatment_energy_cum += treatment_energy
        elevation_change = plant_elevation - home_elevation #m
        operating_head = foot_of_head_conversion * operating_pressure * 0.3048 #m
        friction_loss = distance_from_plant * friction_loss_coefficient #(m)
        total_head = elevation_change + friction_loss + operating_head #(m)
        centralized_pumping_energy = outflow * water_density * 9.8 * total_head / central_pump_efficiency / 3600000 #(kWh)
        centralized_pumping_energy_cum += centralized_pumping_energy #kWh
        avoided_pumping_energy = centralized_pumping_energy * energy_conversion_factor + treatment_energy #MJ
        avoided_pumping_energy_cum += avoided_pumping_energy #MJ
        
        if outflow > 0:
            indoor_use_ratio=flushing/outflow  #ratio of toilet flushing over total outflow
        else:
            indoor_use_ratio=0
        pumping_energy = outflow*indoor_use_ratio*water_density*9.8*(building_height/2)*.000000278/pump_efficiency  #kWh/day
        pumping_energy_cost = electricity_price * pumping_energy #$
        pumping_energy_cost_cum += pumping_energy_cost #$
        pumping_energy_cost_1.append(pumping_energy_cost) #$
        pumping_energy_cum += pumping_energy #kWh
        pumping_energy_cum_1.append(pumping_energy_cost_cum) #kWh
        operation_energy = pumping_energy_cum * energy_conversion_factor + total_maint_energy #MJ
        net_embodied_energy_saving = avoided_pumping_energy_cum - construction_energy - operation_energy #MJ
    
    outflow_cum_1.append(outflow_cum)  #m3
    cost_saving_cum_1.append(cost_saving_cum)   #$
    pumping_energy_cost_cum_1.append(pumping_energy_cost_cum)    #$    
    net_saving = cost_saving_cum - system_base_cost - pumping_energy_cost_cum    #$
    net_saving_1.append(net_saving) #$
    treatment_energy_1.append(treatment_energy)   #MJ
    centralized_pumping_energy_1.append(centralized_pumping_energy) #MJ
    avoided_pumping_energy_1.append(avoided_pumping_energy) #MJ
    treatment_energy_cum_1.append(treatment_energy_cum) #MJ
    centralized_pumping_energy_cum_1.append(centralized_pumping_energy_cum) #kWh
    avoided_pumping_energy_cum_1.append(avoided_pumping_energy_cum) #MJ
    operation_energy_1.append(operation_energy) #MJ
    net_embodied_energy_saving_1.append(net_embodied_energy_saving ) #MJ
    
plt.plot (tank_size_1, cost_saving_cum_1, 'mo')
plt.show ()
plt.plot (tank_size_1, net_saving_1 , 'c-')
plt.show ()
plt.plot (tank_size_1, net_embodied_energy_saving_1 , 'r-')
plt.show ()
plt.plot (tank_size_1, pump_manufacture_energy_1, 'c2') #pump_manufacture_energy has 0 slope because the pump size is always 0.5
plt.show ()
plt.plot (tank_size_1, centralized_pumping_energy_cum_1, 'm2')
plt.show ()
plt.plot (tank_size_1, avoided_pumping_energy_cum_1, 'g2')
plt.show ()