import numpy as np
import pynetlogo
import pandas as pd
import random
import scipy.stats as stats
import pickle

# Initialize PyNetLogo
# netlogo = pynetlogo.NetLogoLink(netlogo_home='E:/netlogo/')
netlogo = pynetlogo.NetLogoLink(netlogo_home='/afs/inf.ed.ac.uk/user/s19/s1911520/Desktop/NetLogo-6.4.0-64')

# Load the NetLogo model
netlogo.load_model('moss_model.nlogo')

netlogo.command('setup')



oil_price = 115
solid_price = 79
electricity_price = 100
hassel_factor = 0.1

def break_down(age):
    if age < 15:
        return False  # Assuming no breakdown probability before 15 years
    elif age > 20:
        return True  # Assuming certain breakdown after 20 years

    # Define probabilities at 15 and 20 years
    prob_at_15 = 0.1  # 10% probability at 15 years
    prob_at_20 = 1.0  # 100% probability at 20 years

    # Calculate the rate of increase per year
    rate_of_increase = (prob_at_20 - prob_at_15) / (20 - 15)

    # Calculate the probability for the given age
    breakdown_probability = prob_at_15 + (age - 15) * rate_of_increase

    # Generate a random number and compare with the breakdown probability
    return random.random() < breakdown_probability


def TCP_calculator(UIC,name):
    DC = random.uniform(500,2000)
    if name == 'oil':
        return UIC + oil_price*36 + DC
    elif name == 'solid':
        return UIC + solid_price*36 + DC
    elif name == 'electric':
        return UIC + electricity_price*36 + DC
    # Introduce 75% loan to heat pumps
    elif name == "GSHP":
        return 0.25*UIC + electricity_price * 36 + DC
    elif name == "ASHP":
        return 0.25*UIC + electricity_price * 36 + DC
    else:
        return

def get_available_systems_with_TPC(heating_system_type, heat_pumps_available, heating_budget, solid_prices, oil_prices, ASHP_price,
                          electic_boiler_price, GSHP_price, innovation=False, timestep=0):
    available_list = {}
    budget = heating_budget * 10
    #Oil ban at step 96
    if timestep >= 96:
        if budget >= electic_boiler_price:
            available_list['electric'] = TCP_calculator(electic_boiler_price,'electric')
        if budget >= ASHP_price and heat_pumps_available and innovation:
            available_list['ASHP'] = TCP_calculator(ASHP_price, 'ASHP')
        if budget >= GSHP_price and heat_pumps_available and innovation:
            available_list['GSHP'] = TCP_calculator(GSHP_price, 'GSHP')
    else:
        if budget >= oil_prices:
            available_list["oil"] = TCP_calculator(oil_prices,'oil')
        if budget >= solid_prices:
            available_list['solid'] = TCP_calculator(solid_price,'solid')
        if budget >= electic_boiler_price:
            available_list['electric'] = TCP_calculator(electic_boiler_price,'electric')
        if budget >= ASHP_price and heat_pumps_available and innovation:
            available_list['ASHP'] = TCP_calculator(ASHP_price, 'ASHP')
        if budget >= GSHP_price and heat_pumps_available and innovation:
            available_list['GSHP'] = TCP_calculator(GSHP_price, 'GSHP')
    # if heating_system_type in available_list:
    #     available_list.remove(heating_system_type)
    return available_list

def select_heating_system(system_costs, heating_budget, hassle_factors):
    probabilities = {}
    total_probability = 0

    # Calculate probabilities for each system
    for system, TPC in system_costs.items():
        if not(system == "GSHP" or system == "ASHP"):
            hassle_factors = 0
        if (system == "solid"):
            hassle_factors = 1
        probability = (1 - hassle_factors) * np.exp(-TPC / heating_budget)
        probabilities[system] = probability
        total_probability += probability

    # Normalize probabilities
    normalized_probabilities = {system: prob / total_probability for system, prob in probabilities.items()}

    # Random selection based on normalized probabilities
    systems, probs = zip(*normalized_probabilities.items())
    selected_system = np.random.choice(systems, p=probs)

    return selected_system

def renovation(i):
    # if i % 12 == 0:
    #     x = random.uniform(0, 10)
    #     if x <= 1:
    #         return True
    # return False
    return random.random() < 1/120


def insulation():
    random_float = random.uniform(0, 1)

    # Check if the random float is less than or equal to 0.18
    return random_float <= 0.18


def updata_heating_system():
    random_float = random.uniform(0, 1)

    # Check if the random float is less than or equal to 0.18
    return random_float <= 0.33


heating_system_type_start = list(netlogo.report("map [s -> [heating-system-type] of s] sort households"))
ashp_start = heating_system_type_start.count("ASHP")
gshp_start = heating_system_type_start.count("GSHP")
oil_start = heating_system_type_start.count('oil')
solid_start = heating_system_type_start.count('solid')
electric_start = heating_system_type_start.count('electric')
if __name__ == '__main__':
    results = []
    for i in range(1, 240):
        solid_heater_prices = netlogo.report('solid-heater-price')
        oil_boiler_prices = netlogo.report('oil-boiler-price')
        electic_boiler_price = netlogo.report("electric-boiler-price")
        ASHP_price = netlogo.report('ASHP')
        GSHP_price = netlogo.report('GSHP')
        who = netlogo.report("map [s -> [who] of s] sort households")
        heating_system_type = netlogo.report("map [s -> [heating-system-type] of s] sort households")
        heating_system_age = netlogo.report("map [s -> [heating-system-age] of s] sort households")
        heating_budget = netlogo.report("map [s -> [heating-budget] of s] sort households")
        heat_pumps_available = netlogo.report("map [s -> [heat-pumpsuitability] of s] sort households")
        color = netlogo.report("map [s -> [color] of s] sort households")
        data = {
            'who': who,
            'heating-system-type': heating_system_type,
            'heating-system-age': heating_system_age,
            'heating-budget': heating_budget,
            'heat-pumpsuitability': heat_pumps_available,
            'color': color
        }
        df = pd.DataFrame(data)
        for index, row in df.iterrows():
            df.at[index, 'heating-system-age'] += 1 / 12
            heating_system_type = df.loc[index, 'heating-system-type']
            heating_budget = df.loc[index, 'heating-budget']
            heating_system_age = df.loc[index, 'heating-system-age']
            heat_pumps_available = df.loc[index, 'heat-pumpsuitability']

            if break_down(heating_system_age):
                available_systems = get_available_systems_with_TPC(heating_system_type, heat_pumps_available, heating_budget,
                                                          solid_heater_prices, oil_boiler_prices, ASHP_price, electic_boiler_price,
                                                          GSHP_price, timestep=i)
                if available_systems:
                    df.at[index, 'heating-system-type'] = select_heating_system(available_systems,heating_budget,hassel_factor)
                    df.at[index, 'heating-system-age'] = 0
            elif renovation(i):
                if insulation():
                    df.at[index, 'heat-pumpsuitability'] = True
                if updata_heating_system():
                    available_systems = get_available_systems_with_TPC(heating_system_type, heat_pumps_available, heating_budget,
                                                              solid_heater_prices, oil_boiler_prices, ASHP_price, electic_boiler_price,
                                                              GSHP_price, innovation=True, timestep=i)
                    if available_systems:
                        df.at[index, 'heating-system-type'] = select_heating_system(available_systems,heating_budget,hassel_factor)
                        df.at[index, 'heating-system-age'] = 0
            if df.loc[index, 'heating-system-type'] in ['ASHP', 'GSHP']:
                df.at[index, 'color'] = 128

        netlogo.write_NetLogo_attriblist(
            df[["who", "heating-system-type", "heating-system-age", "heating-budget", "heat-pumpsuitability", "color"]],
            "household")
        heating_system_type_in_process = list(netlogo.report("map [s -> [heating-system-type] of s] sort households"))
        ashp_end = heating_system_type_in_process.count("ASHP")
        gshp_end = heating_system_type_in_process.count("GSHP")
        oil_end = heating_system_type_in_process.count('oil')
        solid_end = heating_system_type_in_process.count('solid')
        electric_end = heating_system_type_in_process.count('electric')
        hp_end = ashp_end + gshp_end
        results.append([oil_end, solid_end, electric_end, hp_end])
        print(
            'iteratuions' + str(i) + '\noil' + str(oil_end) + '\nelectric' + str(electric_end) + '\nsolid' + str(solid_end)
            + '\nheat-pums' + str(hp_end))
    columns = ['oil', 'solid', 'electric', 'hp']

    ban_subsidy_75 = pd.DataFrame(results, columns=columns)
    with open('ban_subsidy_75.pickle', 'wb') as file:
        pickle.dump(ban_subsidy_75, file)


heating_system_type_end = list(netlogo.report("map [s -> [heating-system-type] of s] sort households"))
ashp_end = heating_system_type_end.count("ASHP")
gshp_end = heating_system_type_end.count("GSHP")
oil_end = heating_system_type_end.count('oil')
solid_end = heating_system_type_end.count('solid')
electric_end = heating_system_type_end.count('electric')
hp_start = ashp_start + gshp_start
hp_end = ashp_end + gshp_end

print('oil' + str(oil_start) + '\nelectric' + str(electric_start) + '\nsolid' + str(solid_start)
      + '\heat-pums' + str(hp_start))
print('oil' + str(oil_end) + '\nelectric' + str(electric_end) + '\nsolid' + str(solid_end)
      + '\heat-pums' + str(hp_end))
netlogo.kill_workspace()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/