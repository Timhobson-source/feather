import os
import sys
import random
import tempfile
import time
import numpy as np

import pandas as pd

from logger import log


def build_dataframe(n: int):
    # build data frame of random numbers
    df = pd.DataFrame({'column': np.array(random.sample(range(n), n))})
    return df


def get_size_of_dataframe_in_Mb(df: pd.DataFrame):
    # get size of dataframe in Mb
    size = df.memory_usage(deep=True).sum() / 1024 ** 2
    return size


def write_dataframe(df: pd.DataFrame, file_name: str, extension: str):
    if extension == 'feather':
        # write data frame to feather file
        df.reset_index(drop=True).to_feather(file_name)
    elif extension == 'csv.gz':
        df.reset_index(drop=True).to_csv(file_name, compression='gzip')
    else:
        raise ValueError("Unsupported extension: {}".format(extension))


def read_dataframe(file_name: str, extension: str):
    if extension == 'feather':
        df = pd.read_feather(file_name)
    elif extension == 'csv.gz':
        df = pd.read_csv(file_name, compression='gzip')
    else:
        raise ValueError("Unsupported extension: {}".format(extension))

    return df


def test(N: int, extension: str):
    sizes = []
    write_times = []
    read_times = []

    df = build_dataframe(100)
    i = 0
    try:
        while i < N:
            # add 10000 rows to df
            df = df.append(build_dataframe(10000))

            size = get_size_of_dataframe_in_Mb(df)
            log.info("Size of dataframe with {} rows is {} Mb".format(i, size))
            sizes.append(size)

            with tempfile.TemporaryDirectory() as tmpdir:
                tmp_path = os.path.join(tmpdir, f"test.{extension}")
                log.info(f"Writing dataframe to {extension} file")
                start = time.time()
                write_dataframe(df, tmp_path, extension)
                end = time.time()
                log.info("Writing dataframe took {} seconds".format(end - start))

                write_times.append(end - start)

                log.info(f"Reading dataframe from {extension} file")
                start = time.time()
                df = read_dataframe(tmp_path, extension)
                end = time.time()
                log.info("Reading dataframe took {} seconds".format(end - start))

                read_times.append(end - start)

                i += 5000
    except KeyboardInterrupt:
        # so we can stop the loop early and still get results
        log.info("Keyboard interrupt")

    return sizes, write_times, read_times


def parse_args(args):
    # parse arguments using argparse
    import argparse
    parser = argparse.ArgumentParser(
        description='Test feather & .csv.gz file writing and reading'
    )
    parser.add_argument(
        '-e',
        '--extension',
        dest="extension",
        type=str,
        default='feather',
        choices=['feather', 'csv.gz'],
        help='extention of file to write and read'
    )
    parser.add_argument(
        '-N',
        '--number-of-iterations',
        dest="N",
        type=int,
        default=10000000,
        help='number of iterations'
    )
    return parser.parse_args(args)


def parse_results(sizes, write_times, read_times, extension):
    results = pd.DataFrame(
        {
            'size (Mb)': sizes,
            'write time (s)': write_times,
            'read time (s)': read_times
        }
    )

    log.info("Writing results to csv")
    name = 'csvgz' if extension == 'csv.gz' else 'feather'
    results.to_csv(f'results/{name}.csv')


if __name__ == '__main__':
    log.info("Start of script.")
    args = parse_args(sys.argv[1:])
    log.info("Arguments: {}".format(str(args)))

    log.info(f"Beginning test of {args.extension} files")
    sizes, write_times, read_times = test(args.N, args.extension)
    log.info("Test complete")
    parse_results(sizes, write_times, read_times, args.extension)

    log.info("End of script.")
