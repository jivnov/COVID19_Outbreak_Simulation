from plot import create_plot
import numpy as np
from country import CountryCreator
from seir import seibqhr
import time

countries_arr, countries_keys = CountryCreator.initialization()
FATALITY_RATE = 0.01
DAYS_TO_DEATH = 17.3
DOUBLING_TIME = 6.18
AIR_TRANSPORT_USAGE = 0.6
ROAD_TRANSPORT_USAGE = 1 - AIR_TRANSPORT_USAGE

INCUBATION_PERIOD = 7
INCUBATION_RATE = 1 / INCUBATION_PERIOD
QUARANTINE_DURATION = 14
QUARANTINE_RATE = 1 / QUARANTINE_DURATION

RECOVERY_RATE_INFECTED = 0.33
RECOVERY_RATE_CONFIRMED = 0.15

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

countries_arr['CHN'].infected = 1
# countries_arr['CHN'].exposed = 4000
# countries_arr['CHN'].suspected = 800
# countries_arr['CHN'].quarantined = 2132
# countries_arr['CHN'].confirmed = 494
# countries_arr['CHN'].susceptible = countries_arr['CHN'].population - 8361
# countries_arr['CHN'].contact_rate_exp_rate = 0.15
# countries_arr['CHN'].quarantined_rate_exp_rate = 0.1531
# countries_arr['CHN'].diagnose_speed_exp_rate = 0.2


infected_countries_arr.append('CHN')


def infec(code):
    target = countries_arr[code]
    road_dep = countries_arr[code].departure * ROAD_TRANSPORT_USAGE
    air_dep = countries_arr[code].departure * AIR_TRANSPORT_USAGE
    pop = countries_arr[code].population
    infec_people = countries_arr[code].infected + countries_arr[code].exposed
    infec_prob = infec_people / pop

    for _ in range(int(road_dep)):
        if np.random.sample() < infec_prob:
            target_prob = np.random.sample()

            for prob_i in range(1, len(target.borders_prob)):
                if target.borders_prob[prob_i - 1] < target_prob < target.borders_prob[prob_i]:
                    if (countries_arr[countries_arr[code].borders[prob_i - 1]]).infected == 0:
                        print(countries_arr[countries_arr[code].borders[prob_i - 1]].name + " INFECTED")
                        infected_countries_arr.append(countries_arr[code].borders[prob_i - 1])
                    countries_arr[countries_arr[code].borders[prob_i - 1]].infected += 1
                    countries_arr[code].infected -= 1

                    countries_arr[countries_arr[code].borders[prob_i - 1]].contact_rate_exp_rate = 0.01
                    countries_arr[countries_arr[code].borders[prob_i - 1]].quarantined_rate_exp_rate = 0.01
                    countries_arr[countries_arr[code].borders[prob_i - 1]].diagnose_speed_exp_rate = 0.01
                    break

    for _ in range(int(air_dep)):
        if np.random.sample() < infec_prob:
            target_prob = np.random.sample()
            for prob_i in range(1, len(probability_arr) - 1):
                if probability_arr[prob_i - 1] < target_prob < probability_arr[prob_i]:
                    if (countries_arr[countries_keys[prob_i]]).infected == 0:
                        print(countries_arr[countries_keys[prob_i]].name + " INFECTED")
                        infected_countries_arr.append(countries_keys[prob_i])
                    countries_arr[countries_keys[prob_i]].infected += 1
                    countries_arr[code].infected -= 1

                    countries_arr[countries_keys[prob_i]].contact_rate_exp_rate = 0.01
                    countries_arr[countries_keys[prob_i]].quarantined_rate_exp_rate = 0.01
                    countries_arr[countries_keys[prob_i]].diagnose_speed_exp_rate = 0.01
                    break


def main(data):
    for day in range(1, int(data) + 1):
        print("DAY " + str(day))
        day_deaths = 0
        day_cases = 0
        day_recovered = 0

        if day == 47:
            countries_arr['CHN'].contact_rate_exp_rate = 0.15
            countries_arr['CHN'].quarantined_rate_exp_rate = 0.1531
            countries_arr['CHN'].diagnose_speed_exp_rate = 0.2

        for code, country in countries_arr.items():

            if country.infected > 0 or country.exposed > 0:

                country.susceptible, country.exposed, country.infected, country.suspected, country.quarantined, \
                country.confirmed, country.recovered, country.contact_rate_0, country.quarantined_rate_exposed_0, \
                country.infected_to_confirmed_min = seibqhr(c0=country.contact_rate_0, cb=country.contact_rate_min,
                                                            r1=country.contact_rate_exp_rate,
                                                            beta=country.transmission_prob,
                                                            q0=country.quarantined_rate_exposed_0,
                                                            qm=country.quarantined_rate_exposed_max,
                                                            r2=country.quarantined_rate_exp_rate,
                                                            m=country.susceptible_to_suspected_rate,
                                                            b=country.detection_rate,
                                                            f=country.suspected_to_confirmed, sigma=INCUBATION_RATE,
                                                            lamb=QUARANTINE_RATE,
                                                            deltaI0=country.infected_to_confirmed_min,
                                                            deltaIf=country.infected_to_confirmed_max,
                                                            r3=country.diagnose_speed_exp_rate,
                                                            gammaI=RECOVERY_RATE_INFECTED,
                                                            gammaH=RECOVERY_RATE_CONFIRMED,
                                                            alpha=country.death_rate,
                                                            S0=country.susceptible, E0=country.exposed,
                                                            I0=country.infected,
                                                            B0=country.suspected, Q0=country.quarantined,
                                                            H0=country.confirmed,
                                                            R0=country.recovered)

                country.deaths = country.population - country.confirmed - country.exposed - country.infected - \
                                 country.recovered - country.quarantined - country.suspected - country.susceptible

                country.infected_arr.append(country.confirmed + country.infected + country.exposed)
                country.deaths_arr.append(country.deaths)
                country.exposed_arr.append(country.exposed)
                country.recovered_arr.append(country.recovered)

                infec(code)




            else:
                country.infected_arr.append(0)
                country.deaths_arr.append(0)
                country.exposed_arr.append(0)
                country.recovered_arr.append(0)

            day_cases = day_cases + country.confirmed + country.infected
            day_deaths += country.deaths
            day_recovered += country.recovered

        total_cases_arr.append(day_cases)
        total_deaths_arr.append(day_deaths)
        total_recovered_arr.append(day_recovered)
        total_cases = total_cases_arr[-1]
        total_deaths = total_deaths_arr[-1]
        total_recovered = total_recovered_arr[-1]

        print(countries_arr["CHN"].infected)
        print(countries_arr["CHN"].confirmed)
        print(countries_arr["CHN"].quarantined)
        print(countries_arr["CHN"].exposed)
        print(countries_arr["CHN"].suspected)
        print(countries_arr["CHN"].quarantined_rate_exposed_0)



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
