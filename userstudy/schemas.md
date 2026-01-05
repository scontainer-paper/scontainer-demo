# Part 1: Task Datasets (Schemas)

The following datasets represent the tasks presented to participants. For each task, the "Scenario" part could be provided to the participants for context, followed by the specific "Field Requirements" they need to model.

## Schema 1: Simple Run
**Scenario for Participants:**
"Imagine you are a lab assistant recording the results of a simple experiment. You don't need complex structures yet; you just need a digital form to save the basic metadata of the run—like its name, ID, and location—along with a simple list of the raw numbers you measured."

**Field Requirements:**
1. **experiment** — short text; name of the experiment (e.g., “pH check”).
2. **runId** — short text; identifier for this run.
3. **isCalibrated** — boolean (yes/no); indicates whether the setup was calibrated before the run.
4. **context** — object containing details about the run:
   * **duration** — number; how many minutes the run took.
   * **location** — short text; label for the place (e.g., “Lab A”, “Field site 3”).
5. **values** — list of numbers; measurements collected during this run.

## Schema 2: Device Record
**Scenario for Participants:**
"Now, imagine you are the lab manager responsible for inventory. You need to create a standard record for every device in the lab. This record must track exactly two things: the specific employee currently in charge of the device, and the purchase history of the hardware itself."

**Field Requirements:**
1. **personInCharge** — object; the person responsible for the device:
   * **name** — text; name of the person.
   * **ID** — text; employee ID of the person.
2. **device** — object; information about the hardware:
   * **name** — short text (e.g., “pH meter”).
   * **dateOfPurchase** — object:
     * **date** — text (e.g., "2020-01-01").
     * **weekOfYear** — number.

## Schema 3: Mixed Data Log
**Scenario for Participants:**
"In this experiment, the data is messy. You are monitoring a process where you sometimes record a measurement (a number) and sometimes write a quick note (like 'started heater' or 'error'). You need a 'Log' list that allows you to mix these two types of entries together in the same sequence."

**Field Requirements:**
1. **study** — short text; name of the study (e.g., “buffer test”).
2. **runId** — short text; code for this run (e.g., “R-11”).
3. **unit** — short text; unit for numeric measurements (e.g., “mV”, “AU”).
4. **log** — list of items; **each item is either a number or text**:
   * **number** — a measurement value.
   * **text** — a quick marker or note (e.g., “start”, “flush”, “spike added”).

## Schema 4: Time-Series Run
**Scenario for Participants:**
"For this study, a simple list of numbers isn't enough because the timing matters. You need to record a series of measurements where every single value is strictly paired with the exact time (in seconds) it was recorded. You cannot have a value without a timestamp."

**Field Requirements:**
1. **study** — short text; name of the study (e.g., “buffer test”).
2. **runId** — short text; code for this run (e.g., “R-12”).
3. **unit** — short text; unit for the readings (e.g., “mV”, “AU”).
4. **measurements** — list of reading objects. Each reading contains:
   * **time** — number (seconds from start).
   * **value** — number (the measured value).

## Schema 5: Result Source Variant
**Scenario for Participants:**
"You are aggregating data from different teams. Some teams use a machine that automatically uploads results, while other teams measure manually and type results in by hand. Your data structure must force the user to choose exactly one of these methods—they cannot fill in both the 'Automatic' fields and the 'Manual' fields for the same result."

**Field Requirements:**
1. **project** — short text; name of the study (e.g., “buffer test”).
2. **trial** — short text; code for this trial/run (e.g., “T-03”).
3. **sampleId** — short text; sample code (e.g., “S-17”).
4. **resultSource** — object; the result collection method (**can only be exactly one of these**):
   * **automatic:**
     * **deviceName** — short text describing the device.
     * **values** — one or more numbers.
   * **manual:**
     * **experimenterName** — short text; name of the experimenter.
     * **values** — one or more numbers.

## Schema 6: Multi-Sample Prep
**Scenario for Participants:**
"This is the most complex task. You are running a batch where you test multiple samples at once. Each sample has its own ID and readings. However, each sample was prepared differently: either by mixing a specific 'Solution' OR by heating it to a specific 'Temperature'. You need to create a list of samples where each sample records its specific preparation method."

**Field Requirements:**
1. **project** — short text; name of the study (e.g., “buffer test”).
2. **run** — short text; code for this run (e.g., “R-09”).
3. **samples** — list of sample records. Each sample contains:
   * **sampleId** — short text; code for the sample (e.g., “S-21”).
   * **readings** — one or more numbers; the measurements for this sample.
   * **unit** — short text; unit for the readings (e.g., “mS/cm”, “AU”).
   * **prep** — object; preparation method (**choose exactly one**):
     * **bySolution:**
       * **solution** — short text (e.g., “NaCl”).
       * **concentration** — number (e.g., grams per liter).
     * **byTemperature:**
       * **temperatureC** — number (degrees Celsius).
       * **durationMin** — number (minutes).

---
# Part 2: Study Methodology & Reproducibility

To ensure the reproducibility of the study and clarify the experimental conditions for the review committee, the following protocol details were documented.

## 1. Participants
The study included **10 participants** with similar educational backgrounds (graduate students majoring in Materials Science). 
Key aspects of participant selection:
* **Screening:** All participants were screened to ensure they were "novices," defined as having **no prior knowledge** of JSON/JSON Schema/XML/XSD/Protobuf.
* **Grouping:** Participants were randomly assigned to one of two groups:
    * **Group 1 (Control):** Used the *JSON Schema Builder* (JS).
    * **Group 2 (Experimental):** Used our *Prototype System* (SC).

## 2. Tools
* **Control Tool (JS):** The *JSON Schema Builder* was selected as the baseline.
    * *Note on Tool Selection:* The tool "Adamant" was considered but excluded because it lacked support for essential features required for the study, specifically the `anyOf` construct (which maps to the "Choice" requirement in the tasks).
* **Experimental Tool (SC):** A prototype system based on our proposed model. 

## 3. Experimental Procedure
The study used a **between-subjects design**. Participants in both groups were tasked with building 6 schemas of incremental complexity (as detailed in Part 1).

### Phase 1: Induction & Learning (Schema 1)
This phase measured how quickly participants could grasp the concepts of schema building using their assigned tool.
* **Group 1 (JS):** Participants received an introduction to basic JSON Schema concepts (focusing on document structure rather than raw syntax with only essential keywords) and instructions on using the JS interface. They were then asked to build **Schema 1**.
* **Group 2 (SC):** Participants received basic instructions on how to use the SC prototype. They were then asked to build **Schema 1**.
* **Correction Policy:** If errors occurred, participants were instructed to correct them.
* **Measurement:** The time taken to successfully build Schema 1 was recorded as **Learning Time**.

Time spent communicating with the experiment leader was excluded from the final timing logs.

### Phase 2: Task Execution (Schemas 2–6)
After completing the training schema, participants built the remaining five schemas based on the descriptive text provided. 
* **Correction Policy:** Participants were required to build schemas without errors. If errors were identified, they were instructed to fix them. Limited hints were provided only when necessary. 
* **Measurement:** The time taken to complete each schema correctly was recorded as **Completion Time**.

Time spent communicating with the experiment leader was excluded from the final timing logs.

## 4. Metrics & Definitions
To assess usability and efficiency, the following metrics were defined:

| Metric Name | Target Scope | Definition |
| :--- | :--- | :--- |
| **Learning Time** | Each Participant | The time taken to learn the basics of schema building, defined as the time required to successfully build **Schema 1** without errors. |
| **Completion Time** | Each Participant (per schema) | The time taken to compose a specific schema (Schemas 2–6) without errors. |

## 5. Summary of Results
* **Learning Time:** The SC group demonstrated significantly faster learning (mean: **1.46 min**) compared to the JS group (mean: **3.46 min**).
* **Completion Time:** The SC group was faster across all subsequent schemas. The performance gap widened as complexity increased (e.g., for Schema 6, JS averaged **4.1 min** vs. SC **2.58 min**).

These results suggest that the streamlined concepts in the SC model reduce the cognitive load for novice users, particularly as task difficulty increases.