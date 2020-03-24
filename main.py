from plot import create_plot
import numpy as np
from country import CountryCreator
from seir import seir

countries_arr, countries_keys = CountryCreator.initialization()
FATALITY_RATE = 0.0087
DAYS_TO_DEATH = 17.3
DOUBLING_TIME = 6.18
INCUBATION_PERIOD = 7
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

total_cases_arr = []
total_deaths_arr = []
total_recovered_arr = []
infected_countries_arr = []
data_transmitter = 0

countries_arr['CHN'].true_cases = 1
infected_countries_arr.append('CHN')


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
                        infected_countries_arr.append(countries_arr[code].borders[prob_i - 1])
                    countries_arr[countries_arr[code].borders[prob_i - 1]].true_cases += 1
                    countries_arr[code].true_cases -= 1
                    break

    for _ in range(int(air_dep)):
        if np.random.sample() < infec_prob:
            target_prob = np.random.sample()
            for prob_i in range(1, len(probability_arr) - 1):
                if probability_arr[prob_i - 1] < target_prob < probability_arr[prob_i]:
                    if (countries_arr[countries_keys[prob_i]]).true_cases == 0:
                        print(countries_arr[countries_keys[prob_i]].name + " INFECTED")
                        infected_countries_arr.append(countries_keys[prob_i])
                    countries_arr[countries_keys[prob_i]].true_cases += 1
                    countries_arr[code].true_cases -= 1

                    break


def main(data):
    for day in range(1, int(data) + 1):
        print("DAY " + str(day))
        day_deaths = 0
        day_cases = 0
        day_recovered = 0
        for code, country in countries_arr.items():
            if code == 'CHN':
                print(country.deaths)

            if country.true_cases > 0 or country.inc_cases > 0:

                country.deaths, country.inc_cases, country.true_cases, country.recovered = seir(
                    N=float(country.population) - float(country.deaths), alpha=1 / INCUBATION_PERIOD, beta=0.35,
                    gamma=0.03,
                    mu=0.01,
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
        total_cases = total_cases_arr[-1]
        total_deaths = total_deaths_arr[-1]
        total_recovered = total_recovered_arr[-1]

        print(countries_arr["POL"].true_cases)
        print(countries_arr["POL"].deaths)
        print(countries_arr["POL"].recovered)

        days = day

        infected_countries_str = ""
        for ic in infected_countries_arr:
            infected_countries_str += ic
            infected_countries_str += " "

        result = {
            "confirmed": int(total_cases),
            "deaths": int(total_deaths),
            "recovered": int(total_recovered),
            "plot": "0",
            "infected_countries_arr": infected_countries_arr
        }

        plot_data = [days, total_cases_arr, total_deaths_arr, total_recovered_arr]
        result["plot"] = create_plot(plot_data)

        yield result


def connect(get):
    global data_transmitter
    if "init" in get:
        days = get.split()[1]
        print(days)
        data_transmitter = main(days)

    print(data_transmitter)
    return next(data_transmitter)
