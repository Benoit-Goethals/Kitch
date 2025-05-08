from sqlalchemy import Column, String, Integer, ForeignKey, Date, DECIMAL, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Address(Base):
    __tablename__ = 'address'
    address_id = Column(Integer, primary_key=True)
    street = Column(String(100), nullable=False)
    house_number = Column(String(10), nullable=False)
    postal_code = Column(String(4), nullable=False)
    municipality = Column(String(25), nullable=False)
    country = Column(String(50), default='BE')
    longitude = Column(DECIMAL(10, 8))
    latitude = Column(DECIMAL(10, 8))

    people = relationship('Person', back_populates='address', lazy='noload')
    companies = relationship('Company', back_populates='address', lazy='noload')
    phases = relationship('Phase', back_populates='delivery_address', lazy='noload')

    def __str__(self):
        return f'{self.street} {self.house_number}, {self.postal_code} {self.municipality}'
    def __repr__(self):
        return f'{self.street} {self.house_number}, {self.postal_code} {self.municipality}'


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

    address = relationship('Address', back_populates='people', lazy='joined')  # Retained eager loading if frequently accessed
    companies_as_contact = relationship('Company', back_populates='contact_person', foreign_keys='Company.contactperson_id')
    projects_as_calculator = relationship('Project', back_populates='calculator', foreign_keys='Project.calculator_id')
    projects_as_salesman = relationship('Project', back_populates='salesman', foreign_keys='Project.salesman_id')
    projects_as_leader = relationship('Project', back_populates='project_leader', foreign_keys='Project.project_leader_id')
    assignments = relationship('Assignment', back_populates='person')

    def __str__(self):
        return f'{self.name_first} {self.name_last}'

    def __repr__(self):
        return f'{self.name_first} {self.name_last}'

class Company(Base):
    __tablename__ = 'company'
    company_id = Column(Integer, primary_key=True)
    address_id = Column(Integer, ForeignKey('address.address_id'))
    contactperson_id = Column(Integer, ForeignKey('person.person_id'))
    company_name = Column(String(100), nullable=False)
    tax_number = Column(String(20), unique=True, nullable=False)

    address = relationship('Address', back_populates='companies', lazy='joined')
    contact_person = relationship('Person', back_populates='companies_as_contact', lazy='joined')
    client = relationship('Client', back_populates='company', uselist=False, lazy='joined')
    supplier = relationship('Supplier', back_populates='company', uselist=False, lazy='joined')


    def __str__(self):
        return f'{self.company_name}'
    def __repr__(self):
        return f'{self.company_name}'


class Client(Base):
    __tablename__ = 'client'
    client_id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('company.company_id'))

    company = relationship('Company', back_populates='client', lazy='joined')




class Supplier(Base):
    __tablename__ = 'supplier'
    supplier_id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('company.company_id'))

    company = relationship('Company', back_populates='supplier', lazy='joined')
    articles = relationship('Article', back_populates='supplier', lazy='joined')


class Article(Base):
    __tablename__ = 'article'
    article_id = Column(Integer, primary_key=True)
    supplier_id = Column(Integer, ForeignKey('supplier.supplier_id'))
    supplier_article_code = Column(String(40))
    purchase_price = Column(DECIMAL(10, 2))
    description = Column(String(100), nullable=True)

    supplier = relationship('Supplier', back_populates='articles', lazy='joined')
    orderlines = relationship('OrderLine', back_populates='article', lazy='joined')

    def __str__(self):
        return f'{self.supplier_article_code, self.purchase_price, self.description, self.supplier}'
    def __repr__(self):
        return f'{self.supplier_article_code, self.purchase_price, self.description, self.supplier}'



class Project(Base):
    __tablename__ = 'project'
    project_id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('person.person_id'))
    calculator_id = Column(Integer, ForeignKey('person.person_id'), nullable=False)
    salesman_id = Column(Integer, ForeignKey('person.person_id'))
    project_leader_id = Column(Integer, ForeignKey('person.person_id'))
    scheduling = Column(String(10))
    date_acceptance = Column(Date, nullable=False)
    date_start = Column(Date)
    date_end = Column(Date)

    client = relationship('Person', back_populates='projects_as_calculator', foreign_keys=[client_id], lazy='joined')
    calculator = relationship('Person', back_populates='projects_as_calculator', foreign_keys=[calculator_id], lazy='joined')
    salesman = relationship('Person', back_populates='projects_as_salesman', foreign_keys=[salesman_id], lazy='joined')
    project_leader = relationship('Person', back_populates='projects_as_leader', foreign_keys=[project_leader_id], lazy='joined')
    phases = relationship('Phase', back_populates='project', lazy='noload')

    def __str__(self):
        return f'{self.project_id, self.client, self.calculator, self.salesman, self.project_leader, self.scheduling, self.date_acceptance, self.date_start, self.date_end}'
    def __repr__(self):
        return f'{self.project_id, self.client, self.calculator, self.salesman, self.project_leader, self.scheduling, self.date_acceptance, self.date_start, self.date_end}'


class Phase(Base):
    __tablename__ = 'phase'
    phase_id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('project.project_id'))
    delivery_address_id = Column(Integer, ForeignKey('address.address_id'))
    name = Column(String(10))
    description = Column(String(100))

    project = relationship('Project', back_populates='phases', lazy='joined')
    delivery_address = relationship('Address', back_populates='phases', lazy='joined')
    orderlines = relationship('OrderLine', back_populates='phase', lazy='joined')
    assignments = relationship('Assignment', back_populates='phase', lazy='joined')

    def __str__(self):
        return f'{self.phase_id, self.project, self.delivery_address, self.name, self.description}'
    def __repr__(self):
        return f'{self.phase_id, self.project, self.delivery_address, self.name, self.description}'


class OrderLine(Base):
    __tablename__ = 'orderline'
    orderline_id = Column(Integer, primary_key=True)
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

    phase = relationship('Phase', back_populates='orderlines', lazy='joined')
    article = relationship('Article', back_populates='orderlines', lazy='joined')

    def __str__(self):
        return f'{self.orderline_id, self.phase, self.sales_price, self.amount, self.article, self.date_acceptance, self.date_ordered, self.date_received, self.date_issued, self.date_delivered, self.date_installed, self.date_accepted, self.date_invoiced, self.date_paid, self.date_closed}'
    def __repr__(self):
        return f'{self.orderline_id, self.phase, self.sales_price, self.amount, self.article, self.date_acceptance, self.date_ordered, self.date_received, self.date_issued, self.date_delivered, self.date_installed, self.date_accepted, self.date_invoiced, self.date_paid, self.date_closed}'



class Assignment(Base):
    __tablename__ = 'assignment'
    assignment_id = Column(Integer, primary_key=True)
    phase_id = Column(Integer, ForeignKey('phase.phase_id'))
    person_id = Column(Integer, ForeignKey('person.person_id'))
    date = Column(Date)
    description = Column(String(100))

    phase = relationship('Phase', back_populates='assignments', lazy='joined')
    person = relationship('Person', back_populates='assignments', lazy='joined')

    def __str__(self):
        return f'{self.assignment_id, self.phase, self.person, self.date, self.assignment_description}'
    def __repr__(self):
        return f'{self.assignment_id, self.phase, self.person, self.date, self.assignment_description}'