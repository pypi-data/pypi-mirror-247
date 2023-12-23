# DCS Interactive

Interactive Simulations and Visualizations for the Lecture in [Digital
Communication Systems](https://github.com/pl33/dcs-lecture-notes) at
the Otto-von-Guericke-University Magdeburg.

## Installation

Prerequisites:

- Python 3.10+ must be installed on the system

For Windows systems, ensure that Python is available in the PATH variable.

For installation, execute in a terminal (the example shows a Bash terminal
on Linux):

```shell
# 1. Create a virtual environment
python -m venv dcs_venv
# 2. Activate the virtual environment
source ./dcs_venv/bin/activate
# 3. Installation
pip install dcs-interactive
# 4. Deactivate the virtual environment
deactivate
```

## Run the Application

```shell
# 1. Activate the virtual environment
source ./dcs_venv/bin/activate
# 2. Run it
dcs-interactive
# 3. Deactivate the virtual environment
deactivate
```

## Troubleshooting

### Application does not start

Perhaps, an incorrect value has been set in an input field. Unfortunately,
the application does not validate the values before saving, but before
loading it from the permanent storage. This leads to an error. This bug
is going to be fixed in future versions.

**Solution:** Edit the permanent configuration storage or delete it. The
storage can be found:

- on Linux systems: `$HOME/.config/dcs_interactive/config.toml`
- on Windows: `C:\Users\<username>\AppData\Roaming\Philipp Le\dcs_interactive\config.toml`

## Screenshot

![Chapter 05 - Modulation](./docs/screenshot.png)

## Contents

The currently available simulations and visualizations are listed belows.
The chapters correspond to the Lecture Notes of the Course [Digital
Communication Systems](https://github.com/pl33/dcs-lecture-notes).

- Chapter 2 - Time-Continuous Signals and Systems
    - Phasor
    - Fourier Series
- Chapter 3 - Stochastic and Deterministic Processes
    - Ergodic Process
    - Cross Correlation
    - Power Spectral Distribution
- Chapter 4 - Sampling and Time-Discrete Signals and Systems
    - Sampling
    - Windowing
    - Quantization Noise
- Chapter 5 - Modulation and Mixing
    - Modulation
    - IQ Mixing
    - QAM Modulation
- Chapter 6 - Digital Signal Processing
    - Digital Filter
    - Digital Mixer
    - Down Sampling
    - Up Sampling
- Chapter 7 - Spread Spectrum and Multiple Access
    - Spreading
