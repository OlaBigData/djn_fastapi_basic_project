from fastapi import FastAPI, HTTPException, status
from typing import Union, Optional
from pydantic import BaseModel

app = FastAPI()

class Course(BaseModel):
    title: str
    teacher: str
    students: Optional[list[str]] = []
    year: str 


courses = {
    1: {
        "title": "Chemistry",
        "teacher": "Adebambo",
        "students": ["Ola", "Dikajah", "Kazeem"],
        "year": "basic"
    },
    2: {
        "title": "Histoy",
        "teacher": "Samuel Johnson",
        "students": ["Ola", "Tayo", "Tobi"],
        "year": "advanced"
    },
    3: {
        "title": "Yoruba",
        "teacher": "Malomon",
        "students": ["Ola", "Timothy", "Adbulquadri"],
        "year": "begineer"
    }
}




@app.get("/api/courses/")
def get_courses(year: Union[str, None] = None ):
    if year:
        year_course =[]
        for index in courses.keys():
            if courses[index]["year"] == year:
                year_course.append(courses[index])
        return year_course
    return courses

@app.get("/api/courses/{course_id}/")
def get_course(course_id: int):
    try:
        return courses[course_id]
    except KeyError:
        raise HTTPException(
            status_code=404, detail=f'Course with id:{course_id} was not found!'
        )


@app.delete("/api/courses/{course_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int):
    try:
        del courses[course_id]
    except KeyError:
        raise HTTPException(
            status_code=404, detail=f'Course with id:{course_id} was not found!'
        )

@app.post("/api/courses", status_code=status.HTTP_201_CREATED)
def create_course(new_course: Course):
    course_id = max(courses.keys()) + 1
    courses[course_id] = new_course.model_dump()
    return courses[course_id]

@app.put("/api/courses/{course_id}/")
def update_course(course_id: int, updated_course: Course):
    try:
        course = courses[course_id]
        course["title"] = updated_course.title
        course["teacher"] = updated_course.teacher
        course["students"] = updated_course.students
        course["year"]  = updated_course.year
        return course
    except KeyError:
        raise HTTPException(
            status_code=404, detail=f'Course with id:{course_id} was not found!'
        )