from sqlalchemy import Column, Integer, String, DateTime,Float
from database import Base


class Project(Base):
    __tablename__ = "project"

    id = Column(String(255), primary_key=True, index=True)
    projectNameTH = Column(String(255), index=True)
    projectNameEN = Column(String(255), index=True)
    projectNameTHSlug = Column(String(255), nullable=True)
    projectNameENSlug = Column(String(255), nullable=True)
    propertyType = Column(String(20), index=True)
    startingPrice = Column(Float, index=True)
    cityCode = Column(Integer, index=True)
    creationTime = Column(DateTime,nullable=True)
    lastEditTime = Column(DateTime,nullable=True)
    publishTime = Column(DateTime, nullable=True)
    logoMediaId = Column(String(255), nullable=True)
    countryName = Column(String(255), nullable=True)

    class Config:
        orm_mode = True

class CountryCodes(Base):
    __tablename__ = "country_codes"
    country_name = Column(String(255),nullable=False)
    alpha_2_code = Column(String(2),primary_key=True,)
    alpha_3_code = Column(String(3),nullable=False)
    dial_code = Column(String(5),nullable=False)