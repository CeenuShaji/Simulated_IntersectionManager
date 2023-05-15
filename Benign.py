#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
import time


class Vehicle:
    def __init__(self, ID, origin, destination, time_to_reach_intersection, time_to_cross):
        self.ID = ID

        if origin.lower() in ['east', 'west', 'north', 'south']:
            self.origin = origin
        elif destination.lower() in ['east', 'west', 'north', 'south']:
            self.destination = destination
        else:
            raise ValueError("Invalid origin.")

        self.destination = destination
        self.time_to_reach_intersection = time_to_reach_intersection
        self.time_to_cross = time_to_cross

def generate_random_id():
    random_id = random.choice([10*"emergency" + str(i) for i in range(20)])  # Generate a random ID starting with "EM"
    return random_id

#list of vehicles
vehicle_ids = set("emergency" + str(i) for i in range(10))| set(str(i) for i in range(20))
# print(vehicle_ids)

# Ensure vehicle_ids has atleast 31 unique IDs
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

# # destination from east
E_W = []
E_S = []
E_N = []

# destination from west
W_E = []
W_S = []
W_N = []


queue_order_NS=[]
queue_order_EW=[]

def print_vehicles(queue):
    count=0
    for vehicle in queue:
        count+=1
        print("Vehicle #",count,".", vehicle.ID)
        
        
# Queues the REQUEST signal and assumes they all get CONFIRM signal from Int. Manager 
def queue_vehicle_request_from_origin(vehicle, origin):
    if vehicle.origin == 'north':
        north_queue.append(vehicle)
    elif vehicle.origin == 'south':
        south_queue.append(vehicle)
    elif vehicle.origin == 'east':
        east_queue.append(vehicle)
    elif vehicle.origin == 'west':
        west_queue.append(vehicle)




# In[2]:




def random_NSqueue_simulator():
    print("\nNorth-South traffic:")
    #based on the size of the vehicle or other obstacles on way
    time_toreach=1 
    # Randomly queue the north and south directions with vehicles
    for index, origin in enumerate(random.choices(['north', 'south'], k=5)):
        veh_id = random.choice(list(vehicle_ids))
        vehicle_ids.remove(veh_id)  # Remove the used ID from the set
        
        available_destinations = ['east', 'west', 'north', 'south']
        available_destinations.remove(origin)  # Remove the origin from the available destinations
        destination = random.choice(available_destinations)

        random_timetoreach = random.randint(1, 2)

       
        time_tocross = 20
        time_toreach+=random_timetoreach
        
        vehicle_instance = Vehicle(veh_id, origin, destination, time_toreach, time_tocross)
        queue_vehicle_request_from_origin(vehicle_instance, origin)

        # Append vehicle to queue ordered list to ensure FIFO indices
        queue_order_NS.append(vehicle_instance)  

        # Print the order of cars in the queue
        if origin == 'north':
            print(f"North Queue: {index + 1}. {vehicle_instance.ID} has sent REQUEST to manager with {time_toreach} seconds to reach")
        elif origin == 'south':
            print(f"South Queue: {index + 1}. {vehicle_instance.ID} has sent REQUEST to manager with {time_toreach} seconds to reach")
            
        # Introduce a delay to display time elapsed
        #time.sleep(time_toreach)  



def random_EWqueue_simulator():
    time_toreach=1 
    print("\nEast-West traffic:")
    # Randomly queue the east and west directions with vehicles
    for index, origin in enumerate(random.choices(['east', 'west'], k=5)):
        veh_id = random.choice(list(vehicle_ids))
        vehicle_ids.remove(veh_id)  # Remove the used ID from the set

        available_destinations = ['east', 'west', 'north', 'south']
        available_destinations.remove(origin)  # Remove the origin from the available destinations
        destination = random.choice(available_destinations)


        #based on the size of the vehicle or other obstacles on way
        random_timetoreach = random.randint(1, 2)

        time_tocross = 20
        #assuming allowed time to reach intersection is only 2 seconds
        #if time_toreach<=2:
        time_toreach+=random_timetoreach #Shows how far the vehicle is from intersection


        vehicle_instance = Vehicle(veh_id, origin, destination, time_toreach, time_tocross)
        queue_vehicle_request_from_origin(vehicle_instance, origin)

        # Append vehicle to queue ordered list to ensure FIFO indices
        queue_order_EW.append(vehicle_instance) 




        # Print the order of cars in the queue
        if origin == 'east':
            print(f"East Queue: {index + 1}. {vehicle_instance.ID} has sent REQUEST to manager with {time_toreach} seconds to reach")
        elif origin == 'west':
            print(f"West Queue: {index + 1}. {vehicle_instance.ID} has sent REQUEST to manager with {time_toreach} seconds to reach")
        #else:

        #Introduce a 2-second delay to show time elapsed
        #time.sleep(time_toreach)  


# In[3]:


# Define a custom key function to extract the last string for elements starting with 'A'
def custom_key(vehicle):
    if vehicle.ID.startswith('A'):
        return vehicle.ID[-1]  # Sort by the last character of ID when it starts with 'A'
    else:
        return vehicle.ID  # Preserve the original order for other elements


def prioritize_emergency_vehicles(north_queue, south_queue, queue_order_NS):
    # One emergency vehicle
    # Element is popped from its current index and inserted at index 0
    # Assuming other vehicles went to shoulder
    em_vehicles_south = [vehicle for vehicle in south_queue if vehicle.ID[:2] == 'em']
    em_vehicles_north = [vehicle for vehicle in north_queue if vehicle.ID[:2] == 'em']

    em_vehicles_south.sort(key=lambda vehicle: vehicle.ID[-1], reverse=True)
    em_vehicles_north.sort(key=lambda vehicle: vehicle.ID[-1], reverse=True)

    non_em_vehicles_south = [vehicle for vehicle in south_queue if vehicle.ID[:2] != 'em']
    non_em_vehicles_north = [vehicle for vehicle in north_queue if vehicle.ID[:2] != 'em']

    south_queue[:] = em_vehicles_south + non_em_vehicles_south
    north_queue[:] = em_vehicles_north + non_em_vehicles_north
    
    # When there is two emergency vehicle
    # the EV at the intersection with highest priority or higher ID last string goes

    queue_order_NS.clear()
    queue_order_NS[:] = south_queue + north_queue
    queue_order_NS.sort(key=custom_key, reverse=True)


# In[4]:


# Dequeues vehicles as they leave the intersection -- Intersection 
def dequeue_and_enqueue_confirm(vehicle_instance,origin):
    origin.pop(0)
    if vehicle.origin == 'north':
        if vehicle.destination == 'south':
            N_S.append(vehicle)
        
        elif vehicle.destination == 'east':        
            N_E.append(vehicle)

        elif vehicle.destination == 'west':
            N_W.append(vehicle)       
       
    elif vehicle.origin == 'south':
        if vehicle.destination == 'north':
            S_N.append(vehicle)
        
        elif vehicle.destination == 'east':        
            S_E.append(vehicle)

        elif vehicle.destination == 'west':
            S_W.append(vehicle) 
    
    elif vehicle.origin == 'east':
        if vehicle.destination == 'north':
            E_N.append(vehicle)
        
        elif vehicle.destination == 'south':        
            E_S.append(vehicle)

        elif vehicle.destination == 'west':
            E_W.append(vehicle) 
        
    elif vehicle.origin == 'west':
        if vehicle.destination == 'north':
            W_N.append(vehicle)
        
        elif vehicle.destination == 'east':        
            W_E.append(vehicle)

        elif vehicle.destination == 'south':
            W_S.append(vehicle)


# In[5]:



    
#Simulating North South and East West traffic flow
random_NSqueue_simulator()
random_EWqueue_simulator()

# Print the IDs of vehicles in each queue
print("\nVehicles that sent REQUEST from North Queue:")
print_vehicles(north_queue)

print("\nVehicles that sent REQUEST from South Queue:")
print_vehicles(south_queue)

print("\nVehicles that sent REQUEST from East Queue:")
print_vehicles(east_queue)

print("\nVehicles that sent REQUEST from West Queue:")
print_vehicles(west_queue)
 


# ![image.png](attachment:image.png)

# In[6]:


#Emergency vehicles

print("\nSouth Queue:")
print_vehicles(south_queue)

print("\nNorth Queue:")
print_vehicles(north_queue)
  
print("\nNS Queue:")
print_vehicles(queue_order_NS)

########################

print("\nEast Queue:")
print_vehicles(east_queue)

print("\nWest Queue:")
print_vehicles(west_queue)
   
print("\nEast-West Queue:")
print_vehicles(queue_order_EW)



prioritize_emergency_vehicles(north_queue, south_queue, queue_order_NS)
prioritize_emergency_vehicles(east_queue, west_queue, queue_order_EW)
    


print("\n \t After applying the priortization rules:")

print("\nSouth Queue:")
print_vehicles(south_queue)

print("\nNorth Queue:")
print_vehicles(north_queue)

    
# For 2 EV, intersection allows the higher priority (starting from 0) vehicle to go
       
print("\nNS Queue:")
print_vehicles(queue_order_NS)

########################

print("\nEast Queue:")
print_vehicles(east_queue)

print("\nWest Queue:")
print_vehicles(west_queue)

    
# For 2 EV, intersection allows the higher priority (starting from 0) vehicle to go
       
print("\nEast-West Queue:")
print_vehicles(queue_order_EW)
    


# In[7]:




# Dequeues vehicles as they leave the intersection
for vehicle in queue_order_NS:
    if vehicle.origin == 'north':
        dequeue_and_enqueue_confirm(vehicle,north_queue)
        print(f"Vehicle {vehicle.ID} leaves north lane to {vehicle.destination} lane")
    
    elif vehicle.origin == 'south':
        dequeue_and_enqueue_confirm(vehicle,south_queue)
        print(f"Vehicle {vehicle.ID} leaves south lane to {vehicle.destination} lane")

print("\n Now for East-West direction")

# Dequeues vehicles as they leave the intersection
for vehicle in queue_order_EW:
    if vehicle.origin == 'east':
        dequeue_and_enqueue_confirm(vehicle,east_queue)
        print(f"Vehicle {vehicle.ID} leaves east lane to {vehicle.destination} lane")
    
    elif vehicle.origin == 'west':
        dequeue_and_enqueue_confirm(vehicle,west_queue)
        print(f"Vehicle {vehicle.ID} leaves west lane to {vehicle.destination} lane")
        
              
# Print the IDs of vehicles in each queue to show they departed from the lanes
print("\nNorth Queue:")
print_vehicles(north_queue)

print("\nSouth Queue:")
print_vehicles(south_queue)
    
# Print the IDs of vehicles in each queue of the outgoing lane (example North to..)
print("\nNorth-east Queue:")
print_vehicles(N_E)

print("\nNorth-South Queue:")
print_vehicles(N_S)
    
print("\nNorth-West Queue:")
print_vehicles(N_W)


    


# ![image.png](attachment:image.png)

# ![image.png](attachment:image.png)

# ![image-2.png](attachment:image-2.png)

# In[8]:


import time

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
#graph nodes - Use networkX instead

node_headway_seconds = 1
import datetime
import threading

# In[9]:

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



# In[10]:



    
# define_Nodes(N_S)
# print("\n")
# define_Nodes(N_E)
# print("\n")
# define_Nodes(N_W)
import threading

# Define the target function for each thread
def define_nodes_thread(incoming):
    define_Nodes(incoming)
    

# Create and start threads for each function
threads = []

# From north

thread_N_S = threading.Thread(target=define_nodes_thread, args=(N_S,))
threads.append(thread_N_S)
thread_N_S.start()


thread_N_E = threading.Thread(target=define_nodes_thread, args=(N_E,))
threads.append(thread_N_E)
thread_N_E.start()


thread_N_W = threading.Thread(target=define_nodes_thread, args=(N_W,))
threads.append(thread_N_W)
thread_N_W.start()

# From South

thread_S_N = threading.Thread(target=define_nodes_thread, args=(S_N,))
threads.append(thread_S_N)
thread_S_N.start()


thread_S_E = threading.Thread(target=define_nodes_thread, args=(S_E,))
threads.append(thread_S_E)
thread_S_E.start()

thread_S_W = threading.Thread(target=define_nodes_thread, args=(S_W,))
threads.append(thread_S_W)
thread_S_W.start()

# From east

thread_E_S = threading.Thread(target=define_nodes_thread, args=(E_S,))
threads.append(thread_E_S)
thread_E_S.start()


thread_E_N = threading.Thread(target=define_nodes_thread, args=(E_N,))
threads.append(thread_E_N)
thread_E_N.start()


thread_E_W = threading.Thread(target=define_nodes_thread, args=(E_W,))
threads.append(thread_E_W)
thread_E_W.start()

# From west

thread_W_S = threading.Thread(target=define_nodes_thread, args=(W_S,))
threads.append(thread_W_S)
thread_W_S.start()


thread_W_E = threading.Thread(target=define_nodes_thread, args=(W_E,))
threads.append(thread_W_E)
thread_W_E.start()


thread_W_N = threading.Thread(target=define_nodes_thread, args=(W_N,))
threads.append(thread_W_N)
thread_W_N.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()

# def define_Threads():
#     global Node1, Node2, Node3, Node4, Node5, Node6, Node7, Node8, Node9, Node10, Node11, Node12, Node13, Node14, Node15, Node16

#     # Create threads for each node
#     threads = []
#     nodes = [Node1, Node2, Node3, Node4, Node5, Node6, Node7, Node8, Node9, Node10, Node11, Node12, Node13, Node14, Node15, Node16]
#     for node in nodes:
#         thread = threading.Thread(target=define_Node, args=(node,))
#         threads.append(thread)
#         thread.start()

#     # Wait for all threads to finish
#     for thread in threads:
#         thread.join()


# define_Threads()
# In[ ]:


# #Time Scheduling

# # Create an empty array
# NtoS = []

# #(node_name, node_available?, vehicle)

# # Add nodes to the array north to south
# NtoS.append(("1", None, None))
# NtoS.append(("2", None, None))
# NtoS.append(("3", None, None)) #######
# NtoS.append(("4", None, None))

# # Create an empty array
# StoW = []

# # Add nodes to the array 
# StoW.append(("16", None, None))
# StoW.append(("15", None, None))
# StoW.append(("3", None, None))  #######
# StoW.append(("5", None, None))

# # Create an empty array
# NtoE = []

# # Add nodes to the array 
# NtoE.append(("6", None, None))
# NtoE.append(("8", None, None))
# NtoE.append(("10", None, None)) ########
# NtoE.append(("11", None, None))



# # Create an empty array
# StoN = []

# # Add nodes to the array 
# StoN.append(("13", None, None))
# StoN.append(("12", None, None))
# StoN.append(("10", None, None)) ########
# StoN.append(("9", None, None))  



# In[ ]:


# # NtoSVehicleID = random.randint(1000, 9999)
# # StoWVehicleID = random.randint(1000, 9999)

# # Create the initial NtoS list with vehicle IDs
# # (Node_name, Occupancy_boolean, vehicle_ID, remaining_time)
# NtoS = [("1", False,NtoSVehicleID) , ("2", False, NtoSVehicleID),
#         ("3", False, NtoSVehicleID), ("4", False, NtoSVehicleID)]

# # Create the initial StoW list with vehicle IDs
# StoW = [("16", False,StoWVehicleID ), ("15", False, StoWVehicleID),
#         ("3", False, StoWVehicleID), ("5", False, StoWVehicleID)]
        

# print("NtoS:", NtoS)

# # Simulate the vehicle passing through North to South
# for i in range(len(NtoS)):
#     NtoS[i] = (NtoS[i][0], True, NtoS[i][2])  # Set the boolean value to True
#     print("NtoS:", NtoS)
    
#     # Check if the condition for StoW permission is met
#     if NtoS[1][1] and not NtoS[2][1]:
#         print()
#         print("Asking permission to go from StoW.")
#         print()

#     time.sleep(1)  # Pause for 1 second

# print()
# # Reset the values in NtoS to False
# NtoS = [(node[0], False, "vehicleID") for node in NtoS]
# print("NtoS reset to:", NtoS)

# print()

# print("StoW:", StoW)

# print()
# # Simulate the vehicle passing through South to West
# for i in range(len(StoW)):
#     StoW[i] = (StoW[i][0], True, StoW[i][2])  # Set the boolean value to True
#     print("StoW:", StoW)
#     time.sleep(1)  # Pause for 1 second
# print()
# # Reset the values in StoW to False
# StoW = [(node[0], False,"vehicleID" ) for node in StoW]
# print("StoW reset to:", StoW)


# In[ ]:





# In[ ]:


# def display_intersection():
#     lane_width = 7  # Width of each lane
#     intersection_width = lane_width  # Width of the intersection (same as each lane)
#     intersection_height = lane_width  # Height of the intersection (same as each lane)

    
#     for j in range(intersection_height):
#             print( 25*" " + "|" + 25*" " +"|")
         
#     print(75*"-")
    
#     # Middle part of the intersection
#     for _ in range(intersection_width):
#         print( 25*" " + "|" + 25*" " + "|")

#     # Bottom part of the intersection
#     print(75*"-")
    
#     for i in range(intersection_height):
#         print( 25*" " + "|" + 25*" " + "|")
        


# # Call the function to display the intersection
# display_intersection()


###################### NetworkX #########################################

# Create an empty graph
# G = nx.Graph()
# #('SL1', 'SO1'), ('SO1', 'SS1'), ('SL2', 'SO2'), ('SO2', 'SS2'), ('SL3', 'SO3'), ('SO3', 'SS3'),
# # List of edges as paths
# edges = [('SL3', 'SL2'), ('SL2', 'SL1'), ('SL1', 'Node6'), ('Node6', 'Node8'),
#          ('Node8', 'Node11'), ('Node11', 'Node10'), ('Node10', 'Node12'), ('Node9', 'Node8'),
#          ('Node8', 'Node7'), ('Node7', 'Node1'),('SO3', 'SO2'), ('SO2', 'SO1'),         
#          ('SO1', 'Node1'), ('Node1', 'Node2'), ('Node2', 'Node3'), ('Node3', 'Node4'),          
#          ('SS3', 'SS2'), ('SS2', 'SS1'), ('NL3', 'NL2'), ('NL2', 'NL1'), ('NL1', 'Node16'),
#          ('Node16', 'Node15'), ('Node15', 'Node3'), ('Node3', 'Node5'), ('NO3', 'NO2'),
#          ('NO2', 'NO1'), ('NO1', 'Node13'), ('Node13', 'Node12'), ('Node12', 'Node11'),
#          ('Node11', 'Node9'), ('NS3', 'NS2'), ('NS2', 'NS1'), ('EL3', 'EL2'), ('EL2', 'EL1'),
#          ('EL1', 'Node5'), ('Node5', 'Node2'), ('Node2', 'Node7'), ('Node7', 'Node6'),
#          ('EO3', 'EO2'), ('EO2', 'EO1'), ('EO1', 'Node4'), ('Node4', 'Node15'),
#          ('Node15', 'Node14'), ('Node14', 'Node13'), ('Node13', 'Node9'), 
#          ('WS3', 'WS2'), ('WS2', 'WS1'), ('WO3', 'WO2'), ('WO2', 'WO1'), ('WL3', 'WL2'), ('WL2', 'WL1'),
#          ('WL1', 'Node10'), ('Node12','Node14') ,('Node14', 'Node16'),
#          ('WO1', 'Node9'), ('SR1', 'SR2'), ('SR2', 'SR3'), ('NR1', 'NR2'), ('NR2', 'NR3'), ('ER1', 'ER2'), ('ER2', 'ER3'), ('WR1', 'WR2'), ('WR2', 'WR3')
#          ]

# # Add edges to the graph
# G.add_edges_from(edges)

# # Define the positions for specific nodes
# fixed_positions = {
#     'Node1': (2, -2),
#     'Node2': (2, -1),
#     'Node3': (2, 1),
#     'Node4': (2, 2),
#     'Node5': (3,0),
#     'Node6': (0, -3),
#     'Node7': (1,-2),
#     'Node8': (-1, -2),
#     'Node9': (-2, -2),
#     'Node10': (-3, 0),
#     'Node11': (-2, -1),
#     'Node12': (-2, 1),
#     'Node13': (-2, 2),
#     'Node14': (-1, 2),
#     'Node15': (1, 2),
#     'Node16': (0, 3),

#     'SL1': (1, -4),
#     'SL2': (1, -5),
#     'SL3': (1, -6),
#     'SO1': (2, -4),
#     'SO2': (2, -5),
#     'SO3': (2, -6),
#     'SR1': (3, -4),
#     'SR2': (3, -5),
#     'SR3': (3, -6),
#     'SS1': (4, -4),
#     'SS2': (4, -5),
#     'SS3': (4, -6),

#     'NL1': (-1, 4),
#     'NL2': (-1, 5),
#     'NL3': (-1, 6),
#     'NO1': (-2, 4),
#     'NO2': (-2, 5),
#     'NO3': (-2, 6),
#     'NR1': (-3, 4),
#     'NR2': (-3, 5),
#     'NR3': (-3, 6),
#     'NS1': (-4, 4),
#     'NS2': (-4, 5),
#     'NS3': (-4, 6),

#     'EL1': (4, 1),
#     'EL2': (5, 1),
#     'EL3': (6, 1),
#     'EO1': (4, 2),
#     'EO2': (5, 2),
#     'EO3': (6, 2),
#     'ER1': (4, 3),
#     'ER2': (5, 3),
#     'ER3': (6, 3),
#     'ES1': (4, 4),
#     'ES2': (5, 4),
#     'ES3': (6, 4),

#     'WL1': (-4, -1),
#     'WL2': (-5, -1),
#     'WL3': (-6, -1),
#     'WO1': (-4, -2),
#     'WO2': (-5, -2),
#     'WO3': (-6, -2),
#     'WR1': (-4, -3),
#     'WR2': (-5, -3),
#     'WR3': (-6, -3),
#     'WS1': (-4, -4),
#     'WS2': (-5, -4),
#     'WS3': (-6, -4)
# }


# # Compute the layout using a spring layout algorithm (excluding nodes with fixed positions)
# layout = nx.spring_layout(G, pos=fixed_positions, fixed=fixed_positions.keys())

# # Draw the graph with the specified positions
# # nx.draw(G, layout, with_labels=True, node_size=1200, node_color='skyblue', font_size=9)
# # plt.show()



# # Function to update the node colors
# def update_node_colors(node_colors, vehicles):
#     for node in node_colors:
#         if node in vehicles.values():
#             node_colors[node] = 'red'
#         else:
#             node_colors[node] = 'blue'
#     return node_colors

# # Function to update the animation
# # def animate(i):
# #     plt.clf()
# #     node_colors = update_node_colors(nx.get_node_attributes(G, 'pos'), vehicles)
# #     nx.draw_networkx(G, pos, with_labels=True, node_size=5000, node_color=list(node_colors.values()),
# #                      font_size=12, font_weight='bold', arrows=True, arrowstyle='->', arrowsize=12)
# #     plt.title(f"Time Step: {i}")




