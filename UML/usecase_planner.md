## Case Transport
Voor de transportplanning heeft de planner nood aan een overzicht van hieronder vermelde `phases` met bijhorende status

### Overzicht
+ weer te geven phases / orderlines:
	+ die aanwezig zijn in het magazijn
		+ `date_received` niet gelijk is aan `null`
		+ `date_issued` gelijk is aan `null`

### Weergave
+ **Tabelvorm**:
	+ Naam van de klant
	+ Status
	+ Gemeente
	+ Regio (provincie, te berekenen uit postcode)
	+ Straat + huisnummer
	+ Bedrag van uitvoering
	+ Startdatum opgelegd door de klant (uit project)
	+ Einddatum opgelegd door de klant (uit project)
+ **Kaartvorm**:
	+ Alle projecten die volledig ontvangen zijn en dus nog kunnen uitgevoerd worden
	+ Radius van de markers volgens bedrag van uitvoering
	+ Kleur van de markers volgens status

## Case Opvolging Leveringen
Om de termijnplanning te kunnen aanhouden en verder te kunnen uitwerken tot een detailplanning, dienen leveringen van suppliers opgevolgd te worden. Op die manier kunnen onnodige vertragingen en laattijdige annulaties vermeden worden.

### Weergave
+ **Tabelvorm**:
	+ orderlines die voldoen aan elk van volgende voorwaarden:
		+ `date_ordered` niet op `null` (het item is reeds besteld)
		+ `date_received` wel op `null` (het item is nog niet ontvangen)
		+ `date_confirmed` ofwel:
			+ Op vandaag
			+ In het verleden
			+ Niet ingevuld is (indien er (nog) geen `confirmed_date` ingevuld is, wordt er uitgegaan van een levertermijn van zes weken)
	+ Extra kolommen in de tabel:
		+ Naam van de leverancier
		+ Verwachte leverdatum (berekend op basis van `confirmed_date` of standaard levertermijn van zes weken)
		+ Aantal bestelde items
		+ Totaalbedrag van de bestelling
		+ Status van de bestelling (bijvoorbeeld: "Besteld", "In afwachting van levering", "Vertraagd")

## Case Omzet Volgens Periode
De directie vraagt een overzicht van de omzet die gedraaid werd in een bepaalde periode en had graag een weergave van de locaties waar er gewerkt is.

### Weergave
+ **Tabelvorm**:
	+ Periode (start- en einddatum)
	+ Naam van de klant
	+ Projectnaam
	+ Locatie (gemeente, straat + nr)
	+ Omzetbedrag
	+ Status van het project (bijvoorbeeld: "Afgerond", "In uitvoering")
+ **Kaartvorm**:
	+ Heatmap:
		+ Intensiteit gebaseerd op omzetbedrag
		+ Locaties van projecten weergegeven op de kaart
	+ Markers:
		+ Kleur volgens status van het project
		+ Tooltip met details (klantnaam, projectnaam, omzetbedrag)
+ **Grafiekvorm** (optioneel):
	+ Omzet per maand binnen de geselecteerde periode
	+ Vergelijking van omzet per regio (bijvoorbeeld provincie)
	+ Totale omzet per klant binnen de geselecteerde periode

## Case Last-Minute
Een opdracht die ingepland stond wordt geannuleerd. De planner moet een overzicht krijgen van alle leveringen die momenteel in uitvoering zijn of in uitvoering kunnen gaan, zodat een mogelijk alternatief kan gezocht worden en de arbeiders aan het werk kunnen blijven

### Weergave
+ **Tabelvorm**:
	+ Naam van de klant
	+ fase- en projectnaam
	+ Locatie (gemeente, straat + nr)
	+ Status van de levering (bijvoorbeeld: "In uitvoering", "Gereed voor uitvoering")
	+ Verwachte leverdatum
	+ Bedrag van de levering
	+ Prioriteit (indien beschikbaar)
+ **Kaartvorm**:
	+ Markers:
		+ Kleur volgens status van de levering
		+ Tooltip met details (klantnaam, projectnaam, status, verwachte leverdatum)
		+ Radius van de markers volgens bedrag van de levering
		+ Mogelijkheid om te filteren op status of prioriteit
+ **Grafiekvorm** (optioneel):
	+ Overzicht van leveringen per status
	+ Aantal leveringen per regio
	+ Totale waarde van leveringen per status


## Case expences voorbije periode
cfr omzet volgens periode, maar dan met aankoopbedragen


## Case overzicht klanten
cfr case omzet volgens periode





<br><br><br><br><br>


# DRAFT

## Requirements for Operations
+ It must be possible to get a status overview of all orderlines, optionally grouped by phase.
	+ The overview must be displayed at 3 levels:
		+ project level
		+ phase level
		+ orderline level
	+ The overview must display the following details for the respective grouping (project/phase/orderline):
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