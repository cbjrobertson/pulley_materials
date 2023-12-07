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
PATH = "../pulleys/tex/crossed/simple/*.tex"
OUTPUT_PATH = "../pulleys/tex/crossed/random/rand_{}.tex"
BASE_PATH = "../pulleys/static_materials/article_base.tex"
CROSSED = True

# =============================================================================
# parse args
# =============================================================================
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--inpath", help="inpath directory to load tikz files")
parser.add_argument("-o", "--outpath", help="output directory to save modified tikz files")
parser.add_argument("--crossed", action="store_true", help="whether script is processing crossed tikz designs or not")
parser.add_argument("-b", "--basepath", help="path to the base .tex file")
parser.set_defaults(crossed=None)

args = vars(parser.parse_args())

if all(vals == None for vals in args.values()):
    inpath = PATH
    outpath = OUTPUT_PATH
    crossed = CROSSED
    bpath = BASE_PATH
else:
    inpath = args['inpath'] 
    outpath = args['outpath']
    crossed = args["crossed"]
    bpath = args["basepath"]

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
        key,
        crossed
        ):
    if crossed:
        lookup_key = f"simp_{'_'.join([x for x in key.split('_')][1:4])}"
    else:
        lookup_key = key
    return df.loc[df.design_name == lookup_key,"relevent_len"].iloc[0]

def get_addlines(
        key,
        crossed
        ):
    return max_lines - lookup_len(key,crossed)

def get_insert_point(
        lst
        ):
    blanks = [idx for idx, x in enumerate(lst) if x == ""][1:-1]
    return choice(blanks)

def add_lines(
        eg,
        key,
        crossed,
        extra_lines=5
        ):
    lst = make_lst(eg)
    x_range, y_range = get_range(lst)
    start = get_insert_point(lst)
    sec_a = lst[:start]
    sec_b = lst[start:]
    num_lines = get_addlines(key, crossed)
    rand_ext = randint(0,extra_lines)
    sec_add = [""]
    for i in range(num_lines+rand_ext):
        sec_add += [make_line(x_range, y_range)]
        add_break = randint(3,5)
        if i % add_break == 0:
            sec_add += [""]
    return sec_a + sec_add + sec_b

def main(
        inpath, 
        outpath,
        crossed,
        bpath
        ):
    tikz = load_tikz(inpath)
    with open(bpath,"r") as f:
        r_base = f.read()
    for key, eg in tikz.items():
       rand = add_lines(eg, key, crossed)
       if bpath.endswith("article_base.tex"):
           tab = "\t\t\t{}"
       else:
           tab = "\t\t{}"
       rand_tabbed = "\n".join([tab.format(line) for line in rand])
       rand_out = r_base.replace(R,rand_tabbed)
       with open(outpath.format(key.lstrip('simp_')), "w") as f:
           f.write(rand_out)
           
if __name__ == "__main__":
    main(inpath, outpath, crossed, bpath)
    

    


    
    
    

   
    
