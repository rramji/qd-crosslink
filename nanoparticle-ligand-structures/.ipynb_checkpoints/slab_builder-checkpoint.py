# Randomly select N sites from `coords`, with a minimum of X distance between them
# Usage: select_coordinates(coords, N, X)
# clearly there are issues with this implementation, sometimes it can't find enough sites even when
# it should be possible

import mbuild as mb
import numpy as np
from scipy.spatial.distance import pdist, squareform
import random


def select_coordinates(ports, num_to_select, min_distance):
    
    coords = [port.pos for port in ports]

    num_coords = len(coords)
    if num_to_select > num_coords:
        print("Warning: Not enough coordinates available to select.")
        return None
    
    distance_matrix = squareform(pdist(coords))

    valid_indices = set(range(num_coords))
    selected_ports = []

    for _ in range(num_to_select):
        if not valid_indices:
            print("Warning: Unable to find enough coordinates with the given constraints.")
            break

        index = random.choice(list(valid_indices))
        selected_ports.append(ports[index])
        valid_indices.remove(index)

        too_close_indices = set(np.where(distance_matrix[index] < min_distance)[0])
        valid_indices -= too_close_indices

    return selected_ports


# Attempt to place a ligand on the slab

def place_ligand(smiles, port, slab_coords):
    # 1) Generate the ligand structure
    ligand = mb.load(smiles, smiles=True)
    
    bond_orientation = port.pos - port.anchor.pos
    bond_orientation = bond_orientation / np.linalg.norm(bond_orientation)

    # 2) Translate the ligand to the slab coordinate
    ligand.add(mb.Port(anchor=ligand[18], separation=0.12, orientation=(ligand[18].pos - ligand[17].pos)))
    mb.force_overlap(move_this=ligand,
                     from_positions=ligand['Port[0]'],
                     to_positions=port)
       
    orient = ligand[18].pos - ligand[17].pos
    orient = orient / np.linalg.norm(orient)
    
    # print(bond_orientation, orient)

    coords = np.array(slab_coords)  # Convert list to numpy array for easier manipulation
    # print(slab_coords)
    min_coords = np.min(slab_coords, axis=0)
    max_coords = np.max(slab_coords, axis=0)
    # dimensions = max_coords - min_coords

    # 3) Check if ligand's x,y coordinates are within bounds of slab
    for attempt in range(36):  # Rotate up to 360 degrees
        x_coords = ligand.xyz[:, 0]
        y_coords = ligand.xyz[:, 1]

        min_x, max_x = np.min(x_coords), np.max(x_coords)
        min_y, max_y = np.min(y_coords), np.max(y_coords)
        
        if (min_x >= min_coords[0] and max_x <= max_coords[0] and
            min_y >= min_coords[1] and max_y <= max_coords[1]):
            # 3a) If they are within the bounds, return True
            return True, ligand
        else:
            # 3b) If they are not, try rotating by 10 degrees
            ligand.rotate(theta=np.deg2rad(10), around=bond_orientation)  # Rotate around z-axis

    # If no suitable orientation found after rotating through all 360 degrees, return False
    return False, ligand