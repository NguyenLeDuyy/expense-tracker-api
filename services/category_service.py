from models.category import Category
from crud.category import create_category
from schemas.category import CategoryCreate
from sqlalchemy.orm import Session
def create_category_service(db: Session, category_data: CategoryCreate, user_id: int):
    category = create_category(db, category_data, user_id)
    
    db.commit()
    db.refresh(category)
    return category

def get_categories_service(db: Session, user_id: int):
    return db.query(Category).filter(Category.user_id == user_id).all()