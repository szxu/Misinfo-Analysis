from datetime import datetime

class Date_retriever():

    @staticmethod
    def retrieve_date(str, website):
        onlynumber = ''.join([i for i in str if i.isdigit()])
        if website == "MIT":
            year = onlynumber[0:4]
            month = onlynumber[4:6]
            day = onlynumber[6:8]
            hour = onlynumber[8:10]
            minute = onlynumber[10:12]
            second = onlynumber[12:14]
        elif website == "WXC":
            month = onlynumber[0:2]
            day = onlynumber[2:4]
            year = onlynumber[4:8]
            hour = onlynumber[8:10]
            minute = onlynumber[10:12]
            second = onlynumber[12:14]
        elif website == "HR":
            year = onlynumber[0:4]
            month = onlynumber[4:6]
            day = onlynumber[6:8]
            hour = onlynumber[8:10]
            minute = onlynumber[10:12]
            second = '0'
        else:
            year = '1900'
            month = '1'
            day = '1'
            hour = '0'
            minute = '0'
            second = '0'



        timestamp = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))

        return timestamp

# if __name__ == '__main__':
#     print(Date_retriever.retrieve_date(" 07/17/2022  16:21:02", "WXC"))