import os

class DateSetter(object):
    def get_month_name(self, mm):
        return {
                '01': 'Jan',
                '02': 'Feb',
                '03': 'Mar',
                '04': 'Apr',
                '05': 'May',
                '06': 'Jun',
                '07': 'Jul',
                '08': 'Aug',
                '09': 'Sep',
                '10': 'Oct',
                '11': 'Nov',
                '12': 'Dec',
                }.get(mm, -1)

    def set_system_date(self, button_string):
        if len(button_string) == 12:
            yyyy = button_string[0:4]
            mm = button_string[4:6]
            dd = button_string[6:8]
            hh = button_string[8:10]
            mte = button_string[10:12]

            #os.system("sudo date -s \"10 Dec 2017 16:25\"")
            cmd = "sudo date -s " + "'" + dd + " " + self.get_month_name(mm) + " " + yyyy + " " + hh + ":" + mte + "'"
            #print cmd
            os.system(cmd)
        else:
            return -1
