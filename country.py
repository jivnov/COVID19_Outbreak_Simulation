import csv


class Country:
    def __init__(self, name, country_code, population):
        self.name = name
        self.country_code = country_code
        self.population = population
        self.young = 0
        self.middle = 0
        self.old = 0
        self.hospital_beds = 0
        self.arrive = 0
        self.departure = 0
        self.density = 0
        self.confirmed = 0
        self.deaths = 0
        self.recovered = 0
        self.true_cases = 0
        self.inc_cases = 0
        self.true_cases_arr = []
        self.inc_cases_arr = []
        self.deaths_arr = []
        self.recovered_arr = []
        self.air_departures = 0
        self.borders = []


class CountryCreator:
    @staticmethod
    def initialization():
        countries_arr = {}
        countries_keys = []
        countries_code_2_to_3_dict = {}
        countries_code_3_to_2_dict = {}
        cv = CSVReader('data/population_total.csv')
        tmp_arr = cv.read([0, 1, 62])
        for i in range(0, len(tmp_arr), 3):
            key_value = tmp_arr[i + 1]
            countries_arr.update({key_value:
                                      Country(tmp_arr[i], tmp_arr[i + 1], float(tmp_arr[i + 2]))})
            countries_keys.append(key_value)

        cv = CSVReader('data/wikipedia-iso-country-codes.csv')
        tmp_arr = cv.read([1, 2])
        for i in range(0, len(tmp_arr), 2):
            countries_code_2_to_3_dict.update({tmp_arr[i]: tmp_arr[i + 1]})
            countries_code_3_to_2_dict.update({tmp_arr[i + 1]: tmp_arr[i]})

        cv = CSVReader('data/population014per.csv')
        tmp_arr = cv.read([62])
        for i in range(len(tmp_arr)):
            countries_arr[countries_keys[i]].young = tmp_arr[i]

        cv = CSVReader('data/population1564per.csv')
        tmp_arr = cv.read([62])
        for i in range(len(tmp_arr)):
            countries_arr[countries_keys[i]].middle = tmp_arr[i]

        cv = CSVReader('data/population60upper.csv')
        tmp_arr = cv.read([62])
        for i in range(len(tmp_arr)):
            countries_arr[countries_keys[i]].old = tmp_arr[i]

        cv = CSVReader('data/hospital_beds_per_1k.csv')
        tmp_arr = cv.read([62])
        for i in range(len(tmp_arr)):
            countries_arr[countries_keys[i]].hospital_beds = tmp_arr[i]

        cv = CSVReader('data/tourism_arvl.csv')
        tmp_arr = cv.read([62])
        for i in range(len(tmp_arr)):
            countries_arr[countries_keys[i]].arrive = tmp_arr[i]

        cv = CSVReader('data/tourism_dprt.csv')
        tmp_arr = cv.read([62])
        for i in range(len(tmp_arr)):
            countries_arr[countries_keys[i]].departure = tmp_arr[i]

        cv = CSVReader('data/density.csv')
        tmp_arr = cv.read([62])
        for i in range(len(tmp_arr)):
            countries_arr[countries_keys[i]].density = tmp_arr[i]

        cv = CSVReader('data/air_departures.csv')
        tmp_arr = cv.read([62])
        for i in range(len(tmp_arr)):
            countries_arr[countries_keys[i]].air_departures = tmp_arr[i]

        cv = CSVReader('data/borders.csv')
        tmp_arr = cv.read([0, 2])
        for i in range(0, len(tmp_arr), 2):
            if tmp_arr[i] in countries_code_2_to_3_dict.keys() and tmp_arr[i+1] in countries_code_2_to_3_dict:
                if countries_code_2_to_3_dict[tmp_arr[i]] in countries_arr.keys():
                    countries_arr[countries_code_2_to_3_dict[tmp_arr[i]]].borders.append(
                        countries_code_2_to_3_dict[tmp_arr[i + 1]])

        print(countries_arr["CHN"].borders)
        return countries_arr


class CSVReader:
    def __init__(self, csv_file, delimiter=','):
        self.csv_file = csv_file
        self.delimiter = delimiter

    def read(self, columns):
        to_return_arr = []
        with open(self.csv_file, newline='') as csvf:
            reader = csv.reader(csvf, delimiter=self.delimiter, quotechar='"')

            for row in reader:
                if row[1] == 'Country Code' or row[1] == "country_name":
                    continue
                for c in columns:
                    if row[c] != '':
                        to_return_arr.append(row[c])
                    else:
                        to_return_arr.append(0)
        return to_return_arr


CountryCreator.initialization()
