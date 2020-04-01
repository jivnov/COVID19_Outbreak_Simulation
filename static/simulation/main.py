from static.simulation.plot import create_plot
import numpy as np
from static.simulation.country import CountryCreator
from static.simulation.seir import seibqhr

countries_arr, countries_keys = CountryCreator.initialization()
FATALITY_RATE = 0.01

AIR_TRANSPORT_USAGE = 0.6
ROAD_TRANSPORT_USAGE = 1 - AIR_TRANSPORT_USAGE

INCUBATION_PERIOD = 7
INCUBATION_RATE = 1 / INCUBATION_PERIOD
QUARANTINE_DURATION = 14
QUARANTINE_RATE = 1 / QUARANTINE_DURATION

RECOVERY_RATE_INFECTED = 0.053  # 0.33
RECOVERY_RATE_CONFIRMED = 0.025  # 0.15

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
true_cases_arr = []
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


def infec(code, day):
    target = countries_arr[code]
    road_dep = countries_arr[code].departure * ROAD_TRANSPORT_USAGE
    air_dep = countries_arr[code].departure * AIR_TRANSPORT_USAGE
    pop = countries_arr[code].population
    infec_people = countries_arr[code].infected + countries_arr[code].exposed
    infec_prob = infec_people / pop
    oc_contact_rate_exp_rate = 0.003
    oc_quarantined_rate_exp_rate = 0.003
    oc_diagnose_speed_exp_rate = 0.02

    for _ in range(int(road_dep)):
        if np.random.sample() < infec_prob:
            target_prob = np.random.sample()

            for prob_i in range(1, len(target.borders_prob)):
                if target.borders_prob[prob_i - 1] < target_prob < target.borders_prob[prob_i]:
                    if countries_arr[code].borders[prob_i - 1] not in infected_countries_arr:
                        print(countries_arr[countries_arr[code].borders[prob_i - 1]].name + " INFECTED")
                        infected_countries_arr.append(countries_arr[code].borders[prob_i - 1])
                        countries_arr[countries_arr[code].borders[prob_i - 1]].contact_rate_exp_rate = oc_contact_rate_exp_rate
                        countries_arr[countries_arr[code].borders[prob_i - 1]].quarantined_rate_exp_rate = oc_quarantined_rate_exp_rate
                        countries_arr[countries_arr[code].borders[prob_i - 1]].diagnose_speed_exp_rate = oc_diagnose_speed_exp_rate
                        countries_arr[countries_arr[code].borders[prob_i - 1]].day_when_infected = day
                    countries_arr[countries_arr[code].borders[prob_i - 1]].infected += 1
                    countries_arr[code].infected -= 1


                    break

    for _ in range(int(air_dep)):
        if np.random.sample() < infec_prob:
            target_prob = np.random.sample()
            for prob_i in range(1, len(probability_arr) - 1):
                if probability_arr[prob_i - 1] < target_prob < probability_arr[prob_i]:
                    if countries_keys[prob_i] not in infected_countries_arr:
                        print(countries_arr[countries_keys[prob_i]].name + " INFECTED")
                        infected_countries_arr.append(countries_keys[prob_i])
                        countries_arr[countries_keys[prob_i]].contact_rate_exp_rate = oc_contact_rate_exp_rate
                        countries_arr[countries_keys[prob_i]].quarantined_rate_exp_rate = oc_quarantined_rate_exp_rate
                        countries_arr[countries_keys[prob_i]].diagnose_speed_exp_rate = oc_diagnose_speed_exp_rate
                        countries_arr[countries_keys[prob_i]].day_when_infected = day
                    countries_arr[countries_keys[prob_i]].infected += 1
                    countries_arr[countries_keys[prob_i]].population += 1

                    countries_arr[code].infected -= 1
                    countries_arr[code].population -= 1



                    break


def main(data):
    for day in range(1, int(data) + 1):
        print("DAY " + str(day))
        day_deaths = 0
        day_cases = 0
        true_cases = 0
        day_recovered = 0

        if day == 47:
            countries_arr['CHN'].contact_rate_exp_rate = 0.053
            countries_arr['CHN'].quarantined_rate_exp_rate = 0.053
            countries_arr['CHN'].diagnose_speed_exp_rate = 0.022
            countries_arr['CHN'].day_when_infected = day



        for code, country in countries_arr.items():

            if country.infected > 0 or country.exposed > 0:

                country.susceptible, country.exposed, country.infected, country.suspected, country.quarantined, \
                country.confirmed, country.recovered = seibqhr(day_after_infected=day - country.day_when_infected,
                                                               c0=country.contact_rate_0, cb=country.contact_rate_min,
                                                               r1=country.contact_rate_exp_rate,
                                                               beta=country.transmission_prob,
                                                               q0=country.quarantined_rate_exposed_0,
                                                               qm=country.quarantined_rate_exposed_max,
                                                               r2=country.quarantined_rate_exp_rate,
                                                               m=country.susceptible_to_suspected_rate,
                                                               b=country.detection_rate,
                                                               f0=country.suspected_to_confirmed_0,
                                                               fm=country.suspected_to_confirmed_max,
                                                               r4=country.suspected_to_confirmed_exp_rate,
                                                               sigma=INCUBATION_RATE,
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

                infec(code, day)




            else:
                country.infected_arr.append(0)
                country.deaths_arr.append(0)
                country.exposed_arr.append(0)
                country.recovered_arr.append(0)

            day_cases = day_cases + country.confirmed
            true_cases = true_cases + country.confirmed + country.infected
            day_deaths += country.deaths
            day_recovered += country.recovered

        total_cases_arr.append(day_cases)
        true_cases_arr.append(true_cases)
        total_deaths_arr.append(day_deaths)
        total_recovered_arr.append(day_recovered)
        total_cases = total_cases_arr[-1]
        true_cases = true_cases_arr[-1]
        total_deaths = total_deaths_arr[-1]
        total_recovered = total_recovered_arr[-1]

        print(countries_arr["CHN"].infected)
        print(countries_arr["CHN"].confirmed)
        print(countries_arr["CHN"].recovered)
        print(countries_arr["CHN"].quarantined)
        print(countries_arr["CHN"].exposed)
        print(countries_arr["CHN"].suspected)
        print(day - countries_arr["CHN"].day_when_infected)

        days = day

        infected_countries_str = ""
        for ic in infected_countries_arr:
            infected_countries_str += ic
            infected_countries_str += " "

        result = {
            "confirmed": int(total_cases),
            "true_cases": int(true_cases),
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


def testing():
    global data_transmitter
    data_transmitter = main(120)
    for i in data_transmitter:
        1 + 1

# testing()