def main(infectivity):
    healthy = 7000000000
    infectivity = 0.01
    confirmed = 0
    for i in range(1000):
        new_confirmed = int(healthy * infectivity)
        confirmed += new_confirmed
        healthy -= new_confirmed
        print(str(healthy) + " " + str(confirmed))

    return confirmed
