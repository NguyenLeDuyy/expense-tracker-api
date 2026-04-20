from models.category import Category
from schemas.category import CategoryCreate
from sqlalchemy.orm import Session

def get_category_by_name(db: Session, name: str, user_id: int):
    return db.query(Category).filter(
        Category.user_id == user_id,
        Category.name == name
    ).first()

def create_category(db: Session, category_data: CategoryCreate, user_id: int):
    category = Category(name=category_data.name, monthly_budget=category_data.monthly_budget, user_id=user_id)
    db.add(category)
    return category

def delete_category(db: Session, category_id: int, user_id: int):
    category = db.query(Category).filter(Category.id == category_id, Category.user_id == user_id).first()
    if not category:
        return None
    db.delete(category)
    return category

def update_category(db: Session, category_data: CategoryCreate, category_id: int, user_id: int):
    category = db.query(Category).filter(Category.id == category_id, Category.user_id == user_id).first()
    if not category:
        return None
    category.name = category_data.name
    category.monthly_budget = category_data.monthly_budget
    return category