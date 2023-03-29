#!/usr/bin/env python3
from typing import List

from fastapi import APIRouter, Body, HTTPException, Request, Response, status
from fastapi.encoders import jsonable_encoder

from model import Book, BookUpdate

router = APIRouter()

@router.post("/", response_description="Post a new book", status_code=status.HTTP_201_CREATED, response_model=Book)
def create_book(request: Request, book: Book = Body(...)):
    book = jsonable_encoder(book)
    new_book = request.app.database["books"].insert_one(book)
    created_book = request.app.database["books"].find_one(
        {"_id": new_book.inserted_id}
    )

    return created_book


@router.get("/", response_description="Get all books", response_model=List[Book])
def list_books(request: Request, rating: float = 0, text_review_count: int = 0, ratings_count: int = 0, title: str = "", limit: int = 5, skip: int = 0):
    books = list(request.app.database["books"].find(
        {
            "$or": [
                {"average_rating": {"$gte": rating}},
                {"ratings_count": {"$gte": ratings_count}},
                {"text_review_count": {"$gte": text_review_count}},
                {"title": {"$regex": title}}]
        }, limit=limit, skip=skip))
    return books


@router.get("/{id}", response_description="Get a single book by id", response_model=Book)
def find_book(id: str, request: Request):
    if (book := request.app.database["books"].find_one({"_id": id})) is not None:
        return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")

@router.put("/{id}", response_description="Update a book by id", response_model=Book)
def update_book(id: str, request: Request, book: BookUpdate = Body(...)):
    pass

@router.delete("/{id}", response_description="Delete a book")
def delete_book(id: str, request: Request, response: Response):
    pass
