import glob
import pandas as pd



START = "%%%%% START %%%%%"
END = "%%%%% END %%%%%"

def make_dict(_crossed):
    if _crossed == "crossed":
        result = dict(
            design_name=list(),
            relevent_len=list(),
            total_len=list(),
            MA=list(),
            ceiling_height=list(),
            pulley_radius=list(),
            rope_width=list()
            )
    else:
        result = dict(
            design_name=list(),
            relevent_len=list(),
            total_len=list(),
            MA=list()
            )
    return result

def process_design_name(design_name, _crossed):
    MA = int(''.join(x for x in design_name.split("_")[1] if x.isnumeric()))
    if _crossed == "crossed":
        try:
            ceiling_height = int("".join(x for x in design_name.split("_")[4] if x.isnumeric()))
            pulley_radius = float(design_name.split("_")[-2].replace("radlg",""))
            rope_width = float(design_name.split("_")[-1].replace("width","").replace("mm",""))
        except Exception as e:
            print(e)
            print(design_name)
        return MA, ceiling_height, pulley_radius, rope_width
    else:
        return MA

def make_result(fns, _crossed):
    # make dict
    result = make_dict(_crossed)
    for fn in fns:
        with open(fn, "r") as f:
            diag_list = [l.strip() for l in f.readlines()]
        design_name = fn.split("/")[-1].rstrip(".tex")
        diag_striped = [l for l in diag_list if not l == ""]
        total_len = len(diag_list)
        relevent_len = diag_striped.index(END) - diag_striped.index(START) - 1
        if _crossed == "crossed":
            MA, ceiling_height, pulley_radius, rope_width = process_design_name(design_name, _crossed)
        else:
            MA = process_design_name(design_name, _crossed)
        
        #strip type
        #design_name = design_name.lstrip("_simp").lstrip("_rand")
        #save results to dict
        result["design_name"] += [design_name]
        result["relevent_len"] += [relevent_len]
        result["total_len"] += [total_len]
        result["MA"] += [MA]
        if _crossed == "crossed":
            result["ceiling_height"] += [ceiling_height]
            result["pulley_radius"] += [pulley_radius]
            result["rope_width"] += [rope_width]
    return result

def main(_crossed, _type):
    assert _crossed in ["crossed", "constant"], "_crossed must == `crossed` | `constant`"
    assert _type in ["random", "simple"], "_type must == `random` | `simple`"
    #get fns
    fns = [fn for fn in glob.glob(f"../pulleys/tex/{_crossed}/{_type}/*.tex")]
    result = make_result(fns, _crossed)
    df = pd.DataFrame(result)

    df["key"] = df.design_name.apply(lambda dn: '_'.join(i for i in dn.split('_')[1:4]))
        
    dx = pd.read_excel("../metadata/pulley_key.xlsx")
    
    dy = pd.merge(dx,df,on="key")
    dy["condition"] = "no_distractor" if _type == "simple" else "distractor"
    #dy.to_excel(f"../metadata/pulley_master_key_{_type}_{_crossed}.xlsx", index=False)
    return dy
    
if __name__ == "__main__":
    df = pd.concat([main(_crossed, _type) for _crossed in ["crossed"] for _type in ["random", "simple"]])
    df.to_excel(f"../metadata/pulley_master_key.xlsx", index=False)

