from sqlalchemy import (
    Column,
    Integer,
    String,
    DECIMAL,
    VARCHAR,
    ForeignKey,
    Date,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# Address Class
class Address(Base):
    __tablename__ = "address"

    address_id = Column(Integer, primary_key=True)
    street = Column(String(100), nullable=False)
    house_number = Column(String(10), nullable=False)
    postal_code = Column(String(4), nullable=False)
    city = Column(String(25), nullable=False)
    longitude = Column(DECIMAL(10, 8))
    latitude = Column(DECIMAL(10, 8))

    companies = relationship("Company", back_populates="address")


# Person Class
class Person(Base):
    __tablename__ = "person"

    person_id = Column(Integer, primary_key=True)
    name_first = Column(String(50), nullable=False)
    name_last = Column(String(50), nullable=False)
    name_title = Column(String(50))
    phone_number = Column(String(20))
    email = Column(String(100))

    companies = relationship("Company", back_populates="contactperson")
    daily_assignment_lines = relationship(
        "DailyAssignmentLine", back_populates="person"
    )


# Company Class
class Company(Base):
    __tablename__ = "company"

    company_id = Column(Integer, primary_key=True)
    address_id = Column(Integer, ForeignKey("address.address_id"))
    company_name = Column(String(100), nullable=False)
    contactperson_id = Column(Integer, ForeignKey("person.person_id"))
    tax_number = Column(String(20), unique=True, nullable=False)

    address = relationship("Address", back_populates="companies")
    contactperson = relationship("Person", back_populates="companies")
    suppliers = relationship("Supplier", back_populates="company")


# Client Class
class Client(Base):
    __tablename__ = "client"

    client_id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("company.company_id"))

    company = relationship("Company")


# Assignment Class
class Assignment(Base):
    __tablename__ = "assignment"

    assignment_id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("person.person_id"))
    calculator_id = Column(Integer, ForeignKey("person.person_id"))
    salesman_id = Column(Integer, ForeignKey("person.person_id"))
    project_leader_id = Column(Integer, ForeignKey("person.person_id"))
    scheduling = Column(VARCHAR(10))
    acceptance_date = Column(Date)
    date_start = Column(Date)
    date_end = Column(Date)

    client = relationship("Person", foreign_keys=[client_id])
    calculator = relationship("Person", foreign_keys=[calculator_id])
    salesman = relationship("Person", foreign_keys=[salesman_id])
    project_leader = relationship("Person", foreign_keys=[project_leader_id])
    subassignments = relationship("Subassignment", back_populates="assignment")
    daily_assignments = relationship("DailyAssignment", back_populates="assignment")


# Subassignment Class
class Subassignment(Base):
    __tablename__ = "subassignment"

    subassignment_id = Column(Integer, primary_key=True)
    assignment_id = Column(Integer, ForeignKey("assignment.assignment_id"))
    address_id = Column(Integer, ForeignKey("address.address_id"))
    sub_name = Column(String(100))

    assignment = relationship("Assignment", back_populates="subassignments")
    address = relationship("Address")
    assignment_lines = relationship("AssignmentLine", back_populates="subassignment")


# AssignmentLine Class
class AssignmentLine(Base):
    __tablename__ = "assignmentline"

    assignmentline_id = Column(Integer, primary_key=True)
    subassignment_id = Column(Integer, ForeignKey("subassignment.subassignment_id"))
    sales_price = Column(DECIMAL(10, 2))

    subassignment = relationship("Subassignment", back_populates="assignment_lines")
    daily_assignment_lines = relationship(
        "DailyAssignmentLine", back_populates="assignmentline"
    )


# Article Class
class Article(Base):
    __tablename__ = "article"

    article_id = Column(Integer, primary_key=True)
    supplier_id = Column(Integer, ForeignKey("supplier.supplier_id"))
    supplier_code = Column(String(20))
    purchase_price = Column(DECIMAL(10, 2))

    supplier = relationship("Supplier", back_populates="articles")


# Supplier Class
class Supplier(Base):
    __tablename__ = "supplier"

    supplier_id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("company.company_id"))

    company = relationship("Company", back_populates="suppliers")
    articles = relationship("Article", back_populates="supplier")


# DailyAssignment Class
class DailyAssignment(Base):
    __tablename__ = "daily_assignment"

    daily_assignment_id = Column(Integer, primary_key=True)
    assignment_id = Column(Integer, ForeignKey("assignment.assignment_id"))
    date = Column(Date)
    assignment_description = Column(String(100))

    assignment = relationship("Assignment", back_populates="daily_assignments")
    daily_assignment_lines = relationship(
        "DailyAssignmentLine", back_populates="daily_assignment"
    )


# DailyAssignmentLine Class
class DailyAssignmentLine(Base):
    __tablename__ = "daily_assignment_line"

    daily_assignment_line_id = Column(Integer, primary_key=True)
    assignmentline_id = Column(Integer, ForeignKey("assignmentline.assignmentline_id"))
    person_id = Column(Integer, ForeignKey("person.person_id"))
    assignment_description = Column(String(100))

    assignmentline = relationship(
        "AssignmentLine", back_populates="daily_assignment_lines"
    )
    person = relationship("Person", back_populates="daily_assignment_lines")