from dataStructure import *
import random
from ClockAndTime import *


class Node:
    def __init__(self):

        self.children = {}
        self.last = False
        self.value = None


class Commons:
    def __init__(self):
        self.root = Node()
        self.word_list = []

    def insert(self, key, value):
        node = self.root
        for a in list(key):
            if not node.children.get(a):
                node.children[a] = Node()

            node = node.children[a]

        node.last = True
        node.value = value

    def search(self, key):
        node = self.root
        found = True

        for a in list(key):
            if not node.children.get(a):
                found = False
                break

            node = node.children[a]

        if node and node.last and found:
            return node.value

    def suggestionsRec(self, node, word):

        if node.last:
            self.word_list.append(word)

        for a, n in node.children.items():
            self.suggestionsRec(n, word + a)

    def printAutoSuggestions(self, key):

        node = self.root
        not_found = False
        temp_word = ""

        for a in list(key):
            if not node.children.get(a):
                not_found = True
                break

            temp_word += a
            node = node.children[a]

        if not_found:
            return 0
        elif node.last and not node.children:
            return -1

        self.suggestionsRec(node, temp_word)
        if len(self.word_list) != 0:
            print("Did you mean:")
        for s in self.word_list:
            print(s)
        return 1


class Shift:
    shifts = []
    futureList = []

    def __init__(self, start, long, intersection, officer):
        print(start)
        self.startTime = start
        self.duration = long
        self.endTime = start.add(long)
        self.intersection = intersection
        self.officer = officer
        Shift.shifts.append(self)

    def __str__(self):
        return (
            "start time="
            + str(self.startTime)
            + " ,long="
            + str(self.duration)
            + " ,intersection="
            + str(self.intersection.name)
        )

    @classmethod
    def check(obj):
        for shift in obj.shifts:
            if shift.startTime.get_time_distance(SoftwareTimer.instance.time) == 600:
                obj.sendSMS(shift.officer.id, shift.intersection.id)
                shift.officer.currentShift = shift


class Officer:
    officerIds = BinarySearchTree()
    officerTriples = Commons()
    officersList = []

    def __init__(self, name, id):
        self.id = id
        self.name = name
        self.firstStatus = False
        self.injectedIntersection = None
        self.presenceTime = 0
        self.absenceTime = 0
        self.shiftList = []
        self.currentShift = None
        Officer.officerIds.insert(id, self)
        Officer.officersList.append(self)
        Officer.officerTriples.insert(self.name, self)

    @classmethod
    def search(cls, thingToSearch, type=0):
        # Searches our intersections by name Or id
        # type 1 search by name
        # type 2 search by id
        if type == 0:
            return cls.officerIds.search(thingToSearch)
        else:
            return cls.officerTriples.search(thingToSearch)

    @classmethod
    def findPartOf(cls, partOfName):
        return cls.officerTriples.printAutoSuggestions(partOfName)

    @classmethod
    def attendance(cls, intersectionID, officerID):
        intersection = Intersection.search(intersectionID, 0)
        officer = Officer.search(officerID, 0)
        intersection.attendence(officer)
        return 0

    def setShift(self, hour, long, intersection):
        if len(self.shiftList) < 5:
            self.shiftList.append(Shift(Time(0, 0, hour), long, intersection, self))
            return 0
        else:
            return 1

    def checkIsSet(self):
        if self.firstStatus:
            return "Set"
        else:
            return "Not Set"

    def getIntersectionName(self):
        if self.injectedIntersection is None:
            return "None"
        else:
            return self.injectedIntersection.name

    def __str__(self):
        return (
            "- name= "
            + self.name
            + " ,id="
            + str(self.id)
            + " ,present time="
            + str(self.presenceTime)
            + " ,status="
            + self.checkIsSet()
            + " ,setted intersection="
            + self.getIntersectionName()
        )


class Intersection:
    # Static attribute that holds all the intersections
    intersectionTrieTree = Commons()
    intersectionList = []
    intersectionBTree = BinarySearchTree()
    maxNumOfIntersections = 500

    # We use Decorator for calss methods
    @classmethod
    def search(cls, thingToSearch, type):
        # Searches our intersections by name Or id
        # type 1 search by name
        # type 2 search by id
        if type == 0:
            return cls.intersectionBTree.search(thingToSearch)
        else:
            return cls.intersectionTrieTree.search(thingToSearch)

    @classmethod
    def returnSuggestions(cls, word):
        return cls.intersectionTrieTree.printAutoSuggestions(word)

    def __init__(self, name, officer=None):
        self.id = self.generateId()
        self.name = name
        self.carCount = 0
        self.currentPolice = officer
        self.lastShiftStart = None
        self.ns_l = TrafficLight(1, self, 1, 1)
        self.ew_l = TrafficLight(1, self, 0, 0, self.ns_l)
        self.ns_l.otherLight = self.ew_l
        # Do not forget to add the intersection to the Static Binary Tree
        Intersection.intersectionBTree.insert(self.id, self)
        Intersection.intersectionList.append(self)
        Intersection.intersectionTrieTree.insert(self.name, self)

    def changeLightStates(self, mode=1, maxNumberOfNS=None, maxNumberOfEW=None):
        if mode == 1:
            self.ns_l._mode = 1
            self.ew_l._mode = 1
        else:
            self.ns_l.mode = 0
            self.ew_l.mode = 0
            self.ns_l.maxCounter = maxNumberOfNS
            self.ew_l.maxCounter = maxNumberOfEW

    def attendence(self, newOfficer):
        p_officer = self.currentPolice
        if p_officer is not None:
            p_officer.presenceTime = (
                p_officer.presenceTime
                + SoftwareTimer.instance.time.get_time_distance(self.lastShiftStart)
            )
        self.currentPolice = newOfficer
        self.lastShiftStart = Time(
            SoftwareTimer.instance.time.second,
            SoftwareTimer.instance.time.minute,
            SoftwareTimer.instance.time.hour,
        )

    def getNumberOfPassedCars(self):
        self.carCount = self.ns_l.carCount + self.ew_l.carCount

    def generateId(self):
        # Returns a random id for the intersection
        while True:
            generatedId = random.randint(0, Intersection.maxNumOfIntersections)
            res = Intersection.search(generatedId, 0)
            if res is None:
                return generatedId

    def __str__(self):
        return (
            " -id= "
            + str(self.id)
            + " ,name="
            + self.name
            + " ,Car Count="
            + str(self.carCount)
            + " ,Mode="
            + self.ns_l.getModeString()
        )


class TrafficLight:

    lightList = []

    @classmethod
    def check(cls):
        for light in cls.lightList:
            light.incrementCounter()
            light.checkStateChange()

    def __init__(
        self,
        mode,
        intersection,
        alignment,
        state,
        oLight=None,
        maxCounter=20,
        counter=0,
        passedCars=0,
    ):
        # Manual:0 , Auto:1
        self.mode = mode
        self.intersection = intersection
        # N~S:1 , E~W = 0
        self.alignment = alignment
        # Red:0 , Green:1
        self.state = state
        self.counter = counter
        self.carCount = passedCars
        self.maxCounter = maxCounter
        self.internalCounter = 0
        self.otherLight = oLight
        TrafficLight.lightList.append(self)

    def incrementCarCount(self, numberToIncrease):
        self.carCount = self.carCount + numberToIncrease

    def incrementCounter(self):
        self.counter = self.counter + 1

    def checkStateChange(self):
        if self.state == 0 and self.counter > self.maxCounter:
            self.changeState()

    def changeState(self):
        self.internalCounter = self.internalCounter + 1
        if self.internalCounter == 1:
            self.otherLight.state = 0
            self.otherLight.counter = 0
            stat = self.setLight(self.intersection.id, self.otherLight.alignment, 0)
        elif self.internalCounter == 3:
            self.state = 1
            self.counter = 0
            self.internalCounter = 0
            self.setLight(self.intersection.id, self.alignment, 1)

    def changeMaxCounter(self, stat):
        self.incrementCarCount(stat)
        if self.mode == 1:
            parameter = self.maxCounter * 2 - stat
            if parameter == 0:
                self.maxCounter = self.maxCounter + 1

    def getModeString(self):
        if self.mode == 1:
            return "Auto"
        else:
            return "Manual"

    def getStateString(self):
        if self.state == 1:
            return "Green"
        else:
            return "Red"
