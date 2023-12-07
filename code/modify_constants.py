# =============================================================================
# imports
# =============================================================================
import glob
import os
import re
import itertools

# =============================================================================
# constants
# =============================================================================
a_values = [9, 11.5, 14]
radlg_values = [0.5, 0.8, 1.1]
width_values = ["0.5mm","0.8mm", "1.1mm"] #need to purmute this, too
PATH = "../pulleys/original_designs/MA*/*.tex"
OUTPUT_PATH = "../pulleys/tex/crossed/crossed" 

# =============================================================================
# parse args
# =============================================================================
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--inpath", help="inpath directory to load tikz files")
parser.add_argument("-o", "--outpath", help="output directory to save modified tikz files")
args = vars(parser.parse_args())

if all(vals == None for vals in args.values()):
    inpath = PATH
    outpath = OUTPUT_PATH
else:
    inpath = args['inpath'] 
    outpath = args['outpath']

# =============================================================================
# Cross vals
# =============================================================================
iter_lsts = [a_values, radlg_values, width_values]
cross_lst = list(itertools.product(*iter_lsts))

# =============================================================================
# functions
# =============================================================================
def load_tikz(path):
    files = glob.glob(path)
    return {os.path.basename(f): open(f, "r").read() for f in files}

def replace_values(tikz_content, a, radlg, width):
    #relative definition of radrp
    radrp = radlg + 0.1

    # Regular expressions - \def\a{10}
    a_pattern = r"(\\def\\a\{)\d*\.?\d*(\})"
    radgl_pattern = r"(\\def\\radlg\{)\d*\.?\d*(\})"
    radrp_pattern = r"(\\def\\radrp\{)\d*\.?\d*(\})"
    width_pattern = r"\\def\\width\{\d*\.?\d*\w\w\}" # Add regex for width
    

    # Replace values
    new_content = re.sub(a_pattern, rf"\\def\\a{{{a}}}", tikz_content) 
    # Note you need to replace the whole matched string to get the desired response. Also f-strings are nice
    new_content = re.sub(radgl_pattern, rf"\\def\\radlg{{{radlg}}}", new_content)
    new_content = re.sub(radrp_pattern,  rf"\\def\\radrp{{{radrp}}}", new_content)
    new_content = re.sub(width_pattern,  rf"\\def\\width{{{width}}}", new_content) #added width replace

    return new_content

def save_modified_tikz(name, content, outpath):
    with open(os.path.join(outpath, name), "w") as file:
        file.write(content)


def main(
        inpath, 
        outpath
        ):
    # Load all TikZ files
    tikz_files = load_tikz(inpath)
    
    # Check if files were found
    if not tikz_files:
        print("No files found. Check the PATH.")
    else:
        # Process each file
        for name, content in tikz_files.items(): # TO DO: Change this to the permutation of a_values, radlg_values, and width_values
            # Iterate over each set of values
            for a, radlg, width in cross_lst:
                # Replace the values in the content
                modified_content = replace_values(content, a, radlg, width)
                # Construct the new file name
                modified_name = f"{name[:-4]}_a{a}_radlg{radlg}_width{width}.tex"
                # Save the modified file
                save_modified_tikz(modified_name, modified_content, outpath)
                print(f"Saved modified file: {modified_name}")  # Print out confirmation
    
# =============================================================================
# main script
# =============================================================================
if __name__ == "__main__":
    main(inpath, outpath)

