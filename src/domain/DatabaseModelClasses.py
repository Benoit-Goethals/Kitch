from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
    DECIMAL,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, attributes

Base = declarative_base()


# Utility function to avoid lazy-loading relationship issues
def is_relationship_loaded(instance, attribute):
    """Check if a relationship is loaded to avoid lazy-loading issues."""
    state = attributes.instance_state(instance)
    return attribute in state.load_path or state.persistent


# Address Model
class Address(Base):
    __tablename__ = 'address'

    address_id = Column(Integer, primary_key=True, autoincrement=True)
    street = Column(String(100), nullable=False)
    house_number = Column(String(10), nullable=False)
    postal_code = Column(String(4), nullable=False)
    municipality = Column(String(25), nullable=False)
    country = Column(String(50), default='BE')
    longitude = Column(DECIMAL(10, 8))
    latitude = Column(DECIMAL(10, 8))

    # Bi-directional Relationships
    persons = relationship("Person", back_populates="address", lazy="noload")
    companies = relationship("Company", back_populates="address", lazy="noload")
    phases = relationship("Phase", back_populates="delivery_address", lazy="noload")

    def __str__(self):
        return f"Address({self.street} {self.house_number}, {self.postal_code} {self.municipality})"

    def __repr__(self):
        return f"<Address(id={self.address_id}, street='{self.street}', postal_code='{self.postal_code}', municipality='{self.municipality}')>"


# Person Model
class Person(Base):
    __tablename__ = 'person'

    person_id = Column(Integer, primary_key=True, autoincrement=True)
    address_id = Column(Integer, ForeignKey('address.address_id'))
    name_first = Column(String(50), nullable=False)
    name_last = Column(String(50), nullable=False)
    name_title = Column(String(50))
    job_description = Column(String(50))
    date_of_birth = Column(Date)
    phone_number = Column(String(20))
    email = Column(String(100))
    photo_url = Column(String(255))

    # Bi-directional Relationships
    address = relationship("Address", back_populates="persons",)
    employees = relationship("Employee", back_populates="person", )
    workers = relationship("Worker", back_populates="person", )
    contacted_companies = relationship(
        "Company", back_populates="contactperson",
    )

    def __str__(self):
        return f"Person({self.name_first} {self.name_last})"

    def __repr__(self):
        return f"<Person(id={self.person_id}, name='{self.name_first} {self.name_last}', email='{self.email}')>"


# Employee Model
class Employee(Base):
    __tablename__ = 'employee'

    employee_id = Column(Integer, primary_key=True, autoincrement=True)
    person_id = Column(Integer, ForeignKey('person.person_id'), nullable=False)

    # Bi-directional Relationships
    person = relationship("Person", back_populates="employees", lazy="joined")
    calculated_projects = relationship(
        "Project", foreign_keys="Project.calculator_id", back_populates="calculator", lazy="joined"
    )
    salesperson_projects = relationship(
        "Project", foreign_keys="Project.salesman_id", back_populates="salesman", lazy="joined"
    )
    lead_projects = relationship(
        "Project", foreign_keys="Project.project_leader_id", back_populates="project_leader", lazy="joined"
    )

    def __str__(self):
        return f"Employee(person={self.person})"

    def __repr__(self):
        return f"<Employee(id={self.employee_id}, person_id={self.person_id})>"


# Worker Model
class Worker(Base):
    __tablename__ = 'worker'

    worker_id = Column(Integer, primary_key=True, autoincrement=True)
    person_id = Column(Integer, ForeignKey('person.person_id'), nullable=False)

    # Bi-directional Relationships
    person = relationship("Person", back_populates="workers", lazy="joined")
    assignments = relationship("Assignment", back_populates="worker", lazy="joined")

    def __str__(self):
        return f"Worker(person={self.person})"

    def __repr__(self):
        return f"<Worker(id={self.worker_id}, person_id={self.person_id})>"


# Company Model
class Company(Base):
    __tablename__ = 'company'

    company_id = Column(Integer, primary_key=True, autoincrement=True)
    address_id = Column(Integer, ForeignKey('address.address_id'))
    contactperson_id = Column(Integer, ForeignKey('person.person_id'))
    company_name = Column(String(100), nullable=False)
    tax_number = Column(String(20), unique=True, nullable=False)

    # Bi-directional Relationships
    address = relationship("Address", back_populates="companies", lazy="joined")
    contactperson = relationship("Person", back_populates="contacted_companies", lazy="joined")
    clients = relationship("Client", back_populates="company", lazy="joined")
    suppliers = relationship("Supplier", back_populates="company", lazy="joined")

    def __str__(self):
        return f"Company({self.company_name})"

    def __repr__(self):
        return f"<Company(id={self.company_id}, name='{self.company_name}', tax_number='{self.tax_number}')>"


# Client Model
class Client(Base):
    __tablename__ = 'client'

    client_id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey('company.company_id'))

    # Bi-directional Relationships
    company = relationship("Company", back_populates="clients", lazy="joined")
    projects = relationship("Project", back_populates="client", lazy="joined")

    def __str__(self):
        return f"Client(company={self.company})"

    def __repr__(self):
        return f"<Client(id={self.client_id}, company_id={self.company_id})>"


# Supplier Model
class Supplier(Base):
    __tablename__ = 'supplier'

    supplier_id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey('company.company_id'))

    # Bi-directional Relationships
    company = relationship("Company", back_populates="suppliers", lazy="joined")
    articles = relationship("Article", back_populates="supplier", lazy="joined")

    def __str__(self):
        return f"Supplier(company={self.company})"

    def __repr__(self):
        return f"<Supplier(id={self.supplier_id}, company_id={self.company_id})>"


# Article Model
class Article(Base):
    __tablename__ = 'article'

    article_id = Column(Integer, primary_key=True, autoincrement=True)
    supplier_id = Column(Integer, ForeignKey('supplier.supplier_id'))
    supplier_article_code = Column(String(40))
    purchase_price = Column(DECIMAL(10, 2))
    description = Column(String(100))

    # Bi-directional Relationships
    supplier = relationship("Supplier", back_populates="articles", lazy="joined")

    def __str__(self):
        return f"Article({self.supplier_article_code}, {self.purchase_price}, {self.description})"

    def __repr__(self):
        return f"<Article(id={self.article_id}, supplier_id={self.supplier_id}, description='{self.description}')>"


# Project Model
class Project(Base):
    __tablename__ = 'project'

    project_id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('client.client_id'))
    calculator_id = Column(Integer, ForeignKey('employee.employee_id'), nullable=False)
    salesman_id = Column(Integer, ForeignKey('employee.employee_id'))
    project_leader_id = Column(Integer, ForeignKey('employee.employee_id'))
    scheduling = Column(String(10))
    date_acceptance = Column(Date)
    date_start = Column(Date)
    date_end = Column(Date)

    # Bi-directional Relationships
    client = relationship("Client", back_populates="projects", lazy="joined")
    calculator = relationship("Employee", foreign_keys=[calculator_id], back_populates="calculated_projects", lazy="joined")
    salesman = relationship("Employee", foreign_keys=[salesman_id], back_populates="salesperson_projects", lazy="joined")
    project_leader = relationship("Employee", foreign_keys=[project_leader_id], back_populates="lead_projects", lazy="joined")
    phases = relationship("Phase", back_populates="project", lazy='noload')

    def __str__(self):
        return f"Project(scheduling={self.scheduling})"

    def __repr__(self):
        client_repr = f"{self.client}" if is_relationship_loaded(self, "client") else "Not Loaded"
        return f"<Project(id={self.project_id}, scheduling='{self.scheduling}', client={client_repr})>"


# Phase Model
class Phase(Base):
    __tablename__ = 'phase'

    phase_id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('project.project_id'))
    delivery_address_id = Column(Integer, ForeignKey('address.address_id'))
    name = Column(String(10))
    description = Column(String(100))

    # Bi-directional Relationships
    project = relationship("Project", back_populates="phases", lazy="joined")
    delivery_address = relationship("Address", back_populates="phases", lazy="joined")
    order_lines = relationship("OrderLine", back_populates="phase", lazy="joined")
    assignments = relationship("Assignment", back_populates="phase", lazy="joined")

    def __str__(self):
        return f"Phase(name={self.name}, description={self.description})"

    def __repr__(self):
        project_repr = f"{self.project}" if is_relationship_loaded(self, 'project') else "Not Loaded"
        return f"<Phase(id={self.phase_id}, name='{self.name}', project={project_repr})>"


# OrderLine Model
class OrderLine(Base):
    __tablename__ = 'orderline'

    orderline_id = Column(Integer, primary_key=True, autoincrement=True)
    phase_id = Column(Integer, ForeignKey('phase.phase_id'))
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

    # Bi-directional Relationships
    phase = relationship("Phase", back_populates="order_lines", lazy="joined")

    def __str__(self):
        return f"OrderLine(amount={self.amount}, sales_price={self.sales_price})"

    def __repr__(self):
        phase_repr = f"{self.phase}" if is_relationship_loaded(self, "phase") else "Not Loaded"
        return f"<OrderLine(id={self.orderline_id}, phase={phase_repr}, sales_price={self.sales_price})>"


# Assignment Model
class Assignment(Base):
    __tablename__ = 'assignment'

    assignment_id = Column(Integer, primary_key=True, autoincrement=True)
    phase_id = Column(Integer, ForeignKey('phase.phase_id'), nullable=False)
    worker_id = Column(Integer, ForeignKey('worker.worker_id'), nullable=False)
    date = Column(Date, nullable=False)
    description = Column(String(100))

    # Bi-directional Relationships
    phase = relationship("Phase", back_populates="assignments", lazy="joined")
    worker = relationship("Worker", back_populates="assignments", lazy="joined")

    def __str__(self):
        return f"Assignment(description={self.description}, date={self.date})"

    def __repr__(self):
        phase_repr = f"{self.phase}" if is_relationship_loaded(self, "phase") else "Not Loaded"
        worker_repr = f"{self.worker}" if is_relationship_loaded(self, "worker") else "Not Loaded"
        return f"<Assignment(id={self.assignment_id}, phase={phase_repr}, worker={worker_repr})>"

