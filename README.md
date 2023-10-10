# Pulley Experiments

Hi Sam. We can use this repo to manage shared work on developing 
experimental materials for the pulley experiments which test the 
mechanical reasoning abilities of LLMs.

If you want to use a desktop Latex editor, I recommend 
[TeXstudio](https://www.texstudio.org/), or just use 
[Overleaf](https://www.overleaf.com/), though that will mean you'll have 
to either faff with uploading these source files, or set up [Dropbox 
syncing](https://www.overleaf.com/learn/how-to/Dropbox_Synchronization). 
You should have a premium account through your .edu email. 

Pulley systems are in `original_materials/`. If you write any python scripts to do anything, put them in `code/`. Systems `MA1_A`, `MA1_B`, and `MA2_A` are done, so have a look at them. 
The task is to refactor the TeX code for the rest of the systems such that
we can alter: 
1. Ceiling height (defined with \a)
1. Pulley diameter (defined with \radlg and \radrp)
1. rope thickness (you'll need to add a `\width` variable for this, as I showed you on Friday).

Please set baseline values as follows:

```latex
\a{10}
\radlg{1}
\radrp{1.1}
\width{1mm}
```

Let me know if you have any questions. 
