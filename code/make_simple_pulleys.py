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
from numpy import cos, sin

# =============================================================================
# constants
# =============================================================================
START = "%%%%% START %%%%%"
END = "%%%%% END %%%%%"
R = "%%%%% REPLACE %%%%%"
PATH = "../pulleys/MA*/*.tex"
PRECISION = 3

# =============================================================================
# functions
# =============================================================================
def load_tikz(path):
    keys = [key.split("/")[-1].split(".")[0] for key in glob.glob(path)]
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

if __name__ == "__main__":
    pics = load_tikz(PATH)
    with open("../static_materials/base/single_base.tex","r") as f:
        s_base = f.read()
    for name, pic in pics.items():
        ts = sub_numbers_for_vars(pic)
        ts_eval = sub_in_evaluated(ts)
        ts_tabbed = "\n".join([f"\t\t\t\t{line}" for line in ts_eval.split("\n")])
        ts_out = s_base.replace(R,ts_tabbed)
        with open(f"../simple_pulleys/simp_{name}.tex", "w") as f:
            f.write(ts_out)
