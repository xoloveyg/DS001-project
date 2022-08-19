import Officer
import threading
import ClockAndTime
import CLInter


def attendance(intersection_id, officer_id):
    print("******************** Attendance ********************")
    CLInter.CLI.Officer.attendance(intersection_id, officer_id)
    print("****************************************************")


def clock():
    ClockAndTime.SoftwareTimer.instance.time_up()
    Officer.TrafficLight.check()
    Officer.Shift.check()


def init(light: callable, sms: callable):
    ClockAndTime.SoftwareTimer()
    Officer.TrafficLight.setLight = light
    Officer.Shift.sendSMS = sms
    CLInter.NowState()
    proc = threading.Thread(target=CLInter.CLI.prompt, args=())
    proc.start()
