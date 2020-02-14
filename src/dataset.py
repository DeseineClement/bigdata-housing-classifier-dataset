from functools import reduce

from faker import Faker
from faker.providers import address
from sys import argv
from getopt import getopt
from pandas import DataFrame


def generate_row(carry, faker):
    lat, long, _, country_code, city = faker.location_on_land()

    carry['housing_type'].append(
        faker.random_element(['Housing', 'Hospital', 'Train station', 'Business', 'Police Station', 'Shop']))
    carry['latitude'].append(lat)
    carry['longitude'].append(long)
    carry['country_code'].append(country_code)
    carry['surface (m2)'].append(faker.random_int(min=20, max=300))
    carry['height (m)'].append(faker.random_int(min=2, max=20))
    carry['city'].append(city)
    return carry


def generate_random_dataset(row_count):
    faker = Faker()
    faker.add_provider(address)
    return DataFrame(
        data=reduce(
            lambda carry, index: generate_row(carry, faker),
            range(0, row_count),
            {'housing_type': [], 'latitude': [], 'longitude': [], 'country_code': [], 'surface (m2)': [],
             'height (m)': [], 'city': []}
        ),
        columns=['housing_type', 'latitude', 'longitude', 'country_code', 'surface (m2)', 'height (m)', 'city']
    )


def main():
    options, *_ = getopt(argv[1:], 'or', ['output-file=', 'rows='])
    output_file_src = 'output/data.csv'
    row_count = 1000
    for opt, arg in options:
        if opt in ('-o', '--output-file'):
            output_file_src = arg
        elif opt in ('-r', '--rows'):
            row_count = int(arg)
    generate_random_dataset(row_count).to_csv(output_file_src)


if __name__ == "__main__":
    main()
