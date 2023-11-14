#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 16:54:50 2023

@author: cole
"""
Í
# =============================================================================
# imports
# =============================================================================
import itertools
import random
import glob
import pandas as pd

# =============================================================================
# CONSTNTS
# =============================================================================
PATH = "../simple_pulleys/MA*/*.tex"
START = "%%%%% START %%%%%"
END = "%%%%% END %%%%%"
R1 = "%%%%% REPLACE 1 %%%%%"
R2 = "%%%%% REPLACE 2 %%%%%"

# =============================================================================
# functions
# =============================================================================
def load_tikz(path):
    keys = [key.split("/")[-1].split(".")[0] for key in glob.glob(path)]
    pics = [open(x,"r").read() for x in glob.glob(path)]
    pics = [pic.split(START)[1].split(END)[0] for pic in pics]
    return dict(zip(keys,pics))

def ma_from_key(key,
                slc=1):
    return int(key.split("_")[slc][-1])

def make_df(pics):
    keys = list(pics.keys())
    comps = [random.sample(list(x),len(x)) for x in itertools.combinations(keys,2)]
    
    df = pd.DataFrame({"key_1": [x[0] for x in comps],
                       "key_2": [x[1] for x in comps]})
    
    df["fig_1"] = df.key_1.apply(lambda key: pics[key])
    df["fig_2"] = df.key_2.apply(lambda key: pics[key])
    
    df["correct"] = df.apply(lambda row: "B" if ma_from_key(row.key_1)-ma_from_key(row.key_2) < 0 else "A" if \
                             ma_from_key(row.key_1)-ma_from_key(row.key_2) > 0 else "C",axis=1)
        
    df["test"] = df.apply(lambda row: base.replace(R1,row.fig_1).replace(R2,row.fig_2),axis=1)
    
    df = df.reset_index(drop=True,inplace=False)
    df["id"] = df.index
    df["uneek"] = df.key_1 + "_" + df.key_2
    return df


# =============================================================================
# OPEN FILES
# =============================================================================
with open("../experimental_materials/base/base.tex","r") as f:
    base = f.read()
    
    
if __name__ == "__main__":
    pics = load_tikz(PATH)
    df = make_df(pics)
    df.to_pickle("../experimental_materials/exp_df_simple.pkl")
    df.to_excel("../experimental_materials/exp_df_simple.xlsx",index=False)





