from core.data_structures import ReasoningTreeNode, ReasoningTree, Fact, FactType

def create_template() -> ReasoningTree:
    """Creates the symbolic reasoning tree structure for a medical expenses case."""
    root = ReasoningTreeNode(
        description="Calculate taxable income for a taxpayer with high medical expenses.",
        children=[
            ReasoningTreeNode(
                description="Income",
                facts=[Fact("Gross Annual Income", 0, FactType.QUANTITATIVE, is_income=True)]
            ),
            ReasoningTreeNode(
                description="Extraordinary Burdens",
                facts=[
                    Fact("Total Medical Expenses Incurred", 0, FactType.QUANTITATIVE)
                ]
            )
        ]
    )
    return ReasoningTree(root=root)