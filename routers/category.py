from schemas.category import CategoryResponse
from services.category_service import get_categories_service
from services.category_service import create_category_service
from fastapi import Depends
from schemas.category import CategoryCreate
from fastapi import APIRouter
from app.core.deps import get_db
from sqlalchemy.orm import Session
from app.core.deps import get_current_user
from models.user import User


router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=CategoryResponse)
def create_category(
    category: CategoryCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    return create_category_service(db, category, current_user.id)

@router.get("/", response_model=list[CategoryResponse])
def get_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    return get_categories_service(db, current_user.id)