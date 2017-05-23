import QueueClass
import pandas as pd
import numpy as np
import sys


def main(csv_file_name, matrix_size_param):
    matrix_size = int(matrix_size_param)
    df_raw_data = pd.read_csv(csv_file_name, parse_dates=['timestamp'])
    curr_window = QueueClass.Queue(matrix_size)

    # Creating auxiliary column with the difference between timestamps in seconds
    aux_col = list()
    aux_col.append(np.nan)
    for i in range(1, df_raw_data.shape[0]):
        aux_col.append((df_raw_data.timestamp[i] - df_raw_data.timestamp[i - 1]).seconds)
    df_raw_data['deltaInSecs'] = aux_col

    for location in df_raw_data.locationId.unique():
        aux_df = df_raw_data.loc[df_raw_data['locationId'] == location]
        aux_df.index = range(aux_df.shape[0])
        curr_mode = aux_df.deltaInSecs.mode()
        for outerIndex in range(matrix_size - 1, aux_df.shape[0]):
            for innerIndex in range(matrix_size - 1):  # The final element will be inserted after the loop
                nb_of_points_to_insert = int(aux_df.deltaInSecs[outerIndex - innerIndex] / curr_mode) - 1
                if nb_of_points_to_insert > 0:
                    curr_window.reset_queue()
                else:
                    curr_window.enqueue(aux_df.mains[outerIndex-innerIndex])
            if not curr_window.is_empty:  # Enqueueing the 5th value for mains
                curr_window.enqueue(aux_df.mains[outerIndex - (matrix_size - 1)])


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])