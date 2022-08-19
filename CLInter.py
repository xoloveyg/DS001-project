from Officer import *
from ClockAndTime import *
from CommonTypes import CommonTypes


class NowState:
    instance = None

    def __init__(self):
        if NowState.instance is not None:
            raise Exception("you can't create instance from singleton!")
        elif NowState.instance is None:
            self.type = CommonTypes.HOME
            NowState.instance = self


class CLI:
    def mainMenu(command):
        if NowState.instance.type == CommonTypes.HOME:
            if command == "2":
                NowState.instance.type = CommonTypes.Officers
            elif command == "1":
                NowState.instance.type = CommonTypes.INTERSECTIONS
            else:
                print("wrong command")
        elif NowState.instance.type == CommonTypes.addIntersection:
            intersection = Intersection(command)
            print("intersection id is: " + str(intersection.id))
            NowState.instance.type = CommonTypes.INTERSECTIONS

        elif NowState.instance.type == CommonTypes.ATTENDANCE:
            commands = command.split()
            Officer.attendance(int(commands[1]), int(commands[0]))
            NowState.instance.type = CommonTypes.Officers

        elif NowState.instance.type == CommonTypes.ADD_OFFICER:
            commands = command.split()
            founded_officer = Officer(commands[1], int(commands[0]))
            NowState.instance.type = CommonTypes.Officers

        elif NowState.instance.type == CommonTypes.SHOW_SHIFT_OFFICER:
            commands = command.split()
            founded_officer = Officer.search(int(commands[0]))
            if founded_officer is not None:
                for shift in founded_officer.shiftList:
                    print(shift.__str__() + "\n")
            NowState.instance.type = CommonTypes.Officers

        elif NowState.instance.type == CommonTypes.SET_SHIFT_OFFICER:
            if command == "return":
                NowState.instance.type = CommonTypes.Officers
            else:
                commands = command.split()
                founded_officer = Officer.search(int(commands[0]))
                intersection = Intersection.search(int(commands[1]), 0)
                result = founded_officer.setShift(
                    int(commands[2]), int(commands[3]), intersection
                )
                if result == 0:
                    print("Shift successfully added")
                else:
                    print("!!!Error setting shift!!!")
                NowState.instance.type = CommonTypes.Officers

        elif NowState.instance.type == CommonTypes.CHANGE_LIGHT_INTERSECTION:
            commands = command.split()
            intersection = Intersection.search(int(commands[0]), 0)
            if int(commands[1]) == 1:
                intersection.changeLightStates(1)
                NowState.instance.type = CommonTypes.INTERSECTIONS
            else:
                intersection.changeLightStates(0, int(commands[2]), int(commands[3]))
                NowState.instance.type = CommonTypes.INTERSECTIONS

        elif NowState.instance.type == CommonTypes.searchInterSection:
            if command.isdigit():
                intersection = Intersection.search(int(command), 0)
                if intersection == None:
                    print("Not found!!")
            else:
                intersection = Intersection.search(command, 1)
                if intersection == None:
                    result = Intersection.returnSuggestions(command)
                    if result != 1:
                        print("Not found!!")

            if intersection != None:
                print("*" + intersection.__str__())

            NowState.instance.type = CommonTypes.INTERSECTIONS
        elif NowState.instance.type == CommonTypes.SEARCH_OFFICER:
            if command.isdigit():
                founded_officer = Officer.search(int(command), 0)
                if founded_officer == None:
                    print("Not found")
            else:
                founded_officer = Officer.search(command, 1)
                if founded_officer == None:
                    result = Officer.findPartOf(command)
                    if result != 1:
                        print("Not found")
            if founded_officer != None:
                print("*" + founded_officer.__str__())
            NowState.instance.type = CommonTypes.Officers
        elif NowState.instance.type == CommonTypes.INTERSECTIONS:
            if command == "1":
                print("Intersections:\n")
                for i in range(0, len(Intersection.intersectionList)):
                    print(
                        str(i + 1) + ". " + Intersection.intersectionList[i].__str__()
                    )
                NowState.instance.type = CommonTypes.INTERSECTIONS
            elif command == "2":
                NowState.instance.type = CommonTypes.addIntersection
            elif command == "3":
                NowState.instance.type = CommonTypes.searchInterSection
            elif command == "4":
                NowState.instance.type = CommonTypes.CHANGE_LIGHT_INTERSECTION
            elif command == "5":
                NowState.instance.type = CommonTypes.HOME
            else:
                print("You entered the wrong command")
        elif NowState.instance.type == CommonTypes.Officers:
            if command == "1":
                print("Officers:\n")
                for i in range(0, len(Officer.officersList)):
                    print(str(i + 1) + ". " + Officer.officersList[i].__str__())
                NowState.instance.type = CommonTypes.Officers
            elif command == "5":
                NowState.instance.type = CommonTypes.SHOW_SHIFT_OFFICER
            elif command == "2":
                print("Add a officer")
                NowState.instance.type = CommonTypes.ADD_OFFICER
            elif command == "4":
                NowState.instance.type = CommonTypes.SET_SHIFT_OFFICER
            elif command == "6":
                NowState.instance.type = CommonTypes.HOME
            elif command == "3":
                NowState.instance.type = CommonTypes.SEARCH_OFFICER
            elif command == "7":
                NowState.instance.type = CommonTypes.ATTENDANCE
            else:
                print("You entered the wrong command")

    def prompt():
        while True:
            onlineTime = SoftwareTimer.instance.__str__()
            if NowState.instance.type == CommonTypes.HOME:
                CLI.mainMenu(
                    input(
                        "#### Software First Page ####\n1.intersections\n2.officers\nEnter index of menu you want to work\n\n*** time: "
                        + onlineTime
                        + " ***"
                        + "\n"
                    )
                )
            elif NowState.instance.type == CommonTypes.EXIT:
                return False
            elif NowState.instance.type == CommonTypes.INTERSECTIONS:
                CLI.mainMenu(
                    input(
                        "##### Intersections #####\n1.show\n2.add\n3.search\n4.change light\n5.back\nEnter index of ypur choice\n*** time: "
                        + onlineTime
                        + " ***"
                        + "\n"
                    )
                )
            elif NowState.instance.type == CommonTypes.Officers:
                CLI.mainMenu(
                    input(
                        "##### Officers #####\n1.show\n2.add\n3.search\n4.set shift\n5.show shifts\n6.back\n7.attendence\nEnter index of ypur choice\n*** time: "
                        + onlineTime
                        + " ***"
                        + "\n"
                    )
                )
            elif NowState.instance.type == CommonTypes.addIntersection:
                CLI.mainMenu(
                    input(
                        "##### Add Intersection #####\nEnter a name for intersection:\n"
                    )
                )
            elif NowState.instance.type == CommonTypes.searchInterSection:
                CLI.mainMenu(
                    input(
                        "##### Search Intersection #####\nEnter code or a part of the name of intersection:\n"
                    )
                )
            elif NowState.instance.type == CommonTypes.CHANGE_LIGHT_INTERSECTION:
                CLI.mainMenu(
                    input(
                        "##### Change light #####\nEnter the id of intersection and light status\n(pattern [id] [mode] [NorthSouthCounter] [EastWestCounter])\n"
                    )
                )
            elif NowState.instance.type == CommonTypes.ADD_OFFICER:
                CLI.mainMenu(
                    input(
                        "##### Add Officer #####\nEnter the id and name of the officer\n(pattern: [id] [name] [lastNAme]\n"
                    )
                )
            elif NowState.instance.type == CommonTypes.SET_SHIFT_OFFICER:
                CLI.mainMenu(
                    input(
                        "##### Set Shift #####\nSet a shift for officer or enter 'back'\n(pattern [id] [intersection] [begin time] [duration])\n"
                    )
                )
            elif NowState.instance.type == CommonTypes.SEARCH_OFFICER:
                CLI.mainMenu(
                    input(
                        "##### Search Intersection #####\nEnter id or a part of the name of officer:\n"
                    )
                )
            elif NowState.instance.type == CommonTypes.SHOW_SHIFT_OFFICER:
                CLI.mainMenu(
                    input(
                        "##### Show Shifts #####\nEnter id or a part of the name of officer:\n"
                    )
                )
            elif NowState.instance.type == CommonTypes.ATTENDANCE:
                CLI.mainMenu(
                    input(
                        "##### Manual Mode #####\nEnter officer id and intersection id:\n(pattern: [id] [intersection])\n"
                    )
                )
            else:
                break
