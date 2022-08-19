class Time:
    def __init__(self, s=0, m=0, h=0):
        self.second = s
        self.minute = m
        self.hour = h


    def get_time_distance(self, input_time):
        ref_second = self.hour * 3600 + self.minute * 60 + self.second
        input_second = (
            input_time.hour * 3600 + input_time.minute * 60 + input_time.second
        )
        output_second = ref_second - input_second
        if output_second < 0:
            output_second = output_second + 12 * 3600
        return output_second

    def format_clock(self, number):
        if number < 10:
            return "0" + str(number)
        return str(number)

    def add(self, seconds):
        cs = Time(self.second, self.minute, self.hour)
        cs.second = cs.second + seconds
        if cs.second > 60:
            cs.minute = cs.minute + int(cs.second / 60)
            cs.second = cs.second % 60
        if cs.minute > 60:
            cs.hour = cs.hour + int(cs.minute / 60)
            cs.minute = cs.minute % 60
        if cs.hour > 24:
            cs.hour = cs.hour % 24
        return cs

    def __str__(self):
        return (
            self.format_clock(self.hour)
            + ":"
            + self.format_clock(self.minute)
            + ":"
            + self.format_clock(self.second)
        )


class SoftwareTimer:
    instance = None

    def __init__(self):
        if SoftwareTimer.instance is not None:
            raise Exception("you cant create instance from singleton!")
        else:
            self.timeStamp = 0
            self.time = Time(0, 0, 0)
            SoftwareTimer.instance = self

    def time_up(self):
        self.timeStamp = self.timeStamp + 1
        self.time.hour = (int(self.timeStamp / 3600)) % 24
        self.time.minute = int((self.timeStamp % 3600) / 60)
        self.time.second = self.timeStamp % 60

    def __str__(self):
        return self.time.__str__()
