

## case transport
In functie van de transportplanning heeft de planner nood aan een overzicht van alle opdrachten (sub-assignments) die "volledig aanwezig zijn in het magazijn"

overzicht:
+ alle subassignments waarbij:
	+ alle assignmentlines voldoen aan:
		+ date_received niet gelijk aan null
		+ date_issued gelijk aan nul

weergave: 
+ tabelvorm:
	+ naam van de klant
	+ benaming betreffende fase (sub_assignment)
	+ gemeente
	+ regio (provincie te berekenen uit postcode)
	+ straat + nr
	+ bedrag van uitvoering
	+ startdatum opgelegd door de klant
	+ einddatum opgelegd door de klant
+ kaartvorm:
	+ alle projecten waar nog gewerkt kan worden
	+ alle projecten die volledig ontvangen zijn en dus nog kunnen uitgevoerd worden.
	+ radius van de markers volgens bedrag van uitvoering
	+ kleur van de markers volgens status


## case opvolging leveringen
Om de termijnplanning te kunnen aanhouden en verder te kunnen uitwerken tot een detailplanning, dienen leveringen van suppliers opgevolgd te worden. Op die manier kunnen onnodige vertragingen en laattijdige annulaties vermden worden.
+ weergave:
	+ tabelvorm: 
		+ assignment_lines die voldoen aan elk van volgende voorwaarden:
			+ date_ordered niet op Null (het item is reeds besteld)
			+ date_received wel op Null staat (het item is nog niet ontvangen)
			+ date_confirmed ofwel
				+ op vandaag
				+ in het verleden
				+ niet ingevuld is (indien er (nog) geen confirmed_date ingevuld is, wordt er uitgegaan van een levertermijn van zes weken)
			
## case omzet volgens periode
De directie vraagt een overzicht van de omzet die gedraaid werd in een bepaalde periode en had graag een weergave van de locaties waar er gerwerkt is.
+ weergave:
	+ tabelvorm
	+ kaartvorm
		+ heatmap


## case last-minute
Een opdracht die ingepland stond wordt geanulleerd. De planner moet een overzicht krijgen van alle leveringen die momenteel in uitvoering zijn of in uitvoering kunnen gaan, zodat een mogelijk alternatief kan gezocht worden.
+ weergave:
	+ tabelvorm:
	+ kaartvorm:











<br><br><br><br><br>


# DRAFT

## Requirements for Operations
+ It must be possible to get a status overview of all assignment lines, optionally grouped by sub-assignment.
	+ The overview must be displayed at 3 levels:
		+ Assignment level
		+ Sub-assignment level
		+ Assignment-line level
	+ The overview must display the following details for the respective grouping (assignment/sub-assignment/assignment-line):
		+ The name of the grouping
		+ The status of the respective grouping
		+ The status date of the respective grouping
		+ The total purchase amount of the respective grouping
		+ The total sales amount of the respective grouping
		+ The location of the respective grouping
+ The planner must quickly obtain an overview on a map and in table format of all projects that:
	+ Regarding transport planning:
		+ Still need to be delivered to the customer and are fully received in the warehouse
	+ Regarding resource planning:
		+ An overview of all construction sites where something has been delivered but is not yet completed
## Requirements for financial followup
+ Financial responsible persons need to be able to view on charts
	+ amounts (cost and salesprice) that where delivered in per month
		

## Requirements for salesman
+ 