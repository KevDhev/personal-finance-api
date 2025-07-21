from pydantic import BaseModel, Field

class BalanceSummary(BaseModel):
    """
    Esquema para la respuesta del resumen financiero.
    Contiene los totales de ingresos, gastos y el balance resultante.
    """

    total_income: float=Field(
        ...,
        description="Suma total de todos los movimientos de ingreso",
        examples=[1500.50],
        ge=0
    )

    total_expense: float=Field(
        ...,
        description="Suma total de todos los movimientos de gasto",
        examples=[750.25],
        ge=0
    )

    balance: float=Field(
        ...,
        description="Diferencia entre ingresos y gastos (income - expense)",
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