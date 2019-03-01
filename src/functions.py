"""
This module is a first & naive approach for the program structure.

Considering 

1 - The programm is small for now
2 - We don't have any idea of the program architecture

We prefer to use module level functions, easier to use & call.
We'll eventually refactor into potential classes later.
"""
import numpy as np
import sys, math

def bresenham(x1, y1, x2, y2, max_lenght = 10000):
    """
    Tracé de segment d'apres l'algorithme de bresenham
    (x1 y1) : le point de départ en haut a gauche, (x2 y2) point d'arrivé en bas a droite.
    retourne une liste contenant les double (x, y) de chacun des points.
    """
    segment = [] # Contient tout les pixels du segment.
 
    delta_x = x2 - x1
    delta_y = y2 - y1
    
    if delta_x >= 0:
        x_sign = 1
    else:
        x_sign = -1

    if delta_y >= 0:
        y_sign = 1
    else:
        y_sign = -1

    if delta_x == 0:
        err_x_inc = 1 # To ensure vertical ray is drawn
    else:
        err_x_inc = abs(delta_y / delta_x)
    
    if delta_y == 0:
        err_y_inc = 1 # To ensure horizontal ray is drawn
    else:
        err_y_inc = abs(delta_x / delta_y)
    
    err_x = 0.0
    err_y = 0.0
    iteration = 0
    x = x1
    y = y1
   
    while ( (x <= max_lenght and x >= 0) or (y >= 0 and y <= max_lenght)) and iteration < max_lenght:
        
        if (abs(err_x) >= 0.5):
            x += x_sign
            err_x -= x_sign
            
        if (abs(err_y) >= 0.5):
            y += y_sign
            err_y-= y_sign

        if x < max_lenght and y < max_lenght:
            segment.append([x, y])
    
        err_x += err_x_inc
        err_y += err_y_inc
        
        iteration += 1

    return segment

#
# Applies the BRESENHAM algorithm from a starting point
# to a direction set by an angle (in degres)
# @param {*} x1 X position of the starting point
# @param {*} y1 Y position of the starting point
# @param {*} angle The direction of the ray
#
def bresenham_angle(x1, y1, degres, diagonal):

    angle = degres * math.pi / 180
    
    x2 = diagonal * math.cos(angle)
    y2 = diagonal * math.sin(angle)

    return bresenham(x1, y1, x2, y2, diagonal)

def scan_parrallel(segment, max_size):
    """
    This function get all the parrallels segments in an image from a single segment
    the segments returned 
    """

    if segment[0][0] - segment[-1][0] != 0:
        angle = (segment[0][1] - segment[-1][1]) / (segment[0][0] - segment[-1][0])
    else:
        angle = max_size

    segments = []
    
    # Adding all the segments below the first segment
    for actual_segment in range(1, max_size):
        segments.append([])
        for actual_point in range(max_size):
            if angle >= 1:
                if segment[actual_point][0]-actual_segment >= 0: # Check pixel exists
                    segments[-1].append([segment[actual_point][0] - actual_segment, segment[actual_point][1]])
            elif segment[actual_point][1]-actual_segment >= 0: # Check pixel exists
                    segments[-1].append([segment[actual_point][0],segment[actual_point][1]-actual_segment])

    segments.append(segment)

    # Adding all the segments above the first segment
    for actual_segment in range(1, max_size):
        segments.append([])
        for actual_point in range(max_size):
            if angle >= 1:
                if segment[actual_point][0]+actual_segment < max_size: # Check pixel exists
                    segments[-1].append([segment[actual_point][0]+actual_segment, segment[actual_point][1]])
            elif segment[actual_point][1]+actual_segment < max_size: # Check pixel exists
                    segments[-1].append([segment[actual_point][0], segment[actual_point][1]+actual_segment])

    return segments

def histogram(cardinal=16):
    """
    We want this function to produce a data structure representing a histogram
    of [what does it represent ?] depeding on the number of directions passed in arguments.
    """
    raise NotImplementedError('The histogram function is not implemented yet')

def print_segment(segment, max_size):
    print(segment, "\n")
    result = np.zeros((max_size, max_size))
