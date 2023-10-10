import glob
import pandas as pd

fns = [fn for fn in glob.glob("./simple_pulleys/*.tex")]

START = "%%%%% START %%%%%"
END = "%%%%% END %%%%%"


result = dict(
    relevent_len=list(),
    total_len=list(),
    uneek=list()
    )

for fn in fns:
    with open(fn, "r") as f:
        diag_list = [l.strip() for l in f.readlines()]
    uneek = fn.split("/")[-1].split(".")[0]
    diag_striped = [l for l in diag_list if not l == ""]
    total_len = len(diag_list)
    relevent_len = diag_striped.index(END) - diag_striped.index(START) - 1
    
    #save results to dict
    result["relevent_len"] += [relevent_len]
    result["total_len"] += [total_len]
    result["uneek"] += [uneek]
    
df = pd.DataFrame(result)

df.to_excel("number_of_lines.xlsx", index=False)
