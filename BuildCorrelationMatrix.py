import QueueClass
import pandas as pd
import numpy as np
import sys
import csv


def main(csv_file_name, matrix_size_param):
    matrix_size = int(matrix_size_param)
    df_raw_data = pd.read_csv(csv_file_name, parse_dates=['timestamp'])
    curr_window = QueueClass.Queue(matrix_size)
    lst_output = list()
    aux_lst = list()

    # Creating auxiliary column with the difference between timestamps in seconds
    aux_col = list()
    aux_col.append(np.nan)
    for i in range(1, df_raw_data.shape[0]):
        aux_col.append((df_raw_data.timestamp[i] - df_raw_data.timestamp[i - 1]).seconds)
    df_raw_data['deltaInSecs'] = aux_col

    for location in df_raw_data.locationId.unique():
        lst_output = []
        aux_df = df_raw_data.loc[df_raw_data['locationId'] == location]
        aux_df.index = range(aux_df.shape[0])
        curr_mode = aux_df.deltaInSecs.mode()
        outer_indices = iter(range(matrix_size - 1, aux_df.shape[0]))
        for outerIndex in outer_indices:
            aux_lst = []
            for innerIndex in range(matrix_size - 1):  # The final element will be inserted after the loop
                nb_of_points_to_insert = int(aux_df.deltaInSecs[outerIndex - innerIndex] / curr_mode) - 1
                if nb_of_points_to_insert > 0:
                    curr_window.reset_queue()
                    # Skipping the rows whose windows cannot be created due to missing data
                    for j in range(matrix_size - innerIndex - 1):
                        next(outer_indices, None)
                    break
                else:
                    curr_window.enqueue(aux_df.mains[outerIndex-innerIndex])
            if not curr_window.is_empty:  # Enqueueing the 5th value for mains and pushing window into output list
                # Notice that the dequeueing process inverts the order in the queue, which, in the output list, puts
                # the measures back to its chronological order
                aux_lst.append(aux_df.status[outerIndex-innerIndex])
                for i in range(curr_window.size):
                    aux_lst.append(curr_window.dequeue())
                aux_lst.append(aux_df.mains[outerIndex - (matrix_size - 1)])
                lst_output.append(aux_lst)
        if len(lst_output) > 0:
            with open("C:\Simptek\Assignment01_20170519\CorrelationMatrix_" + location + ".csv", 'wb') as my_file:
                wr = csv.writer(my_file)
                wr.writerows(lst_output)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])