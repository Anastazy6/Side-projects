import AlledrogoSearch, sys, csv, Alledrogo, os

sys.argv
#path = os.getcwd()

if len(sys.argv) > 1:
    szukaj = ' '.join(sys.argv[1:])
else:
    print("Podaj czego szukasz!")



def run():
    TMPpath = AlledrogoSearch.searchAlledrogo(szukaj)
    Alledrogo.main(TMPpath, True)
   # os.remove(TMPpath)

run()
