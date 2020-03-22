from _collections import deque
from plot import create_plot
import numpy as np
from country import CountryCreator
from seir import seir
import time
from scipy.special import binom, comb
from decimal import *
import math

# import matplotlib.pyplot as plt
countries_arr, countries_keys = CountryCreator.initialization()
FATALITY_RATE = 0.0087
DAYS_TO_DEATH = 17.3
DOUBLING_TIME = 6.18
INCUBATION_PERIOD = 5.5
AIR_TRANSPORT_USAGE = 0.6
ROAD_TRANSPORT_USAGE = 1 - AIR_TRANSPORT_USAGE

total_road_arrives = 0
total_air_arrives = 0
probability_arr = [0]
for _, target_country in countries_arr.items():
    probability_arr.append(target_country.arrive)
    total_air_arrives += probability_arr[-1]
probability_arr = list(map(lambda x: x / total_air_arrives, probability_arr))
for prob_i in range(1, len(probability_arr)):
    probability_arr[prob_i] = probability_arr[prob_i] + probability_arr[prob_i - 1]


time0 = time.time()
countries_arr['CHN'].true_cases = 1

total_cases_arr = []
total_deaths_arr = []
total_recovered_arr = []

result_arr = []


def infec(code):
    target = countries_arr[code]
    road_dep = countries_arr[code].departure * ROAD_TRANSPORT_USAGE
    air_dep = countries_arr[code].departure * AIR_TRANSPORT_USAGE
    pop = countries_arr[code].population
    infec_people = countries_arr[code].true_cases + countries_arr[code].inc_cases
    infec_prob = infec_people / pop


    for _ in range(int(road_dep)):
        if np.random.sample() < infec_prob:
            target_prob = np.random.sample()

            for prob_i in range(1, len(target.borders_prob)):
                if target.borders_prob[prob_i - 1] < target_prob < target.borders_prob[prob_i]:
                    if (countries_arr[countries_arr[code].borders[prob_i - 1]]).true_cases == 0:
                        print(countries_arr[countries_arr[code].borders[prob_i - 1]].name + " INFECTED")
                    countries_arr[countries_arr[code].borders[prob_i - 1]].true_cases += 1
                    countries_arr[code].true_cases -= 1
                    break


    for _ in range(int(air_dep)):
        if np.random.sample() < infec_prob:
            target_prob = np.random.sample()
            for prob_i in range(1, len(probability_arr)-1):
                if probability_arr[prob_i - 1] < target_prob < probability_arr[prob_i]:
                    if(countries_arr[countries_keys[prob_i]]).true_cases == 0:
                        print(countries_arr[countries_keys[prob_i]].name + " INFECTED")
                    countries_arr[countries_keys[prob_i]].true_cases += 1
                    countries_arr[code].true_cases -= 1

                    break

    # while road_dep % 10 == 0 and pop % 10 == 0 and infec_people
    # prob_arr, probability = infec_probability(countries_arr[code].departure * ROAD_TRANSPORT_USAGE, countries_arr[code].population, countries_arr[code].inc_cases + countries_arr[code].true_cases)


def main(data):






    total_cases = 0
    total_deaths = 0
    total_recovered = 0
    for day in range(1, int(data)+1):
        print("DAY " + str(day))
        day_deaths = 0
        day_cases = 0
        day_recovered = 0
        for code, country in countries_arr.items():
            if code == 'CHN':
                print(country.deaths)

            if country.true_cases > 0 or country.inc_cases > 0:

                country.deaths, country.inc_cases, country.true_cases, country.recovered = seir(
                    N=float(country.population) - float(country.deaths), alpha=1 / INCUBATION_PERIOD, beta=0.4,
                    gamma=0.02,
                    mu=0.00001,
                    E0=country.inc_cases, I0=country.true_cases, R0=country.recovered)
                country.true_cases_arr.append(country.true_cases)
                country.deaths_arr.append(country.deaths)
                country.inc_cases_arr.append(country.inc_cases)
                country.recovered_arr.append(country.recovered)

                infec(code)




            else:
                country.true_cases_arr.append(0)
                country.deaths_arr.append(0)
                country.inc_cases_arr.append(0)
                country.recovered_arr.append(0)

            day_cases += country.true_cases
            day_deaths += country.deaths

            day_recovered += country.recovered

        total_cases_arr.append(day_cases)
        total_deaths_arr.append(day_deaths)
        total_recovered_arr.append(day_recovered)
        total_cases += total_cases_arr[-1]
        total_deaths += total_deaths_arr[-1]
        total_recovered += total_recovered_arr[-1]

        print(countries_arr["POL"].true_cases)
        print(countries_arr["POL"].deaths)
        print(countries_arr["POL"].recovered)
            # fig = plt.figure(facecolor='w')
            # ax = fig.add_subplot(111, axisbelow=True)
            # tlin = np.linspace(0, 250, 251)
            # S = np.array(S)
            # E = np.array(E)
            # I = np.array(I)
            # R = np.array(R)
            # ax.plot(tlin, S / 1000000000, 'b', alpha=0.5, lw=2, label='Susceptible')
            # ax.plot(tlin, E / 1000000000, 'orange', alpha=0.5, lw=2, label='Susceptible')
            # ax.plot(tlin, I / 1000000000, 'r', alpha=0.5, lw=2, label='Infected')
            # ax.plot(tlin, R / 1000000000, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
            # ax.set_xlabel('Time /days')
            # ax.set_ylabel('Number (1000s)')
            # ax.set_ylim(0, 1.2)
            # ax.yaxis.set_tick_params(length=0)
            # ax.xaxis.set_tick_params(length=0)
            # ax.grid(b=True, which='major', c='w', lw=2, ls='-')
            # legend = ax.legend()
            # legend.get_frame().set_alpha(0.5)
            # for spine in ('top', 'right', 'bottom', 'left'):
            #     ax.spines[spine].set_visible(False)
            # plt.show()

    # healthy = 7000000000
        days = day
    #
    # infectivity = 0.0000000001
    # mortality = 0.1
    # recovery = 1 - mortality
    # disease_duration = 14
    #
    # incubation_deque = deque()
    # for i in range(14):
    #     incubation_deque.append(0)
    #
    # deaths_deque = deque()
    # for i in range(14):
    #     deaths_deque.append(0)

        result = {
            "confirmed": int(total_cases),
            "deaths": int(total_deaths),
            "recovered": int(total_recovered),
            "plot": "0"
        }

    # confirmed = []
    # deaths = []
    # recovered = []
    #
    # for i in range(days):
    #     new_confirmed = int(healthy * infectivity * result["confirmed"])
    #     # print(result["confirmed"])
    #     result["confirmed"] += new_confirmed
    #     healthy -= new_confirmed
    #
    #     new_deaths = int(result["confirmed"] * mortality / disease_duration)
    #     result["deaths"] += new_deaths
    #     result["confirmed"] -= new_deaths
    #
    #     incubation_deque.append(new_confirmed)
    #     deaths_deque.append(new_deaths)
    #     new_recovered = int(incubation_deque.popleft() - deaths_deque.popleft())
    #     result["recovered"] += new_recovered
    #     result["confirmed"] -= new_recovered
    #
    #     # print("healthy: " + str(healthy) + "; confirmed: " + str(result["confirmed"]) + "; deaths: " + str(
    #     #     result["deaths"]) + "; recovered: " + str(result["recovered"]))
    #
    #     confirmed.append(result["confirmed"])
    #     deaths.append(result["deaths"])
    #     recovered.append(result["recovered"])

        plot_data = [days, total_cases_arr, total_deaths_arr, total_recovered_arr]
        result["plot"] = create_plot(plot_data)

        print(time.time()-time0)
        yield result



def connect(get):
    if "init" in get:
        days = get.split()[1]
        print(days)
        data = main(days)
        result_arr.append(data)

    print(result_arr)
    return next(result_arr[0])


#
# tmp = main(10)
# for i in range(10):
#     print(next(tmp))