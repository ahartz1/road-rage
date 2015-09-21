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

    def __init__(self, location, car_id, gap=28, speed_limit=33, start_speed=27):
        self.location = location
        self.gap = gap
        self.desired_speed = speed_limit
        self.speed = start_speed
        self.size = 5
        self.bumper = 0
        self.update_bumper()
        self.car_id = car_id
        self.acceleration = 2
        self.slowing_chance = 0.1

    def __str__(self):
        return 'Car(location={},car_id={},bumper={},gap={},speed={})'.format(
                self.location, self.car_id, self.bumper, self.gap, self.speed)

    def __repr__(self):
        return self.__str__()

    def drive(self, car_ahead, slow_factor):

        if self.location + self.speed >= car_ahead.bumper:
            self.speed = 0
            self.location = car_ahead.bumper - 1
        elif self.location + self.speed > car_ahead.bumper - self.safety_gap():
            self.speed = car_ahead.speed
        elif random.random() < (self.slowing_chance * slow_factor):
            self.speed -= 2
            if self.speed < 0:
                self.speed = 0
        elif self.speed < self.desired_speed:
            self.speed += self.acceleration
            if self.speed > self.desired_speed:
                self.speed = self.desired_speed

        self.location += self.speed
        self.bumper = self.location - self.size + 1
        if self.location >= 1000:
            return True
        else:
            return False

    def safety_gap(self):
        return self.speed

    def update_bumper(self):
        self.bumper = self.location - self.size + 1


class BigRig(Car):
    def __init__(self):
        super().__init__(self, location, car_id, speed_limit=28)
        self.size = 25
        self.acceleration = 1.5

    def safety_gap(self):
        return self.speed * 2

class Aggressive(Car):
    def __init__(self):
        super().__init__(self, location, car_id, speed_limit=39)
        self.acceleration = 5
        self.slowing_chance = 0.05

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
    def __init__(self, speed_limit=33, slow_factor=1):
        self.speed_limit = speed_limit
        self.slow_factor = slow_factor
        self.initial_total_vehicle_space = (30 * 5)
        self.initial_gap = int((1000 - self.initial_total_vehicle_space) / 30)
        self.vehicles = []
        self.place_cars()

    def place_cars(self):
        self.vehicles = [Car((4 + int(33.333333333*n)),n, self.initial_gap,
                         speed_limit=self.speed_limit) for n in range(30)]
        self.vehicles[-1].gap = (1000 - self.vehicles[-1].location)

    def num_cars(self):
        return len(self.vehicles)


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

    def __init__(self, speed_limit=33, mode=0):
        self.speed_limit = speed_limit
        self.mode = mode
        self.roads = []
        self.ticks = 0
        self.car_speeds = []
        self.sim_data = []
        self.tick_graph = []
        self.sim_graph = []
        self.mean = None
        self.add_roads()
        self.num_roads = len(self.roads)

    def add_roads(self):
        if self.mode == 0:
            self.roads.append(Road(self.speed_limit))
        elif self.mode == 1:
            self.roads.append(Road(self.speed_limit))
            self.roads.append(Road(self.speed_limit, slow_factor=1.4))
            self.roads.append(Road(self.speed_limit))
            self.roads.append(Road(self.speed_limit, slow_factor=2))
            self.roads.append(Road(self.speed_limit))
            self.roads.append(Road(self.speed_limit, slow_factor=1.2))
            self.roads.append(Road(self.speed_limit))

    def run_sim(self, duration=1):
        while self.ticks < duration:
            self.iterate()
            self.ticks += 1
        #TODO: Update to get a mean of each road segment?
        self.mean = np.mean(np.array(self.sim_data[-1]))
        return self.mean

    def iterate(self):
        self.car_speeds = []
        self.tick_graph = np.repeat(1, (1000 * self.num_roads))
        off_the_road = [[] for _ in range(self.num_roads)]
        for n, r in enumerate(self.roads):
            r_num_cars = r.num_cars()
            del_bumper = False
            for idx in range(r_num_cars):
                v = r.vehicles[- idx - 1]
                if idx > 0:
                    car_ahead = deepcopy(r.vehicles[- idx])
                else:
                    # If we're looking at the last car on the road, the "next"
                    # car will be the [1] car if only bumper is on previous road
                    # In the 1 road scenario, bumper only is moved to begining
                    # and we add 1000 to bumper to accommodate
                    if n < (self.num_roads - 1) and self.num_roads > 1:
                        if len(self.roads[n + 1].vehicles) > 0:
                            car_ahead = deepcopy(self.roads[n + 1].vehicles[0])
                        else:
                            car_ahead = Car(150, 0)
                        if car_ahead.location - car_ahead.size + 1 < 0:
                            if len(self.roads[n + 1].vehicles) > 2:
                                car_ahead = deepcopy(self.roads[n + 1].vehicles[1])
                            else:
                                car_ahead.location = 150
                    elif n == (self.num_roads - 1) and self.num_roads > 1:
                        if len(self.roads[0].vehicles) > 0:
                            car_ahead = deepcopy(self.roads[0].vehicles[0])
                        else:
                            car_ahead = Car(150, 0)
                        if car_ahead.location - car_ahead.size + 1 < 0:
                            if len(self.roads[0].vehicles) > 1:
                                car_ahead = deepcopy(self.roads[0].vehicles[1])
                            else:
                                car_ahead.location = 150
                    else:
                        car_ahead = deepcopy(self.roads[0].vehicles[0])

                    car_ahead.location += 1000
                    if car_ahead.gap < car_ahead.speed:
                        car_ahead.location += car_ahead.gap
                    else:
                        car_ahead.location += car_ahead.speed
                    car_ahead.bumper = car_ahead.location - car_ahead.size + 1

                if v.location - v.size + 1 < 0 and self.num_roads > 1:
                    del_bumper = True

                if v.drive(car_ahead, r.slow_factor):
                    off_the_road[n].append(- idx - 1)

                if car_ahead.bumper - v.location > 0:
                    v.gap = car_ahead.bumper - v.location
                else:
                    v.gap = car_ahead.bumper + 1000 - v.location

                self.car_speeds.append(v.speed)

                if v.location <= 1000:
                    self.tick_graph[(v.bumper + (n * 1000)):
                                    (v.location + 1 + (n * 1000))] = 0
                else:
                    if v.bumper <= 1000:
                        self.tick_graph[(v.bumper + (n * 1000)):
                                        (v.location + 1001 + (n * 1000))] = 0
                    else:
                        self.tick_graph[(v.bumper + 1000 + (n * 1000)):
                                        (v.location + 1001 + (n * 1000))] = 0

            # Delete cars who started with only a bumper in this road section
            if del_bumper and self.num_roads > 1:
                del r.vehicles[-1]

        # Add cars whose location is beyond this road section to next road section
        # Keep car in current section if bumper is still inside this road section
        for m, off_list in enumerate(off_the_road):
            bumper_only = None
            while len(off_the_road[m]) > 0:
                off_car = deepcopy(self.roads[m].vehicles[-1])
                off_car.location -= 1000
                if off_car.location >= off_car.size - 1:
                    off_car.update_bumper()
                else:
                    off_car.bumper = off_car.location - off_car.size + 1 + 1000
                    if self.num_roads > 1:
                        bumper_only = deepcopy(self.roads[m].vehicles[-1])
                del self.roads[m].vehicles[-1]
                if m < (self.num_roads - 1) and self.num_roads > 1:
                    self.roads[m + 1].vehicles.insert(0, off_car)
                else:
                    self.roads[0].vehicles.insert(0, off_car)
                del off_the_road[m][0]
            if self.num_roads > 1 and type(bumper_only) == Car:
                self.roads[m].vehicles.append(bumper_only)

        self.sim_data.append(self.car_speeds)
        self.sim_graph.append(self.tick_graph.tolist())














#
