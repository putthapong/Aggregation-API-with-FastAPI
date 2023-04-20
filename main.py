from xmlrpc.client import Boolean
from fastapi import FastAPI, Depends, HTTPException,UploadFile,File,Query
from sqlalchemy.orm import Session
import models,crud,database,schemas
from typing import List

app = FastAPI()
models.Base.metadata.create_all(bind=database.engine)

async def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/projects/{project_id}", response_model=schemas.Project)
async def read_project(project_id: str, db: Session = Depends(get_db)):
    project_dict = await crud.get_project(db, project_id=project_id)
    if project_dict is None:
        raise HTTPException(status_code=404, detail="Project_id not found")
    return project_dict

@app.get("/projects/", response_model=List[schemas.Project])
async def read_projects(db: Session = Depends(get_db)):
    return await crud.get_projects(db)

@app.put("/projects/{project_id}", response_model=schemas.Project)
async def update_project(
    project_id: str, project: schemas.ProjectUpdate, db: Session = Depends(get_db)
):
    db_project = crud.get_project(db, id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    update_data = project.dict(exclude_unset=True)
    updated_project = crud.update_project(db, db_project=db_project, **update_data)
    return updated_project

@app.post("/projects/csv")
async def create_projects_from_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type != 'text/csv':
        raise HTTPException(status_code=400, detail="File must be in CSV format.")
    contents = await file.read()
    csv_data = contents.decode('utf-8')
    project_dicts = await crud.create_projects_from_csv(db=db,csv_data=csv_data)
    return {"message": f"{len(project_dicts)} projects inserted."}

@app.get("/projects/add")
async def add_country_name(db: Session = Depends(get_db)):
    return await crud.add_country_name(db=db)
    
@app.get("/countrycodes/",response_model=List[schemas.CountryCodes])
async def get_countrycodes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return await crud.get_countrycodes(db, skip=skip, limit=limit)

@app.post("/countrycodes/csv")
async def create_countrycodes_from_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type != 'text/csv':
        raise HTTPException(status_code=400, detail="File must be in CSV format.")
    contents = await file.read()
    csv_data = contents.decode('utf-8')
    countrycodes_dicts = await crud.create_countrycodes_from_csv(db=db,csv_data=csv_data)
    return {"message": f"{len(countrycodes_dicts)} countrycodes inserted."}

@app.get("/projects/property_type/")
async def get_projects_by_property_type(property_type: str = Query("บ้านเดี่ยว",enum=["บ้านเดี่ยว","บ้านแฝด","บ้านเเฝด","ทาวน์โฮม","คอนโดมิเนี่ยม","อาคารพาณิชย์"]), db: Session = Depends(get_db)):
    projects = await crud.get_projects_by_property_type(db, property_type=property_type)
    return {"projects": projects}

@app.get("/projects/by_country_name/")
async def get_projects_by_country_name(country_name: str, db: Session = Depends(get_db)):
    projects = await crud.get_projects_by_country_name(db, country_name=country_name)
    if not projects:
        raise HTTPException(status_code=404, detail="Projects not found")
    return projects

@app.get("/projects/citycode/")
async def get_citycode(citycode:int,db:Session = Depends(get_db)):
    project =  await crud.get_citycode(db = db,citycode = citycode)
    if not project:
        raise HTTPException(status_code=404, detail="Projects not found")
    return project

@app.get("/projects/price_range/")
async def get_price_range(price_min: float = 50000,price_max: float = 1000000,db:Session= Depends(get_db)):
    project =  await crud.price_range(db = db,price_min = price_min,price_max=price_max)
    if not project:
        raise HTTPException(status_code=404, detail="Projects not found")
    return project
