import yaml
from .data_structures import ReasoningTreeNode

class ReasoningEngine:
    """Performs tax calculations based on a populated reasoning tree."""
    def __init__(self, config_path="configs/tax_rules_2025.yaml"):
        with open(config_path, 'r') as f:
            self.rules = yaml.safe_load(f)

    def calculate(self, root_node: ReasoningTreeNode) -> (float, float):
        """Calculates total taxable income and total deductions."""
        total_income, total_deductions = self._calculate_recursive(root_node)
        
        # Handle special cases like extraordinary burdens which depend on total income
        if "Extraordinary Burdens" in [child.description for child in root_node.children]:
            reasonable_burden = total_income * self.rules['reasonable_burden_percentage_low_income']
            medical_expenses_node = next(c for c in root_node.children if c.description == "Extraordinary Burdens")
            actual_medical_expenses = medical_expenses_node.facts[0].value
            deductible_medical_expenses = max(0, actual_medical_expenses - reasonable_burden)
            # Adjust total deductions to reflect only the deductible portion
            total_deductions = (total_deductions - actual_medical_expenses) + deductible_medical_expenses
            
        taxable_income = total_income - total_deductions
        taxable_income_after_allowance = max(0, taxable_income - self.rules['grundfreibetrag'])
        return taxable_income_after_allowance, total_deductions

    def _calculate_recursive(self, node: ReasoningTreeNode) -> (float, float):
        """Helper to recursively sum income and deductions, applying rules."""
        income = 0
        deductions = 0

        # Handle special calculation logic at the node level before summing
        if node.description == "Commuter Allowance Deduction":
            distance = next(f.value for f in node.facts if "Distance" in f.description)
            days = next(f.value for f in node.facts if "Work Days" in f.description)
            rate = self.rules['commuter_allowance_per_km']
            # Simplified: does not account for >20km rate change
            node.facts[0].value = distance * days * rate
        
        for fact in node.facts:
            if fact.is_income:
                income += fact.value
            elif fact.is_deduction:
                deductions += fact.value
        
        for child in node.children:
            child_income, child_deductions = self._calculate_recursive(child)
            income += child_income
            deductions += child_deductions
            
        return income, deductions