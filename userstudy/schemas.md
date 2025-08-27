# Schema 1

## Purpose

Describe one simple scientific run with a few basics and a small set of numeric readings.

## Fields

1. **experiment** — short text name for the experiment (e.g., “pH check”).
2. **runId** — short text identifier for this run
3. **isCalibrated** — yes/no (true/false) indicating whether the setup was calibrated before the run.
4. **context** — other details about the run:
   * **duration** — how many minutes did the run take
   * **location** — short text label for the place (e.g., “Lab A”, “Field site 3”).
5. **values** — one or more numbers representing measurements from this run.


# Schema 2

## Purpose

A simple record of a device

## Fields (all required; no extra fields)

1. **personInCharge** - person in charge of the device
   * **name** - text. name of the person
   * **ID** - text. employee ID of the person.
2. **device** — information about the device:
   * **name** — short text (e.g., “pH meter”).
   * **dateOfPurchase** — date of purchase.
     * **date** - text, (e.g., "2020-01-01")
     * **weekOfYear** - week of the year (number)





# Schema 3

## Purpose

Capture one simple run where the log mixes **numeric measurements and short text markers**.

## Fields

1. **study** — short text name of the study (e.g., “buffer test”).
2. **run** — short text code for this run (e.g., “R-11”).
3. **unit** — short text for numeric measurements (e.g., “mV”, “AU”).
4. **log** — **one or more** items; **each item is either a number or text**:
   * a **number** — a measurement
   * a **text** — a quick marker or note (e.g., “start”, “flush”, “spike added”).
# Schema 4

## Purpose

Describe one simple run where readings are taken over time

## Fields

1. **study** — short text name of the study (e.g., “buffer test”).
2. **run** — short text code for this run (e.g., “R-12”).
3. **unit** — short text unit for the readings (e.g., “mV”, “AU”).
4. **measurements** — **one or more** readings. Each reading has:
   * **time** — number (e.g., seconds from start).
   * **value** — number (the measured value).


# Schema 5

## Purpose

Capture one small study snapshot with basic info and results recorded exclusively in one of the two formats.

## Fields

1. **project** — short text name of the study (e.g., “buffer test”).
2. **trial** — short text code for this trial/run (e.g., “T-03”).the run.
3. **sampleId** — short text sample code (e.g., “S-17”).
4. **resultSource** — result may be manually measured or automatically collected by device (cannot be both):
   * **automatic**:
     * **deviceName** — short text describing the device.
     * **values** — one or more numbers.
   * **manual**:
     * **experimenterName** — name of the experimenter.
     * **values** — one or more numbers.

# Schema 6

## Purpose

Record one run that measures **multiple samples**, where each sample has a small **one or more readings** and a **simple choice** for how the sample was prepared.

1. **project** — short text name of the study (e.g., “buffer test”).
2. **run** — short text code for this run (e.g., “R-09”).
3. **samples** — **one or more** sample records.
   Each **sample** has:

   * **sampleId** — short text code for the sample (e.g., “S-21”).
   * **readings** — **one or more** numbers; the measurements for this sample.
   * **unit** — short text for the readings (e.g., “mS/cm”, “AU”).
   * **prep** — **choose exactly one** of:
     * **bySolution**:
       * **solution** — short text (e.g., “NaCl”).
       * **concentration** — number (e.g., grams per liter).
     * **byTemperature**:
       * **temperatureC** — number (degrees Celsius).
       * **durationMin** — number (minutes).
