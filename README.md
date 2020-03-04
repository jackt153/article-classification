# Kaggle

This is our repo for our kaggle competition code. This is mainly so we can all learn from each other. Its not all about what metric we maxmise but best practices when writing code to help us further our careers.

### Creating a virtual environment (with Conda)
It's typically best practice to use a virtual environment. There are different options for this including:
- [venv](https://docs.python.org/3/library/venv.html#module-venv).
- [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
- [Pipenv](https://pipenv.kennethreitz.org/en/latest/)

Feel free to use the virtual enviroment of your choice. Here's how to set up a Conda environment (assuming that you obtained your Python installation with Anaconda).
- Run `conda create -n [ENVIRONMENT_NAME] python=3.7 pip`,

Where `[ENVIRONMENT_NAME]` is replaced with whatever name you'd like to use for the environment. I've called my environment `kaggle` so the command I used was:
```
conda create -n kaggle python=3.7 pip
```
This command creates an environment with Python 3.7 and also installs `pip`.

### Activating the environment
To use the environment you have to activate it. You can do this by running
```
conda activate [ENVIRONMENT_NAME]
```
Where `[ENVIRONMENT_NAME]` is the name of your environment.

To exit the environment you just need to execute
```
conda deactivate
```

### Installing the required python packages
The required Python packages are contained in the `requirements.txt` and the `dev-requirements.txt` files. However, we also require have common utility modules that the rest of the code in the repository depends on. These are contained in the `common_utils` folder in the root directory. We need to ensure that all scripts in the repo can see this, hence we've created a `setup.py` script that finds this `common_utils` directory and treats it as an internal package.

To ensure that you get all the required packages (including the `common_utils` package) you can run the following commands from the root directory AFTER you've activated your virtural environment (using a virtual environment is highly recommended):
```
pip install -e .
pip install -r dev-requirements.txt
```
