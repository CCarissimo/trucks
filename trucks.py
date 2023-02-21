import numpy as np
import matplotlib.pyplot as plt
from tqdm.auto import tqdm


def add_random_objects(inventory, incoming=1):
    for k, v in inventory.items():
        for n in range(incoming):
            obj = np.random.randint(0, 3)
            if obj != k:
                v.append(obj)
    return inventory


def load_shared_truck(storage, boot):
    if len(boot) == 0:
        # try fill to capacity
        free_space = truck_capacity - len(boot)
        while free_space > 0 and len(storage) > 0:
            counts = np.bincount(storage, minlength=3)
            amax = np.argmax(counts)
            if counts[amax] <= free_space:
                for i in range(counts[amax]):
                    storage.remove(amax)
                    boot.append(amax)
            else:
                for i in range(free_space):
                    storage.remove(amax)
                    boot.append(amax)

            free_space = truck_capacity - len(boot)

    else:
        free_space = truck_capacity - len(boot)

        while free_space > 0 and len(storage) > 0:
            # print(free_space, len(storage))

            counts = np.bincount(storage, minlength=3)
            amax = np.argmax(counts)
            boot_elements = np.bincount(boot, minlength=3)
            boot_amax = np.argmax(boot_elements)

            if counts[boot_amax] == 0:
                if counts[amax] <= free_space:
                    for i in range(counts[amax]):
                        storage.remove(amax)
                        boot.append(amax)
                else:
                    for i in range(free_space):
                        storage.remove(amax)
                        boot.append(amax)

            elif counts[boot_amax] <= free_space:
                for i in range(counts[boot_amax]):
                    storage.remove(boot_amax)
                    boot.append(boot_amax)
            elif counts[boot_amax] > free_space:
                for i in range(free_space):
                    # print(boot_amax, boot, storage)
                    storage.remove(boot_amax)
                    boot.append(boot_amax)

            free_space = truck_capacity - len(boot)

    return storage, boot


initial_inventory_size = 100
inventory = {}
nodes = [0, 1, 2]

for node in nodes:
    inventory[node] = []
    for i in range(initial_inventory_size):
        obj = np.random.randint(0, 3)
        if obj != node:
            inventory[node].append(obj)

truck_capacity = 10

trucks = {
    0: [],
    1: [],
    2: []
}

truck_locations = [0, 2, 1]

tmap = {
    0: {0: 1, 1: 0},
    1: {0: 2, 2: 0},
    2: {1: 2, 2: 1}
}

M = {}

iterations = 1000

for t in tqdm(range(iterations, 2 * iterations)):

    # fill trucks
    for truck, boot in trucks.items():
        node = truck_locations[truck]
        inventory[node], boot = load_shared_truck(inventory[node], boot)

    empty_spots = np.sum([truck_capacity - len(boot) for boot in trucks.values()])
    inventory_size = np.sum([len(inventory[node]) for node in nodes])

    # move trucks
    truck_locations = [np.argmax(np.bincount(boot, minlength=3)) for truck, boot in trucks.items()]
    # print(truck_locations)
    # print(trucks)

    # unload trucks
    for truck, boot in trucks.items():
        node = truck_locations[truck]
        tmp = []
        for i in range(len(boot)):
            obj = boot.pop()
            if obj != node:
                tmp.append(obj)
        for obj in tmp:
            boot.append(obj)

    # grow inventory
    inventory = add_random_objects(inventory, incoming=5)

    M[t] = {
        "empty_spots": empty_spots,
        "inventory_size": inventory_size
    }

plt.figure(0)
plt.plot([M[t]["empty_spots"] for t in M.keys()])

plt.figure(1)
plt.plot([M[t]["inventory_size"] for t in M.keys()])

plt.show()
