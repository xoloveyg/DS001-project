import time
import app


def sms(police_id, intersection_id):
    print(
        "officer:"
        + str(police_id)
        + " intersection:"
        + str(intersection_id)
        + " received alarm sms"
    )


def light(obj, id, alignment, state):
    return None


if __name__ == "__main__":
    app.init(light, sms)
    while not False:
        # this is 0.1 second in real world and 1 second in our software
        time.sleep(0.1)
        # start time
        app.clock()
