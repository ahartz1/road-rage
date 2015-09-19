import math
import numpy as np
import random
from copy import deepcopy


class Car:
    """
    Responsibilities:
    - Know speed (in m/s)
    - Know distance to driver ahead
    - Keep distance from driver ahead
    - Accelerate if possible
    - Match speed of those ahead if within safety zone
    - Stop if new location would result in crash (0 distance to car ahead)
    """

    def __init__(self, location, gap=28, speed_limit=33, start_speed=27):
        self.location = location
        self.gap = gap
        self.desired_speed = speed_limit
        self.speed = start_speed
        self.size = 5
        self.bumper = 0
        self.update_bumper()

    def __str__(self):
        return 'Car(location={},bumper={},gap={},speed={})'.format(
                self.location, self.bumper, self.gap, self.speed)

    def __repr__(self):
        return self.__str__()

    def drive(self, car_ahead):

        if self.location + self.speed >= car_ahead.bumper:
            self.speed = 0
            self.location = car_ahead.bumper - 1
        elif self.location + self.speed > car_ahead.bumper - self.speed:
            self.speed = car_ahead.speed
        elif random.random() < 0.1:
            self.speed -= 2
            if self.speed < 0:
                self.speed = 0
        elif self.speed < self.desired_speed:
            self.speed += 2
            if self.speed > self.desired_speed:
                self.speed = self.desired_speed

        self.location += self.speed
        if self.location >= 1000:
            print("I'm off the road, man!")
            return 'off_the_road'
        else:
            return 'on_the_road'

    def update_bumper(self):
        if self.location - (self.size - 1) < 1000:
            self.bumper = self.location - (self.size - 1)
        else:
            self.bumper = self.location - 1000 - (self.size - 1)


class Road:
    """
    Responsibilities:
    - Hold length of road
    - Keep a list of vehicles on road
        - Initialize with number of cars
        - (1000 - sum(vehicle.size)) // len(self.vehicles)
    - Hold potential for slowdown

    Collaborators:
    - Car
    """
    def __init__(self):
        self.total_vehicle_space = (30 * 5)
        self.initial_gap = int((1000 - self.total_vehicle_space) / 30)
        self.vehicles = [Car((4 + int(33.333333333*n)), self.initial_gap) for n in range(30)]
        self.vehicles[-1].gap = (1000 - self.vehicles[-1].location)


class HighwaySim:
    """
    Responsibilities:
    - Have road place cars at beginning of road when they reach the end
    - Keep track of time (seconds)
    - Step through time (ticks)
        - For each car on Road, tell car behind new situation and allow it to react
    - Report stats; return traffic jam status
    - Pop, Append

    Collaborators:
    - Car
    - Road
    """

    def __init__(self):
        self.road = Road()
        self.ticks = 0
        self.is_traffic = []

    def run_sim(self, duration=1):
        while self.ticks < duration:
            self.iterate()
            self.ticks += 1
        if self.is_traffic.count(True) > 0:
            return True
        else:
            return False

    def iterate(self):
        off_the_road = []
        num_cars = len(self.road.vehicles)
        for idx in range(num_cars):
            v = self.road.vehicles[- idx - 1]
            if idx > 0:
                car_ahead = deepcopy(self.road.vehicles[- idx])
                if car_ahead.location < v.location:
                    car_ahead.location + 1000
                    car_ahead.update_bumper()
            else:
                car_ahead = deepcopy(self.road.vehicles[0])
                car_ahead.location += 1000
                if car_ahead.gap < car_ahead.speed:
                    car_ahead.location += car_ahead.gap
                else:
                    car_ahead.location += car_ahead.speed
                car_ahead.bumper = car_ahead.location - (car_ahead.size - 1)

            if v.drive(car_ahead) == 'off the road':
                off_the_road.append(- idx - 1)

            if car_ahead.bumper - v.location > 0:
                v.gap = car_ahead.bumper - v.location
            else:
                v.gap = car_ahead.bumper + 1000 - v.location

            v.update_bumper()

            if v.speed == 0:
                self.is_traffic.append(True)
            else:
                self.is_traffic.append(False)

        while len(off_the_road) > 0:
            off_car = self.road.vehicles.pop(-1)
            off_car.location -= 1000
            if off_car.location >= off_car.size - 1:
                off_car.update_bumper()
            else:
                off_car.bumper = off_car.location - (off_car.size -1) + 1000
            self.road.vehicles.insert(0, off_car)
            off_the_road.pop(0)









#
