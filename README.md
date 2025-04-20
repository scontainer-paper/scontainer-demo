# SContainer: A Document Data Model for GUI-Based Schema Building in the Sharing of Generic Scientific Research Data

## Requirements

1. Clone the repository.
2. Create and activate a Python 3.10+ environment.
3. Navigate to the directory of the cloned repository and run:

   ```bash
   pip install -r requirements.txt
   ```

## Experiment

- The `experiments` folder contains the JSON datasets along with the three schemas.
- To run the experiment, execute `python run_test.py`.

### C++ Experiment

- The C++ code is located in the `experiments/cpp` folder.
- This is a CMake project. You can either build it using CMake or run it directly in CLion.
- Please update the dataset path in `main.cpp` (line 13) to point to the location of your local datasets.

## Data Model

- The data model is implemented in the `datamodel` folder.
- In the `datamodels/examples` folder, you will find 9 examples demonstrating the core concepts of the data model. Run these examples individually to view the results in the console.
(Make sure to run them after navigating into the `examples` folder, otherwise you'll get a 'No module named datamodel' error.)

## Prototype GUI

- *TODO*