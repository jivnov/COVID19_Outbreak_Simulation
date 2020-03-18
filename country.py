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


class CountryCreator:
    @staticmethod
    def initialization():
        countries_arr = []

        cv = CSVReader('data/population_total.csv')
        tmp_arr = cv.read([0, 1, 62])
        for i in range(0, len(tmp_arr), 3):
            countries_arr.append(Country(tmp_arr[i], tmp_arr[i + 1], tmp_arr[i + 2]))

        cv = CSVReader('data/population014per.csv')
        tmp_arr = cv.read([62])
        for i in range(len(tmp_arr)):
            countries_arr[i].young = tmp_arr[i]

        cv = CSVReader('data/population1564per.csv')
        tmp_arr = cv.read([62])
        for i in range(len(tmp_arr)):
            countries_arr[i].middle = tmp_arr[i]

        cv = CSVReader('data/population60upper.csv')
        tmp_arr = cv.read([62])
        for i in range(len(tmp_arr)):
            countries_arr[i].old = tmp_arr[i]

        cv = CSVReader('data/hospital_beds_per_1k.csv')
        tmp_arr = cv.read([62])
        for i in range(len(tmp_arr)):
            countries_arr[i].hospital_beds = tmp_arr[i]

        cv = CSVReader('data/tourism_arvl.csv')
        tmp_arr = cv.read([62])
        for i in range(len(tmp_arr)):
            countries_arr[i].arrive = tmp_arr[i]

        cv = CSVReader('data/tourism_dprt.csv')
        tmp_arr = cv.read([62])
        for i in range(len(tmp_arr)):
            countries_arr[i].departure = tmp_arr[i]

        cv = CSVReader('data/density.csv')
        tmp_arr = cv.read([62])
        for i in range(len(tmp_arr)):
            countries_arr[i].density = tmp_arr[i]

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
                for c in columns:
                    to_return_arr.append(row[c])
        return to_return_arr
