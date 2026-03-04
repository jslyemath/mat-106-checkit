# CheckIt Bank for Number Systems and Operations

## Purpose

This repo is for MAT 106 - Number Systems and Operations at SUNY Oswego. It uses both the CheckIt system for online practice and a personal python-based script for local LaTeX generation.

## Warning

The file structure of this project is different from your typical CheckIt bank, due to the need to create more customized LaTeX files locally. If you have interest in using CheckIt directly for local printing, I would suggest moving the generation logic out of the pygenerator.py files and back into the generator.sage files.

## To-Dos

TODO: Edit G1 JSON to get the first 20 problems aligned properly.

## Setup for Collaborators (Local Setup)

To generate the PDFs on your own computer, you will need to set up a small, isolated Python environment so all the background tools run correctly. 

**Before you start:**
Because this script generates PDFs, your computer **must** have LaTeX installed. Python cannot do this by itself! If you don't have it, please install [TeX Live](https://tug.org/texlive/) (Windows/Linux) or [MacTeX](https://tug.org/mactex/) (Mac) before continuing.

### Step 1: Open the Terminal
Open this project folder in VS Code. At the top of the screen, click **Terminal** -> **New Terminal**. A small command-line window will pop up at the bottom of your screen. 

*(Note: You will type all the following commands directly into this terminal window and press **Enter** after each one.)*

### Step 2: Create a Virtual Environment
We need to create a hidden folder (called a `venv`) to hold our specific Python packages. Type this into the terminal and press Enter:
`python -m venv venv`

*(Wait a few seconds. When your terminal cursor blinks again, it is done. You won't see a success message.)*

### Step 3: Activate the Virtual Environment
Now we have to turn the environment "on". The command is different depending on your operating system. Type the correct one for your computer into the terminal and press Enter:

* **For Windows:**
  `venv\Scripts\activate`
* **For Mac / Linux:**
  `source venv/bin/activate`

*(You should now see `(venv)` pop up at the very beginning of your terminal prompt line.)*

### Step 4: Install the Required Packages
With the venv activated, install the exact tools this script needs. Type this into the terminal and press Enter:
`pip install -r requirements.txt`

### Step 5: Run the Generator
You are fully set up! To generate the PDFs, just type this into the terminal and press Enter:
`python pdfgenerator.py`

## About CheckIt

Learn more at <https://github.com/StevenClontz/checkit>
and <https://github.com/StevenClontz/checkit/wiki>.
