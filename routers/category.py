from schemas.response import success_response
from schemas.response import ApiResponse
from services.category_service import delete_category_service, update_category_service
from schemas.category import CategoryResponse
from services.category_service import get_categories_service, create_category_service
from fastapi import Depends
from schemas.category import CategoryCreate
from fastapi import APIRouter
from app.core.deps import get_db
from sqlalchemy.orm import Session
from app.core.deps import get_current_user
from models.user import User


router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=ApiResponse[CategoryResponse],
    summary="Create a category",
    description="Create a new expense category with an optional monthly budget limit."
)
def create_category(
    category: CategoryCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    category = create_category_service(db, category, current_user.id)
    return success_response(data=category, message="Category created successfully")

@router.get("/", response_model=ApiResponse[list[CategoryResponse]],
    summary="List categories",
    description="Retrieve all expense categories belonging to the current user."
)
def get_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    categories = get_categories_service(db, current_user.id)
    return success_response(data=categories, message="Categories retrieved successfully")

@router.delete("/{category_id}",
    summary="Delete a category",
    description="Permanently delete a category by ID. Only the owner can delete their own categories."
)
def delete_category(
    category_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    delete_category_service(db, category_id, current_user.id)
    return success_response(message="Category deleted successfully")

@router.put("/{category_id}", response_model=ApiResponse[CategoryResponse],
    summary="Update a category",
    description="Update the name or monthly budget of an existing category."
)
def update_category(
    updated: CategoryCreate, 
    category_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    updated_category = update_category_service(db, updated, category_id, current_user.id)
    return success_response(data=updated_category, message="Category updated successfully")