from datetime import date, datetime

class Input():
    @staticmethod
    def get_startend_date(start_or_end):
        date_entry = input('Enter a ' + start_or_end + ' date in YYYY-MM-DD numerical format: ')
        year, month, day = map(int, date_entry.split('-'))
        date1 = date(year, month, day)
        return date1

    @staticmethod
    def get_date(target):
        target["start_date"] = Input.get_startend_date('start')
        target["end_date"] = Input.get_startend_date('end')
        print("This program scraps from " + str(target["start_date"]) + ' to ' + str(target["end_date"]))
        return target