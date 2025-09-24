# TaxGenius

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

TaxGenius is a state-of-the-art Python framework for generating synthetic German tax law case studies. It provides a complete, end-to-end **generate-and-evaluate pipeline**. After creating a high-quality, complex synthetic case, it immediately uses that case to test the reasoning abilities of a Large Language Model (LLM).

The architecture is directly inspired by the source code and methodology of the ICLR 2024 paper **"MuSR: Testing the Limits of Chain-of-thought with Multistep Soft Reasoning"**.

## Key Features

-   **End-to-End Pipeline**: The main script handles both the complex generation process and the subsequent evaluation, providing immediate feedback on model performance for the generated case.
-   **Structured Evaluation**: The `core/evaluator.py` module systematically tests an LLM against the generated narrative using a Chain-of-Thought style prompt with hints, a method adapted from the paper's `eval.py` script.
-   **Open-Source & Cost-Effective**: Utilizes the **Groq API** with the Llama 3 model for both generation and evaluation.
-   **Structured JSON Output**: The primary artifact is a JSON file containing both the underlying "input data" (the symbolic reasoning tree) and the "generated data" (the narrative and ground truth), making evaluation straightforward.
-   **Mad-Libs for Scenario Seeding**: Programmatically creates diverse scenarios by sampling from data pools, a technique used in the MuSR repository.
-   **LLM-based Validation**: During generation, a `TaxModelValidator` ensures each generated fact is logically sound and relevant, a technique adapted from the advanced validators in the MuSR codebase.
-   **Chapter-Based Narrative Generation with Fact Recall**: Creates stories in logical "chapters" and validates that all critical facts are present, rewriting the story if necessary. This addresses the challenge of maintaining factual consistency in long narratives, a core problem tackled by the MuSR generation process.

## Getting Started

Follow these steps to set up and run the project.

### Prerequisites
-   Python 3.8 or higher
-   Git

### 1. Clone the Repository

Clone this project to your local machine:
```bash
git clone <your-repository-url>
cd taxgenius
````

### 2\. Set Up a Virtual Environment

It is highly recommended to use a virtual environment to manage dependencies.

**On macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**

```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3\. Install Dependencies

This project uses a `pyproject.toml` file to manage dependencies. Install the project and all required packages with a single command:

```bash
pip install -e .
```

*(Using `-e` installs the project in "editable" mode, which is good practice for development.)*

### 4\. Configure Your API Key

This is a critical step for the application to run.

1.  Go to the [GroqCloud Console](https://console.groq.com/keys) to get a free API key.
2.  Open the `configs/config.yaml` file.
3.  Paste your key into the `groq_api_key` field.

## How to Run and Use the Project

The application is run from the command line, allowing you to specify which tax scenario you want to generate.

### Generating a Case

To run the full "generate-and-evaluate" pipeline, use the `python main.py` command with the `--template` flag.

**Example 1: Generate the Complex Freelancer Case (Default)**

```bash
python main.py --template combined_freelancer_case
```

**Example 2: Generate an Employee Commuter Allowance Case**

```bash
python main.py --template employee_commuter_case
```

**Example 3: Generate a Medical Expenses Case**

```bash
python main.py --template extraordinary_burdens_medical
```

### Understanding the Output

When you run the script, you will see two main outputs:

1.  **Console Log**: Your terminal will display the step-by-step progress of the generation and evaluation pipeline, finishing with a formatted `EVALUATION RESULTS` block that shows the LLM's reasoning and its final score (CORRECT/INCORRECT).
2.  **JSON File**: A new `.json` file will be created in the `output/` directory. This file is the primary deliverable and contains the complete synthetic case, including the underlying reasoning tree and the final narrative, ready for further analysis.

## Using it Further: How to Add a New Tax Case

The framework is designed to be easily extensible. To add a new tax law scenario (e.g., "Capital Gains"):

1.  **Add Scenario Data**: Create or update a YAML file in `data/scenarios/` with relevant seed data (e.g., `capital_gains.yaml` with types of assets and gains).
2.  **Create a New Template**: Add a new Python file in `templates/` (e.g., `capital_gains_case.py`). This file defines the symbolic reasoning tree structure for the new case.
3.  **Update Core Logic**:
      - In `core/scenario_sampler.py`, add a new method to sample data for your new case.
      - In `core/tree_completer.py`, add an `elif` block to the `complete_tree` method to call a new completion function for your template.
      - In `core/reasoning_engine.py`, add the specific calculation logic for the new tax rule.
4.  **Run It**: You can now generate your new case by calling `main.py` with the new template name:
    ```bash
    python main.py --template capital_gains_case
    ```

<!-- end list -->

```
```
