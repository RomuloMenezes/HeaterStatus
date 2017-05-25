import HeaterStatus


def main():
    model = HeaterStatus.HeaterStatus()
    model.fit('C:\Simptek\Assignment01_20170519\RawData.csv')
    print model.predict('location02', 15000)

if __name__ == '__main__':
    main()