# TaxGenius (Generate & Evaluate Edition)

## Overview

TaxGenius is a state-of-the-art Python framework for generating synthetic German tax law case studies. This version provides a complete, end-to-end **generate-and-evaluate pipeline**. After creating a high-quality synthetic case, it immediately uses that case to test the reasoning abilities of an LLM.

The architecture is directly inspired by the source code and methodology of the ICLR 2024 paper **"MuSR: Testing the Limits of Chain-of-thought with Multistep Soft Reasoning"**.

## Key Methodologies Implemented

-   **End-to-End Pipeline**: The main script handles both the complex generation process and the subsequent evaluation, providing immediate feedback on model performance for the generated case.
-   **Structured Evaluation**: The `core/evaluator.py` module systematically tests an LLM against the generated narrative using a Chain-of-Thought style prompt with hints, a method adapted from the paper's `eval.py` script.
-   **Open-Source & Cost-Effective**: Utilizes the **Groq API** with the Llama 3 model for both generation and evaluation, aligning with the recruiter's feedback.
-   **Structured JSON Output**: The primary artifact is a JSON file containing both the underlying "input data" (the symbolic reasoning tree) and the "generated data" (the narrative and ground truth), as requested.
-   **Mad-Libs for Scenario Seeding**: Programmatically creates diverse scenarios by sampling from data pools, a technique used in the MuSR repository.
-   **LLM-based Validation**: During generation, a `TaxModelValidator` ensures each generated fact is logically sound and relevant, a technique adapted from the advanced validators in the MuSR codebase.
-   **Chapter-Based Narrative Generation with Fact Recall**: Creates stories in logical "chapters" and validates that all critical facts are present, rewriting the story if necessary. This addresses the challenge of maintaining factual consistency in long narratives, a core problem tackled by the MuSR generation process.

## How to Implement and Run

### 1. Create the File Structure

Create all the directories and empty files as laid out in the project structure diagram.

### 2. Populate the Files

Copy and paste the code provided for each specific file into your project.

### 3. Set Up a Virtual Environment (Recommended)

Open your terminal in the root `taxgenius` directory and run:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`