"""
DevOps Learning API - Simple FastAPI Application
This is a basic API to learn CI/CD and DevOps concepts
"""

import logging
from typing import List, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="DevOps Learning API",
    description="Simple API for studying DevOps pipelines",
    version="0.1.0"
)

# Pydantic models
class ItemBase(BaseModel):
    """Base model for items"""
    title: str
    description: Optional[str] = None
    completed: bool = False


class Item(ItemBase):
    """Item model with ID and timestamp"""
    id: int
    created_at: datetime


class HealthStatus(BaseModel):
    """Health check response model"""
    status: str
    timestamp: datetime
    version: str


# In-memory database (for demo purposes)
items_db: dict = {}
next_id = 1


@app.get("/health", response_model=HealthStatus)
async def health_check():
    """
    Health check endpoint - always returns OK
    Used by load balancers and monitoring systems
    """
    logger.info("Health check requested")
    return HealthStatus(
        status="healthy",
        timestamp=datetime.utcnow(),
        version="0.1.0"
    )


@app.get("/api/items", response_model=List[Item])
async def list_items(skip: int = 0, limit: int = 10):
    """
    List all items with pagination
    
    Args:
        skip: Number of items to skip (default: 0)
        limit: Maximum items to return (default: 10)
    
    Returns:
        List of items
    """
    logger.info(f"Listing items - skip: {skip}, limit: {limit}")
    
    items_list = list(items_db.values())
    return items_list[skip : skip + limit]


@app.post("/api/items", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemBase):
    """
    Create a new item
    
    Args:
        item: Item data (title, description, completed)
    
    Returns:
        Created item with ID and timestamp
    """
    global next_id
    
    logger.info(f"Creating new item: {item.title}")
    
    new_item = Item(
        id=next_id,
        title=item.title,
        description=item.description,
        completed=item.completed,
        created_at=datetime.utcnow()
    )
    
    items_db[next_id] = new_item
    next_id += 1
    
    logger.info(f"Item created with ID: {new_item.id}")
    return new_item


@app.get("/api/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    """
    Get a specific item by ID
    
    Args:
        item_id: Item identifier
    
    Returns:
        Item data
    
    Raises:
        HTTPException: If item not found
    """
    logger.info(f"Fetching item with ID: {item_id}")
    
    if item_id not in items_db:
        logger.warning(f"Item not found: {item_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found"
        )
    
    return items_db[item_id]


@app.put("/api/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: ItemBase):
    """
    Update an existing item
    
    Args:
        item_id: Item identifier
        item: Updated item data
    
    Returns:
        Updated item
    
    Raises:
        HTTPException: If item not found
    """
    logger.info(f"Updating item with ID: {item_id}")
    
    if item_id not in items_db:
        logger.warning(f"Cannot update - item not found: {item_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found"
        )
    
    existing_item = items_db[item_id]
    updated_item = Item(
        id=item_id,
        title=item.title,
        description=item.description,
        completed=item.completed,
        created_at=existing_item.created_at
    )
    
    items_db[item_id] = updated_item
    logger.info(f"Item {item_id} updated successfully")
    
    return updated_item


@app.delete("/api/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    """
    Delete an item
    
    Args:
        item_id: Item identifier
    
    Raises:
        HTTPException: If item not found
    """
    logger.info(f"Deleting item with ID: {item_id}")
    
    if item_id not in items_db:
        logger.warning(f"Cannot delete - item not found: {item_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found"
        )
    
    del items_db[item_id]
    logger.info(f"Item {item_id} deleted successfully")
    return None


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
