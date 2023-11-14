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
from load_materials import load_tikz, PATH

# =============================================================================
# constants
# =============================================================================
R = "%%%%% REPLACE %%%%%"

def get_var_map(line):
    return (x.rstrip("}") for x in line.split("\\")[-1].split("{"))

def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]


def replacer(string, new_string, start, stop):
    # insert the new string between "slices" of the original
    return string[:start] + new_string + string[stop+1:]

def sub_numbers_for_vars(eg):
    # split + strip
    eg = eg.strip()
    lst = [x.strip() for x in eg.split("\n")]
    
    #build var map    
    var_dict = {}
    res = []
    for idx,line in enumerate(lst):
        if line.startswith("\\def"):
            key,val = get_var_map(line)
            var_dict[f"\\{key}"] = val
        else:
            if not line.startswith("%"):
                res += [line]
        
    #join back to string
    pic_string = "\n".join(res)
    
    # replace values
    for key,val in var_dict.items():
        pic_string = pic_string.replace(key,val)
        
    return pic_string

def eval_func(string,precision=2):
    eval_res = eval(string)
    if not isinstance(eval_res,tuple):
        round_eval_res = round(eval_res,precision)
        eval_string = f"({round_eval_res})"
    else:
        round_eval_res = tuple(round(i,precision) for i in eval_res)
        eval_string = str(round_eval_res)
    return eval_string
    
def sub_in_evaluated(ts):
    starts = find(ts,"(")
    stops = find(ts,")")
    spans = [(a,b) for a,b in zip(starts,stops)]
    for start,stop in spans[::-1]:
        span = ts[start:stop+1]
        if ":" not in span:
            eval_string = eval_func(span)
            string = replacer(ts,eval_string,start,stop)
        ts = string
    return ts

def make_simple(pics):
    import os
    for key,eg in pics.items():
        ts = sub_numbers_for_vars(eg)
        res = sub_in_evaluated(ts)
        res_tabbed = "\n".join([f"\t\t\t\t{line}" for line in res.split("\n")])
        res_out = s_base.replace(R,res_tabbed)
        fp = f"../simple_pulleys/{key.strip('.tex')}"
        if not os.path.exists(fp):
            os.mkdir(fp)
        with open(fp + f"/simp_{key}.tex", "w") as f:
            f.write(res_out)

# =============================================================================
# OPEN FILES
# =============================================================================
if __name__ == "__main__":
    pics = load_tikz(PATH)
    with open("../experimental_materials/base/single_base.tex","r") as f:
        s_base = f.read()
    make_simple(pics)
