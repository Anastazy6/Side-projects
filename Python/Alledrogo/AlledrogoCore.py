import bs4, requests, re
from normalComma import normal_comma as kuwa
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def getAlledrogoPrice(productUrl, cout = False):
    try:
        res = requests.get(productUrl)
        res.raise_for_status()

        soup = str(bs4.BeautifulSoup(res.text, "html.parser"))

        productNameRegEx = re.compile(r'<title>(.+) (\d+) - Allegro.pl</title>')         # first is product name, second is ID
        sellerRegEx = re.compile(r'href="#aboutSeller">(.+)<!-- --> - (\d+,?\d*)%')
        priceRegEx = re.compile(r'(\d+\.?\d*)"\sitemprop="price"><meta\scontent="(\w+)')
        noDiscountRegEx = re.compile(r'("discount":null,"price":{"original")')
        discountRegEx = re.compile(r'discount":\{"percentage":(\d+\.?(\d+)?),"percentageLabel":"(\d+\.?(\d+)?)","total":\{"amount":"(\d+\.?(\d+)?)","currency":"(\w+)"},')

      #  if cout:
         #   print(soup)    # for testing and regEx writing purposes only

        prices = re.findall(priceRegEx, soup)[0]
        noCheap = re.findall(noDiscountRegEx, soup)
        productNameFull = re.findall(productNameRegEx, soup)[0]
        sellerFull = re.findall(sellerRegEx, soup)[0]

      #  print(productNameFull)
      #  print(sellerFull)
        #print(prices)

        productName = productNameFull[0]
        productID = productNameFull[1]

        sellerName = sellerFull[0]
        sellerOpinion = sellerFull[1]

        price = prices[0]
        currency = prices[1]

        if len(noCheap) == 0:
            isCheap = re.findall(discountRegEx, soup)[0]
           # print(isCheap)
            percentage = isCheap[2]
            rawDiscount = isCheap[4]
            fullPrice = float(price) + float(rawDiscount)
            if cout:
                print(
                    "{}, ID: {} \n\tod \"{}\" ({}% pozytywnych opinii)\n\tza {} {}.\n\tNormalna cena produktu wynosi {} {}, został "
                    "więc on przeceniony o {} {}, tj. {}%.\n\t".format(
                        productName, productID, sellerName, sellerOpinion, price, currency, kuwa(fullPrice), currency, rawDiscount,
                        currency, percentage))
        else:
            percentage = 0
            rawDiscount = 0
            fullPrice = price
            if cout:
                print("{}, ID: {} \n\tod {} ({}% pozytywnych opinii)\n\tza {} {}.\n\t".format(
                    productName,productID,sellerName,sellerOpinion,price,currency))
        return (productName, productID, sellerName, sellerOpinion, kuwa(price), currency, kuwa(fullPrice), kuwa(rawDiscount), percentage)

    except:
        logging.warning("Something went wrong. First of all, check if the following address exists:\n"
                        "{}\n".format(productUrl))
        return None


