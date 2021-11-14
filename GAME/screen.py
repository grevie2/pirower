#! /usr/bin/python3

from constants import WIN_HEIGHT, VIEWABLE_HEIGHT_R


def get_r_in_pixels(r):
    num_pixels = (WIN_HEIGHT/VIEWABLE_HEIGHT_R) * r
    #round this to nearest whole number
    return int(round(num_pixels))

"""
#TODO: we will need to toggle this to use WIDTH instead of height
    
def get_new_r_in_pixels(r_change, layer_multiplier):
	num_pixels = (WIN_HEIGHT/VIEWABLE_HEIGHT_R * layer_multiplier) * r_change
	return int(round(num_pixels)) #rounding should not be needed
"""
