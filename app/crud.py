from sqlalchemy.orm import Session
from sqlalchemy import func
from app.schemas import MovementCreate, MovementUpdate
from app.models import Movement
from app.models.user import User
from typing import Optional, Dict
from datetime import datetime, timezone, date

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
    Obtiene movimientos filtrados por varios criterios.
    
    Args:
        db: Sesión de base de datos
        user_id: ID del usuario dueño de los movimientos
        start_date: Fecha inicial para filtrar (opcional)
        end_date: Fecha final para filtrar (opcional)
        movement_type: Tipo de movimiento ('ingreso'/'gasto') (opcional)
        skip: Número de registros a saltar (paginación)
        limit: Máximo número de registros a devolver
    
    Returns:
        Lista de movimientos que cumplen con los filtros
    """

    # Crear consulta base filtrando por usuario
    query = db.query(Movement).filter(Movement.user_id == user_id)

    # Aplicar filtros adicionales si se proporcionan
    if start_date:
        query = query.filter(Movement.date >= start_date)
    if end_date:
        query = query.filter(Movement.date <= end_date)
    if movement_type:
        query = query.filter(Movement.type == movement_type)
    
    # Aplicar paginación y devolver resultados
    return query.offset(skip).limit(limit).all()

def update_movement(
    db: Session,
    movement_id: int,
    movement: MovementUpdate,
    user_id: int
):
    """
    Actualiza un movimiento existente.
    
    Args:
        db: Sesión de base de datos
        movement_id: ID del movimiento a actualizar
        movement: Datos actualizados validados por MovementUpdate
    
    Returns:
        El movimiento actualizado si existe, None si no se encuentra
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

def get_balance_summary(
    db: Session,
    user_id: int,
    start_date: Optional[date]=None,
    end_date: Optional[date]=None,
) -> Dict[str, float]:
    """
    Calcula el resumen financiero para un usuario:
    - Total ingresos
    - Total gastos
    - Balance (ingresos - gastos)
    
    Args:
        db: Sesión de base de datos
        user_id: ID del usuario
        start_date: Fecha inicial opcional para filtrar
        end_date: Fecha final opcional para filtrar
    
    Returns:
        Diccionario con totals y balance
    """

    # Filtro base por usuario
    base_query = db.query(Movement).filter(Movement.user_id == user_id)

    # Aplicar filtros de fecha si existen
    if start_date:
        base_query = base_query.filter(Movement.date >= start_date)
    if end_date:
        base_query = base_query.filter(Movement.date <= end_date)
    
    # Calcular totales por tipo
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
    Obtiene un usuario por su nombre de usuario.
    
    Args:
        db: Sesión de la base de datos.
        username: Nombre de usuario a buscar.
        
    Returns:
        El objeto User si existe, None si no se encuentra.
    """

    return db.query(User).filter(User.username == username).first()