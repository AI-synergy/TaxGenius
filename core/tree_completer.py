from .data_structures import ReasoningTree, Fact, FactType
from .scenario_sampler import ScenarioSampler
from .validators import TaxModelValidator
from utils.llm_api import LLM_API

class TreeCompleter:
    """
    Populates a reasoning tree template with data from a sampled scenario
    and validates generated narrative facts using an LLM-based validator.
    This process is inspired by the "Reasoning Tree Completion" stage of the MuSR paper
    and the use of validators in its codebase.
   
    """
    def __init__(self, llm_api: LLM_API, scenario_sampler: ScenarioSampler):
        self.llm_api = llm_api
        self.sampler = scenario_sampler
        self.validator = TaxModelValidator(llm_api)

    def complete_tree(self, template: ReasoningTree, template_name: str) -> ReasoningTree:
        """Dynamically calls the correct completer based on the template name."""
        if template_name == "combined_freelancer_case":
            return self._complete_freelancer_tree(template)
        elif template_name == "employee_commuter_case":
            return self._complete_commuter_tree(template)
        elif template_name == "extraordinary_burdens_medical":
            return self._complete_medical_tree(template)
        else:
            raise ValueError(f"No completion logic found for template: {template_name}")

    def _complete_freelancer_tree(self, template: ReasoningTree) -> ReasoningTree:
        scenario = self.sampler.sample_freelancer_scenario()
        # --- Populate Quantitative Facts ---
        template.root.children[0].facts[0].value = scenario["income"]
        home_office_node = template.root.children[1].children[0]
        equipment_node = template.root.children[1].children[1]
        home_office_node.facts[0].value = scenario["home_office_cost"]
        equipment_node.facts[0].value = scenario["equipment_cost"]
        insurance_node = template.root.children[2].children[0]
        donation_node = template.root.children[2].children[1]
        insurance_node.facts[0].value = scenario["insurance_premium"]
        donation_node.facts[0].value = scenario["donation"]
        # --- Populate Narrative Facts with Validation ---
        home_office_node.facts[1].value = self._generate_and_validate_narrative("Justify a home office deduction.", f"The taxpayer, a {scenario['profession']}, bought a {scenario['home_office_item']}.", "Home Office Deduction")
        equipment_node.facts[1].value = self._generate_and_validate_narrative("Justify purchasing new work equipment.", f"The taxpayer purchased a {scenario['equipment_item']}.", "Work Equipment (Arbeitsmittel)")
        template.root.facts.extend([Fact("Taxpayer Name", scenario["name"], FactType.NARRATIVE), Fact("Taxpayer Profession", scenario["profession"], FactType.NARRATIVE), Fact("Narrative Hook", scenario["narrative_hook"], FactType.NARRATIVE)])
        return template

    def _complete_commuter_tree(self, template: ReasoningTree) -> ReasoningTree:
        scenario = self.sampler.sample_commuter_scenario()
        template.root.children[0].facts[0].value = scenario["income"]
        deduction_node = template.root.children[1].children[0]
        deduction_node.facts[1].value = scenario["distance_km"]
        deduction_node.facts[2].value = scenario["work_days"]
        template.root.facts.extend([Fact("Taxpayer Name", scenario["name"], FactType.NARRATIVE), Fact("Taxpayer Profession", scenario["profession"], FactType.NARRATIVE), Fact("Work Location", scenario["work_location"], FactType.NARRATIVE)])
        return template

    def _complete_medical_tree(self, template: ReasoningTree) -> ReasoningTree:
        scenario = self.sampler.sample_medical_scenario()
        template.root.children[0].facts[0].value = scenario["income"]
        burden_node = template.root.children[1]
        burden_node.facts[0].value = scenario["medical_cost"]
        burden_node.facts[0].is_deduction = True # Marked for initial sum, engine adjusts later
        template.root.facts.extend([Fact("Taxpayer Name", scenario["name"], FactType.NARRATIVE), Fact("Medical Condition", scenario["medical_condition"], FactType.NARRATIVE)])
        return template
        
    def _generate_and_validate_narrative(self, purpose: str, context: str, intended_purpose: str, max_retries: int = 3) -> str:
        for i in range(max_retries):
            prompt = f"In one sentence, create a plausible narrative justification for the following situation in a German tax context.\nSituation: {purpose}\nContext: {context}"
            narrative = self.llm_api.generate(prompt)
            print(f"  - Validating narrative for '{intended_purpose}': \"{narrative[:50]}...\"")
            if self.validator.validate(generated_fact=narrative, intended_purpose=intended_purpose):
                print("    > Validation PASSED")
                return narrative
            else:
                print(f"    > Validation FAILED (Attempt {i+1}/{max_retries}). Retrying...")
        print(f"[WARNING] Could not generate a valid narrative for '{intended_purpose}' after {max_retries} attempts.")
        return "Narrative generation failed validation."