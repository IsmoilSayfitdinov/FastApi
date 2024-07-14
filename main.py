from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4, UUID

app = FastAPI()

class Blog(BaseModel):
    id: Optional[UUID] = None
    title: str
    content: str

blogs = []

@app.post("/blogs/", response_model=Blog)
def create_blog(blog: Blog):
    blog.id = uuid4()
    blogs.append(blog)
    return blog

@app.get("/blogs/", response_model=List[Blog])
def get_blogs():
    return blogs

@app.get("/blogs/{blog_id}", response_model=Blog)
def get_blog(blog_id: UUID):
    for blog in blogs:
        if blog.id == blog_id:
            return blog
    raise HTTPException(status_code=404, detail="Blog not found")

@app.put("/blogs/{blog_id}", response_model=Blog)
def update_blog(blog_id: UUID, updated_blog: Blog):
    for index, blog in enumerate(blogs):
        if blog.id == blog_id:
            updated_blog.id = blog.id
            blogs[index] = updated_blog
            return updated_blog
    raise HTTPException(status_code=404, detail="Blog not found")

@app.delete("/blogs/{blog_id}", response_model=Blog)
def delete_blog(blog_id: UUID):
    for index, blog in enumerate(blogs):
        if blog.id == blog_id:
            deleted_blog = blogs.pop(index)
            return deleted_blog
    raise HTTPException(status_code=404, detail="Blog not found")
