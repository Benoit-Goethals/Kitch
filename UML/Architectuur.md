# Projectsamenvatting

Dit project maakt gebruik van een eenvoudige maar doeltreffende architectuur, gebaseerd op drie kerncomponenten:

## GUI
- **Flet**: Lichtgewicht en modern Python-framework voor het bouwen van web-, desktop- en mobiele apps.
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

| Component       | Technologie  | Functie                                     |
|----------------|--------------|---------------------------------------------|
| GUI            | Flet         | Gebruikersinterface                         |
| Kaartvisualisatie | Folium     | Interactieve kaarten (Leaflet.js)          |
| ORM / Datalaag | SQLAlchemy   | Abstractie van SQL, communicatie met DB     |
| Database       | PostgreSQL   | Opslag van gegevens, relationele structuur  |

## Dataflow

```plaintext
Gebruiker
   ↓
Flet (GUI)
   ├──→ Folium (voor kaartvisualisatie)
   ↓
SQLAlchemy (ORM)
   ↓
PostgreSQL (Database)
