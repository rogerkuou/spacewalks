import matplotlib.pyplot as plt
import pandas as pd
import sys


def read_json_to_clean_dataframe(file_name):
    """
    Reads a JSON file into a pandas DataFrame, cleans the data, and sorts the DataFrame by date.

    Arguments:
        file_name : The path to the json file to read.

    Returns:
        pd.DataFrame: A cleaned and sorted dataframe containing the data from the json file.
    """
    df = pd.read_json(file_name, convert_dates=['date'], encoding='ascii')
    df['eva'] = df['eva'].astype(float)
    df.dropna(axis=0, subset=['duration', 'date'], inplace=True)
    df.sort_values('date', inplace=True)
    return df


def text_to_duration(duration):
    hours, minutes = duration.split(":")
    duration = int(hours) + int(minutes) / 60
    return duration


def compute_durations(df):
    """
    Convert duration to hours and calculate cumulative time.

    Creates a copy of the input df, converts the values in the
    ``duration`` column to numeric hour values using ``text_to_duration`` function,
    and computes a running cumulative sum of those durations.

    Parameters
    ----------
    df : pandas.DataFrame
        Input dataframe must contain ``duration`` column in a format modified by ``text_to_duration`` function.

    Returns
    -------
    pandas.DataFrame
        A copy of the input dataframe with two additional columns:

        - ``duration_hours``: Duration converted to hours as a numeric value.
        - ``cumulative_time``: Running cumulative sum of ``duration_hours``.

    """
    df_copy = df.copy()
    df_copy['duration_hours'] = df_copy['duration'].apply(text_to_duration)
    df_copy['cumulative_time'] = df_copy['duration_hours'].cumsum()
    return df_copy


def plot_eva_durations(file_name, df):
    """
    Plot the durations of extravehicular activity (EVA) and save the plot. 

    Arguments:
        file_name: The name of the file the plot is written to.
        df : Dataframe that contains the date and cumulative duration of the EVAs.
    """
    plt.plot(df['date'], df['cumulative_time'], 'ko-')
    plt.xlabel('Year')
    plt.ylabel('Total time spent in space to date (hours)')
    plt.tight_layout()
    plt.savefig(file_name)
    plt.show()

def main(input_file, output_file, graph_file):
    eva_df = read_json_to_clean_dataframe(input_file)
    eva_df.to_csv(output_file, index=False, encoding='utf-8')
    eva_df = compute_durations(eva_df)
    plot_eva_durations(graph_file, eva_df)


if __name__ == "__main__":  # if dunder name equals dunder main

    if len(sys.argv) >= 3:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        print("Using custom input and output filenames")
    else:
        # Data source: https://data.nasa.gov/resource/eva.json (with modifications)
        input_file = './data/eva_data.json'
        output_file = './results/eva_data.csv'
        print("Using default filenames")

    graph_file = './results/cumulative_eva_graph.png'

    main(input_file, output_file, graph_file)
