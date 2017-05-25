from sklearn.linear_model import LogisticRegression


class HeaterStatus:
    logistic = LogisticRegression()
    logistic_loc = list()
    location_dict = dict()
    score_all_locations = 0
    score_per_location = list()

    def fit(self, raw_data_file_name):
        import pandas as pd
        import numpy as np
        from sklearn.model_selection import train_test_split

        df_raw_data = pd.read_csv(raw_data_file_name, parse_dates=['timestamp'])
        location_index = 0
        for location in df_raw_data.locationId.unique():
            self.location_dict[location] = location_index
            location_index += 1

        # Training one model for all the locations
        x = np.ndarray(shape=(df_raw_data.shape[0], 2), dtype='int')
        for i in range(df_raw_data.shape[0]):
            x[i, 0] = self.location_dict[df_raw_data.locationId[i]]
            x[i, 1] = df_raw_data.mains[i]
        y = df_raw_data.status
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.15, stratify=x[:, 0])
        logistic = LogisticRegression()
        logistic.fit(x_train, y_train)
        self.score_all_locations = logistic.score(x_test, y_test)

        # Training one model for each location
        curr_logistic = LogisticRegression()
        for location in df_raw_data.locationId.unique():
            aux_df = df_raw_data.loc[df_raw_data['locationId'] == location]
            x_train, x_test, y_train, y_test = train_test_split(aux_df.mains, aux_df.status, test_size=0.15)
            curr_logistic.fit(x_train.values.reshape(-1, 1), y_train.values.reshape(-1, 1))
            self.logistic_loc.append(curr_logistic)
            self.score_per_location.append(curr_logistic.score(x_test.values.reshape(-1,1),
                                                               y_test.values.reshape(-1,1)))

    def predict(self, location, mains):
        if len(self.logistic_loc) == 0:
            # The method fit has not yet been called
            return -1
        else:
            if self.score_all_locations > self.score_per_location[self.location_dict[location]]:
                return self.logistic.predict(mains)
            else:
                return self.logistic_loc[self.location_dict[location]].predict(mains)
