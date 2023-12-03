import glob
import os
import re

# =============================================================================
# constants
# =============================================================================
a_values = [10, 12, 14]
radgl_values = [0.5, 0.75, 1]
width_values = ["0.5mm", "0.75mm", "1mm"] #need to purmute this, too


#PATH = "../pulley_materials/pulleys/MA*/*.tex" # I must have changed the dir name from pulley_materials -> pulleys :?
PATH = "../pulleys/MA*/*.tex"
OUTPUT_PATH = "../modified_pulleys" 

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

def save_modified_tikz(name, content):
    with open(os.path.join(OUTPUT_PATH, name), "w") as file:
        file.write(content)


# =============================================================================
# some debugging vals
# =============================================================================
a = 40
width = "0.75mm"
radlg=0.5
tikz_content=tikz_files["MA1_B_0.tex"]
print(replace_values(tikz_content, a, radlg, width))
# =============================================================================
# main script
# =============================================================================
if __name__ == "__main__":
    # Load all TikZ files
    tikz_files = load_tikz(PATH)
    
    # Check if files were found
    if not tikz_files:
        print("No files found. Check the PATH.")
    else:
        # Process each file
        for name, content in tikz_files.items(): # TO DO: Change this to the permutation of a_values, radlg_values, and width_values
            # Iterate over each set of values
            for i in range(len(a_values)):
                # Replace the values in the content
                modified_content = replace_values(content, a_values[i], radgl_values[i], width_values[i])
                # Construct the new file name
                modified_name = f"{name[:-4]}_a{a_values[i]}_radgl{radgl_values[i]}_width{width_values[i]}.tex"
                # Save the modified file
                save_modified_tikz(modified_name, modified_content)
                print(f"Saved modified file: {modified_name}")  # Print out confirmation
