#!/usr/bin/env python3
# (C) Vadelma Pii 2019. Licensed under GPLv3, with the exception that
# use of trivial parts as templates is explicitly allowed for any
# legal purpose.
#
# Displays command line argument on SenseHAT until interrupted. Clears 
# screen at exit.
# 
# (C) Vadelma Pii 2019. Lisenssi GPLv3, mutta triviaaleja osia saa
# käyttää mallina missä tahansa laillisessa tarkoituksessa.
# 
# Näyttää komentorivillä annetun tekstin SenseHATin näytöllä
# keskeytetään painamalla Ctrl-C. Tyhjentää näytön poistuttaessa.

import atexit, sys, getopt
from sense_hat import SenseHat
# Määritellään värejä. Käytetään Pythonin sanakirjarakennetta.
cd={
  "R":(255,0,0),
  "G":(0,255,0),
  "B":(0,0,255),
  "C":(0,255,255),
  "M":(255,0,255),
  "Y":(255,255,0),
  "K":(0,0,0),
  "W":(255,255,255),
}
# Opastusteksti, joka näytetään jos käyttäjä on hukassa.
usage = 'scroll.py -t <text> [-f <text_colour> [-b <bg_colour>]]'
try:
  sense=SenseHat()
except:
  # Tapahtui virhe. Olikos Sense HAT varmasti kunnolla paikallaan?
  print("Please check that your Sense HAT is properly installed.")
  sys.exit(2)

# Tällä funktiolla tyhjennetään näyttö.
def clearscreen():
  sense.clear(cd["K"])
  
# Rekisteröidään näytöntyhjennysfunktio suoritettavaksi poistuessa.
atexit.register(clearscreen)

# Määritellään main-funktio. Tätä ei yleensä Pythonissa tarvita, mutta se
# selkiyttää getoptin toimintaa: ensimmäinen argumentti eli ohjelman oma nimi
# siivotaan tässä pois kuljeksimasta.
def main(argv):
  # Asetetaan oletusarvot. Näytetään tyhjä teksti punaisilla merkeillä mustalla pohjalla.
  displayString = ''
  tc = "R"
  bc = "K"
  # getoptille annetaan kirjaimet, jotka hyväksytään. Jos kirjaimen perässä on kaksoispiste,
  # siihen liittyy lisäargumentti.
  # Jos optioiden käsittelyssä tapahtuu virhe, näytetään ohjeteksti ja poistutaan virhekoodin kera.
  # TODO: tulostetaan virheteksti standard erroriin.
  try:
    opts, args = getopt.getopt(argv, "ht:f:b:")
  except getopt.GetoptError:
    print(usage)
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print(usage)
      sys.exit(2)
    elif opt == '-t':
      displayString = arg
    elif opt == '-f':
      tc = arg
    elif opt == '-b':
      bc = arg

  # Päättymätön silmukka, katkeaa vasta kun ohjelma keskeytetään.
  while True:
    sense.show_message(displayString, text_colour=cd[tc], back_colour=cd[bc])

# Tässä siivotaan komentoriviargumenteista ensimmäinen eli ohjelman oma nimi
# ja käynnistetään main-funktio.
if __name__ == "__main__":
  main(sys.argv[1:])
