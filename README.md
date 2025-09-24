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
