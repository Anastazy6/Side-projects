from AlledrogoCore import getAlledrogoPrice as opracuj
#opracuj returns (productName, productID, sellerName, sellerOpinion, price, currency, fullPrice, rawDiscount, percentage) - a tuple
import logging, csv, sys, os


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.DEBUG)

def main(filename, verbosexD = False):
    obserwowane = open(r"C:\Users\kamil\Desktop\Alledrogo\Obserwowane\{}.txt".format(filename), "r", encoding="utf8")
    result = open(r"C:\Users\kamil\Desktop\Alledrogo\Obserwowane\{}.csv".format(filename), "w", newline="", encoding="utf8")

    values = []
    for line in obserwowane:
        try:
            logging.debug('Starting work on a line')
            if line[-1] in ["\n", " ", "\r", "\t"]:
                temp = opracuj(line[:-1], verbosexD)
            else:
                temp = opracuj(line, verbosexD)
            if temp == None:
                continue
            appendMe = [";{};{};{};{};{};{};{};{};{};{};".format(temp[0],temp[1],temp[2],temp[3],temp[4],temp[5],
                                                                 temp[6],temp[7],temp[8],line[:-1])]
            values.append(appendMe)
            logging.debug('Line finished')

        except:
            logging.info("A line was skipped")
            continue

    with result:
        writer = csv.writer(result)
        result.write(";NAZWA;ID;SPRZEDAWCA;OPINIA;CENA;WALUTA;PEŁNA CENA; OBNIŻKA; PROCENT; LINK\n")
        writer.writerows(values)
    print("Zapisano do CSV.")
#main("Alledrogo")
