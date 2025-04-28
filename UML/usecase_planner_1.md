

## case 1: Transport combineren met lopende werf
een opdracht wordt gecancelled en de planner wil een overzicht van alle projecten die in uitvoering kunnen gaan. Het doel is om transport van een lopende werf te combineren met transport van een nog uit te leveren werf.

+ volgende subprojecten moeten weergegeven worden in een tabel en op kaart 
    + in tabel
        + gemeente
        + naam klant
        + bedrag
        + naam subproject
        + naam klant
        + bedrag van uitvoering
        + ... (verder te bekijken)
    + op kaart weer te geven:
        + alle projecten die nog lopende zijn
        + alle projecten die volledig ontvangen zijn en dus nog kunnen uitgevoerd worden.
        + radius van de markers volgens bedrag van uitvoering
        + kleur van de markers volgens status

## case 2: Op zoek naar werk

## case 3: Op zoek naar omzet
het einde van het kwartaal nadert en de cijfers zijn te laag. De planner heeft een overzicht nodig van de hoogste bedragen die kunnen uitgeleverd worden.

## case 4: Einde van het jaar
de directie vraag naar een overzicht van de omzet van het voorbije jaar (tabel), en hoe dit gespreid is over Belgie(heatmap)







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