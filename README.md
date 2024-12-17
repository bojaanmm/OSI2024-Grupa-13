# OSIprojekat
--------------------------------------------------------------
Kada pocinjete sa radom prvo pullajte projekat pa onda radite.
Ako bude nekih smetnji pri pusanju ostavite tako.
--------------------------------------------------------------
Sistem za naplatu parkinga
--------------------------------------------------------------
Implementirati jednostavan sistem za naplatu parkinga. Sistem se sastoji od 3 odvojena
programa i koriste ga različite grupe korisnika:

a)Program koji kontroliše ulaz i izlaz vozila
  Prilikom ulaska na parking ovaj program očitava tablice vozila. Ovo se za potrebe
  projektnog zadatka može simulirati običnim unosom broja registarskih tablica u
  program. Prilikom ulaska vozila na parking očitava se vrijeme na osnovu kojeg se
  računa cijena parkiranja. Korisnik parkinga dobija karticu (tekstualni fajl) u kojem se
  nalazi jedinstveni identifikator koji se koristi za obračun cijene parkiranja, kao i ostali
  bitni podaci. Osim ulaska, ovaj program kontroliše da li vozilo može napustiti parking
  ili ne. Napuštanje parkinga dozvoljeno je samo nakon n sekundi/minuta od plaćanja
  parkinga.
  
b)Program za plaćanje parkinga
  Na osnovu kreiranog tekstualnog fajla, računa se trajanje parkiranja i obračun iznosa
  za plaćanje. Potrebno je podržati različite cijene u zavisnosti od zone gdje se parking
  nalazi, dana (radni dan, vikend, praznik). Za plaćanje se može koristiti gotovina ili
  kartica, a naplatu simulirati samo unosom podataka bez dodatne obrade. Nakon
  plaćanja korisnik dobija karticu u tekstualnom fajlu koja se koristi prilikom
  odobravanja izlaska sa parkingac).
  
c)Program za upravljanje parkingom
  Ovaj program koriste operateri i uprava. Uprava može dobiti izvještaje o radu
  parkinga: dnevni, sedmični i mjesečni, gdje se prikazuju podaci o poslovanju. Važno
  je prikazati broj korisnika i zaradu. Uprava takođe definiše cjenovnik. Operateri mogu
  dobiti prikaz svih trenutno parkiranih vozila na parkingu (spisak i ukupan broj),
  provjeriti ko je platio parking i rješavati konfliktne situacije (žalbe na račune, probleme
  sa ulaskom ili izlaskom). Žalbe podnose korisnici u programu za plaćanje parkinga
  (unos teksta), a svaka žalba ima status aktivna i riješena.
  Sve navedene opcije je potrebno dodatno analizirati, precizno definisati i po potrebi proširiti..
  
--------------------------------------------------------------
