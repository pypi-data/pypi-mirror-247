# Unifying and Aligning Multifacted AI Explanations


## Code Structure

- `/src`: Contains the TypeScript code used to generate the visualizations.
- `/pyWidget` contains the python code that create ML models, generate explanations, and call the visualization code.


## Depedencies

- run `npm install` to install the dependencies for typescript

- `conda env create -f environment.yaml`  to install the dependencies for python

## How to Run

### Dev Mode

1. Execute `npm run widgetDev`. The compiled TypeScript code will be stored in the `/bundle` directory. The hot module replacement will re-bundle the outputs when there is a change in `src`.
2. Activate the conda environment using `conda activate mixai`.
3. Launch the notebook `pyWidget/explanation.ipynb`. The Python code within will invoke the bundled TypeScript code to produce visualizations.


### Product Mode
[place holder]
