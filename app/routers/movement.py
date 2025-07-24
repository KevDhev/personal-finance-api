from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app import crud
from datetime import date
from app.schemas import MovementCreate, MovementOut, MovementUpdate, BalanceSummary
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.database import get_db

router = APIRouter(
    prefix="/movements",
    tags=["movements"]
)

@router.post("/", response_model=MovementOut, status_code=201)
def create_movement(
    movement: MovementCreate,
    db: Session=Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Crea un nuevo movimiento financiero.
    
    - **amount**: Monto del movimiento (debe ser positivo)
    - **type**: Tipo de movimiento (ingreso/gasto)
    - **description**: Descripción opcional
    - **date**: Fecha opcional (default: ahora)
    - **user_id**: ID del usuario asociado (requerido)
    """

    try:
        return crud.create_movement(
            db=db,
            movement=movement,
            user_id=current_user.id # type: ignore
        )
    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
    
@router.get("/", response_model=List[MovementOut])
def read_movements(
    start_date: Optional[date]=Query(
        None,
        description="Filtrar movimientos desde esta fecha (YYYY-MM-DD)"
    ),
    end_date: Optional[date]=Query(
        None,
        description="Filtrar movimientos hasta esta fecha (YYYY-MM-DD)"
    ),
    movement_type: Optional[str]=Query(
        None,
        description="Tipo de movimiento: 'ingreso' o 'gasto'",
        regex="^(income|expense)$"
    ),
    skip: int=0,
    limit: int=100,
    db: Session=Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtiene movimientos con filtros opcionales:
    
    - **start_date**: Fecha inicial (inclusive)
    - **end_date**: Fecha final (inclusive)
    - **movement_type**: 'ingreso' o 'gasto'
    - **skip**: Paginación (registros a saltar)
    - **limit**: Máximo de registros (hasta 100)
    """

    # Validación adicional de fechas
    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="La fecha de inicio no puede ser mayor a la fecha final"
        )
    
    # Llamar a la función CRUD con los filtros
    return crud.get_movements(
        db=db,
        user_id=current_user.id,    #type: ignore
        start_date=start_date,
        end_date=end_date,
        movement_type=movement_type,
        skip=skip,
        limit=limit
    )

@router.get("/summary", response_model=BalanceSummary)
def get_financial_summary(
    start_date: Optional[date]=Query(None, description="Fecha inicial (YYYY-MM-DD)"),
    end_date: Optional[date]=Query(None, description="Fecha final (YYYY-MM-DD)"),
    db: Session=Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Resumen financiero con:
    - Total ingresos
    - Total gastos
    - Balance
    
    Filtros opcionales por fecha.
    """

    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="La fecha inicial no puede ser mayor a la final"
        )
    
    return crud.get_balance_summary(
        db=db,
        user_id=current_user.id, # type: ignore
        start_date=start_date,
        end_date=end_date
    )

@router.get("/{movement_id}", response_model=MovementOut)
def read_movement(
    movement_id: int,
    db: Session=Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtiene un movimiento financiero específico por su ID.
    
    - **movement_id**: ID del movimiento a recuperar
    """

    db_movement = crud.get_movement(db, movement_id=movement_id)

    if db_movement is None or db_movement.user_id != current_user.id:   #type: ignore
        raise HTTPException(
            status_code=404,
            detail="Movement not found"
        )
    
    return db_movement

@router.put("/{movement_id}", response_model=MovementOut)
def update_movement(
    movement_id: int,
    movement: MovementUpdate,
    db: Session=Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Actualiza un movimiento financiero existente.
    
    - **movement_id**: ID del movimiento a actualizar
    - **amount**: Nuevo monto (opcional)
    - **type**: Nuevo tipo (opcional)
    - **description**: Nueva descripción (opcional)
    """
    
    db_movement = crud.get_movement(db, movement_id=movement_id)

    if db_movement is None or db_movement.user_id != current_user.id:   # type: ignore
        raise HTTPException(
            status_code=404,
            detail="Movement not found"
        )
    
    return crud.update_movement(
        db=db,
        movement_id=movement_id,
        movement=movement,
        user_id=current_user.id # type: ignore
    )

@router.delete("/{movement_id}", status_code=204)
def delete_movement(
    movement_id: int,
    db: Session=Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Elimina un movimiento financiero.
    
    - **movement_id**: ID del movimiento a eliminar
    """

    db_movement = crud.get_movement(db, movement_id=movement_id)

    if db_movement is None or db_movement.user_id != current_user.id:   # type: ignore
        raise HTTPException(
            status_code=404,
            detail="Movement not found"
        )
    
    crud.delete_movement(db, movement_id=movement_id)

    return None