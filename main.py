from fastapi import Path # type: ignore
from fastapi import FastAPI, HTTPException, Query, Body # type: ignore
from fastapi.routing import APIRouter # type: ignore
from bson import ObjectId # type: ignore
from database import students_collection
from models import StudentCreateModel, StudentResponseModel
from typing import Optional
from typing import Dict, Any

api_router = APIRouter()
app = FastAPI(
    title="Backend Intern Hiring Task",
    version="1.0.0",
    description=(
        "I have implemented these APIs in FastAPI and MongoDB tech stack "
        "as mentioned on your problem statement document."
    )
)
app.include_router(api_router, prefix="/api")

# Helper function to serialize MongoDB objects
def serialize_student(student):
    student["_id"] = str(student["_id"])
    return student

@app.post(
    "/students",
    status_code=201,
    response_model=StudentResponseModel,  # Return only the ID in the response
    responses={
        201: {
            "description": "A JSON response sending back the ID of the newly created student record.",
            "content": {
                "application/json": {
                    "example": {
                        "id": "String"
                    }
                }
            },
        }
    },
    summary="Create Students",
    description="API to create a student in the system. All fields are mandatory and required while creating the student in the system."
)
async def create_student(student: StudentCreateModel):
    student_dict = student.dict()  # Convert the student model to a dictionary
    result = students_collection.insert_one(student_dict)  # Insert into MongoDB
    return {"id": str(result.inserted_id)}  # Return only the ID of the newly created student


@app.get(
    "/students",
    response_model=list[dict],
    responses={
        200: {
            "description": "sample response",
            "content": {
                "application/json": {
                    "example":
                        {
                            "data": [
                                {
                                    "name": "string",
                                    "age": 0
                                }
                                ]
                        }
                }
            },
        }
    },
    summary="List students",
    description=(
        "An API to find a list of students. You can apply filters on this API by passing the query parameters as listed below:\n\n"
    ),
)
async def list_students(
    country: Optional[str] = Query(None, description="To apply filter of country. If not given or empty, this filter should be applied."),
    age: Optional[int] = Query(None, description="Only records which have age greater than equal to the provided age should be present in the result. If not given or empty, this filter should be applied."),
):
    query = {}
    if country:
        query["address.country"] = country
    if age:
        query["age"] = {"$gte": age}

    students = students_collection.find(query, {"name": 1, "age": 1, "_id": 0})
    return [student for student in students]


@app.get(
    "/students/{id}",
    response_model=StudentCreateModel,
    responses={
        200: {
            "description": "Sample Response",
            "content": {
                "application/json": {
                    "example": {
                        "name": "string",
                        "age": 0,
                        "address": {
                            "city": "string",
                            "country": "string"
                        }
                    }
                }
            },
        },
        
    },
    summary="Fetch student",
)
async def fetch_student(id: str = Path(..., description="The ID of the student previously created.")):
    student = students_collection.find_one({"_id": ObjectId(id)})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return serialize_student(student)


@app.patch("/students/{id}", status_code=204,
           responses={
        204: {
            "description": "No content",
            "content": {
                "application/json": {
                    "example": {}
                }
            }
        },
    },
           description=(
        "API to update the student's properties based on information provided. "
        "Not mandatory that all information would be sent in PATCH, only what fields are sent should be updated in the Database.\n\n"
        
    ),)
async def update_student(id: str, student_update: Dict[str, Any] = Body(..., example={
    "name": "string",
    "age": 0,
    "address": {
        "city": "string",
        "country": "string"
    }
})):

    # Ensure there's data to update
    if not student_update:
        raise HTTPException(status_code=400, detail="No data provided for update")

    # Perform the update
    result = students_collection.update_one(
        {"_id": ObjectId(id)}, {"$set": student_update}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")


@app.delete("/students/{id}", status_code=200,responses={
        200: {
            "description": "sample response",
            "content": {
                "application/json": {
                    "example": {}
                }
            }
        },
    })
async def delete_student(id: str):
    result = students_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {}
