import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import time
import heapq
from prettytable import PrettyTable
import copy
import threading
import csv
from queue import Queue
import datetime

current_node='not_updating'

class Vehicle:
    def __init__(self, ID, origin, destination, time_to_reach_intersection, time_to_cross, current_node):
        self.ID = ID

        if origin.lower() in ['east', 'west', 'north', 'south']:
            self.origin = origin
        elif destination.lower() in ['east', 'west', 'north', 'south']:
            self.destination = destination
        else:
            raise ValueError("Invalid origin.")

        self.destination = destination
        self.time_to_reach_intersection = float(time_to_reach_intersection)
        self.time_to_cross = time_to_cross
        self.current_node = current_node

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

# # destination from east
E_W = []
E_S = []
E_N = []

# destination from west
W_E = []
W_S = []
W_N = []

# Queues the REQUEST signal and assumes they all get CONFIRM signal from Int. BEFORE MOVING
NO=[]
NL=[]
NR=[]
NS=[]

SR=[]
SL=[]
SO=[]
SS=[]

EO=[]
EL=[]
ER=[]
ES=[]

WR=[]
WL=[]
WO=[]
WS=[]


class Node:
    def __init__(self):
        self.vehicles = []
        self.time = 0
        self.presence = False

Node1 = Node()
Node2 = Node()
Node3 = Node()
Node4 = Node()
Node5 = Node()
Node6 = Node()
Node7 = Node()
Node8 = Node()
Node9 = Node()
Node10 = Node()
Node11 = Node()
Node12 = Node()
Node13 = Node()
Node14 = Node()
Node15 = Node()
Node16 = Node()

Exited_north = Node()
Exited_south = Node()
Exited_east = Node()
Exited_west = Node()

all_queues = [SO, SR, SL, NO, NR, NL, EO, ER, EL, WO, WR, WL, SS, NS, WS, ES]  

queue_order_NSEW=[]
FROsorted_queue=[]
node_headway_seconds=1

# Initialize current_node to None
#current_node = None 

# Initialize vehicle IDs and the queue
vehicle_ids = set("emergency" + str(i) for i in range(20)) | set(str(i) for i in range(40))
def print_queue(queue):
    if not queue:  # Check if the queue is empty
        print("\nEmpty Queue!!")
    else:
        count = 0
        print("\n")
        for vehicle in queue:
            count += 1
            print("Vehicle #", count, ".", vehicle.ID)

def print_vehicles(queue, queue_name):
    #print(queue, queue_name)

    table = PrettyTable()
    table.field_names = ["Index", "Vehicle ID", "Time to Reach", "Origin", "Current Node", "Destination"]
    for count, vehicle in enumerate(queue, 1): #initialize count to one
        
        table.add_row([count, vehicle.ID, vehicle.time_to_reach_intersection, vehicle.origin, vehicle.current_node, vehicle.destination])
        

    print(f"\n{queue_name} Queue:")
    print(table)


####################  STORAGE ZONE  #####################################        
def queue_vehicle_request_from_origin(vehicle, origin):
    if vehicle.origin == 'north':
        north_queue.append(vehicle)
        if vehicle.destination == 'south':
            #if len(SO) < 3: #needs for Networkx
            NO.append(vehicle)
            vehicle.current_node = 'NO'
        
        elif vehicle.destination == 'east':
            #if len(SR) < 3:
            NL.append(vehicle)
            vehicle.current_node = 'NL'

        elif vehicle.destination == 'west':
            #if len(SL) < 3:
            NR.append(vehicle)
            vehicle.current_node = 'NR'
       
    elif vehicle.origin == 'south':
        south_queue.append(vehicle)
        if vehicle.destination == 'north':
            #if len(NO) < 3:
            SO.append(vehicle)
            vehicle.current_node = 'SO'
        
        elif vehicle.destination == 'east':
            #if len(NL) < 3:
            SR.append(vehicle)
            vehicle.current_node = 'SR'

        elif vehicle.destination == 'west':
            #if len(NR) < 3:
            SL.append(vehicle)
            vehicle.current_node = 'SL'
    
    elif vehicle.origin == 'east':
        east_queue.append(vehicle)
        if vehicle.destination == 'north':
            #if len(ER) < 3:
            ER.append(vehicle)
            vehicle.current_node = 'ER'
        
        elif vehicle.destination == 'south':
            #if len(EL) < 3:
            EL.append(vehicle)
            vehicle.current_node = 'EL'

        elif vehicle.destination == 'west':
            #if len(EO) < 3:
            EO.append(vehicle)
            vehicle.current_node = 'EO'
    
    elif vehicle.origin == 'west':
        west_queue.append(vehicle)
        if vehicle.destination == 'north':

            WL.append(vehicle)
            vehicle.current_node = 'WL'
        
        elif vehicle.destination == 'east':
            #print("I am here")
            WO.append(vehicle)
            vehicle.current_node = 'WO'
        

        elif vehicle.destination == 'south':
            #WR.vehicle.current_node = 'WR'
            WR.append(vehicle)
            vehicle.current_node = 'WR'
            

    

def random_NSEWvehicle_REQUESTS():
    global queue_order_NSEW, current_node
    # Initialize the queue
    queue_order_NSEW = []
    count=1
    print("\nTraffic flow:")
    # Randomly queue the north and south directions with vehicles
    table = PrettyTable()
    table.field_names = ["Index", "Vehicle ID", "Time to Reach", "Origin", "Dest", "Current Node", "Message_byIM"]

    origin_counts = {'east': 0, 'west': 0, 'north': 0, 'south': 0}
    destination_counts = {'south': 0, 'north': 0, 'east': 0, 'west': 0}


    for origin in random.choices(['east', 'west', 'north', 'south'], k=36):

        if origin_counts[origin] >= 9:
            continue
            
        veh_id = random.choice(list(vehicle_ids))
        vehicle_ids.remove(veh_id)  # Remove the used ID from the set
        
        available_destinations = ['east', 'west', 'north', 'south']
        available_destinations.remove(origin)  # Remove the origin from the available destinations
        destination = random.choice(available_destinations)

        time_tocross = 20
        
        # Randomly assign distinct times to each vehicle in the destination lane
        time_to_reach_list = random.sample([1, 2, 3], 3)

         # Use the origin_counts to access the correct time from the time_to_reach_list
        time_to_reach_intersection = time_to_reach_list[destination_counts[destination] % 3]

        #current_node='abc'

        vehicle_instance = Vehicle(veh_id, origin, destination, time_to_reach_intersection, time_tocross, current_node)
        
        queue_vehicle_request_from_origin(vehicle_instance, origin)
     
        origin_counts[origin] += 1
        
       
        queue_order_NSEW.append(vehicle_instance)

        message_byIM = "REQUEST"
        table.add_row([count, vehicle_instance.ID, time_to_reach_intersection, vehicle_instance.origin, vehicle_instance.destination, vehicle_instance.current_node, message_byIM])
        count+=1

        destination_counts[destination] += 1  # Update destination_counts
        #Check if the destination queue has less than 3 vehicles before populating
        if (vehicle_instance.destination == 'south' and len(SO) >= 3) or \
           (vehicle_instance.destination == 'north' and len(NO) >= 3) or \
           (vehicle_instance.destination == 'east' and len(EO) >= 3) or \
           (vehicle_instance.destination == 'west' and len(WO) >= 3) or \
           (vehicle_instance.destination == 'south' and len(SR) >= 3) or \
           (vehicle_instance.destination == 'north' and len(NR) >= 3) or \
           (vehicle_instance.destination == 'east' and len(ER) >= 3) or \
           (vehicle_instance.destination == 'west' and len(WR) >= 3) or \
           (vehicle_instance.destination == 'south' and len(SL) >= 3) or \
           (vehicle_instance.destination == 'north' and len(NL) >= 3) or \
           (vehicle_instance.destination == 'east' and len(EL) >= 3) or \
           (vehicle_instance.destination == 'west' and len(WL) >= 3):
            continue
    #print_queue(queue_order_NSEW)
    print(table)

  #print_vehicles(WO, 'WO')
        # print_vehicles(WR, 'WR')
        # print_vehicles(WL, 'WL')

        # print_vehicles(EO, 'EO')
        # print_vehicles(ER, 'ER')
        # print_vehicles(EL, 'EL')

def arrange_vehicle_requests_by_time(queue_order):
    # Sort the vehicles in descending order based on time to reach 
    # First Ready Out
    global FROsorted_queue
    FROsorted_queue = sorted(queue_order, key=lambda vehicle: vehicle.time_to_reach_intersection)

    # Create a table
    table = PrettyTable()
    table.field_names = ["Index", "Vehicle ID", "Time to Reach", "Origin", "Current Node", "message_byIM"]

    # Print the new order of vehicles and add rows to the table
    print("\nNew order of vehicles (First one Ready goes First):")
    for index, vehicle in enumerate(FROsorted_queue):
        message_byIM = "CONFIRM"
        table.add_row([index + 1, vehicle.ID, vehicle.time_to_reach_intersection, vehicle.origin, vehicle.current_node, message_byIM])
  
    # Sort the destination queues based on time_to_reach_intersection for destination queues
    destination_queues = [NO, NL, NR, SO, SR, SL, EO, EL, ER, WO, WR, WL]

    for queue in destination_queues:
        queue.sort(key=lambda vehicle: vehicle.time_to_reach_intersection)

    # Print the table
    print(table)

    return FROsorted_queue

#random_NSEWvehicle_REQUESTS() #None after len>3.. change that
# print_vehicles(WO, 'WO')
# print_vehicles(WR, 'WR')
# print_vehicles(WL, 'WL')

# print_vehicles(EO, 'EO')
# print_vehicles(ER, 'ER')
# print_vehicles(EL, 'EL')

#current_node not available outside randomn and arrange
#arrange_vehicle_requests_by_time(queue_order_NSEW)

# Function to get the name of the queue from its value
def get_queue_name(queue_value):
    # Create a dictionary to map the queue names to their corresponding values
    queues_dict = {
        'SO': SO,
        'SR': SR,
        'SL': SL,
        'NO': NO,
        'NR': NR,
        'NL': NL,
        'EO': EO,
        'ER': ER,
        'EL': EL,
        'WO': WO,
        'WR': WR,
        'WL': WL,

        'SS': SS,
        'NS': NS,
        'ES': ES,
        'WS': WS,
    }

    for name, value in queues_dict.items():
        if value is queue_value:
            return name
    return None

def Yield_IM(queue_order_NSEW):
    global all_queues
    tlost=1
    treenter=1
    # Exclude empty queues from all_queues
    #all_queues = [queue for queue in all_queues if queue]

 
    # Create a dictionary to map the second letter to the adjacent queue identifier
    adjacent_yielding_queue_map = {
        'L': 'O',  # For 'LEFT', adjacent queue is 'OPPOSITE' (e.g., SL -> SO)
        'O': 'R',  # For 'OPPOSITE', adjacent queue is 'RIGHT' (e.g., SO -> SR)
        'R': 'S',  # For 'RIGHT', adjacent queue is 'SHOUDLER' (e.g., ER -> ES)
        
    }
    table = PrettyTable()
    table.field_names = ["Vehicle ID", "Time to Reach", "Origin", "Current Node", "Yield Node", "Dest"]

    for queue in all_queues:
        for vehicle in queue:
            if vehicle.ID.startswith('emergency'):
                
                queue_name = get_queue_name(queue)
                # Find the adjacent queue based on the second letter of the queue name
                second_letter=queue_name[1]
                
                # Get the adjacent queue identifier using the dictionary (SO->SL)
                adjacent_queue_id = queue_name[0] + adjacent_yielding_queue_map[second_letter]

                # Update time
                vehicle.time_to_reach_intersection = vehicle.time_to_reach_intersection + tlost + treenter
                table.add_row([vehicle.ID, vehicle.time_to_reach_intersection, vehicle.origin, vehicle.current_node, adjacent_queue_id, vehicle.destination])
                # Print direction and time for the emergency vehicle
                #print(f"Emergency Vehicle {vehicle.ID} at {vehicle.origin}, {queue_name} should go to {adjacent_queue_id} (dest: {vehicle.destination})")
    print("\nEmergency vehicle order - Changed time with reentry")
    print(table)
    #return adjacent_queue_id

#Yield_IM(queue_order_NSEW)

def thread_save(queue):
    direction = get_queue_name(queue)  # For title
    filename = f'vehicle_data_{direction}.csv'
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['Vehicle ID', 'Time to Reach', 'Origin', 'Current Node', 'Destination']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        while True:
            # Write vehicle data row by row
            for vehicle in queue:
                writer.writerow({
                    # 'Vehicle ID': vehicle.ID,
                    # 'Time to Reach': vehicle.time_to_reach_intersection,
                    # 'Origin': vehicle.origin,
                    # 'Current Node': vehicle.current_node,
                    # 'Destination': vehicle.destination
                    'Vehicle ID': 1,
                    'Time to Reach': 2,
                    'Origin': 3,
                    'Current Node': 4,
                    'Destination': 5
                })
            # Sleep for some time before saving data again
            #time.sleep(2)  # Adjust the sleep time according to your needs

            



# def thread_save(queues):
#     with open('C:/Users/ceenu/OneDrive/Desktop/vehicleIM_data/all_queues_data.csv', 'a', newline='') as csvfile:
#         fieldnames = ['Queue', 'Vehicle ID', 'Time to Reach', 'Origin', 'Current Node', 'Destination']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()
#         for queue_name, queue in queues.items():
#                 for vehicle in queue:
#                     print("##############################", queue_name)

#         while True:
#             for queue_name, queue in queues.items():
#                 for vehicle in queue:
#                     writer.writerow({
#                         'Queue': queue_name,
#                         'Vehicle ID': vehicle.ID,
#                         'Time to Reach': vehicle.time_to_reach_intersection,
#                         'Origin': vehicle.origin,
#                         'Current Node': vehicle.current_node,
#                         'Destination': vehicle.destination
#                     })
#             # Sleep for some time before saving data again
#             time.sleep(2)  # Adjust the sleep time according to your needs

# Create and start the thread for saving all queue data
save_all_queues = {
    'SR': SR, 'SL': SL, 'NO': NO, 'NR': NR, 'NL': NL, 'EO': EO, 'ER': ER, 'EL': EL, 'WO': WO, 'WR': WR, 'WL': WL,
    'SS': SS, 'NS': NS, 'ES': ES, 'WS': WS
}

#a:append




# Create and start the thread for saving queue data
queues_to_save = {
        'SR': SR,
        'SL': SL,
        'NO': NO,
        'NR': NR,
        'NL': NL,
        'EO': EO,
        'ER': ER,
        'EL': EL,
        'WO': WO,
        'WR': WR,
        'WL': WL,

        'SS': SS,
        'NS': NS,
        'ES': ES,
        'WS': WS}

# Create and start the thread for saving all queue data
#all_queues = [SR, SL, NO, NR, NL, EO, ER, EL, WO, WR, WL, SS, NS, ES, WS]

# Create and start a thread for each queue
for queue in all_queues:
    save_thread = threading.Thread(target=thread_save, args=(queue,))
    save_thread.start()

# Wait for the save thread to finish (You can set a timeout or use a signal handler to stop the thread gracefully)
# save_thread.join()

# Define a function to check if NSEW has 10 or more vehicles
def check_NSEW_length():
    return len(queue_order_NSEW) >= 10

# Function to run random_NSEWvehicle_REQUESTS, arrange_vehicle_requests_by_time, and Yield_IM (STORAGE ZONE)
def thread_populating():
    while not check_NSEW_length():
        
        random_NSEWvehicle_REQUESTS()
        arrange_vehicle_requests_by_time(queue_order_NSEW)
        Yield_IM(queue_order_NSEW)

# Create and start the thread
populating_thread = threading.Thread(target=thread_populating)
populating_thread.start()

# Wait for the populating thread to finish (You can set a timeout or use a signal handler to stop the thread gracefully)
#populating_thread.join()

# CONFLICT ZONE MOVEMENT
def define_Nodes(incoming):
    global Node1, Node2, Node3, Node4, Node5, Node6, Node7, Node8, Node9, Node10, Node11, Node12, Node13, Node14, Node15, Node16, Exited_north, Exited_south, Exited_east, Exited_west
    count=0
    # for j in incoming:
    #     print(j.ID)

    

    for i in range(len(incoming)):
        
        veh = incoming[0]  # starting from the first vehicle and onwards
        # print(i,"\n")
        # print(incoming,"\n")
        # print(veh,"\n")

        if veh.origin == 'south':
            if veh.destination == 'north':
                while not (Node1.presence or Node2.presence or Node3.presence or Node4.presence):
                    if incoming[0].ID == veh.ID:
                        incoming.pop(0)
                        Node1.vehicles.append(veh.ID)
                        Node1.presence = True
                        Node1.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"Vehicle {veh.ID} entered Node1 at time {Node1.time}")
                        time.sleep(node_headway_seconds)

                        Node1.vehicles.pop(0)
                        Node1.presence = False
                        Node1.time = 0
                        Node2.vehicles.append(veh.ID)
                        Node2.presence = True
                        Node2.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"Vehicle {veh.ID} entered Node2 at time {Node2.time}")
                        time.sleep(node_headway_seconds)

                        Node2.vehicles.pop(0)
                        Node2.presence = False
                        Node2.time = 0
                        Node3.vehicles.append(veh.ID)
                        Node3.presence = True
                        Node3.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"Vehicle {veh.ID} entered Node3 at time {Node3.time}")
                        time.sleep(node_headway_seconds)

                        Node3.vehicles.pop(0)
                        Node3.presence = False
                        Node3.time = 0
                        Node4.vehicles.append(veh.ID)
                        Node4.presence = True
                        Node4.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"Vehicle {veh.ID} entered Node4 at time {Node4.time}")
                        time.sleep(node_headway_seconds)

                        Node4.vehicles.pop(0)
                        Node4.presence = False
                        Node4.time = 0
                        Exited_north.vehicles.append(veh.ID)
                        Exited_north.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"Vehicle {veh.ID} exited to north at time {Exited_north.time}")
                        time.sleep(node_headway_seconds)
                        break

            if veh.destination == 'west':
                while not (Node6.presence or Node8.presence or Node11.presence or Node10.presence):
                    if incoming[0].ID == veh.ID:
                        incoming.pop(0)
                        Node6.vehicles.append(veh.ID)
                        Node6.presence = True
                        Node6.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"Vehicle {veh.ID} entered Node6 at time {Node6.time}")
                        time.sleep(node_headway_seconds)

                        Node6.vehicles.pop(0)
                        Node6.presence = False
                        Node6.time = 0
                        Node8.vehicles.append(veh.ID)
                        Node8.presence = True
                        Node8.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"Vehicle {veh.ID} entered Node8 at time {Node8.time}")
                        time.sleep(node_headway_seconds)

                        Node8.vehicles.pop(0)
                        Node8.presence = False
                        Node8.time = 0
                        Node11.vehicles.append(veh.ID)
                        Node11.presence = True
                        Node11.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"Vehicle {veh.ID} entered Node11 at time {Node11.time}")
                        time.sleep(node_headway_seconds)

                        Node11.vehicles.pop(0)
                        Node11.presence = False
                        Node11.time = 0
                        Node10.vehicles.append(veh.ID)
                        Node10.presence = True
                        Node10.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"Vehicle {veh.ID} entered Node10 at time {Node10.time}")
                        time.sleep(node_headway_seconds)

                        Node10.vehicles.pop(0)
                        Node10.presence = False
                        Node10.time = 0
                        Exited_west.vehicles.append(veh.ID)
                        Exited_west.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"Vehicle {veh.ID} exited to west at time {Exited_west.time}")
                        time.sleep(node_headway_seconds)
                        break

            if veh.destination == 'east':
                if incoming[0].ID == veh.ID:
                    incoming.pop(0)
                    Exited_east.vehicles.append(veh.ID)
                    Exited_east.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                    print(f"For {veh.origin} to {veh.destination}\n")
                    print(f"Vehicle {veh.ID} exited to (righ turn) east at time {Exited_east.time}")
                    time.sleep(node_headway_seconds)
                    break

        if veh.origin == 'north':
            print(veh.ID)
            if veh.destination == 'east':
                while not (Node16.presence or Node15.presence or Node3.presence or Node5.presence):
                    # if not incoming:
                    #     break
                    print(count)
                    if incoming[0].ID == veh.ID:
                        print(veh.ID, " in east")
                        incoming.pop(0)
                        Node16.vehicles.append(veh)
                        Node16.presence = True
                        Node16.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"Vehicle {veh.ID} entered Node16 at time {Node16.time}")
                        time.sleep(node_headway_seconds)

                        Node16.vehicles.pop(0)
                        Node16.presence = False
                        Node16.time = 0
                        Node15.vehicles.append(veh)
                        Node15.presence = True
                        Node15.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"Vehicle {veh.ID} entered Node15 at time {Node15.time}")
                        time.sleep(node_headway_seconds)

                        Node15.vehicles.pop(0)
                        Node15.presence = False
                        Node15.time = 0
                        Node3.vehicles.append(veh)
                        Node3.presence = True
                        Node3.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"Vehicle {veh.ID} entered Node3 at time {Node3.time}")
                        time.sleep(node_headway_seconds)

                        Node3.vehicles.pop(0)
                        Node3.presence = False
                        Node3.time = 0
                        Node5.vehicles.append(veh)
                        Node5.presence = True
                        Node5.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"Vehicle {veh.ID} entered Node5 at time {Node5.time}")
                        time.sleep(node_headway_seconds)

                        Node5.vehicles.pop(0)
                        Node5.presence = False
                        Node5.time = 0
                        Exited_east.vehicles.append(veh)
                        Exited_east.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"Vehicle {veh.ID} exited to east at time {Exited_east.time}")
                        time.sleep(node_headway_seconds)
                        break
                        #Node16.presence, Node15.presence, Node3.presence, Node5.presence = False, False, False, False
                        # count+=1
                        # if count==len(incoming):
                        #     break
                        #i+=1
            if veh.destination == 'south':
                while not (Node13.presence or Node12.presence or Node11.presence or Node9.presence):
                    # if not incoming:
                    #     break
                    

                    if incoming[0].ID == veh.ID:
                        incoming.pop(0)
                        Node13.vehicles.append(veh)
                        Node13.presence = True
                        Node13.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"Vehicle {veh.ID} entered Node13 at time {Node13.time}")
                        time.sleep(node_headway_seconds)

                        Node13.vehicles.pop(0)
                        Node13.presence = False
                        Node13.time = 0
                        Node12.vehicles.append(veh)
                        Node12.presence = True
                        Node12.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"Vehicle {veh.ID} entered Node12 at time {Node12.time}")
                        time.sleep(node_headway_seconds)

                        Node12.vehicles.pop(0)
                        Node12.presence = False
                        Node12.time = 0
                        Node11.vehicles.append(veh)
                        Node11.presence = True
                        Node11.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"Vehicle {veh.ID} entered Node11 at time {Node11.time}")
                        time.sleep(node_headway_seconds)

                        Node11.vehicles.pop(0)
                        Node11.presence = False
                        Node11.time = 0
                        Node9.vehicles.append(veh)
                        Node9.presence = True
                        Node9.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"Vehicle {veh.ID} entered Node9 at time {Node9.time}")
                        time.sleep(node_headway_seconds)

                        Node9.vehicles.pop(0)
                        Node9.presence = False
                        Node9.time = 0
                        Exited_south.vehicles.append(veh)
                        Exited_south.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"Vehicle {veh.ID} exited to south at time {Exited_south.time}")
                        time.sleep(node_headway_seconds)
                        break
                        # count+=1
                        # if count==len(incoming):
                        #     break
                    
            if veh.destination == 'west':
                # if not incoming:
                #     break
                if incoming[0].ID == veh.ID:
                    incoming.pop(0)
                    Exited_east.vehicles.append(veh)
                    Exited_east.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                    print(f"For {veh.origin} to {veh.destination}\n")
                    print(f"Vehicle {veh.ID} exited to (right turn) east at time {Exited_east.time}")
                    time.sleep(node_headway_seconds)
                    break
                # count+=1
                # if count==len(incoming):
                #     break

        if veh.origin == 'east':
            if veh.destination == 'south':
                while not (Node5.presence or Node2.presence or Node7.presence or Node6.presence):
                    if incoming[0].ID == veh.ID:
                        incoming.pop(0)
                        Node5.vehicles.append(veh.ID)
                        Node5.presence = True
                        Node5.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"Vehicle {veh.ID} entered Node5 at time {Node5.time}")
                        time.sleep(node_headway_seconds)

                        Node5.vehicles.pop(0)
                        Node5.presence = False
                        Node5.time = 0
                        Node2.vehicles.append(veh.ID)
                        Node2.presence = True
                        Node2.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"Vehicle {veh.ID} entered Node2 at time {Node2.time}")
                        time.sleep(node_headway_seconds)

                        Node2.vehicles.pop(0)
                        Node2.presence = False
                        Node2.time = 0
                        Node7.vehicles.append(veh.ID)
                        Node7.presence = True
                        Node7.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"Vehicle {veh.ID} entered Node7 at time {Node7.time}")
                        time.sleep(node_headway_seconds)

                        Node7.vehicles.pop(0)
                        Node7.presence = False
                        Node7.time = 0
                        Node6.vehicles.append(veh.ID)
                        Node6.presence = True
                        Node6.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"Vehicle {veh.ID} entered Node6 at time {Node6.time}")
                        time.sleep(node_headway_seconds)

                        Node6.vehicles.pop(0)
                        Node6.presence = False
                        Node6.time = 0
                        Exited_south.vehicles.append(veh.ID)
                        Exited_south.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"Vehicle {veh.ID} exited to south at time {Exited_south.time}")
                        time.sleep(node_headway_seconds)
                        break

            if veh.destination == 'west':
                while not (Node4.presence or Node15.presence or Node14.presence or Node13.presence):
                    if incoming[0].ID == veh.ID:
                        incoming.pop(0)
                        Node4.vehicles.append(veh.ID)
                        Node4.presence = True
                        Node4.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"Vehicle {veh.ID} entered Node4 at time {Node4.time}")
                        time.sleep(node_headway_seconds)

                        Node4.vehicles.pop(0)
                        Node4.presence = False
                        Node4.time = 0
                        Node15.vehicles.append(veh.ID)
                        Node15.presence = True
                        Node15.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"Vehicle {veh.ID} entered Node15 at time {Node15.time}")
                        time.sleep(node_headway_seconds)

                        Node15.vehicles.pop(0)
                        Node15.presence = False
                        Node15.time = 0
                        Node14.vehicles.append(veh.ID)
                        Node14.presence = True
                        Node14.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"Vehicle {veh.ID} entered Node14 at time {Node14.time}")
                        time.sleep(node_headway_seconds)

                        Node14.vehicles.pop(0)
                        Node14.presence = False
                        Node14.time = 0
                        Node13.vehicles.append(veh.ID)
                        Node13.presence = True
                        Node13.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"Vehicle {veh.ID} entered Node13 at time {Node13.time}")
                        time.sleep(node_headway_seconds)

                        Node13.vehicles.pop(0)
                        Node13.presence = False
                        Node13.time = 0
                        Exited_west.vehicles.append(veh.ID)
                        Exited_west.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"Vehicle {veh.ID} exited to west at time {Exited_west.time}")
                        time.sleep(node_headway_seconds)
                        break

            if veh.destination == 'north':
                if incoming[0].ID == veh.ID:
                    incoming.pop(0)
                    Exited_south.vehicles.append(veh.ID)
                    Exited_south.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                    print(f"For {veh.origin} to {veh.destination}\n")
                    print(f"Vehicle {veh.ID} exited to (right turm) south at time {Exited_south.time}")
                    time.sleep(node_headway_seconds)
                    break

        if veh.origin == 'west':
            if veh.destination == 'east':
                while not (Node10.presence or Node12.presence or Node14.presence or Node16.presence):
                    if incoming[0].ID == veh.ID:
                        incoming.pop(0)
                        Node10.vehicles.append(veh.ID)
                        Node10.presence = True
                        Node10.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"Vehicle {veh.ID} entered Node10 at time {Node10.time}")
                        time.sleep(node_headway_seconds)

                        Node10.vehicles.pop(0)
                        Node10.presence = False
                        Node10.time = 0
                        Node12.vehicles.append(veh.ID)
                        Node12.presence = True
                        Node12.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"Vehicle {veh.ID} entered Node12 at time {Node12.time}")
                        time.sleep(node_headway_seconds)

                        Node12.vehicles.pop(0)
                        Node12.presence = False
                        Node12.time = 0
                        Node14.vehicles.append(veh.ID)
                        Node14.presence = True
                        Node14.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"Vehicle {veh.ID} entered Node14 at time {Node14.time}")
                        time.sleep(node_headway_seconds)

                        Node14.vehicles.pop(0)
                        Node14.presence = False
                        Node14.time = 0
                        Node16.vehicles.append(veh.ID)
                        Node16.presence = True
                        Node16.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"Vehicle {veh.ID} entered Node16 at time {Node16.time}")
                        time.sleep(node_headway_seconds)

                        Node16.vehicles.pop(0)
                        Node16.presence = False
                        Node16.time = 0
                        Exited_north.vehicles.append(veh.ID)
                        Exited_north.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"Vehicle {veh.ID} exited to north at time {Exited_north.time}")
                        time.sleep(node_headway_seconds)
                        break

            if veh.destination == 'east':
                while not (Node9.presence or Node8.presence or Node7.presence or Node1.presence):
                    if incoming[0].ID == veh.ID:
                        incoming.pop(0)
                        Node9.vehicles.append(veh.ID)
                        Node9.presence = True
                        Node9.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"Vehicle {veh.ID} entered Node9 at time {Node9.time}")
                        time.sleep(node_headway_seconds)

                        Node9.vehicles.pop(0)
                        Node9.presence = False
                        Node9.time = 0
                        Node8.vehicles.append(veh.ID)
                        Node8.presence = True
                        Node8.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"Vehicle {veh.ID} entered Node8 at time {Node8.time}")
                        time.sleep(node_headway_seconds)

                        Node8.vehicles.pop(0)
                        Node8.presence = False
                        Node8.time = 0
                        Node7.vehicles.append(veh.ID)
                        Node7.presence = True
                        Node7.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"Vehicle {veh.ID} entered Node7 at time {Node7.time}")
                        time.sleep(node_headway_seconds)

                        Node7.vehicles.pop(0)
                        Node7.presence = False
                        Node7.time = 0
                        Node1.vehicles.append(veh.ID)
                        Node1.presence = True
                        Node1.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"Vehicle {veh.ID} entered Node1 at time {Node1.time}")
                        time.sleep(node_headway_seconds)

                        Node1.vehicles.pop(0)
                        Node1.presence = False
                        Node1.time = 0
                        Exited_east.vehicles.append(veh.ID)
                        Exited_east.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"Vehicle {veh.ID} exited to east at time {Exited_east.time}")
                        time.sleep(node_headway_seconds)
                        break

            if veh.destination == 'south':
                if incoming[0].ID == veh.ID:
                    incoming.pop(0)
                    Exited_south.vehicles.append(veh.ID)
                    Exited_south.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                    print(f"For {veh.origin} to {veh.destination}\n")
                    print(f"Vehicle {veh.ID} exited to (right turn) south at time {Exited_south.time}")
                    time.sleep(node_headway_seconds)
                    break
        

        #incoming.pop(0)

        # Check if all vehicles have been processed
        if not incoming:
            break


thread_N_S = threading.Thread(target=define_Nodes, args=(NO,))
thread_N_S.start()


thread_N_E = threading.Thread(target=define_Nodes, args=(NL,))
thread_N_E.start()


thread_N_W = threading.Thread(target=define_Nodes, args=(NR,))
thread_N_W.start()

# From South

thread_S_N = threading.Thread(target=define_Nodes, args=(SO,))
thread_S_N.start()


thread_S_E = threading.Thread(target=define_Nodes, args=(SR,))
thread_S_E.start()

thread_S_W = threading.Thread(target=define_Nodes, args=(SL,))
thread_S_W.start()

# From east

thread_E_S = threading.Thread(target=define_Nodes, args=(EL,))
thread_E_S.start()


thread_E_N = threading.Thread(target=define_Nodes, args=(ER,))
thread_E_N.start()


thread_E_W = threading.Thread(target=define_Nodes, args=(EO,))
thread_E_W.start()

# From west

thread_W_S = threading.Thread(target=define_Nodes, args=(WR,))
thread_W_S.start()

thread_W_E = threading.Thread(target=define_Nodes, args=(WO,))
thread_W_E.start()


thread_W_N = threading.Thread(target=define_Nodes, args=(WL,))
thread_W_N.start()




    







def update_vehicle_time_lost(queue, time_lost):
    for vehicle in queue:
        vehicle.time_to_reach_intersection += time_lost

def dequeue_and_append_toadj(source_queue, dest_queue, num_vehicles, time_lost=1, time_reenter=1):
    dequeued_vehicles = []
    for vehicle in source_queue:
        source_queue.pop(0)
        vehicle.time_to_reach_intersection += time_lost
        dequeued_vehicles.append(vehicle)
    # insert elements from the dequeued_vehicles list, at the beginning of the dest_queue
    dest_queue[:0] = dequeued_vehicles

#dequeue_and_append_toadj(SO, NO, 3)
#####dest
def prioritize_queue_vehicle_request_from_origin(queue, time_lost=1, time_reenter=1):
    if any(vh.ID.startswith('emergency') for vh in queue):
        for index, vh in enumerate(queue):
            if vh.ID.startswith('emergency'):
                priority_vehicle = queue.pop(index)
                queue.insert(0, priority_vehicle)
                break

        next_queue = get_next_queue(queue)
        if next_queue is not None:
            num_vehicles_to_move = min(len(queue), len(next_queue))
            dequeue_and_append_toadj(queue, next_queue, num_vehicles_to_move, time_lost, time_reenter)

def get_next_queue(queue):
    origin_prefix = queue[0].origin[0].upper()
    destination_prefix = queue[0].destination[0].upper()

    for i in queue:
        if origin_prefix == 'S':
            if destination_prefix == 'N':
                return 'SO'
            elif destination_prefix == 'E':
                return 'SR'
            elif destination_prefix == 'W':
                return 'SL'
        elif origin_prefix == 'N':
            if destination_prefix == 'S':
                return 'NO'
            elif destination_prefix == 'E':
                return 'NR'
            elif destination_prefix == 'W':
                return 'NL'
        elif origin_prefix == 'E':
            if destination_prefix == 'N':
                return 'ER'
            elif destination_prefix == 'S':
                return 'EL'
            elif destination_prefix == 'W':
                return 'EO'
        elif origin_prefix == 'W':
            if destination_prefix == 'N':
                return 'WL'
            elif destination_prefix == 'S':
                return 'WR'
            elif destination_prefix == 'E':
                return 'WO'


# Prioritize emergency vehicles
# for queue in [NO, NL, NR, SO, SR, SL, EO, EL, ER, WO, WR, WL]:
#     prioritize_queue_vehicle_request_from_origin(queue)

# print_vehicles(FROsorted_queue, 'FRO')


# print_vehicles(WO, 'WO')
# print_vehicles(WR, 'WR')
# print_vehicles(WL, 'WL')

# print_vehicles(EO, 'EO')
# print_vehicles(ER, 'ER')
# print_vehicles(EL, 'EL')
###############################NetworkX#########################################
# 