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
from numpy import cos as _cos
from numpy import sin as _sin
from math import pi

# =============================================================================
# constants
# =============================================================================
START = "%%%%% START %%%%%"
END = "%%%%% END %%%%%"
R = "%%%%% REPLACE %%%%%"
PATH = "../pulleys/original_designs/MA*/*.tex"
OUTPUT_PATH = "../pulleys/tex/crossed/simple/simp_{}.tex"
BASE_PATH = "../pulleys/static_materials/standalone_base.tex"
PRECISION = 4

# =============================================================================
# parse args
# =============================================================================
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--inpath", help="inpath directory to load tikz files")
parser.add_argument("-o", "--outpath", help="output directory to save modified tikz files")
parser.add_argument("-b", "--basepath", help="path to the base .tex file")

args = vars(parser.parse_args())

if all(vals == None for vals in args.values()):
    inpath = PATH
    outpath = OUTPUT_PATH
    bpath = BASE_PATH
else:
    inpath = args['inpath'] 
    outpath = args['outpath']
    bpath = args["basepath"]

# =============================================================================
# functions
# =============================================================================

def convert_deg(deg):
    return deg/180*pi

def cos(deg):
    return _cos(convert_deg(deg))

def sin(deg):
    return _sin(convert_deg(deg))
    
def load_tikz(path):
    keys = [key.split("/")[-1].rstrip(".tex") for key in glob.glob(path)]
    pics = [open(x,"r").read() for x in glob.glob(path)]
    pics = [pic.split(START)[1].split(END)[0] for pic in pics]
    return dict(zip(keys,pics))

def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

def replacer(string, new_string, start, stop):
    # insert the new string between "slices" of the original
    return string[:start] + new_string + string[stop+1:]

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def make_simple_complex(_var_map):
    # Make map of within var replacements
    simple_map = {}
    for name, val in _var_map.items():
        if is_number(val):
            simple_map[name] = str(eval(val))
        elif val.endswith("mm"):
            simple_map[name] = val
    
    # Seperate out compound variables
    complex_map = {k:v for k,v in _var_map.items() if k not in simple_map}

    # Sub in simple for compound values    
    complex_map_subbed = {}
    for c_key,c_val in complex_map.items():
        for s_key,s_val in simple_map.items():
            if s_key in c_val:
                c_val = c_val.replace(s_key,str(s_val))
            complex_map_subbed[c_key] = c_val
   
    # Evaluate compound vars
    complex_map_subbed_eval = {}
    for key,val in complex_map_subbed.items():
        try:
            v = str(eval(val))
        except SyntaxError:
            v = val
        complex_map_subbed_eval[key] = v
        
    # Combine simple and subbed compount vars
    _var_map = {**simple_map, **complex_map_subbed_eval}
   
    # Recursion to catch any recursively defined variables 
    if len(complex_map_subbed) > 0:
        _var_map = make_simple_complex(_var_map)
    return _var_map

def sub_numbers_for_vars(eg):
    # split + strip
    eg = eg.strip()
    lst = [x.strip() for x in eg.split("\n")]
    
    # Build var map    
    var_lst = [line for line in lst if line.startswith("\\def")]
    var_names = [line.replace("\\def","")[0:line.replace("\\def","").index("{")] for line in var_lst]
    var_vals = [line[line.index("{")+1:line.index("}")] for line in var_lst]
    var_map = {name:val for name,val in zip(var_names,var_vals)}
    
    # Recursive function to weed out chain definitions
    var_map = make_simple_complex(var_map)
        
    # Get non var lines
    pic_lst = [x for x in lst if not x.startswith("\\def")]
    pic_list = [val for idx,val in enumerate(pic_lst) if val != "" or idx != 0]

    #join back to string
    pic_string = "\n".join(pic_list)
    
    # replace values
    for key,val in var_map.items():
        pic_string = pic_string.replace(key,val)
    return pic_string

def cos_play(ts,func_name):
    start = ts.index(func_name)
    stop = ts.index(func_name) + ts[ts.index(func_name):].index(")")
    return start, stop, ts[start:stop+1]

def eval_trig(ts):
    funcs = ["cos","sin"]
    for fname in funcs:
        while fname in ts:
            start, stop, string =  cos_play(ts,fname)
            new_string = str(round(eval(string),PRECISION))
            ts = replacer(ts,new_string,start,stop)
    return ts

def eval_func(string):
    try:
        eval_res = eval(string)
    except SyntaxError:
        eval_res = string
    return eval_res


def clean_evals(eval_val):
    if isinstance(eval_val,tuple):
        vals = []
        for val in eval_val:
            if isinstance(val,set):
                val = list(val)[0]
            vals += [val]
        return str(tuple(round(i,PRECISION) for i in vals))
    else:
        return f"({eval_val})"
    
def sub_in_evaluated(ts):
    ts = eval_trig(ts)
    starts = find(ts,"(")
    stops = find(ts,")")
    spans = [(a,b) for a,b in zip(starts,stops)]
    
    evals = []
    for start,stop in spans[::-1]:
        span = ts[start:stop+1]
        if ":" not in span:
            eval_val = eval_func(span)
            eval_str_clean = clean_evals(eval_val)
            string = replacer(ts,eval_str_clean,start,stop)      
        ts = string
    return ts

def main(
        inpath,
        outpath,
        bpath
        ):
    pics = load_tikz(inpath)
    with open(bpath,"r") as f:
        s_base = f.read()
    for name, pic in pics.items():
        ts = sub_numbers_for_vars(pic)
        ts_eval = sub_in_evaluated(ts)
        if bpath.endswith("article_base.tex"):
            tab = "\t\t\t{}"
        else:
            tab = "\t\t{}"
        ts_tabbed = "\n".join([tab.format(line.replace('\t','').lstrip()) for line in ts_eval.split("\n")])
        ts_out = s_base.replace(R,ts_tabbed)
        with open(outpath.format(name), "w") as f:
            f.write(ts_out)
    
if __name__ == "__main__":
    main(inpath, outpath, bpath)
