from sqlalchemy.orm import Session
from sqlalchemy import func
from app.schemas import MovementCreate, MovementUpdate
from app.models import Movement
from app.models.user import User
from typing import Optional, Dict
from datetime import datetime, timezone, date

def create_movement(db: Session, movement: MovementCreate, user_id: int):
    """
    Creates a new movement in the database.
    
    Args:
        db: Database session
        movement: Movement data validated by MovementCreate
        user_id: ID of the user who owns the movement
    
    Returns:
        The created movement (SQLAlchemy model)
    """

    db_movement = Movement(
        amount = movement.amount,
        type = movement.type,
        description = movement.description,
        user_id = user_id,
        date = movement.date if movement.date else datetime.now(timezone.utc)
    )

    db.add(db_movement)
    db.commit()
    db.refresh(db_movement)

    return db_movement

def get_movement(db: Session, movement_id: int):
    """
    Retrieves a movement by its ID.
    
    Args:
        db: Database session
        movement_id: ID of the movement to retrieve
    
    Returns:
        The movement if it exists, None if not found
    """

    return db.query(Movement).filter(Movement.id == movement_id).first()

def get_movements(
    db: Session,
    user_id: int,
    start_date: Optional[date]=None,
    end_date: Optional[date]=None,
    movement_type: Optional[str]=None,
    skip: int=0,
    limit: int=100
):
    """
    Retrieves movements filtered by various criteria.
    
    Args:
        db: Database session
        user_id: ID of the user who owns the movements
        start_date: Start date for filtering (optional)
        end_date: End date for filtering (optional)
        movement_type: Type of movement ('income'/'expense') (optional)
        skip: Number of records to skip (pagination)
        limit: Maximum number of records to return
    
    Returns:
        List of movements matching the filters
    """

    # Create base query filtering by user 
    query = db.query(Movement).filter(Movement.user_id == user_id)

    # Apply additional filters if provided
    if start_date:
        query = query.filter(Movement.date >= start_date)
    if end_date:
        query = query.filter(Movement.date <= end_date)
    if movement_type:
        query = query.filter(Movement.type == movement_type.lower())
    
    # Apply pagination and return results
    return query.offset(skip).limit(limit).all()

def update_movement(
    db: Session,
    movement_id: int,
    movement: MovementUpdate,
    user_id: int
):
    """
    Updates an existing movement.
    
    Args:
        db: Database session
        movement_id: ID of the movement to update
        movement: Updated data validated by MovementUpdate
    
    Returns:
        The updated movement if it exists, None if not found
    """

    db_movement = db.query(Movement).filter(
        Movement.id == movement_id,
        Movement.user_id == user_id
    ).first()

    if db_movement:
        update_data = movement.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_movement, key, value)
        
        db.commit()
        db.refresh(db_movement)

    return db_movement

def delete_movement(db: Session, movement_id: int):
    """
    Deletes a movement from the database.
    
    Args:
        db: Database session
        movement_id: ID of the movement to delete
    
    Returns:
        True if deleted, False if it didn't exist
    """

    db_movement = get_movement(db, movement_id)

    if db_movement:
        db.delete(db_movement)
        db.commit()
        return True
    
    return False

def get_balance_summary(
    db: Session,
    user_id: int,
    start_date: Optional[date]=None,
    end_date: Optional[date]=None,
) -> Dict[str, float]:
    """
    Calculates the financial summary for a user:
    - Total income
    - Total expenses
    - Balance (income - expenses)
    
    Args:
        db: Database session
        user_id: ID of the user
        start_date: Optional start date for filtering
        end_date: Optional end date for filtering
    
    Returns:
        Dictionary with totals and balance
    """

    # Base filter by user 
    base_query = db.query(Movement).filter(Movement.user_id == user_id)

    # Apply date filters if present 
    if start_date:
        base_query = base_query.filter(Movement.date >= start_date)
    if end_date:
        base_query = base_query.filter(Movement.date <= end_date)
    
    # Calculate totals by type 
    total_income = base_query.filter(
        Movement.type == "income"
    ).with_entities(
        func.coalesce(func.sum(Movement.amount), 0.0)
    ).scalar() or 0.0

    total_expense = base_query.filter(
        Movement.type == "expense"
    ).with_entities(
        func.coalesce(func.sum(Movement.amount), 0.0)
    ).scalar() or 0.0

    return {
        "total_income": round(total_income, 2),
        "total_expense": round(total_expense, 2),
        "balance": round(total_income - total_expense, 2)
    }

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """
    Retrieves a user by their username.
    
    Args:
        db: Database session.
        username: Username to search for.
        
    Returns:
        The User object if it exists, None if not found.
    """

    return db.query(User).filter(User.username == username).first()