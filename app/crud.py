from sqlalchemy.orm import Session
from app.schemas import MovementCreate, MovementUpdate
from app.models import Movement
from datetime import datetime, timezone

def create_movement(db: Session, movement: MovementCreate, user_id: int):
    """
    Crea un nuevo movimiento en la base de datos.
    
    Args:
        db: Sesión de base de datos
        movement: Datos del movimiento validados por MovementCreate
        user_id: ID del usuario dueño del movimiento
    
    Returns:
        El movimiento creado (modelo SQLAlchemy)
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
    Obtiene un movimiento por su ID.
    
    Args:
        db: Sesión de base de datos
        movement_id: ID del movimiento a buscar
    
    Returns:
        El movimiento si existe, None si no se encuentra
    """

    return db.query(Movement).filter(Movement.id == movement_id).first()

def get_movements(db: Session, user_id: int, skip: int=0, limit: int=100):
    """
    Obtiene todos los movimientos de un usuario con paginación.
    
    Args:
        db: Sesión de base de datos
        user_id: ID del usuario dueño de los movimientos
        skip: Número de registros a saltar (para paginación)
        limit: Máximo número de registros a devolver
    
    Returns:
        Lista de movimientos del usuario
    """

    return (
        db.query(Movement)
        .filter(Movement.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def update_movement(db: Session, movement_id: int, movement: MovementUpdate):
    """
    Actualiza un movimiento existente.
    
    Args:
        db: Sesión de base de datos
        movement_id: ID del movimiento a actualizar
        movement: Datos actualizados validados por MovementUpdate
    
    Returns:
        El movimiento actualizado si existe, None si no se encuentra
    """

    db_movement = get_movement(db, movement_id)

    if db_movement:
        update_data = movement.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_movement, key, value)
        
        db.commit()
        db.refresh(db_movement)

    return db_movement

def delete_movement(db: Session, movement_id: int):
    """
    Elimina un movimiento de la base de datos.
    
    Args:
        db: Sesión de base de datos
        movement_id: ID del movimiento a eliminar
    
    Returns:
        True si se eliminó, False si no existía
    """

    db_movement = get_movement(db, movement_id)

    if db_movement:
        db.delete(db_movement)
        db.commit()
        return True
    
    return False

