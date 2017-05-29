import HeaterStatus
import pandas as pd


def main():
    right_count = 0
    wrong_count = 0
    false_positive = 0
    false_negative = 0
    model = HeaterStatus.HeaterStatus()
    model.fit('C:\Simptek\Assignment01_20170519\RawData.csv')
    df_raw_data = pd.read_csv('C:\Simptek\Assignment01_20170519\RawData.csv', parse_dates=['timestamp'])
    for i in range(df_raw_data.shape[0]):
        print i
        curr_prediction = model.predict(df_raw_data.locationId[i],df_raw_data.mains[i])
        if curr_prediction == df_raw_data.status[i]:
            right_count += 1
        else:
            wrong_count += 1
            if curr_prediction > df_raw_data.status[i]:
                false_positive += 1
            else:
                false_negative += 1
    print 'Accuracy: ' + str(float(right_count)/float(df_raw_data.shape[0]))
    print '% false positives: ' + str(float(false_positive) / float(df_raw_data.shape[0]))
    print '% false negatives: ' + str(float(false_negative) / float(df_raw_data.shape[0]))


if __name__ == '__main__':
    main()