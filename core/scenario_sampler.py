import yaml
import random
from pathlib import Path

class ScenarioSampler:
    """
    Implements the Mad-Libs style scenario generation. This is a core part of making
    each generated story unique, as seen in the MuSR repository's generation scripts.
   
    """
    def __init__(self, data_path: str = "data/scenarios"):
        self.data_path = Path(data_path)
        self.professions = self._load_yaml("professions.yaml")
        self.expense_types = self._load_yaml("expense_types.yaml")
        self.narrative_hooks = self._load_yaml("narrative_hooks.yaml")
        self.commute_details = self._load_yaml("commute_details.yaml")
        self.medical_expenses = self._load_yaml("medical_expenses.yaml")

    def _load_yaml(self, filename: str):
        with open(self.data_path / filename, 'r') as f:
            return yaml.safe_load(f)

    def sample_commuter_scenario(self) -> dict:
        """Samples a scenario for an employee's commute."""
        commute = random.choice(self.commute_details)
        return {
            "name": random.choice(["Jonas", "Lea", "Ben", "Emilia"]),
            "profession": random.choice(self.professions["employee"]),
            "work_location": commute["location"],
            "distance_km": commute["distance_km"],
            "work_days": random.randint(200, 230),
            "income": random.randint(55000, 95000)
        }

    def sample_medical_scenario(self) -> dict:
        """Samples a scenario for extraordinary medical burdens."""
        expense = random.choice(self.medical_expenses)
        return {
            "name": random.choice(["Sabine", "Michael", "Anja", "Stefan"]),
            "profession": random.choice(self.professions["employee"]),
            "medical_condition": expense["condition"],
            "medical_cost": expense["cost"],
            "income": random.randint(40000, 70000)
        }

    def sample_freelancer_scenario(self) -> dict:
        """Samples a unique scenario for a freelancer tax case."""
        profession = random.choice(self.professions["freelancer"])
        narrative_hook = random.choice(self.narrative_hooks)
        income = random.randint(65000, 150000)
        home_office_cost = 1260
        equipment_cost = random.randint(1200, 3500)
        insurance_premium = random.randint(6000, 12000)
        donation = random.randint(100, 1000)
        return {
            "name": random.choice(["Alex", "Jordan", "Sam", "Chris"]),
            "profession": profession,
            "narrative_hook": narrative_hook,
            "income": income,
            "home_office_cost": home_office_cost,
            "home_office_item": random.choice(self.expense_types["home_office"]),
            "equipment_cost": equipment_cost,
            "equipment_item": random.choice(self.expense_types["work_equipment"]),
            "insurance_premium": insurance_premium,
            "donation": donation
        }