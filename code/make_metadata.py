import glob
import pandas as pd

fns = [fn for fn in glob.glob("../simple_pulleys/*.tex")]

START = "%%%%% START %%%%%"
END = "%%%%% END %%%%%"


result = dict(
    uneek=list(),
    relevent_len=list(),
    total_len=list(),
    MA=list(),
    height=list(),
    pulley_diam=list(),
    thickness=list()
    )

def process_uneek(uneek):
    MA = int(''.join(x for x in uneek.split("_")[1] if x.isnumeric()))
    height = int("".join(x for x in uneek.split("_")[4] if x.isnumeric()))
    pulley_diam = float(uneek.split("_")[-2].replace("radlg",""))
    thickness = float(uneek.split("_")[-1].replace("width","").replace("mm",""))
    return MA, height, pulley_diam, thickness

def make_result(fns):
    for fn in fns:
        with open(fn, "r") as f:
            diag_list = [l.strip() for l in f.readlines()]
        uneek = fn.split("/")[-1].rstrip(".tex")
        diag_striped = [l for l in diag_list if not l == ""]
        total_len = len(diag_list)
        relevent_len = diag_striped.index(END) - diag_striped.index(START) - 1
        MA, height, pulley_diam, thickness = process_uneek(uneek)
        
        #save results to dict
        result["uneek"] += [uneek]
        result["relevent_len"] += [relevent_len]
        result["total_len"] += [total_len]
        result["MA"] += [MA]
        result["height"] += [height]
        result["pulley_diam"] += [pulley_diam]
        result["thickness"] += [thickness]
    return result

if __name__ == "__main__":
    result = make_result(fns)
    df = pd.DataFrame(result)
    df["key"] = df.uneek.apply(lambda uneek: f"{'_'.join(i for i in uneek.split('_')[1:4])}.tex")
    dx = pd.read_excel("../metadata/pulley_key.xlsx")
    dy = pd.merge(dx,df,on="key")
    df.to_excel("../metadata/pulley_master_key.xlsx", index=False)
