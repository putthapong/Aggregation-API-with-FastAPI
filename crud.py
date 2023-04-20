from sqlalchemy.orm import Session
from models import Project,CountryCodes
from schemas import ProjectCreate, ProjectUpdate
import pandas as pd
from io import StringIO
from typing import List
import json

f = open('./file/CountryCodes.json')

alpha_2_codes = {}

for i in json.load(f):
    alpha_2_codes[i['code']] = i['dial_code'][1:]

propertyType = {
    "บ้านเดี่ยว": "S",
    "บ้านแฝด": "D",
    "บ้านเเฝด": "D",
    "ทาวน์โฮม": "T",
    "คอนโดมิเนี่ยม": "C",
    "อาคารพาณิชย์": "B",
}

async def create_project(db: Session, project: ProjectCreate):
    db_project = Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

async def create_projects_from_csv(db: Session, csv_data: str):
    data = pd.read_csv(StringIO(csv_data))
    data.fillna(" ", inplace=True)
    project_dicts = data.to_dict('records')
    for index in range(len(project_dicts)):
        db_project = Project(**project_dicts[index])
        db.add(db_project)
        db.commit()
    
    return project_dicts

async def get_project(db: Session, project_id: str) -> Project:
    db_project = db.query(Project).filter(Project.id == project_id).first()
    db_project.logoMediaId = "https://www.createder.com/media/"+db_project.logoMediaId+".jpg"
    return db_project

async def get_projects(db: Session) -> List[Project]:
    db_project = db.query(Project).all()
    projects = []
    for project in db_project:
        project.logoMediaId = "https://www.createder.com/media/"+project.logoMediaId+".jpg"
        projects.append(project)
    return projects

async def update_project(db: Session, project_id: int, project: ProjectUpdate):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if db_project:
        update_data = project.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_project, key, value)
        db.commit()
        db.refresh(db_project)
    return db_project

async def add_country_name(db: Session):
    db_project = db.query(Project).all()
    for project in db_project:
        country_code = str(project.cityCode)[:2]
        country = db.query(CountryCodes).filter(CountryCodes.dial_code == country_code).first()
        if country:
            project.countryName = country.country_name
    db.commit()
    db.close()
    return db.query(Project).first()

async def get_countrycodes(db: Session, skip: int = 0, limit: int = 100) -> List[CountryCodes]:
    return  db.query(CountryCodes).offset(skip).limit(limit).all()

async def create_countrycodes_from_csv(db: Session, csv_data: str):
    data = pd.read_csv(StringIO(csv_data))
    data.fillna(" ", inplace=True)
    countrycodes_dicts = data.to_dict('records')
    for index in range(len(countrycodes_dicts)):
        country_name = countrycodes_dicts[index]['name']
        alpha_2_code = countrycodes_dicts[index]['alpha-2']
        alpha_3_code = countrycodes_dicts[index]['alpha-3']
        try:
            dial_code = alpha_2_codes[alpha_2_code]
        except KeyError:
            dial_code = ''
        if countrycodes_dicts[index]['name'] == 'Namibia':
            country_dict = {
            'country_name':country_name,
            'alpha_2_code':'NA', 
            'alpha_3_code':alpha_3_code,
            'dial_code':alpha_2_codes['NA']
            }
        else:
            country_dict = {
                'country_name':country_name,
                'alpha_2_code':alpha_2_code, 
                'alpha_3_code':alpha_3_code,
                'dial_code':dial_code
            }
        db_countrycode = CountryCodes(**country_dict)
        db.add(db_countrycode)
        db.commit()
    return countrycodes_dicts

async def get_projects_by_property_type(db: Session, property_type: str):
    property_type = propertyType[property_type]
    return db.query(Project).filter(Project.propertyType == property_type).all()

async def get_projects_by_country_name(db: Session, country_name: str):
    return db.query(Project).join(
        CountryCodes,
        Project.cityCode.startswith(CountryCodes.dial_code)
    ).filter(
        CountryCodes.country_name == country_name
    ).all()

async def get_citycode(db:Session,citycode:int):
    return db.query(Project).filter(Project.cityCode.startswith(citycode)).all()

async def price_range(db: Session,price_min: float = 50000, price_max: float = 1000000):
    return db.query(Project).filter(Project.startingPrice.between(price_min,price_max)).all()