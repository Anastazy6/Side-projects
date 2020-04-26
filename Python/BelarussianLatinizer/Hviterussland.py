#! python3
import Uczytelniacz_białoruskiego as brus

swydd = input("Please type the entire path to the transcribable file\n>>>\t")
justify = input("Wanna have it justified? (Y/n)\n>>>\t")
if justify.upper() == 'Y':
    justify = True
else:
    justify = False

brus.transcribe_file(r'{}'.format(swydd), justify)
