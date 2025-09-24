from core.data_structures import ReasoningTreeNode, ReasoningTree, Fact, FactType

def create_template() -> ReasoningTree:
    """Creates the symbolic reasoning tree structure for a complex freelancer case."""
    root = ReasoningTreeNode(
        description="Calculate comprehensive taxable income for a German freelancer.",
        children=[
            ReasoningTreeNode(
                description="Income",
                facts=[Fact("Gross Annual Revenue", 0, FactType.QUANTITATIVE, is_income=True)]
            ),
            ReasoningTreeNode(
                description="Business Expenses (Werbungskosten)",
                children=[
                    ReasoningTreeNode(
                        description="Home Office Deduction",
                        facts=[
                            Fact("Home Office Deduction Claimed", 0, FactType.QUANTITATIVE, is_deduction=True),
                            Fact("Narrative: Justification for Home Office", "", FactType.NARRATIVE),
                        ]
                    ),
                    ReasoningTreeNode(
                        description="Work Equipment (Arbeitsmittel)",
                        facts=[
                            Fact("Work Equipment Cost", 0, FactType.QUANTITATIVE, is_deduction=True),
                            Fact("Narrative: Reason for Equipment Purchase", "", FactType.NARRATIVE),
                        ]
                    )
                ]
            ),
            ReasoningTreeNode(
                description="Special Expenses (Sonderausgaben)",
                children=[
                    ReasoningTreeNode(
                        description="Health Insurance",
                        facts=[Fact("Private Health Insurance Annual Premium", 0, FactType.QUANTITATIVE, is_deduction=True)]
                    ),
                    ReasoningTreeNode(
                        description="Charitable Donations",
                        facts=[Fact("Donation to Registered Charity", 0, FactType.QUANTITATIVE, is_deduction=True)]
                    )
                ]
            )
        ]
    )
    return ReasoningTree(root=root)