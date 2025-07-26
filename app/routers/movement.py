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
    Creates a new financial movement.
    
    - **amount**: Movement amount (must be positive)
    - **type**: Movement type (income/expense)
    - **description**: Optional description
    - **date**: Optional date (default: now)
    - **user_id**: Associated user ID (required)
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
        description="Filter movements from this date (YYYY-MM-DD)" 
    ),
    end_date: Optional[date]=Query(
        None,
        description="Filter movements up to this date (YYYY-MM-DD)"
    ),
    movement_type: Optional[str]=Query(
        None,
        description="Type of movement: 'income' or 'expense'",
        regex="^(income|expense)$"
    ),
    skip: int=0,
    limit: int=100,
    db: Session=Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieves movements with optional filters:
    
    - **start_date**: Start date (inclusive)
    - **end_date**: End date (inclusive)
    - **movement_type**: 'income' or 'expense'
    - **skip**: Pagination (records to skip)
    - **limit**: Maximum number of records (up to 100)
    """

    # Additional date validation 
    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="The start date cannot be greater than the end date"
        )
    
    # Call the CRUD function with the filters
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
    start_date: Optional[date]=Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[date]=Query(None, description="End date (YYYY-MM-DD)"),
    db: Session=Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Financial summary with:
    - Total income
    - Total expenses
    - Balance

    Optional date filters.
    """

    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="The start date cannot be greater than the end date"
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
    Retrieves a specific financial movement by its ID.
    
    - **movement_id**: ID of the movement to retrieve
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
    Updates an existing financial movement.
    
    - **movement_id**: ID of the movement to update
    - **amount**: New amount (optional)
    - **type**: New type (optional)
    - **description**: New description (optional)
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
    Deletes a financial movement.
    
    - **movement_id**: ID of the movement to delete
    """

    db_movement = crud.get_movement(db, movement_id=movement_id)

    if db_movement is None or db_movement.user_id != current_user.id:   # type: ignore
        raise HTTPException(
            status_code=404,
            detail="Movement not found"
        )
    
    crud.delete_movement(db, movement_id=movement_id)

    return None