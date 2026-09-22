from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from database import BookDatabaseManager

# Initialize FastAPI app
app = FastAPI(
    title="Book Data Pipeline API",
    description="FastAPI Microservice for managing scraped book data",
    version="1.0.0"
)

# Initialize database manager
db_manager = BookDatabaseManager()

# Pydantic schemas
class BookCreate(BaseModel):
    title: str = Field(..., example="A Light in the Attic")
    price: float = Field(..., example=51.77)
    in_stock: bool = Field(True, example=True)
    rating: int = Field(..., ge=1, le=5, example=3)


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, example="Updated Book Title")
    price: Optional[float] = Field(None, example=45.00)
    in_stock: Optional[bool] = Field(None, example=True)
    rating: Optional[int] = Field(None, ge=1, le=5, example=5)


class BookResponse(BaseModel):
    id: int
    title: str
    price: float
    in_stock: bool
    rating: int


# Get all books
@app.get("/books", response_model=List[BookResponse], status_code=status.HTTP_200_OK)
def get_all_books():
    return db_manager.get_all_books()


# Get single book by ID
@app.get("/books/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
def get_book_by_id(book_id: int):
    book = db_manager.get_book_by_id(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )
    return book


# Create new book
@app.post("/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book_data: BookCreate):
    new_book = db_manager.create_book(
        title=book_data.title,
        price=book_data.price,
        in_stock=book_data.in_stock,
        rating=book_data.rating
    )
    return new_book


# Update existing book
@app.put("/books/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
def update_book(book_id: int, book_data: BookUpdate):
    updated_book = db_manager.update_book(
        book_id=book_id,
        title=book_data.title,
        price=book_data.price,
        in_stock=book_data.in_stock,
        rating=book_data.rating
    )
    if not updated_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )
    return updated_book


# Delete book by ID
@app.delete("/books/{book_id}", status_code=status.HTTP_200_OK)
def delete_book(book_id: int):
    success = db_manager.delete_book(book_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )
    return {"message": f"Book with ID {book_id} deleted successfully"}

# Main execution entry point
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

