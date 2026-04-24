from app.core.exceptions import NotFoundException
from app.core.exceptions import BadRequestException
from crud.category import update_category, delete_category, create_category, get_category_by_name
from models.category import Category
from schemas.category import CategoryCreate
from sqlalchemy.orm import Session

def create_category_service(db: Session, category_data: CategoryCreate, user_id: int):
    existing_category = get_category_by_name(db, category_data.name, user_id)
    if existing_category:
        raise BadRequestException("Category already exists")

    category = create_category(db, category_data, user_id)
    
    db.commit()
    db.refresh(category)
    return category

def get_categories_service(db: Session, user_id: int):
    return db.query(Category).filter(Category.user_id == user_id).all()

def delete_category_service(db: Session, category_id: int, user_id: int):
    category = delete_category(db, category_id, user_id)

    if not category:
        raise NotFoundException("Category not found")

    db.commit()
    return category

def update_category_service(db: Session, category_data: CategoryCreate, category_id: int, user_id: int):
    category = update_category(db, category_data, category_id, user_id)
    
    if not category:
        raise NotFoundException("Category not found")

    db.commit()
    db.refresh(category)
    return category
