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
import re

# =============================================================================
# constants
# =============================================================================
START = "%%%%% START %%%%%"
END = "%%%%% END %%%%%"
R1 = "%%%%% REPLACE 1 %%%%%"
R2 = "%%%%% REPLACE 2 %%%%%"
PAD = 2
RADLG = 1
WIDTH = "0.5mm"
N_TABS = 4

# DEFAULT PATHS
INPATH = "../pulleys/tex/constant/simple/simp_*.tex"
OUTPATH = "../pulleys/tex/constant/compare/rand_compare_{}_random_{}.tex"
BPATH = "../pulleys/static_materials/compare_base.tex"

# =============================================================================
# Parser args
# =============================================================================
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--inpath", help="inpath directory to load tikz files")
parser.add_argument("-o", "--outpath", help="output directory to save modified tikz files")
parser.add_argument("-b", "--basepath", help="base tikz proforma into which to impute new designs")


args = vars(parser.parse_args())

if all(vals == None for vals in args.values()):
    inpath = INPATH
    outpath = OUTPATH
    basepath = BPATH
else:
    inpath = args['inpath'] 
    outpath = args['outpath']
    basepath = args["basepath"]
    
# =============================================================================
# Data
# =============================================================================
meta =  pd.read_excel("../metadata/pulley_master_key_simple_constant.xlsx")
with open(basepath, "r") as f:
    base = f.read()

# =============================================================================
# Tikz Functions
# =============================================================================
def make_floor_or_ceiling_tikx(x_start,x_end,height):
    end_height = height - 0.125
    tikz_code = f"""\\draw[fill=black] ({x_start},{height}) rectangle ({x_end},{end_height});
    """
    return tikz_code

def make_rope_pulley_tikz(x,y,radlg, connect_x=None, connect_y=None):        
    tikz_code = f"""\\draw ({x},{y}) circle ({radlg});
    \\draw[fill=black] ({x},{y}) circle (0.1);
    """
    if connect_y:
        assert connect_x is not None, "You have to define both connect_x and connect_y"
        tikz_code += f"""\\draw ({connect_x},{connect_y}) -- ({x},{y});
        """
    return tikz_code

def make_connected_pulley_tikz(x, y, radlg, orientation):
    if orientation == "horizontal":
        # Calculate dimensions for horizontal design
        rectangle_x_start = x - radlg - 0.4  # Adjusted for horizontal alignment
        rectangle_x_end = x + radlg + 0.4
        # Generate TiKZ code for horizontal wall mount pulley
        tikz_code = f"""\\draw ({x},{y}) circle ({radlg});
        \\draw[fill=black] ({x},{y}) circle (0.1);
        \\draw[pattern=north west lines, pattern color=black] ({rectangle_x_start},{y+0.1}) rectangle ({rectangle_x_end},{y-0.1});
        \\draw[fill=black!50] ({rectangle_x_start},{y}) circle (0.1);
        \\draw[fill=black!50] ({rectangle_x_end},{y}) circle (0.1);
        """
    else:
        # Calculate dimensions for vertical design
        rectangle_y_start = y + radlg + 0.5  # Adjusted for vertical alignment
        rectangle_y_end = y - radlg - 0.5
        # Generate TiKZ code for vertical wall mount pulley
        tikz_code = f"""\\draw ({x},{y}) circle ({radlg});
        \\draw[fill=black] ({x},{y}) circle (0.1);
        \\draw[pattern=north west lines, pattern color=black] ({x-0.1},{rectangle_y_start}) rectangle ({x+0.1},{rectangle_y_end});
        \\draw[fill=black!50] ({x},{rectangle_y_start}) circle (0.1);
        \\draw[fill=black!50] ({x},{rectangle_y_end}) circle (0.1);
        """
    return tikz_code

def make_weight(x, y, width, add_segment, height):
    # Generate TiKZ code for segment with weight
    if add_segment == "add":
        tikz_code = f"""\\draw[line width={width}]({x+1},{y+0.5}) -- ({x+1},{height});
        \\draw[line width={width}]({x+0.5},{y}) --  ({x+1},{y+0.5}) -- ({x+1.5},{y});
        \\draw[fill=black!50] ({x}, {y}) rectangle ({x+2}, {y-2});
        """
    else:
        tikz_code = f"""\\draw[line width={width}]({x+0.5},{y}) --  ({x+1},{y+0.5}) -- ({x+1.5},{y});
        \\draw[fill=black!50] ({x}, {y}) rectangle ({x+2}, {y-2});
        """
    return tikz_code

def make_weight_with_attachments(x, y, width, height):
    # Generate TiKZ code for segment with weight and two attachments
    tikz_code = f"""\\draw[fill=black!50] ({x+1},{height}) circle (0.1);
    \\draw[line width={width}]({x+0.5},{y+0.5}) -- ({x+1},{height}) --  ({x+1.5},{y+0.5});
    \\draw[line width={width}]({x},{y}) --  ({x+0.5},{y+0.5}) -- ({x+1},{y}) -- ({x+1.5},{y+0.5}) -- ({x+2},{y});
    \\draw[fill=black!50] ({x}, {y}) rectangle ({x+2}, {y-2});
    """
    return tikz_code

def make_rope_section(x, y, width, radrp):
    # Generate TiKZ code for rope section
    tikz_code = f"""\\draw[line width = {width}] ({x-radrp},{y}) -- ({x-radrp},{y+5});
    \\centerarc[line width = {width}]({x},{y+5})(0:180:{radrp});
    \\draw[line width = {width}] ({x+radrp},{y+5}) -- ({x+radrp},{y+2});
    \\centerarc[line width = {width}]({x+radrp+radrp},{y+2})(270:180:{radrp});
    \\draw[line width = {width}] ({x+radrp+radrp},{y+2-radrp}) -- ({x+3},{y+2-radrp});"""
    return tikz_code

def make_rope_section_two(x, y, width, radrp):
    # Generate TiKZ code for the second rope section
    tikz_code = f"""\\draw[line width = {width}] ({x},{y}) -- ({x+3},{y});
    \\centerarc[line width = {width}]({x},{y-radrp})(90:180:{radrp});
    \\draw[line width = {width}] ({x-radrp},{y-radrp}) -- ({x-radrp},{y-7});
    \\centerarc[line width = {width}]({x},{y-7})(180:360:{radrp});
    \\draw[line width = {width}] ({x+radrp},{y-7}) -- ({x+radrp},{y-3});
    \\centerarc[line width = {width}]({x+radrp+radrp},{y-3})(0:180:{radrp});
    \\draw[line width = {width}] ({x+radrp+radrp+radrp},{y-3}) -- ({x+radrp+radrp+radrp},{y-4});
    \\centerarc[line width = {width}]({x+radrp+radrp+radrp+radrp},{y-4})(180:270:{radrp});
    \\draw[line width = {width}] ({x+radrp+radrp+radrp+radrp},{y-radrp-4}) -- ({x+radrp+radrp+radrp+radrp+3},{y-radrp-4});"""
    return tikz_code

def make_random_rope_segment(x, y, width, radrp):
    length = choice([1,3,5,7])
    height = choice([1,3,5,7])
    # Rope Segment A: Starts with a straight line horizontally, then a 90-degree arc
    def segment_a():
        return f"""\\draw[line width = {width}] ({x},{y}) -- ({x+length},{y});  
        \\draw[line width = {width}] ({x+length},{y}) arc (270:360:{radrp}); 
        \\draw[line width = {width}] ({x+length+radrp},{y+radrp}) -- ({x+length+radrp},{y+radrp+height});"""

    # Rope Segment B: Starts with a 90-degree arc, then a vertical straight line
    def segment_b():
        return f"""\\draw[line width = {width}] ({x},{y}) arc (270:360:{radrp});
        \\draw[line width = {width}] ({x+radrp},{y+radrp}) -- ({x+radrp},{y+radrp+length});
        \\draw[line width = {width}] ({x+radrp},{y+radrp+length}) arc (0:90:{radrp});"""

    # Rope Segment C: Alternates between vertical straight line and a 90-degree arc
    def segment_c():
        return f"""\\draw[line width = {width}] ({x},{y}) -- ({x},{y+length});
        \\draw[line width = {width}] ({x-radrp},{y+length+radrp}) arc (90:0:{radrp});
        \\draw[line width = {width}] ({x-radrp},{y+length+radrp}) -- ({x-3*radrp},{y+5+radrp});"""

    # Randomly select one of the rope segments to return
    segment_functions = [segment_a, segment_b, segment_c]
    selected_segment = choice(segment_functions)()
    return selected_segment
        
def make_man_on_platform_tikz(x, y):
    # Calculate platform dimensions
    platform_x_start = x - 3
    platform_x_end = x + 1
    platform_y_start = y - 1.1
    platform_y_end = y - 1.2
    #arms
    theta_a = randint(-180, 180)
    theta_b = randint(-180, 180)
    # Generate TiKZ code for man on a platform
    tikz_code = f"""\\node at ({x}, {y}) {{\\scriptsize \\Strichmaxerl[10][{theta_a}][{theta_b}]}};
    \\draw[fill=black] ({platform_x_start}, {platform_y_start}) rectangle ({platform_x_end}, {platform_y_end});
    """
    return tikz_code

def make_man(x, y):
    theta_a = randint(-180, 180)
    theta_b = randint(-180, 180)
    # Generate TiKZ code for man on a platform
    tikz_code = f"""\\node at ({x}, {y}) {{\\scriptsize \\Strichmaxerl[10][{theta_a}][{theta_b}]}};
    """
    return tikz_code

# =============================================================================
# Random generate functions
# =============================================================================

def add_random_man(top, bottom, left, right):
    x = randint(int(round(left+PAD, 0)), int(round(right-PAD, 0)))
    y = randint(int(round(bottom+PAD, 0)), int(round(top-PAD, 0)))
    tikz_code = choice([make_man_on_platform_tikz, make_man])(x,y)
    return tikz_to_list(tikz_code)

def add_random_pulley(top, bottom, left, right, radlg):
    choices = ["connected", "rope"]
    kind = choice(choices)
    if kind == "rope":
        x = randint(int(round(left+PAD,0)), int(round(right-PAD,0)))
        y = randint(int(round(bottom+PAD,0)), int(round(top-PAD,0)))
        connect_y = top if abs(y-top) < abs(y-bottom) else bottom
        connect_x = randint(left, right)
        return tikz_to_list(make_rope_pulley_tikz(x,y,radlg,connect_x,connect_y))
    if kind == "connected":
        orientation = choice(["hoizontal", "vertical"])
        x = randint(int(round(left+PAD, 1)), int(round(right-PAD, 1)))
        y = randint(int(round(bottom+PAD, 1)), int(round(top-PAD, 1)))
        return tikz_to_list(make_connected_pulley_tikz(x,y,radlg,orientation))
        
def add_random_weight(top, bottom, left, right, radlg, width):
    x = randint(int(round(left+PAD, 0)), int(round(right-PAD, 0)))
    y = randint(int(round(bottom+PAD, 0)), int(round(top-PAD, 0)))
    kind = choice(["attached","unattached"])
    if kind == "unattached":
        add_segment = choice(["add","dont_add"])
        height = top - randint(1,3) if add_segment == "add" else None
        return tikz_to_list(make_weight(x, y, width, add_segment, height))
    else:
        height = randint(y,top)
        return tikz_to_list(make_weight_with_attachments(x, y, width, height))
    
def add_random_rope(top, bottom, left, right, radlg, width, rope_pad_bump):
    radrp = radlg + 0.1
    x = randint(int(round(left+PAD+rope_pad_bump, 0)), int(round(right-PAD-rope_pad_bump, 0)))
    y = randint(int(round(bottom+PAD+rope_pad_bump+1, 0)), int(round(top-PAD-rope_pad_bump-1, 0)))
    segment_functions = [make_rope_section, make_rope_section_two, make_random_rope_segment]
    selected_segment = choice(segment_functions)(x, y, width, radlg)
    return tikz_to_list(selected_segment)

# =============================================================================
# Helper functions
# =============================================================================
def lookup_pulleys(name):
    return meta.loc[meta.key == name,"num_pulleys"].iloc[0]

def tikz_to_list(tikz_code):
    return [x.strip() for x in tikz_code.split("\n")]

def list_to_tikz(tikz_list):
    return "\n".join(tikz_list)

def get_name(path):
    return path.split(".")[-2].split("/")[-1].replace("simp_","")

def add_tab(lst, n_tabs):
    return ["{}{}".format('\t' * n_tabs, string) for string in lst]

man_func  = lambda x: x.replace("\\Strichmaxerl", "\\scriptsize \\Strichmaxerl") if "\\Strichmaxerl" in x else x

# =============================================================================
# main functions
# =============================================================================
def create_compare(fn, name): 
    with open(fn, "r") as f:
        tikz = [l.strip() for l in f.readlines()]
    original_system = tikz[tikz.index(START)+1:tikz.index(END)]
    num_pulleys = lookup_pulleys(name)
    rects = [original_system[0], original_system[-1]]
    matches = [re.findall(r'\((-?\d+\.?\d*),\s*(-?\d+\.?\d*)\)', rect) for rect in rects]
    left = float(matches[0][0][0])
    right = float(matches[1][1][0])
    top = float(matches[0][0][1])
    bottom = float(matches[-1][1][1])
    random_system = [rects[0], ""]
    for i in range(num_pulleys):
        random_system += add_random_pulley(top, bottom, left, right, RADLG)
    random_system += add_random_weight(top, bottom, left, right, RADLG, WIDTH)
    man = add_random_man(top, bottom, left, right)
    len_man = len(man) - 1
    while len(random_system) < len(original_system) - len_man - 1:
        random_system += add_random_rope(top, bottom, left, right, RADLG, WIDTH, 3)
    random_system += [""]
    random_system += man
    random_system += [rects[1]]
    #adjust man size for font
    original_system = [x for x in map(man_func, original_system)]
    return random_system, original_system
    
def main(inpath, outpath):
    fns = glob.glob(inpath)
    for fn in fns:
        name = get_name(fn)
        random_system, original_system = create_compare(fn, name)
        random_system, original_system = add_tab(random_system, N_TABS), add_tab(original_system, N_TABS)
        direction = choice(["left","right"])
        result = base
        if direction == "left":
            result = result.replace(R1,list_to_tikz(random_system))
            result = result.replace(R2,list_to_tikz(original_system))
        else:
            result = result.replace(R2,list_to_tikz(random_system))
            result = result.replace(R1,list_to_tikz(original_system))    
        with open(outpath.format(name, direction), "w") as f:
            f.write(result)

        
if __name__ == "__main__":
   main(inpath = inpath, outpath=outpath)


  
       
   
   
   
   
   
   
   

