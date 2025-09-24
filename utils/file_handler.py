import json
from pathlib import Path
from datetime import datetime
from core.data_structures import ReasoningTree

def save_case_to_json(
    template_name: str,
    reasoning_tree: ReasoningTree,
    story: str,
    taxable_income: float,
    total_deductions: float,
    output_dir: str = "output"
) -> Path | None:
    """
    Saves the complete generated case to a structured JSON file.
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    case_id = f"{template_name}_{timestamp}"
    filename = output_path / f"{case_id}.json"

    output_data = {
        "case_id": case_id,
        "input_data": {
            "description": "The underlying symbolic reasoning tree used for generation.",
            "symbolic_reasoning_tree": reasoning_tree.to_dict()
        },
        "generated_data": {
            "description": "The final natural language narrative and ground truth answer.",
            "narrative": story,
            "question": "Based on the story, what is the taxpayer's total taxable income for 2025 after all deductions and allowances?",
            "ground_truth_answer": {
                "value_eur": round(taxable_income, 2),
                "total_deductions_eur": round(total_deductions, 2),
                "explanation": "This answer is programmatically calculated from the symbolic reasoning tree."
            }
        }
    }

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        print(f"\n[SUCCESS] Case saved successfully to: {filename}")
        return filename
    except Exception as e:
        print(f"\n[ERROR] Failed to save case to JSON: {e}")
        return None