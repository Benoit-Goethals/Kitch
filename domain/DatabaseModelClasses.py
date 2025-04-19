from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Enum, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Bedrijf Class
class Bedrijf(Base):
    __tablename__ = 'bedrijf'
    bedrijf_id = Column(Integer, primary_key=True)
    adres_id = Column(Integer, ForeignKey('adres.adres_id'))
    persoon_id = Column(Integer, ForeignKey('persoon.persoon_id'))
    btw_nummer = Column(String)

    adres = relationship("Adres", back_populates="bedrijven")
    contactpersoon = relationship("Persoon", foreign_keys=[persoon_id])
    klant = relationship("Klant", uselist=False, back_populates="bedrijf")
    leverancier = relationship("Leverancier", uselist=False, back_populates="bedrijf")


# Klant Class
class Klant(Base):
    __tablename__ = 'klant'
    klant_id = Column(Integer, primary_key=True)
    bedrijf_id = Column(Integer, ForeignKey('bedrijf.bedrijf_id'))

    bedrijf = relationship("Bedrijf", back_populates="klant")
    opdrachten = relationship("Opdracht", back_populates="klant")


# Adres Class
class Adres(Base):
    __tablename__ = 'adres'
    adres_id = Column(Integer, primary_key=True)
    straat = Column(String)
    huisnummer = Column(String)
    postcode = Column(String)
    gemeente = Column(String)

    bedrijven = relationship("Bedrijf", back_populates="adres")
    subopdrachten = relationship("Subopdracht", back_populates="adres")


# Opdracht Class
class Opdracht(Base):
    __tablename__ = 'opdracht'
    opdracht_id = Column(Integer, primary_key=True)
    calculator_id = Column(Integer, ForeignKey('persoon.persoon_id'))
    verkoper_id = Column(Integer, ForeignKey('persoon.persoon_id'))
    projectleider_id = Column(Integer, ForeignKey('persoon.persoon_id'))
    scheduling = Column(Enum('asap', 'datum'))
    datum_start = Column(Date)
    datum_eind = Column(Date)
    datum_aanvaarding = Column(Date)

    calculator = relationship("Persoon", foreign_keys=[calculator_id])
    verkoper = relationship("Persoon", foreign_keys=[verkoper_id])
    projectleider = relationship("Persoon", foreign_keys=[projectleider_id])
    subopdrachten = relationship("Subopdracht", back_populates="opdracht")
    dagopdrachten = relationship("Dagopdracht", back_populates="opdracht")


# Subopdracht Class
class Subopdracht(Base):
    __tablename__ = 'subopdracht'
    subopdracht_id = Column(Integer, primary_key=True)
    werfadres_id = Column(Integer, ForeignKey('adres.adres_id'))
    naam = Column(String)

    adres = relationship("Adres", back_populates="subopdrachten")
    opdracht = relationship("Opdracht", back_populates="subopdrachten")
    opdrachtlijnen = relationship("Opdrachtlijn", back_populates="subopdracht")


# Opdrachtlijn Class
class Opdrachtlijn(Base):
    __tablename__ = 'opdrachtlijn'
    opdrachtlijn_id = Column(Integer, primary_key=True)
    verkoopprijs = Column(Float)
    subopdracht_id = Column(Integer, ForeignKey('subopdracht.subopdracht_id'))
    artikel_id = Column(Integer, ForeignKey('artikel.artikel_id'))

    subopdracht = relationship("Subopdracht", back_populates="opdrachtlijnen")
    artikel = relationship("Artikel", back_populates="opdrachtlijnen")
    dagopdrachtlijnen = relationship("Dagopdrachtlijn", back_populates="opdrachtlijn")


# Artikel Class
class Artikel(Base):
    __tablename__ = 'artikel'
    artikel_id = Column(Integer, primary_key=True)
    leverancierscode = Column(String)
    leverancier_id = Column(Integer, ForeignKey('leverancier.leverancier_id'))
    aankoopprijs = Column(Float)

    leverancier = relationship("Leverancier", back_populates="artikelen")
    opdrachtlijnen = relationship("Opdrachtlijn", back_populates="artikel")


# Persoon Class
class Persoon(Base):
    __tablename__ = 'persoon'
    persoon_id = Column(Integer, primary_key=True)
    naam = Column(String)
    voornaam = Column(String)
    geboortedatum = Column(Date)
    functieomschrijving = Column(String)

    dagopdrachten = relationship("Dagopdracht", back_populates="persoon")


# Dagopdracht Class
class Dagopdracht(Base):
    __tablename__ = 'dagopdracht'
    dagopdracht_id = Column(Integer, primary_key=True)
    opdracht_id = Column(Integer, ForeignKey('opdracht.opdracht_id'))
    datum = Column(Date)
    omschrijving_opdracht = Column(String)

    opdracht = relationship("Opdracht", back_populates="dagopdrachten")
    dagopdrachtlijnen = relationship("Dagopdrachtlijn", back_populates="dagopdracht")


# Leverancier Class
class Leverancier(Base):
    __tablename__ = 'leverancier'
    leverancier_id = Column(Integer, primary_key=True)
    bedrijf_id = Column(Integer, ForeignKey('bedrijf.bedrijf_id'))

    bedrijf = relationship("Bedrijf", back_populates="leverancier")
    artikelen = relationship("Artikel", back_populates="leverancier")


# Dagopdrachtlijn Class
class Dagopdrachtlijn(Base):
    __tablename__ = 'dagopdrachtlijn'
    dagopdrachtlijn_id = Column(Integer, primary_key=True)
    opdrachtlijn_id = Column(Integer, ForeignKey('opdrachtlijn.opdrachtlijn_id'))
    persoon_id = Column(Integer, ForeignKey('persoon.persoon_id'))
    omschrijving_opdracht = Column(String)

    opdrachtlijn = relationship("Opdrachtlijn", back_populates="dagopdrachtlijnen")
    persoon = relationship("Persoon", back_populates="dagopdrachten")