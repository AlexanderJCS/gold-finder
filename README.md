# GOLDEN - Gold Labeling and Density Evaluation Network
Golden is an algorithm that identifies, clusters, and evaluates density of immunigold particles in electron microscopy images of the brain.

Golden uses a 'traditional algorithm' (non-machine learning) approach to identify the particles. It uses an approach derived from network theory to find the density of particles.  

## Python Version

Please use Python 3.12 or later with this project. Earlier versions are not guaranteed to work.

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

Run `main.py` by executing:

```bash
python -m src.main
```

## Tests

To test the project, first navigate to the test package:

```bash
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