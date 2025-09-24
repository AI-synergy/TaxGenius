from core.data_structures import ReasoningTreeNode, ReasoningTree, Fact, FactType

def create_template() -> ReasoningTree:
    """Creates the symbolic reasoning tree structure for an employee commuter allowance case."""
    root = ReasoningTreeNode(
        description="Calculate taxable income for a German employee with a commute.",
        children=[
            ReasoningTreeNode(
                description="Income",
                facts=[Fact("Gross Annual Salary", 0, FactType.QUANTITATIVE, is_income=True)]
            ),
            ReasoningTreeNode(
                description="Income-Related Expenses (Werbungskosten)",
                children=[
                    ReasoningTreeNode(
                        description="Commuter Allowance Deduction",
                        facts=[
                            Fact("Total Commute Deduction", 0, FactType.QUANTITATIVE, is_deduction=True),
                            Fact("One-Way Commute Distance (km)", 0, FactType.QUANTITATIVE),
                            Fact("Number of Work Days", 0, FactType.QUANTITATIVE)
                        ]
                    ),
                ]
            )
        ]
    )
    return ReasoningTree(root=root)