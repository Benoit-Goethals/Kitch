
---
install this extension in vs-code to view the mermaid-diagram, or open it in obsidian

![mermaid-plugin for vscode](mermaid.png)

---

<br>
<br>
<br>

```mermaid
classDiagram


	class ApiCoords {
		+ get_coords_by_address(address)
	}

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
		Address "1"--"M" SubAssignment
		Address "1"--"0-M" Company
		Address -- ApiCoords


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
		+ get_day_assignments(date)
		}
		Person "1"--"0..M" DayAssignment


	class Company {
		+ PK: company_id
		+ FK: address_id
		+ FK: contact_person : person_id
		+ company_name
		+ tax-number
		}
		Company "1"<|--"1" Client
		Company "1"<|--"0..1" Supplier 
		Company "1"--"M" Person


	class Client {
		+ PK: client_id
		+ FK: company_id
		+ rejected_assignments()
		+ get_open_assignments()
		+ get_closed_assignments()
		}
		Client "1"--"M" Assignment

	class Supplier {
		+ PK: supplier_id
		+ FK: company_id
		+ get_open_supplies()
		+ get_closed_supplies()
		}
		Supplier "1"--"M" Article

	class Article {
		+ PK: article_id
		+ FK: supplier_id
		+ supplier_article_code
		+ purchase_price
		}
		Article "1"--"M" AssignmentLine

	class Assignment {
		+ PK: assignment_id
		+ FK: client_id
		+ FK: calculator : person_id
		+ FK: salesman : person_id
		+ FK: projectleader : person_id
		+ sheduling : asap or date
		+ date_acceptance
		+ date_start
		+ date_eind

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

		}
		Assignment "1"--"M" SubAssignment
		Assignment "1"--"M" Person


	class SubAssignment {
		+ PK: sub_assignment_id
		+ FK: assignment_id
		+ delivery_address_id : address_id
		+ sub_name
		+ sub_description

		+ get_assignment_lines() : list
		+ get_status(get_assignment_lines())
		+ get_status_date(get_assignment_lines())
		+ get_date_ordered(get_assignment_lines())
		+ get_date_received(get_assignment_lines())
		+ get_date_issued(get_assignment_lines())
		+ get_date_deliverd(get_assignment_lines())
		+ get_date_installed(get_assignment_lines())
		+ get_date_invoiced(get_assignment_lines())
		
		}
		SubAssignment "1"--"M" AssignmentLine
		SubAssignment "1"--"M" DayAssignment
	

	class AssignmentLine {
		+ PK: assignment_line_id
		+ FK: sub_assignment_id
    	+ FK: article_id   !!!      
    	+ sales_price
     	+ amount
    	+ date_acceptance 
		+ date_ordered      
		+ date_received     
		+ date_issued       
		+ date_delivered     
		+ date_installed    
		+ date_accepted       
		+ date_invoiced     
		+ date_paid         
		+ date_closed
		+ get_status_by_date()
		+ get_status_date()
		}


	class DayAssignment {
		+ PK: dayly_assignment_id
		+ FK: sub_assignment_id
		+ FK: person_id
		+ date
		+ assignment_description
		}







		









	















	












	

```

