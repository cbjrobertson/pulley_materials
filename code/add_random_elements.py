#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 11:19:18 2023

@author: cole
"""
# =============================================================================
# imports
# =============================================================================
import pandas as pd
import glob
from random import randint, choice
from math import ceil

# =============================================================================
# constants
# =============================================================================
START = "%%%%% START %%%%%"
END = "%%%%% END %%%%%"
R = "%%%%% REPLACE %%%%%"
PATH = "../simple_pulleys/*.tex"

# =============================================================================
# data
# =============================================================================
df = pd.read_excel("../metadata/pulley_master_key.xlsx")
max_lines = max(df.relevent_len)

# =============================================================================
# functions
# =============================================================================
def load_tikz(
        path
        ):
    keys = [key.split("/")[-1].rstrip(".tex") for key in glob.glob(path)]
    pics = [open(x,"r").read() for x in glob.glob(path)]
    pics = [pic.split(START)[1].split(END)[0] for pic in pics]
    return dict(zip(keys,pics))

def make_lst(
        eg
        ):
    # slit + strip
    eg = eg.replace("\t","")
    lst = [x.strip() for x in eg.split("\n")]
    return lst

def get_range(
        lst
        ):
    strip_lst = [x for x in lst if not x == ""]
    top = strip_lst[0]
    top_left = top[top.index("(")+1:top.index(")")]
    tl = tuple(float(x.strip()) for x in top_left.split(","))
    bottom = strip_lst[-1].split("rectangle")[-1]
    bottom_right = bottom[bottom.index("(")+1:bottom.index(")")]
    br = tuple(float(x.strip()) for x in bottom_right.split(","))
    x_range = (ceil(tl[0]),ceil(br[0]))
    y_range = (ceil(tl[1]),ceil(br[1]))
    return x_range, y_range

def make_line(
        x_range,
        y_range,
        length=5,
        rec_length=2
        ):
    # Random side
    side_lst = ["left", "right"]
    side = choice(side_lst)
    
    # Randomly chose line type
    kind_lst = ["line", "circle", "rectangle", "man"]
    kind = choice(kind_lst)
    
    # Get box coords
    x_start, x_end, y_start, y_end = get_coords(x_range, y_range, length, side)
    
    # Random opacity
    ope = randint(10,100)
    
    # Random thickness
    thick_list = [x/100 for x in range(20,80,10)]
    thick = choice(thick_list)
    
    #Random rad
    rad = choice([x/10 for x in range(0,25,1)]) 
    
    # Return lines/circles
    if kind == "line":
        return f"\draw[line width=0.5mm, color=black!{ope}]({x_start}, {y_start}) -- ({x_end}, {y_end});"
    elif kind == "circle":
        x_coord = randint(min(x_start,x_end), max(x_start,x_end))
        y_coord = randint(min(y_start,y_end), max(y_start,y_end))
        return 	f"\draw [line width={thick}mm, color=black!{ope}]({x_coord}, {y_coord}) circle ({rad});"
    elif kind == "rectangle":
         # Get box coords
         x_start, x_end, y_start, y_end = get_coords(x_range, y_range, rec_length, side)
         return f"\draw[line width={thick}mm, color=black!{ope}] ({x_start}, {y_start}) rectangle ({x_end}, {y_end});"
    elif kind == "man":
        x_coord = randint(min(x_start,x_end), max(x_start,x_end))
        y_coord = randint(min(y_start,y_end), max(y_start,y_end))
        size = randint(1,7)
        a_1 = randint(0,90)
        a_2 = randint(0,90)
        return f"\\node[line width={thick}mm, color=black!{ope}] at ({x_coord}, {y_coord}) {{\Strichmaxerl[{size}][{a_1}][{a_2}]}};"
        
def get_coords(
        x_range,
        y_range,
        length,
        side
        ):
    if side == "right":
        x_start = randint(x_range[1],x_range[1]+length)
        x_end = randint(x_range[1],x_range[1]+length*2)
    else:
        x_start = randint(x_range[0]-length, x_range[0])
        x_end = randint(x_range[0]-length*2, x_range[0])
    y_start = randint(y_range[1],y_range[0])
    y_end = randint(y_range[1],y_range[0])
    return x_start, x_end, y_start, y_end 

def lookup_len(
        key
        ):
    return df.loc[df.uneek == key,"relevent_len"].iloc[0]

def get_addlines(
        key
        ):
    return max_lines - lookup_len(key)

def get_insert_point(
        lst
        ):
    blanks = [idx for idx, x in enumerate(lst) if x == ""][1:-1]
    return choice(blanks)

def add_lines(
        eg,
        key,
        extra_lines=5
        ):
    st = make_lst(eg)
    x_range, y_range = get_range(lst)
    start = get_insert_point(lst)
    sec_a = lst[:start]
    sec_b = lst[start:]
    num_lines = get_addlines(key)
    rand_ext = randint(0,extra_lines)
    sec_add = [""]
    for i in range(num_lines+rand_ext):
        sec_add += [make_line(x_range, y_range)]
        add_break = randint(3,5)
        if i % add_break == 0:
            sec_add += [""]
    return sec_a + sec_add + sec_b

if __name__ == "__main__":
    tikz = load_tikz(PATH)
    with open("../static_materials/base/rand_base.tex","r") as f:
        r_base = f.read()
    for key, eg in tikz.items():
       rand = add_lines(eg, key)
       rand_tabbed = "\n".join([f"\t\t{line}" for line in rand])
       rand_out = r_base.replace(R,rand_tabbed)
       with open(f"../random_pulleys/rand_{key.lstrip('simp_')}.tex", "w") as f:
           f.write(rand_out)
    

    


    
    
    

   
    
