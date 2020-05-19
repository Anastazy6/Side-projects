#! python3
import sys
import Alledrogo
import time

sys.argv

wykonaj = sys.argv[1]
if len(sys.argv) > 2:
    verboseFFS = True
else:
    verboseFFS = False

print("Pamiętaj: uruchamiając ten program podajesz co najmniej 2 argumenty: pierwszy to jego nazwa.")
print("Drugi to nazwa pliku z zapisanymi linkami obserwowanych rzeczy.")
print("Dalej możesz dodać cokolwiek. Wtedy otrzymasz wersję printującą w CMD wszystkie"
      "zdobyte dane.")
print("Czy uruchomiono wersję wodolejną: {}.\n".format("TAK" if verboseFFS else "NIE"))

startTime = time.time()
Alledrogo.main(wykonaj, verboseFFS)
endTime = time.time()
print("Wykonanie polecenia zajęło {} sekund.".format(round(endTime - startTime, 3)))