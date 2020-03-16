from _collections import deque
from plot import create_plot
import numpy as np
from country import CountryCreator


def main(data):
    countries_arr = CountryCreator.initialization()

    healthy = 7000000000
    days = int(data)

    infectivity = 0.0000000001
    mortality = 0.1
    recovery = 1 - mortality
    disease_duration = 14

    incubation_deque = deque()
    for i in range(14):
        incubation_deque.append(0)

    deaths_deque = deque()
    for i in range(14):
        deaths_deque.append(0)

    result = {
        "confirmed": 10,
        "deaths": 0,
        "recovered": 0,
        "plot": "0"
    }

    confirmed = []
    deaths = []
    recovered = []

    for i in range(days):
        new_confirmed = int(healthy * infectivity * result["confirmed"])
        # print(result["confirmed"])
        result["confirmed"] += new_confirmed
        healthy -= new_confirmed

        new_deaths = int(result["confirmed"] * mortality / disease_duration)
        result["deaths"] += new_deaths
        result["confirmed"] -= new_deaths

        incubation_deque.append(new_confirmed)
        deaths_deque.append(new_deaths)
        new_recovered = int(incubation_deque.popleft() - deaths_deque.popleft())
        result["recovered"] += new_recovered
        result["confirmed"] -= new_recovered

        # print("healthy: " + str(healthy) + "; confirmed: " + str(result["confirmed"]) + "; deaths: " + str(
        #     result["deaths"]) + "; recovered: " + str(result["recovered"]))

        confirmed.append(result["confirmed"])
        deaths.append(result["deaths"])
        recovered.append(result["recovered"])

    plot_data = [days, confirmed, deaths, recovered]
    result["plot"] = create_plot(plot_data)

    return result
