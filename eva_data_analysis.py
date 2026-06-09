import matplotlib.pyplot as plt
import pandas as pd


def read_json_to_clean_dataframe(input_file):
    # Load using 'ascii' encoding to prevent errors on Windows
    eva_df = pd.read_json(input_file, convert_dates=['date'], encoding='ascii')
    eva_df['eva'] = eva_df['eva'].astype(float)
    eva_df.dropna(axis=0, subset=['duration', 'date'], inplace=True)  # Remove rows that don't have a date or duration
    eva_df.sort_values('date', inplace=True)
    return eva_df


def plot_cumulative_time_in_space(df, graph_file):
    df = add_duration_hours(df)
    plt.plot(df['date'], df['cumulative_time'], 'ko-')
    plt.xlabel('Year')
    plt.ylabel('Total time spent in space to date (hours)')
    plt.tight_layout()
    plt.savefig(graph_file)
    plt.show()


def text_to_duration(duration):
    hours, minutes = duration.split(":")
    duration_hours = int(hours) + int(minutes)/6
    return duration_hours


def add_duration_hours(df):
    df_copy = df.copy()
    df_copy["duration_hours"] = df_copy["duration"].apply(text_to_duration)
    df_copy['cumulative_time'] = df_copy['duration_hours'].cumsum()
    return df_copy

# Data source: https://data.nasa.gov/resource/eva.json (with modifications)
input_file = './eva_data.json'
output_file = './eva_data.csv'
graph_file = './cumulative_eva_graph.png'

eva_data = read_json_to_clean_dataframe(input_file)

# Save cleaned data in 'utf-8' encoding to prevent 'ascii' errors on Windows
eva_data.to_csv(output_file, index=False, encoding='utf-8')

plot_cumulative_time_in_space(eva_data, graph_file)
