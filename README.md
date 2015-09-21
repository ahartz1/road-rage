
# Road Rage: Finding the Ideal Speed Limit
### Assumptions
* Drivers want to go up to 120 km/hr (~75 mph).
* The average car is 5 meters long; this changes in "Nightmare Mode" with the addition of simulating commercial vehicles of length 25 meters.
* Drivers want at least a number of meters equal to their speed in meters/second between them and the next car.
* Drivers will accelerate 2 m/s<sup>2</sup> up to their desired speed as long as they have room to do so.
* If another car is too close, drivers will match that car's speed until they have room again.
* If a driver would hit another car by continuing, they stop (i.e., potentially trigger a traffic jam).
* Drivers will randomly (10% chance each second) slow by 2 m/s under normal conditions; this chance increases as indicated below for the bendy sections of the "Hard Mode".
* This section of road is one lane going one way.
* Drivers enter the road at the speed they left.
* Simulation starts with 30 cars per kilometer, evenly spaced.

## Normal Mode
We have a 1 kilometer section of road being built and do not know what the speed limit should be. This notebook simulates the 1 kilometer of road. Even though this road is not circular, the simulation treats it as such in order to generate a continuous flow of traffic. For your use in command-line applications, the `traffic_lib.py` library is in this repo.

## Hard Mode
We have a 7 kilometer section of road being built and do not know what the speed limit should be. This notebook simulates the 7 kilometers of road. Even though this road is not circular, the simulation treats it as such in order to generate a continuous flow of traffic. Again, for your use in command-line applications, the `traffic_lib.py` library is in this repo.
 * km 1: straight
 * km 2: bend (chance to slow + 40%)
 * km 3: straight
 * km 4: tight bend (chance to slow + 100%)
 * km 5: straight
 * km 6: slight bend (chance to slow + 20%)
 * km 7: straight

## Nightmare Mode

Calculates all of the above, but accounts for differing types of drivers.

Driver type      | Normal   | Aggressive | Commercial
-----------------|----------|------------|------------
Acceleration     | 2 m/s/s  | 5 m/s/s    | 1.5 m/s/s
Desired speed    | 120 km/h | 140 km/h   | 100 km/h
Vehicle size     | 5 m      | 5 m        | 25 m
Minimum spacing  | speed    | speed      | 2x speed
Slowing chance   | 10%/s    | 5%/s       | 10%/s
% of drivers     | 75%      | 10%        | 15%

* m = meters
* km = kilometers
* s = second
* h = hour

### To View This Notebook
Just click on the `road-rage.ipynb` file above.

### To Run This Notebook
#### System Requirements / Installation

* You will need to have **python&nbsp;3** installed on your machine. See [python's site](https://www.python.org/) for details.

* Clone this repo onto your machine.

* You will need to make sure that you have a virtual environment running in the folder that you intend to work from. [See this site for details if you're not familiar.](http://docs.python-guide.org/en/latest/dev/virtualenvs/) **Complete this step before attempting the below.**

* In your command-line program (such as Terminal on Mac&nbsp;OS&nbsp;X), navigate into the newly created repo. By default, this will be called `flipping-out`. Install the requirements file by runnning **`pip install -r requirements.txt`**.

#### Opening the Notebook
* Using a command-line program, navigate to the folder containing the downloaded file and run the following line: **`ipython notebook road-rage.ipynb`**

* **Note:** This will open in a browser window and take over the command-line program's window until you close out of IPython Notebook. If you have closed your browser window, but your command line is still running the notebook, kill the process by pressing `Ctrl+C` or quitting the program entirely.
