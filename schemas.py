from pydantic import BaseModel
from typing import List, Optional,Annotated,Union
from datetime import datetime
from fastapi import Body

class ProjectBase(BaseModel):
    projectNameTH: str
    projectNameEN: str
    propertyType: str
    projectNameTHSlug: Optional[str] = None
    projectNameENSlug: Optional[str] = None
    startingPrice: Optional[float] = None
    cityCode: Optional[int] = None
    creationTime: Annotated[Union[datetime, None], Body()] = None
    lastEditTime: Annotated[Union[datetime, None], Body()] = None
    publishTime: Annotated[Union[datetime, None], Body()] = None
    logoMediaId: Optional[str] = None
    countryName: Optional[str] = None
class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    pass

class Project(ProjectBase):
    id: str
    class Config:
        orm_mode = True

class CountryCodes(BaseModel):
    country_name: str
    alpha_2_code: str
    alpha_3_code: str
    dial_code: str

    class Config:
        orm_mode = True
