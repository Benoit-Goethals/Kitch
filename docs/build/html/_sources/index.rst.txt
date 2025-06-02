.. Welcome to Kitch's Documentation

Kitch documentation
===================

Overview
--------

Kitch is een bedrijf dat keukentoestellen plaatst en keukeninrichting doet.

**Wat het bedrijf niet doet:**
- Geen productie van toestellen of meubilair (toestellen worden gekocht via leveranciers).
- Binnenafwerkingen worden uitbesteed aan onderaannemers ("betegeling", "valse plafonds", e.d.).

**Wat het bedrijf wel doet:**
- Offertes maken voor inrichting van grootkeukens;
- Leveren en installeren van keukenmeubilair en toestellen;
- Uitbreken van keukentoestellen en inox-meubilair;
- Aansluiten van keukentoestellen en inox-meubilair.

---

Architectuur
------------

Kitch's structuur is gebaseerd op drie kerncomponenten:

**1. GUI:**
- **Shiny**: Een lichtgewicht framework voor het bouwen van web-, desktop-, en mobiele apps.
- **Folium**: Gebruikt voor het interactief genereren van geografische visualisaties (kaarten).

**2. Datalaag:**
- **SQLAlchemy**: Een ORM voor efficiënte en veilige database-interacties.

**3. Database:**
- **PostgreSQL**: Krachtig en betrouwbaar voor complexe datamodellen met optionele ondersteuning van PostGIS.

---

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: Modules Overview:

   modules