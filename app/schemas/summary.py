from pydantic import BaseModel, Field

class BalanceSummary(BaseModel):
    """
    Schema for the financial summary response.
    Contains total income, expenses, and the resulting balance.
    """

    total_income: float=Field(
        ...,
        description="Total sum of all income movements" ,
        examples=[1500.50],
        ge=0
    )

    total_expense: float=Field(
        ...,
        description="Total sum of all expense movements",
        examples=[750.25],
        ge=0
    )

    balance: float=Field(
        ...,
        description="Difference between income and expenses (income - expense)",
        examples=[750.25]
    )

    class Config():
        json_schema_extra = {
            "example": {
                "total_income": 1500.50,
                "total_expense": 750.25,
                "balance": 750.25
            }
        }