import random
from prettytable import PrettyTable

class Vehicle:
    def __init__(self, veh_id, origin, destination, time_to_reach_intersection, time_to_cross_intersection):
        self.ID = veh_id
        self.origin = origin
        self.destination = destination
        self.time_to_reach_intersection = time_to_reach_intersection
        self.time_to_cross_intersection = time_to_cross_intersection

# List of vehicles
vehicle_ids = set("emergency" + str(i) for i in range(10)) | set(str(i) for i in range(20))

# Ensure vehicle_ids has at least 31 unique IDs
while len(vehicle_ids) < 31:
    vehicle_ids.add(str(random.randint(20, 90)))

# Four arrays of request signal, each for each direction
north_queue = []
south_queue = []
east_queue = []
west_queue = []

# Arrays of confirmation signals, to show dequeue and queue to destination
# destination from north
N_E = []
N_S = []
N_W = []

# destination from south
S_E = []
S_N = []
S_W = []

# destination from east
E_W = []
E_S = []
E_N = []

# destination from west
W_E = []
W_S = []
W_N = []

def print_vehicles(queue, queue_name):
    table = PrettyTable()
    table.field_names = ["Vehicle #", "Vehicle ID"]

    for count, vehicle in enumerate(queue, 1):
        table.add_row([count, vehicle.ID])

    print(f"\n{queue_name} Queue:")
    print(table)

queue_order_NSEW = []

def pick_random_times():
    random_times = []
    for _ in range(6):
        origin = random.choice(['north', 'south', 'east', 'west'])
        time_to_reach = random.randint(1, 3)
        random_times.append((origin, time_to_reach))
    return random_times * 4

def queue_vehicle_request_from_origin(vehicle, origin):
    if vehicle.origin == 'north':
        north_queue.append(vehicle)
    elif vehicle.origin == 'south':
        south_queue.append(vehicle)
    elif vehicle.origin == 'east':
        east_queue.append(vehicle)
    elif vehicle.origin == 'west':
        west_queue.append(vehicle)

def random_NSEWvehicle_REQUESTS():
    print("\nTraffic flow:")
    random_times = pick_random_times()  # Get random times for each direction

    # Updated vehicle_count dictionary
    vehicle_count = {
        'north': {'east': 0, 'west_south': 0},
        'south': {'west': 0, 'east_north': 0},
        'east': {'south': 0, 'north_west': 0},
        'west': {'north': 0, 'south_east': 0}
    }

    table = PrettyTable()
    table.field_names = ["Index", "Vehicle ID", "Time to Reach", "Origin", "Destination", "message_byIM"]

    for index, (origin, time_to_reach) in enumerate(random_times):
        if sum(vehicle_count[origin].values()) >= 6:
            continue  # Skip this origin if it already has 6 vehicles

        veh_id = random.choice(list(vehicle_ids))
        vehicle_ids.remove(veh_id)  # Remove the used ID from the set

        available_destinations = ['east', 'west', 'north', 'south']
        available_destinations.remove(origin)

        destination = None
        for dest in ['east', 'west', 'north', 'south']:
            if dest in vehicle_count[origin] and vehicle_count[origin][dest] < 3 and dest + '_' + origin not in vehicle_count and vehicle_count[dest][origin] < 3:
                destination = dest
                break

        if destination is None:
            continue

        time_tocross = 20

        vehicle_instance = Vehicle(veh_id, origin, destination, time_to_reach, time_tocross)
        queue_vehicle_request_from_origin(vehicle_instance, origin)

        vehicle_count[origin][destination] += 1
        vehicle_count[destination][origin] += 1
        vehicle_count[dest + '_' + origin] = 1

        message_byIM = "REQUEST"
        table.add_row([index + 1, vehicle_instance.ID, vehicle_instance.time_to_reach_intersection, vehicle_instance.origin, vehicle_instance.destination, message_byIM])

    print(table)

random_NSEWvehicle_REQUESTS()

print_vehicles(north_queue, 'north')
print_vehicles(south_queue, 'south')
print_vehicles(east_queue, 'east')
print_vehicles(west_queue, 'west')
