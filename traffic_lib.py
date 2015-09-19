import math
import numpy as np
import random


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

    def __init__(self, location, gap=28, speed_limit=33, start_speed=28):
        self.location = location
        self.gap = gap
        self.desired_speed = speed_limit
        self.speed = start_speed
        self.size = 5
        self.bumper = 0
        self.update_bumper()

    def __str__(self):
        return 'Car(location={},gap={},speed={})'.format(self.location, self.gap, self.speed)

    def __repr__(self):
        return self.__str__()

    def drive(self, car_ahead):

        if self.stop(car_ahead):
            pass

        elif self.match_speed(car_ahead):
            pass

        elif self.random_slowdown(car_ahead):
            pass

        elif self.accelerate(car_ahead):
            pass

        self.update_location(car_ahead)

    def stop(self, car_ahead):
        if self.location + self.speed >= car_ahead.bumper:
            self.speed = 0
            self.location = car_ahead.bumper - 1
            return True

    def match_speed(self, car_ahead):
        if self.location + self.speed < car_ahead.bumper - self.speed:
            self.speed = car_ahead.speed
            return True

    def random_slowdown(self, car_ahead):
        if random.random() < 0.1:
            self.speed -= 2
            if self.speed < 0:
                self.speed = 0
            return True

    def accelerate(self, car_ahead):
        if self.speed < self.desired_speed:
            if self.desired_speed - self.speed <= 2:
                self.speed = self.desired_speed
            else:
                self.speed += 2
            return True

    def update_location(self, car_ahead):
        self.location += self.speed
        self.gap = car_ahead.bumper - self.location

    def update_bumper(self):
        if self.location >= self.size - 1:
            self.bumper = self.location - (self.size - 1)
        else:
            self.bumper = self.location - self.size + 1000
            # Note that to make the bumper location correct, we need to add 1 when adding 1000


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
    def __init__(self, num_trucks=0):
        self.total_vehicle_space = ((30 - num_trucks) * 5) + (num_trucks * 25)
        self.initial_gap = (1000 - self.total_vehicle_space) // 30
        self.vehicles = [Car((4 + 33*n), self.initial_gap) for n in range(30 - num_trucks)]

        if num_trucks > 0:
            [self.vehicles.append(Truck() for _ in range(num_trucks))]

        self.vehicles[-1].gap = (1000 - self.vehicles[-1].location)

    def reinsert_car(self):
        if 1000 <= self.vehicles[-1].location:
            last_car = self.vehicles.pop(-1)
            self.vehicles.insert(0, Car(last_car.location - 1000, last_car.gap))
            if self.vehicles[0].location >= self.vehicles[0].size - 1:
                self.vehicles[0].update_bumper()
            else:
                self.vehicles[0].bumper = self.vehicles[0].location - (self.vehicles[0].size -1) + 1000


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
        for idx, v in enumerate(self.road.vehicles):
            if idx > 0:
                car_ahead = self.road.vehicles[- idx - 1]
            else:
                car_ahead = Car(self.road.vehicles[0].location + 1000, self.road.vehicles[0].gap, 33,
                                self.road.vehicles[0].speed)

            v.drive(car_ahead)

            if v.speed == 0:
                self.is_traffic.append(True)
            else:
                self.is_traffic.append(False)

        for n in range(30):
            self.road.reinsert_car()
