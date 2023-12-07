import glob
import pandas as pd

fns = [fn for fn in glob.glob("../pulleys/tex/constant/simple/*.tex")]

START = "%%%%% START %%%%%"
END = "%%%%% END %%%%%"

CROSSED = False

if CROSSED:
    result = dict(
        design_name=list(),
        relevent_len=list(),
        total_len=list(),
        MA=list(),
        height=list(),
        pulley_diam=list(),
        thickness=list()
        )
else:
    result = dict(
        design_name=list(),
        relevent_len=list(),
        total_len=list(),
        MA=list()
        )

def process_design_name(design_name):
    MA = int(''.join(x for x in design_name.split("_")[1] if x.isnumeric()))
    if CROSSED:
        height = int("".join(x for x in design_name.split("_")[4] if x.isnumeric()))
        pulley_diam = float(design_name.split("_")[-2].replace("radlg",""))
        thickness = float(design_name.split("_")[-1].replace("width","").replace("mm",""))
        return MA, height, pulley_diam, thickness
    else:
        return MA

def make_result(fns):
    for fn in fns:
        with open(fn, "r") as f:
            diag_list = [l.strip() for l in f.readlines()]
        design_name = fn.split("/")[-1].rstrip(".tex")
        diag_striped = [l for l in diag_list if not l == ""]
        total_len = len(diag_list)
        relevent_len = diag_striped.index(END) - diag_striped.index(START) - 1
        if CROSSED:
            MA, height, pulley_diam, thickness = process_design_name(design_name)
        else:
            MA = process_design_name(design_name)
        
        #save results to dict
        result["design_name"] += [design_name]
        result["relevent_len"] += [relevent_len]
        result["total_len"] += [total_len]
        result["MA"] += [MA]
        if CROSSED:
            result["height"] += [height]
            result["pulley_diam"] += [pulley_diam]
            result["thickness"] += [thickness]
    return result

if __name__ == "__main__":
    result = make_result(fns)
    df = pd.DataFrame(result)
    if CROSSED:
        df["key"] = df.design_name.apply(lambda dn: f"{'_'.join(i for i in dn.split('_')[1:4])}.tex")
    dx = pd.read_excel("../metadata/pulley_key.xlsx")
    dy = pd.merge(dx,df,on="key")
    dy.to_excel("../metadata/pulley_master_key.xlsx", index=False)
