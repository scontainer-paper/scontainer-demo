# SContainer: A Document Data Model for GUI-Based Schema Building in the Sharing of Generic Scientific Research Data
# PLEASE RE-CLONE THIS REPO IF YOU CLONED IT BEFORE Oct 10, 2025 12:35 PM UTC+8, AS THERE WAS A FIX ON THE "No module named datamodel" ERROR.
## Requirements

1. Clone the repository.
2. Create and activate a Python 3.10+ environment.
3. (If you want to run the experiment) Navigate to the directory of the cloned repository and run:

   ```bash
   pip install -r requirements.txt
   ```

## Data Model

- The data model is implemented in the `datamodel` folder.
- In the `datamodels/examples` folder, you will find 9 examples demonstrating the core concepts of the data model. Run
  these examples or play with them and view the results in the console.
  (Make sure to run them after navigating into the `examples` folder, otherwise you'll get a 'No module named datamodel'
  error.)

## Prototype GUI

- Navigate to the root folder (the folder containing the folder "prototype") and run:
  ```bash
  python -m http.server 5173 --directory prototype
  ```
- Open your browser and navigate to `http://127.0.0.1:5173/`.

## User Study

- The schemas used in the user study are in the Markdown file `userstudy/schemas.md`.
- The raw results of the user study are in `userstudy/results.xlsx`.

## Experiment

- The `experiments` folder contains the JSON datasets along with the three schemas.
- To run the experiment, execute `python run_test.py`.

### C++ Experiment

- The C++ code is located in the `experiments/cpp` folder.
- This is a CMake project. You can either build it using CMake or run it directly in CLion.
- Please update the dataset path in `main.cpp` (line 13) to point to the location of the datasets (your local path).
