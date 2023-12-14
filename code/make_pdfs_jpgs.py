# =============================================================================
# imports
# =============================================================================
import glob
import argparse
from ironpdf import PdfDocument

# =============================================================================
# constants
# =============================================================================
PATH = "../pulleys/pdfs/constant/random/*.pdf"
OUTPUT_PATH = "../pulleys/jpgs/constant/random/{}.jpg" 

# =============================================================================
# parse args
# =============================================================================

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--inpath", help="inpath directory to load pdfs files")
parser.add_argument("-o", "--outpath", help="output directory to save jpgs")
args = vars(parser.parse_args())

if all(vals == None for vals in args.values()):
    inpath = PATH
    outpath = OUTPUT_PATH
else:
    inpath = args['inpath'] 
    outpath = args['outpath']
    
# =============================================================================
# functions
# =============================================================================
def convert_pdf(inpath, outpath):
    name = inpath.split("/")[-1].rstrip(".pdf")
    pdf = PdfDocument.FromFile(inpath)
    # # Extract all pages to a folder as image files
    pdf.RasterizeToImageFiles(outpath.format(name),DPI=96)
    

def main(inpath, outpath):
    fns = [fn for fn in glob.glob(inpath)]
    for fn in fns:
        try:
            convert_pdf(fn, outpath)
        except Exception as e:
            print(f"The file {fn} caused hte following error: {e}")

# =============================================================================
# Run    
# =============================================================================
if __name__ == "__main__":
    main(inpath, outpath)
