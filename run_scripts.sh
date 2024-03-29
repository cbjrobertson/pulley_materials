#!/bin/bash

## Clean old versions
#find ./pulleys/pdfs -type f -iname '*.pdf' -delete
#find ./pulleys/jpgs -type f -iname '*.jpg' -delete
#find ./pulleys/tex -type f \( -iname '*.pdf' -o -iname '*.aux' -o -iname '*.log' -o -iname '*.gz' \) -delete
#find ./pulleys/tex -type f -iname '*.tex' -delete
find ./pulleys/tex/constant/compare -type f -iname '*.tex' -delete
find ./pulleys/pdfs/constant/compare -type f -iname '*.pdf' -delete
find ./pulleys/jpgs/constant/compare -type f -iname '*.jpg' -delete

#### Run scripts
cd code
### constant versions
#python make_simple_pulleys.py -i "../pulleys/original_designs/MA*/*.tex" -o "../pulleys/tex/constant/simple/simp_{}.tex" -b "../pulleys/static_materials/article_base.tex"
##python add_random_elements.py -i "../pulleys/tex/constant/simple/*.tex" -o "../pulleys/tex/constant/random/rand_{}.tex" -b "../pulleys/static_materials/article_base.tex"
##
### Crossed versions
##python modify_constants.py -i "../pulleys/original_designs/MA*/*.tex" -o "../pulleys/tex/crossed/crossed"
##python make_simple_pulleys.py -i "../pulleys/tex/crossed/crossed/*.tex" -o "../pulleys/tex/crossed/simple/simp_{}.tex" -b "../pulleys/static_materials/article_base.tex"
##python add_random_elements.py -i "../pulleys/tex/crossed/simple/*.tex" -o "../pulleys/tex/crossed/random/rand_{}.tex" -b "../pulleys/static_materials/article_base.tex" --crossed
##
### Compare version
python add_random_blocks.py -i "../pulleys/tex/constant/simple/simp_*.tex" -o "../pulleys/tex/constant/compare/rand_compare_{}_random_{}.tex" -b "../pulleys/static_materials/compare_base.tex"
cd ..
#
## Compile pdfs from .tex docs and clean up
#cd ./pulleys/tex/constant/simple
#find . -type f -name "*.tex" | while read file; do xelatex "$file"; echo "$file"; done
#find . -name "*.pdf" -exec mv {} ../../../pdfs/constant/simple \;
#find . -type f \( -iname '*.pdf' -o -iname '*.aux' -o -iname '*.log' -o -iname '*.gz' \) -delete
#cd ../../../../
#
## #Compile compare
cd ./pulleys/tex/constant/compare
find . -type f -name "*.tex" | while read file; do xelatex "$file"; echo "$file"; done
find . -name "*.pdf" -exec mv {} ../../../pdfs/constant/compare \;
find . -type f \( -iname '*.pdf' -o -iname '*.aux' -o -iname '*.log' -o -iname '*.gz' \) -delete
cd ../../../../
#
## Compile constant random
#cd ./pulleys/tex/constant/random
#find . -type f -name "*.tex" | while read file; do pdflatex "$file"; echo "$file"; done
#find . -name "*.pdf" -exec mv {} ../../../pdfs/constant/random \;
#find . -type f \( -iname '*.pdf' -o -iname '*.aux' -o -iname '*.log' -o -iname '*.gz' \) -delete
#cd ../../../../
#
### Compile crossed simple
#cd ./pulleys/tex/crossed/simple
#find . -type f -name "*.tex" | while read file; do pdflatex "$file"; echo "$file"; done
#find . -name "*.pdf" -exec mv {} ../../../pdfs/crossed/simple \;
#find . -type f \( -iname '*.pdf' -o -iname '*.aux' -o -iname '*.log' -o -iname '*.gz' \) -delete
#cd ../../../../
#
## Compile crossed random
#cd ./pulleys/tex/crossed/random
#find . -type f -name "*.tex" | while read file; do pdflatex "$file"; echo "$file"; done
#find . -name "*.pdf" -exec mv {} ../../../pdfs/crossed/random \;
#find . -type f \( -iname '*.pdf' -o -iname '*.aux' -o -iname '*.log' -o -iname '*.gz' \) -delete
#cd ../../../../
#
#
## Run jpg conversions
cd code
#python make_pdfs_jpgs.py -i "../pulleys/pdfs/constant/random/*.pdf" -o "../pulleys/jpgs/constant/random/{}.jpg"
#python make_pdfs_jpgs.py -i "../pulleys/pdfs/constant/simple/*.pdf" -o "../pulleys/jpgs/constant/simple/{}.jpg"
#python make_pdfs_jpgs.py -i "../pulleys/pdfs/crossed/random/*.pdf" -o "../pulleys/jpgs/crossed/random/{}.jpg"
#python make_pdfs_jpgs.py -i "../pulleys/pdfs/crossed/simple/*.pdf" -o "../pulleys/jpgs/crossed/simple/{}.jpg"
python make_pdfs_jpgs.py -i "../pulleys/pdfs/constant/compare/*.pdf" -o "../pulleys/jpgs/constant/compare/{}.jpg"
cd ..

#Finish
echo "All done!!!"

