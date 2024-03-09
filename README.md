# GOLDEN - Gold Labeling and Density Evaluation Network
Golden is an algorithm that identifies, clusters, and evaluates density of immunigold particles in electron microscopy images of the brain.

Golden uses a 'traditional algorithm' (non-machine learning) approach to identify the particles. It uses an approach derived from network theory to find the density of particles.  

## Python Version

Please use Python 3.12 or later with this project. Earlier versions are not guaranteed to work (3.11+ will probably work, but it may break in the future).

## Dataset
Uses the immunogold dataset from Max Planck Florida Institute for Neuroscience. The paper is linked [here](https://www.researchgate.net/publication/350731155_A_deep_learning_approach_to_identifying_immunogold_particles_in_electron_microscopy_images).

## Installation

To install the program, first clone the repository:

```bash
$ git clone https://github.com/AlexanderJCS/golden.git
```

Then, navigate to the directory and install the package:

```bash
$ cd golden
$ pip install -r ./requirements.txt
```

Installation is complete. To use the program, see the [usage section](#usage).

## Usage

View the help info by running the program with the `-h` flag:

```bash
# from the repository's root dir
$ python -m src.main -h
```

This will show the following help info:
```
usage: Golden [-h] [-m] [-v] name

Find gold particles and their density in electron microscopy images

positional arguments:
  name          The name of the dataset to analyze. This is the name of the folder in the 'analyzed synapses' directory,e.g., 'S1' or 'S7'

options:
  -h, --help    show this help message and exit
  -m, --mask    Whether to apply the mask to the image before finding gold particles. Default: False
  -v, --visual  Whether to display the image with the gold particles marked on it. Default: False
```


To run the program, use the following command:

```bash
# from the repository's root dir
$ python -m src.main S1

# S1 is the name of the image bundle to analyze, e.g., "S1", "S4", "S7" etc.
# See a full list by looking at the directory names in the "analyzed synapses" directory
```

You can also add the following flags:

| Flag               | Action                                                                   |
|--------------------|--------------------------------------------------------------------------|
| `-m` or `--mask`   | Whether to apply the image mask found in the image bundle                |
| `-v` or `--visual` | Whether to use matplotlib to show the results visually after calculation |

## Tests

To test the project, first navigate to the test package:

```bash
# from the repository's root dir
$ cd test
```

Then run the tests:
```bash
$ python -m pytest -k "not gold_accuracy_test"
```

We exclude the gold accuracy test since it is a long-runnning test and does not have a pass/fail condition. Instead, it is used to evaluate the accuracy of the gold-finding portion of the program by generating a confusion matrix. We can run it by using:

```bash
$ python -m pytest -k "gold_accuracy_test" -s
```

The `-s` flag is essential since it is used to print the confusion matrix to the console.

## Contributing

Since this project is for a class, **contributions are not open.**