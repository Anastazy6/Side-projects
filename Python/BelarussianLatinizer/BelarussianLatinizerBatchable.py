def transcribe_string(cyrylic_string):  # for a quick transcription of just one line
    return transcribe(cyrylic_string)


def transcribe_file(cyrylic_text_file, justify=False):  # for more demanding customers
    original = open(cyrylic_text_file, "r", encoding="utf8")
    transcription = open("Latinized {}".format(cyrylic_text_file), "w", encoding="utf8")
    if justify:
        max_line_length = 0
        for line in original:
            current_line_latin = transcribe(line[0:-2])
            if len(current_line_latin) > max_line_length:
                max_line_length = len(current_line_latin)
        original.seek(0)
        for line in original:
            current_line_latin = transcribe(line)
            transcription.write(current_line_latin.center(max_line_length + 10, ' '))
    else:
        for line in original:
            current_line_latin = transcribe(line)
            transcription.write(current_line_latin)
    original.close()
    transcription.close()
    print("Latinized {} saved!".format(cyrylic_text_file))


def transcribe(cyrylic_string):  # MAIN

    def do_the_deed(char, key, caps):  # this will be used a lot later
        if caps:
            latin = key[char]  # Converts a cyrylic upper case char into a latin one according to a dictionary
        else:  # There are several rules of conversion, each needs to have its key declared
            char = char.upper()
            latin = key[
                char]  # This part works exactly the same way as the part above. Upper case cyrylic to upper case latin
            latin = latin.lower()  # Thus a lower case char is first upcased, then converted and finally downcased back.
        list_of_transcribed_chars.append(latin)

    cyrylic_vowels = {"а", "э", 'і', "о", "у", "ы", "я", "е", "ё", "ю",  # lowercase
                      'А', 'Э', 'І', 'О', 'У', 'Ы', 'Я', 'Е', 'Ё', 'Ю'}  # uppercase

    cyrylic_consonants = {"б", "в", "г", "д", "ж", "з", "й", "к", "л", "м", "н", "п", "р", "с", "т", "ў", "ф", "х", "ц",
                          "ч", "ш",  # lowercase
                          'Б', 'В', 'Г', 'Д', 'Ж', 'З', 'Й', 'К', 'Л', 'М', 'Н', 'П', 'Р', 'С', 'Т', 'Ў', 'Ф', 'Х', 'Ц',
                          'Ч', 'Ш'}  # uppercase

    cyrylic_specials = {"ь", "'"}

    transcribable = cyrylic_vowels | cyrylic_consonants

    list_of_chars = []
    for char in cyrylic_string:
        list_of_chars.append(char)

    id = 0
    list_of_transcribed_chars = []
    for char in list_of_chars:
        if char in cyrylic_specials:  # In case of soft sign or apostrophe, it just simply skips it while incrementing the id, which will be used later
            id += 1
            continue
        if char not in transcribable:  # Simply appends a non-cyrylic character as it is to the working list
            list_of_transcribed_chars.append(char)
            id += 1

        else:
            case = char.isupper()

            if char in cyrylic_vowels:
                if id == 0 or list_of_chars[id - 1] not in transcribable | cyrylic_specials or list_of_chars[
                        id - 1] in cyrylic_vowels:  # Vowels at the start of a word or after a vowel
                    action = {"А": "A", "Э": "E", "І": "I", "О": "O", "У": "U", "Ы": "", 'Я': "Ja", 'Е': "Je",
                              'Ё': "Jo", 'Ю': "Ju"}
                    do_the_deed(char, action, case)


                elif list_of_chars[id - 1] in {"Л", "л"}:  # Vowel after cyrylic L
                    action = {"А": "A", "Э": "E", "І": "I", "О": "O", "У": "U", "Ы": "Y", 'Я': "A", 'Е': "E", 'Ё': "O",
                              'Ю': "U"}
                    do_the_deed(char, action, case)

                elif list_of_chars[id - 1] in cyrylic_consonants:  # Vowel after cyrylic consonant
                    action = {"А": "A", "Э": "E", "І": "I", "О": "O", "У": "U", "Ы": "Y", 'Я': "Ia", 'Е': "Ie",
                              'Ё': "Io", 'Ю': "Iu"}
                    do_the_deed(char, action, case)

                elif list_of_chars[id - 1] in cyrylic_specials:  # Vowel after a soft sign or apostrophe.
                    action = {"А": "", "Э": "", "І": "Ji", "О": "", "У": "", "Ы": "", 'Я': "Ja", 'Е': "Je", 'Ё': "Jo",
                              'Ю': "Ju"}
                    do_the_deed(char, action, case)

            elif char in cyrylic_consonants:
                if (len(list_of_chars) > id + 2) and (
                        (list_of_chars[id + 1] in ['Д', "д"] and list_of_chars[id + 2] == "з") or (
                        list_of_chars[id + 1] in ['Н', "н"] and list_of_chars[id + 2] == "я")):
                    action = {'Б': "B", 'В': "V", 'Г': "H", 'Д': "", 'Ж': "", 'З': "Ź", 'Й': "J", 'К': "K", 'Л': "L",
                              'М': "M", 'Н': "Ń", 'П': "P",
                              'Р': "", 'С': "Ś", 'Т': "", 'Ў': "Ŭ", 'Ф': "F", 'Х': "Ch", 'Ц': "Ć", 'Ч': "", 'Ш': "Š"}
                    do_the_deed(char, action, case)
                #      Consonant before a special two-consonant cluster; There were some index-out-of-list errors without that (len(list_of_chars) > id + 2) part...

                elif (len(list_of_chars) > id + 1) and list_of_chars[id + 1] in {'ь', 'п', 'б', 'в', 'ф', 'м', 'с', 'з',
                                                                                 'ц', 'л', 'е', 'ё', 'ю', 'я', 'Ь', 'П',
                                                                                 'Б', 'В', 'Ф', 'М', 'С', 'З', 'Ц', 'Л',
                                                                                 'Е', 'Ё', 'Ю', "Я"}:
                    action = {'Б': "B", 'В': "V", 'Г': "H", 'Д': "D", 'Ж': "", 'З': "Ź", 'Й': "J", 'К': "K", 'Л': "L",
                              "М": "M", 'Н': "Ń", 'П': "P",
                              'Р': "", 'С': "Ś", 'Т': "", 'Ў': "Ŭ", 'Ф': "F", 'Х': "Ch", 'Ц': "Ć", 'Ч': "", 'Ш': "Š"}
                    do_the_deed(char, action, case)
                #        Consonant before a long, hard-coded list of chars... (len(list_of_chars) > id + 1) needed for the same reason as above

                else:
                    action = {'Б': "B", 'В': "V", 'Г': "H", 'Д': "D", 'Ж': "Ž", 'З': "Z", 'Й': "J", 'К': "K", 'Л': "Ł",
                              # Consonant in a normal case
                              'М': "M", 'Н': "N", 'П': "P",
                              'Р': "R", 'С': "S", 'Т': "T", 'Ў': "Ŭ", 'Ф': "F", 'Х': "Ch", 'Ц': "C", 'Ч': "Č", 'Ш': "Š"}
                    do_the_deed(char, action, case)

            id += 1  # Transcribed char is appended to the "results" list, so it's crucial not to forged about updating the id
            # which I've used to refer to a specific char in the cyrylic chars list, so as to process it properly in relation
            # with surrounding chars.

    result = "".join(list_of_transcribed_chars)
    return result

try:
    print(transcribe_string("Магутны Божа, ўладар сусьветаў,    \t\t\t #TEST STRING"), flush=True)  # test
   # transcribe_file("example3_BY.txt")  # file test,
except:
    "There's a test function call in the module and Python didn't know how to transcribe \n" \
    "the file, since its path doesn't specify any directory. The file is in the same directory \n" \
    "with the module. Ignore this message."


