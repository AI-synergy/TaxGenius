import argparse
import importlib
from pathlib import Path
from core.scenario_sampler import ScenarioSampler
from core.tree_completer import TreeCompleter
from core.story_generator import StoryGenerator
from core.reasoning_engine import ReasoningEngine
from core.evaluator import Evaluator
from utils.llm_api import LLM_API
from utils.file_handler import save_case_to_json

def main(template_name: str, output_dir: str):
    """
    Main execution pipeline for the TaxGenius framework.
    Generates a synthetic case, saves it to JSON, and immediately evaluates it.
    """
    print(f"\n[[ TaxGenius: Initializing Generation & Evaluation for template: {template_name} ]]")
    print("-" * 70)

    try:
        # --- Initialization ---
        llm_api = LLM_API()
        evaluator = Evaluator(llm_to_test=llm_api)
        scenario_sampler = ScenarioSampler()
        tree_completer = TreeCompleter(llm_api, scenario_sampler)
        story_generator = StoryGenerator(llm_api)
        reasoning_engine = ReasoningEngine()

        # --- Generation Pipeline ---
        print("[Step 1/6] Loading symbolic tree structure...")
        template_module = importlib.import_module(f"templates.{template_name}")
        template = template_module.create_template()
        print("...Template loaded successfully.")

        print(f"\n[Step 2/6] Sampling scenario and populating tree for '{template_name}'...")
        reasoning_tree = tree_completer.complete_tree(template, template_name)
        print("...Tree populated.")
        
        print("\n[Step 3-4/6] Generating narrative with chaptering and fact-recall validation...")
        final_story = story_generator.generate_story_with_validation(reasoning_tree)
        print("\n...Narrative generation complete.")

        print("\n[Step 5/6] Calculating ground truth from the symbolic tree...")
        taxable_income, total_deductions = reasoning_engine.calculate(reasoning_tree.root)
        print(f"...Ground Truth Calculated: Taxable Income = €{taxable_income:,.2f}")

        # --- Save Output to JSON ---
        json_filepath = save_case_to_json(
            template_name=template_name,
            reasoning_tree=reasoning_tree,
            story=final_story,
            taxable_income=taxable_income,
            total_deductions=total_deductions,
            output_dir=output_dir
        )
        if not json_filepath:
            return

        # --- Step 6: Evaluation ---
        print("\n[Step 6/6] Performing evaluation on the generated case...")
        evaluation_result = evaluator.evaluate_case_from_file(json_filepath)

    except (ImportError, FileNotFoundError):
        print(f"\n[ERROR] Template '{template_name}' not found or its module is invalid.")
        print("Please check the 'templates' directory and the name you provided.")
        return
    except Exception as e:
        print(f"\n[An unexpected error occurred]: {e}")
        return

    # --- Print Evaluation Results ---
    print("\n" + "=" * 70)
    print("EVALUATION RESULTS")
    print("=" * 70)
    print(f"Model's Reasoning:\n---\n{evaluation_result['model_reasoning']}\n---")
    print(f"\nGround Truth Answer: €{evaluation_result['ground_truth_answer_eur']:,.2f}")
    parsed_answer = evaluation_result['parsed_answer_eur']
    print(f"Model's Parsed Answer: €{parsed_answer:,.2f}" if parsed_answer is not None else "Model's Parsed Answer: [Could not parse answer]")
    print(f"\nResult: {'CORRECT' if evaluation_result['is_correct'] else 'INCORRECT'}")
    print("=" * 70)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="TaxGenius: A Comprehensive Synthetic German Tax Case Generator & Evaluator.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--template",
        type=str,
        default='combined_freelancer_case',
        help="The name of the template file to use from the 'templates' directory.\n"
             "Available options:\n"
             "- combined_freelancer_case (default)\n"
             "- employee_commuter_case\n"
             "- extraordinary_burdens_medical"
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default='output',
        help="The directory where the final JSON case file will be saved.\n(default: output/)"
    )
    args = parser.parse_args()
    main(args.template, args.output_dir)