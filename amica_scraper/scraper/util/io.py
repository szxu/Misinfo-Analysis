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

class Output():
    @staticmethod
    def set_filename(type, target):
        filename = " "
        if type == "news":
            if target["web_name"] == "WXC":
                filename = target["web_name"] + "_" + target["cat_name"] + "_" + str(target["start_date"]) + "_" + str(
                    target["end_date"])
            elif target["web_name"] == "PYB":
                filename = target["web_name"] + "_" + str(datetime.today())

        return filename