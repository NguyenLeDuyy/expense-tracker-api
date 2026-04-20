from models.category import Category
from schemas.category import CategoryCreate
from sqlalchemy.orm import Session

def create_category(db: Session, category_data: CategoryCreate, user_id: int):
    category = Category(name=category_data.name, monthly_budget=category_data.monthly_budget, user_id=user_id)
    db.add(category)
    return category