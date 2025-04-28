from sqlalchemy import (
    Column, Integer, String, Date, ForeignKey, DECIMAL
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import re

Base = declarative_base()

# Address Table
class Address(Base):
    __tablename__ = 'address'

    address_id = Column(Integer, primary_key=True)
    street = Column(String(100), nullable=False)
    house_number = Column(String(10), nullable=False)
    postal_code = Column(String(4), nullable=False)
    municipality = Column(String(25), nullable=False)
    country = Column(String(50), default='BE')
    longitude = Column(DECIMAL(10, 8), default=None)
    latitude = Column(DECIMAL(10, 8), default=None)

    # Relationships
    persons = relationship("Person", back_populates="address", lazy="joined")
    companies = relationship("Company", back_populates="address", lazy="joined")
    sub_assignments = relationship("SubAssignment", back_populates="delivery_address", lazy="joined")

    def __repr__(self):
        return f"Address(address_id={self.address_id}, street='{self.street}', house_number='{self.house_number}', postal_code='{self.postal_code}', municipality='{self.municipality}', country='{self.country}', longitude={self.longitude}, latitude={self.latitude})"

    def __str__(self):
        return f"Address(address_id={self.address_id}, street='{self.street}', house_number='{self.house_number}', postal_code='{self.postal_code}', municipality='{self.municipality}', country='{self.country}', longitude={self.longitude}, latitude={self.latitude})"


# Person Table
class Person(Base):
    __tablename__ = 'person'

    person_id = Column(Integer, primary_key=True)
    address_id = Column(Integer, ForeignKey('address.address_id'))
    name_first = Column(String(50), nullable=False)
    name_last = Column(String(50), nullable=False)
    name_title = Column(String(50))
    job_description = Column(String(50))
    date_of_birth = Column(Date)
    phone_number = Column(String(20))
    email = Column(String(100))

    # Relationships
    address = relationship("Address", back_populates="persons", lazy="joined")
    companies = relationship("Company", foreign_keys="Company.contactperson_id", back_populates="contact_person", lazy="joined")
    day_assignments = relationship("DayAssignment", back_populates="person", lazy="joined")

    @staticmethod
    def validate_email(email):
        """Validate the email format using a regex."""
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email) is not None

    def __repr__(self):
        return f"Person(person_id={self.person_id}, address_id={self.address_id}, name_first='{self.name_first}', name_last='{self.name_last}', name_title='{self.name_title}', job_description='{self.job_description}', date_of_birth={self.date_of_birth}, phone_number='{self.phone_number}', email='{self.email}')"

    def __str__(self):
        return f"Person(person_id={self.person_id}, address_id={self.address_id}, name_first='{self.name_first}', name_last='{self.name_last}', name_title='{self.name_title}', job_description='{self.job_description}', date_of_birth={self.date_of_birth}, phone_number='{self.phone_number}', email='{self.email}')"


# Company Table
class Company(Base):
    __tablename__ = 'company'

    company_id = Column(Integer, primary_key=True)
    address_id = Column(Integer, ForeignKey('address.address_id'))
    contactperson_id = Column(Integer, ForeignKey('person.person_id'))
    company_name = Column(String(100), nullable=False)
    tax_number = Column(String(20), unique=True, nullable=False)

    # Relationships
    address = relationship("Address", back_populates="companies", lazy="joined")
    contact_person = relationship("Person", back_populates="companies", lazy="joined")

    def __repr__(self):
        return f"Company(company_id={self.company_id}, address_id={self.address_id}, contactperson_id={self.contactperson_id}, company_name='{self.company_name}', tax_number='{self.tax_number}')"

    def __str__(self):
        return f"Company(company_id={self.company_id}, address_id={self.address_id}, contactperson_id={self.contactperson_id}, company_name='{self.company_name}', tax_number='{self.tax_number}')"


# Client Table
class Client(Base):
    __tablename__ = 'client'

    client_id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('company.company_id'))

    # Relationships
    company = relationship("Company", lazy="joined")

    def __repr__(self):
        return f"Client(client_id={self.client_id}, company_id={self.company_id})"

    def __str__(self):
        return f"Client(client_id={self.client_id}, company_id={self.company_id})"

    def __repr__(self):
        return f"Supplier(supplier_id={self.supplier_id}, company_id={self.company_id})"

    def __str__(self):
        return f"Supplier(supplier_id={self.supplier_id}, company_id={self.company_id})"


# Supplier Table
class Supplier(Base):
    __tablename__ = 'supplier'

    supplier_id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('company.company_id'))

    # Relationships
    company = relationship("Company", lazy="joined")


# Article Table
class Article(Base):
    __tablename__ = 'article'

    article_id = Column(Integer, primary_key=True)
    supplier_id = Column(Integer, ForeignKey('supplier.supplier_id'))
    supplier_article_code = Column(String(40))
    purchase_price = Column(DECIMAL(10, 2))
    description = Column(String(100))

    # Relationships
    supplier = relationship("Supplier", lazy="joined")

    def __repr__(self):
        return f"Article(article_id={self.article_id}, supplier_id={self.supplier_id}, supplier_article_code='{self.supplier_article_code}', purchase_price={self.purchase_price}, description='{self.description}')"

    def __str__(self):
        return f"Article(article_id={self.article_id}, supplier_id={self.supplier_id}, supplier_article_code='{self.supplier_article_code}', purchase_price={self.purchase_price}, description='{self.description}')"


# Assignment Table
class Assignment(Base):
    __tablename__ = 'assignment'

    assignment_id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('person.person_id'))
    calculator_id = Column(Integer, ForeignKey('person.person_id'), nullable=False)
    salesman_id = Column(Integer, ForeignKey('person.person_id'))
    project_leader_id = Column(Integer, ForeignKey('person.person_id'))
    scheduling = Column(String(10))
    date_acceptance = Column(Date, nullable=False)
    date_start = Column(Date, default=None)
    date_end = Column(Date, default=None)

    # Relationships
    client = relationship("Person", foreign_keys=[client_id], lazy="joined")
    calculator = relationship("Person", foreign_keys=[calculator_id], lazy="joined")
    salesman = relationship("Person", foreign_keys=[salesman_id], lazy="joined")
    project_leader = relationship("Person", foreign_keys=[project_leader_id], lazy="joined")
    sub_assignments = relationship("SubAssignment", back_populates="assignment", lazy="joined")

    def __repr__(self):
        return f"Assignment(assignment_id={self.assignment_id}, client_id={self.client_id}, calculator_id={self.calculator_id}, salesman_id={self.salesman_id}, project_leader_id={self.project_leader_id}, scheduling='{self.scheduling}', date_acceptance={self.date_acceptance}, date_start={self.date_start}, date_end={self.date_end})"

    def __str__(self):
        return f"Assignment(assignment_id={self.assignment_id}, client_id={self.client_id}, calculator_id={self.calculator_id}, salesman_id={self.salesman_id}, project_leader_id={self.project_leader_id}, scheduling='{self.scheduling}', date_acceptance={self.date_acceptance}, date_start={self.date_start}, date_end={self.date_end})"


# SubAssignment Table
class SubAssignment(Base):
    __tablename__ = 'sub_assignment'

    sub_assignment_id = Column(Integer, primary_key=True)
    assignment_id = Column(Integer, ForeignKey('assignment.assignment_id'))
    delivery_address_id = Column(Integer, ForeignKey('address.address_id'))
    sub_name = Column(String(10))
    sub_description = Column(String(100))

    # Relationships
    assignment = relationship("Assignment", back_populates="sub_assignments", lazy="joined")
    delivery_address = relationship("Address", back_populates="sub_assignments", lazy="joined")
    assignment_lines = relationship("AssignmentLine", back_populates="sub_assignment", lazy="joined")
    day_assignments = relationship("DayAssignment", back_populates="sub_assignment", lazy="joined")

    def __repr__(self):
        return f"SubAssignment(sub_assignment_id={self.sub_assignment_id}, assignment_id={self.assignment_id}, delivery_address_id={self.delivery_address_id}, sub_name='{self.sub_name}', sub_description='{self.sub_description}')"

    def __str__(self):
        return f"SubAssignment(sub_assignment_id={self.sub_assignment_id}, assignment_id={self.assignment_id}, delivery_address_id={self.delivery_address_id}, sub_name='{self.sub_name}', sub_description='{self.sub_description}')"


# AssignmentLine Table
class AssignmentLine(Base):
    __tablename__ = 'assignment_line'

    assignment_line_id = Column(Integer, primary_key=True)
    sub_assignment_id = Column(Integer, ForeignKey('sub_assignment.sub_assignment_id'))
    sales_price = Column(DECIMAL(10, 2))
    amount = Column(Integer)
    article_id = Column(Integer, ForeignKey('article.article_id'))
    date_acceptance = Column(Date)
    date_ordered = Column(Date)
    date_received = Column(Date)
    date_issued = Column(Date)
    date_delivered = Column(Date)
    date_installed = Column(Date)
    date_accepted = Column(Date)
    date_invoiced = Column(Date)
    date_paid = Column(Date)
    date_closed = Column(Date)

    # Relationships
    sub_assignment = relationship("SubAssignment", back_populates="assignment_lines", lazy="joined")
    article = relationship("Article", lazy="joined")

    def __repr__(self):
        return f"AssignmentLine(assignment_line_id={self.assignment_line_id}, sub_assignment_id={self.sub_assignment_id}, sales_price={self.sales_price}, amount={self.amount}, article_id={self.article_id}, date_acceptance={self.date_acceptance}, date_ordered={self.date_ordered}, date_received={self.date_received}, date_issued={self.date_issued}, date_delivered={self.date_delivered}, date_installed={self.date_installed}, date_accepted={self.date_accepted}, date_invoiced={self.date_invoiced}, date_paid={self.date_paid}, date_closed={self.date_closed})"

    def __str__(self):
        return f"AssignmentLine(assignment_line_id={self.assignment_line_id}, sub_assignment_id={self.sub_assignment_id}, sales_price={self.sales_price}, amount={self.amount}, article_id={self.article_id}, date_acceptance={self.date_acceptance}, date_ordered={self.date_ordered}, date_received={self.date_received}, date_issued={self.date_issued}, date_delivered={self.date_delivered}, date_installed={self.date_installed}, date_accepted={self.date_accepted}, date_invoiced={self.date_invoiced}, date_paid={self.date_paid}, date_closed={self.date_closed})"


# DayAssignment Table
class DayAssignment(Base):
    __tablename__ = 'day_assignment'

    day_assignment_id = Column(Integer, primary_key=True)
    sub_assignment_id = Column(Integer, ForeignKey('sub_assignment.sub_assignment_id'))
    person_id = Column(Integer, ForeignKey('person.person_id'))
    date = Column(Date)
    assignment_description = Column(String(100))

    # Relationships
    sub_assignment = relationship("SubAssignment", back_populates="day_assignments", lazy="joined")
    person = relationship("Person", back_populates="day_assignments", lazy="joined")

    def __repr__(self):
        return f"DayAssignment(day_assignment_id={self.day_assignment_id}, sub_assignment_id={self.sub_assignment_id}, person_id={self.person_id}, date={self.date}, assignment_description='{self.assignment_description}')"

    def __str__(self):
        return f"DayAssignment(day_assignment_id={self.day_assignment_id}, sub_assignment_id={self.sub_assignment_id}, person_id={self.person_id}, date={self.date}, assignment_description='{self.assignment_description}')"
