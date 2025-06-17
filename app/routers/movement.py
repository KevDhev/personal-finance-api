from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import crud
from app.schemas import MovementCreate, MovementOut, MovementUpdate
from app.database import get_db

router = APIRouter(
    prefix="/movements",
    tags=["movements"]
)

@router.post("/", response_model=MovementOut, status_code=status.HTTP_201_CREATED)
def create_movement(movement: MovementCreate, db: Session=Depends(get_db)):
    """
    Crea un nuevo movimiento financiero.
    
    - **amount**: Monto del movimiento (debe ser positivo)
    - **type**: Tipo de movimiento (ingreso/gasto)
    - **description**: Descripción opcional
    - **date**: Fecha opcional (default: ahora)
    - **user_id**: ID del usuario asociado (requerido)
    """

    try:
        return crud.create_movement(db=db, movement=movement, user_id=movement.user_id)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )
    
@router.get("/", response_model=List[MovementOut])
def read_movements( user_id: int=0, skip: int=0, limit: int=100, db: Session=Depends(get_db)):
    """
    Obtiene una lista de movimientos financieros con paginación.
    
    - **skip**: Número de registros a saltar (default: 0)
    - **limit**: Máximo número de registros a devolver (default: 100)
    """

    movements = crud.get_movements(db=db, user_id=user_id, skip=skip, limit=limit)

    return movements

@router.get("/{movement_id}", response_model=MovementOut)
def read_movement(movement_id: int, db: Session=Depends(get_db)):
    """
    Obtiene un movimiento financiero específico por su ID.
    
    - **movement_id**: ID del movimiento a recuperar
    """

    db_movement = crud.get_movement(db, movement_id=movement_id)

    if db_movement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movement not found"
        )
    
    return db_movement

@router.put("/{movement_id}", response_model=MovementOut)
def update_movement(movement_id: int, movement: MovementUpdate, db: Session=Depends(get_db)):
    """
    Actualiza un movimiento financiero existente.
    
    - **movement_id**: ID del movimiento a actualizar
    - **amount**: Nuevo monto (opcional)
    - **type**: Nuevo tipo (opcional)
    - **description**: Nueva descripción (opcional)
    """
    
    db_movement = crud.update_movement(db, movement_id=movement_id, movement=movement)

    if db_movement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movement not found"
        )
    
    return db_movement

@router.delete("/{movement_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movement(movement_id: int, db: Session=Depends(get_db)):
    """
    Elimina un movimiento financiero.
    
    - **movement_id**: ID del movimiento a eliminar
    """

    if not crud.delete_movement(db, movement_id=movement_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movement not found"
        )
    
    return None