#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 10:17:44 2024

@author: cole
"""


import glob
import pandas as pd

fns = [fn for fn in glob.glob("../pulleys/tex/crossed/random/*.tex")]

START = "%%%%% START %%%%%"
END = "%%%%% END %%%%%"

result = []

for fn in fns:
    with open(fn, "r") as f:
        diag_list = [l.strip() for l in f.readlines()]
    design_name = fn.split("/")[-1].rstrip(".tex")
    diag_striped = [l for l in diag_list if not l == ""]
    total_len = len(diag_list)
    relevent_len = diag_striped.index(END) - diag_striped.index(START) - 1
    result += [{"uneek": design_name, "relevent_len": relevent_len}]
    
df = pd.DataFrame(result)
