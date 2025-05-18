# Projectsamenvatting

Dit project maakt gebruik van een eenvoudige maar doeltreffende architectuur, gebaseerd op drie kerncomponenten:

## GUI
- **Shiny**: Lichtgewicht en modern Python-framework voor het bouwen van web-, desktop- en mobiele apps.
- **Folium**: Gebruikt voor interactieve geografische visualisaties (kaarten) op basis van Leaflet.js.
- Samen zorgen ze voor een intuïtieve, responsieve en visueel aantrekkelijke gebruikersinterface.

## Datalaag
- **SQLAlchemy**: Object-Relational Mapper (ORM) voor efficiënte en veilige interactie met de databank.
- Zorgt voor abstractie van SQL en maakt het werken met datamodellen eenvoudig en krachtig.

## Database
- **PostgreSQL**: Krachtig en betrouwbaar relationeel databasesysteem.
- Ideaal voor complexe datamodellen en schaalbare toepassingen.
- (Optioneel: uitbreidbaar met PostGIS voor georuimtelijke gegevens.)

---

# Technisch Overzicht

## Componentenoverzicht

| Component       | Technologie | Functie                                     |
|----------------|-------------|---------------------------------------------|
| GUI            | SHINY       | Gebruikersinterface                         |
| Kaartvisualisatie | Folium      | Interactieve kaarten (Leaflet.js)          |
| ORM / Datalaag | SQLAlchemy  | Abstractie van SQL, communicatie met DB     |
| Database       | PostgreSQL  | Opslag van gegevens, relationele structuur  |

## Dataflow

Gebruiker
   ↓
SHINY (GUI)
   ├──→ Folium (voor kaartvisualisatie)
   ↓
SQLAlchemy (ORM)
   ↓
PostgreSQL (Database)

## To start shiny
uvicorn src.gui.app:app --port 8081



```mermaid

classDiagram

	class Address {
		+ PK: address_id
		+ street
		+ house_number
		+ postal_code
		+ municipality
		+ country default BE
		+ longitude
		+ lattitude
		+ get_region(postal_code)
		+ get_longitude(street,house_number,postal_code, municipality)
		+ get_lattitude(street,house_number,postal_code, municipality)
		}
		Address "1"--"M" Phase
		Address "1"--"0-M" Company


	class Person {
		+ PK: person_id
		+ FK: address_id
		+ name_first
		+ name_last
		+ name_title
		+ job_description
		+ date_of_birth
		+ phone_number
		+ email
		}
		Person "1"<|--"0..1" Worker
		Person "1"<|--"0..1" Employee		

	class Employee {
		+ PK: employee_id
		+ FK: person_id
		}


	class Worker {
		+ PK: worker_id
		+ FK: person_id
		}
		Worker "1"--"0..M" Assignment



	class Company {
		+ PK: company_id
		+ FK: address_id
		+ FK: contact_person : person_id
		+ company_name
		+ tax-number
		}
		Company "1"<|--"0..1" Client
		Company "1"<|--"0..1" Supplier 
		Company "1"--"M" Person


	class Client {
		+ PK: client_id
		+ FK: company_id

		}
		Client "1"--"M" Project

	class Supplier {
		+ PK: supplier_id
		+ FK: company_id
		}
		Supplier "1"--"M" Article

	class Article {
		+ PK: article_id
		+ FK: supplier_id
		+ supplier_article_code
		+ purchase_price
		}
		Article "1"--"M" OrderLine

	class Project {
		+ PK: project_id
		+ FK: client_id
		+ FK: calculator_id
		+ FK: salesman_id
		+ FK: projectleader_id
		+ sheduling : asap or date
		+ date_acceptance
		+ date_start
		+ date_eind
		}
		Project "1"--"M" Phase
		Project "1"--"0..1" Employee : calculator
		Project "1"--"0..1" Employee : salesman
		Project "1"--"0..1" Employee : projectleader


	class Phase {
		+ PK: phase_id
		+ FK: project_id
		+ delivery_address_id : address_id
		+ sub_name
		+ sub_description		
		}
		Phase "1"--"M" OrderLine
		Phase "1"--"M" Assignment
		Phase "1"--"M" Person

	

	class OrderLine {
		+ PK: orderline_id
		+ FK: phase_id
    	+ FK: article_id   !!!      
    	+ sales_price
     	+ amount
    	+ date_acceptance 
		+ date_ordered      
		+ date_confirmed
		+ date_received     
		+ date_issued       
		+ date_delivered     
		+ date_installed    
		+ date_accepted       
		+ date_invoiced     
		+ date_paid         
		+ date_closed
		}


	class Assignment {
		+ PK: assignment_id
		+ FK: phase_id
		+ FK: worker_id
		+ date
		+ assignment_description
		}

```

# DRAFT

nog over te zetten in andere class
		
		+ get_sub_assignments() : list
		+ get_status(get_sub_assignments())
		+ get_status_date(get_sub_assignments())
		+ get_status(get_sub_assignments())
		+ get_status_date(get_sub_assignments())
		+ get_date_ordered(get_sub_assignments())
		+ get_date_received(get_sub_assignments())
		+ get_date_issued(get_sub_assignments())
		+ get_date_deliverd(get_sub_assignments())
		+ get_date_installed(get_sub_assignments())
		+ get_date_invoiced(get_sub_assignments())

		+ get_assignment_lines() : list
		+ get_status(get_assignment_lines())
		+ get_status_date(get_assignment_lines())
		+ get_date_ordered(get_assignment_lines())
		+ get_date_received(get_assignment_lines())
		+ get_date_issued(get_assignment_lines())
		+ get_date_delivered(get_assignment_lines())
		+ get_date_installed(get_assignment_lines())
		+ get_date_invoiced(get_assignment_lines())


		+ get_day_assignments(date)


		+ get_status_by_date()
		+ get_status_date()


	
		+ rejected_projects()
		+ get_open_projects()
		+ get_closed_projects()


		+ get_open_supplies()
		+ get_closed_supplies()


![packages_Kitch.png](packages_Kitch.png)

![classes_Kitch.png](classes_Kitch.png)