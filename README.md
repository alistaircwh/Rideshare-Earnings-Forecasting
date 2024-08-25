[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/Yi0Zbe2y)
# MAST30034 Project 1 README.md
- Name: `ALISTAIR CHEAH WERN HAO`
- Student ID: `1342747`

## Student Instructions
You **must** write up `README.md` for this repository to be eligable for readability marks.

5. All plots must be saved in the `plots` directory.
6. Finally, your report `.tex` files must be inside the `report` directory. If you are using overleaf, you can download the `.zip` and extract it into this folder.
8. Add your relevant `requirements.txt` to the root directory. If you are unsure, run `pip3 list --format=freeze > requirements.txt` (or alternative) and copy the output to the repository.

## README example
This is an example `README.md` for students to use. **Please change this to your requirements**.

**Research Goal:** Predict earnings per hour (assuming driver is always on a trip)

**Timeline:** 2023 May start to 2023 November end

To run the pipeline, please visit the `scripts` directory and run the files in order:
1. `download.py`: This downloads the raw data into the `data/landing` directory.
2. `preprocess.ipynb`: This notebook details all preprocessing steps and outputs it to the `data/raw` and `data/curated` directory.
3. `analysis.ipynb`: This notebook is used to conduct analysis on the curated data.
4. `model.py` and `model_analysis.ipynb`: The script is used to run the model from CLI and the notebook is used for analysing and discussing the model.