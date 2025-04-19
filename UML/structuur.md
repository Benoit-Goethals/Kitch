

```mermaid
classDiagram


	class Company {
		+ PK: company_id
		+ FK: address_id
		+ FK: person_id
		+ tax-number
		}
		Company "1"<|--"1" Client
		Company "1"<--"0..1" Supplier 
		Company "1"--"*" Person


	class Client {
		+ PK: client_id
		+ FK: company_id
		+ rejected_assignments()
		+ open_assignments()
		+ closed_assignments()
		}
		Client "1"--"*" Assignment


	class Address {
		+ PK: address_id
		+ street
		+ house_number
		+ postal_code
		+ municipality
		+ region(postal_code)
		}
		Address "1"--"*" SubAssignment
		Address "1"--"0-*" Company

	
	class Assignment {
		+ PK: assignment_id
		+ FK: client_id
		+ calculator : person
		+ salesman : persoon
		+ projectleader : persoon
		+ sheduling : asap or date
		+ date_start
		+ date_eind
		+ date_acceptance
		}
		Assignment "1"--"*" Subassignment
		Assignment "1"--"*" Person


	class SubAssignment {
		+ PK: sub_assignment_id
		+ FK: assignment_id
		+ delivery_address : address
		+ name
		+ description
		}
		Subassignment "1"--"*" AssignmentLine


	class AssignmentLine {
		+ PK: assignment_line_id
		+ FK: sub_assignment_id
		+ price_sales
		}
		AssignmentLine "*"--"1" Article
		AssignmentLine "1"--"1..*" DayAssignmentline


	class Article {
		+ PK: article_id
		+ FK: supplier_id
		+ supplier_article_code
		+ price_cost
		}


	class Person {
		+ PK: person_id
		+ FK: address_id
		+ name_first
		+ name_last
		+ date_of_birth
		+ job_description
		+ company
		}
		Person "1"--"0..*" DayAssignment


	class DayAssignment {
		+ PK: dagassignment_id
		+ FK: assignment_id
		+ datum
		+ omschrijving_assignment
		}
		Dagassignmentline "*"--"1" Person
		Dagassignment "1"--"1..*" Dagassignmentline
	

	class Supplier {
		+ PK: supplier_id
		+ FK: company_id
		+ open_supplies()
		+ closed_supplies()
		}
		Supplier "1"--"*" Article



	class DayAssignmentline {
		+ PK: dagassignmentline_id
		+ FK: assignmentline_id
		+ FK: persoon_id
		+ assignment_description
	}






	

```

