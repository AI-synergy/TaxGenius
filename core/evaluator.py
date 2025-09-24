import json
import re
from pathlib import Path
from utils.llm_api import LLM_API

class Evaluator:
    """
    Evaluates an LLM's reasoning ability on a generated synthetic tax case.
    The methodology is inspired by the evaluation process in the MuSR repository's eval.py script.
   
    """
    def __init__(self, llm_to_test: LLM_API):
        """
        Initializes the Evaluator with the specific LLM instance to be tested.
        """
        self.llm_to_test = llm_to_test
        with open("prompts/evaluation_prompt.txt", 'r', encoding='utf-8') as f:
            self.eval_prompt_template = f.read()

    def evaluate_case_from_file(self, json_path: Path) -> dict:
        """
        Loads a generated case from a JSON file and evaluates it.
        """
        # 1. Load the dataset case from the JSON file
        with open(json_path, 'r', encoding='utf-8') as f:
            case_data = json.load(f)

        narrative = case_data["generated_data"]["narrative"]
        question = case_data["generated_data"]["question"]
        ground_truth_answer = case_data["generated_data"]["ground_truth_answer"]["value_eur"]

        # 2. Construct the prompt with instructions/hint, similar to CoT+
        prompt = self.eval_prompt_template.format(narrative=narrative, question=question)

        # 3. Run inference to get the model's reasoning and answer
        print("...[Evaluator] Sending case to the LLM for evaluation...")
        model_output = self.llm_to_test.generate(prompt, system_prompt="You are a precise and logical German tax assistant.")
        print("...[Evaluator] Received model's reasoning.")

        # 4. Parse the final answer from the model's output
        parsed_answer = self._parse_final_answer(model_output)

        # 5. Compare the model's answer to the ground truth and score it
        is_correct = False
        if parsed_answer is not None:
            # Using a tolerance for floating point comparison
            is_correct = abs(parsed_answer - ground_truth_answer) < 0.01

        return {
            "model_reasoning": model_output,
            "parsed_answer_eur": parsed_answer,
            "ground_truth_answer_eur": ground_truth_answer,
            "is_correct": is_correct
        }

    def _parse_final_answer(self, model_output: str) -> float | None:
        """
        Extracts the final numerical answer from the model's text output.
        Looks for the pattern "ANSWER: €[amount]".
        """
        match = re.search(r"ANSWER:\s*€?([\d,]+\.?\d*)", model_output, re.IGNORECASE)
        
        if match:
            try:
                answer_str = match.group(1).replace(',', '')
                return float(answer_str)
            except (ValueError, IndexError):
                return None
        return None