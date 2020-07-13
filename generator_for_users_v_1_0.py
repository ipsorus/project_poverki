from datetime import datetime, date, time, timedelta
import os
import errno

#Общее количество записей о поверках СИ
TOTAL_RESULTS = 6848

#Количество записей о поверках СИ в одной заявке (не более 5000 записей)
#Условие: Если общее количество записей не превышает 5000, то вписать значение из TOTAL_RESULTS
RESULTS_IN_APP = 5000

#Тип СИ (№ Гос. реестра)
mitypeNumber = f'77474-20'

#Модификация СИ
modification = f'модель Positherm ТС'

#Заводской номер СИ
start_zav_number = 341142 #Указывается начальное значение Заводского номера

manufactureNum_string = {'начало строки': 'B4488 ', 'изменяемая часть': start_zav_number, 'конец строки': ''}

#Дата производства СИ
manufactureYear = ''

#Номер свидетельства/извещения о непригодности СИ
start_applic_number = 242861 #Указывается начальное значение Номера свидетельства/извещения о непригодности СИ

certNum_string = {'начало строки': '207/C.202005.77474-20.0.B4488 ', 'изменяемая часть': start_applic_number, 'конец строки': '/2020'}

#Условный шифр знака поверки
signCipher = f'М'

#Папка, в которую будут сохранятся созданные заявки
folder = f'test'

#Дата поверки (формат гггг-мм-дд)
vrfDate = f'2020-05-08'

#Дата действия поверки (формат гггг-мм-дд), можно оставить пустое значение ''
validDate = f''

#Методика поверки
method = f'МП 207-034-2019 «Преобразователи термоэлектрические одноразового применения серии Positherm. Методика поверки»'

#Знак поверки в паспорте (true/false)
signPass = 'false'

#Знак поверки на СИ (true/false)
signMi = 'false'

#ГПЭ
npe_number = ''

#Эталоны
uve_number = '3.1.ZZM.0021.2012'

#Стандартные образцы
ses_number = ''             # Тип СО
ses_manufactureYear = ''    # Год производства
ses_manufactureNum = ''     # Заводской номер

#СИ, применяемые в качестве эталонов
mieta_number = ''

#СИ, применяемые при поверке
mis_number = ''             # Тип СИ (№ Гос. реестра)
mis_manufactureNum = ''     # Заводской номер

#Вещества (материалы)
reagent_number = ''


def applic_constructor(result, part):

    #Название файла
    name_of_file = r'заявка_' + mitypeNumber + '_часть_' + str(part) + '_записей_' + str(result) + '_шифр_' + signCipher + '.xml'

    #Путь сохранения файла
    FileFullPath = os.path.join(path_for_files, name_of_file)

    with open (FileFullPath, 'w', encoding='utf-8') as sample:

        header_1 = f'<?xml version="1.0" encoding="utf-8" ?>\n'
        header_2 = f'<gost:application xmlns:gost="urn://fgis-arshin.gost.ru/module-verifications/import/2020-04-14">\n'
        header = header_1 + header_2
        sample.write(header)

    for n in range(result):

        manufactureNum = manufactureNum_string['начало строки'] + str(manufactureNum_string['изменяемая часть']) + manufactureNum_string['конец строки']
        certNum = certNum_string['начало строки'] + str(certNum_string['изменяемая часть']) + certNum_string['конец строки']

        with open (FileFullPath, 'a', encoding='utf-8') as sample_body:

            result_start = f'<gost:result>\n'
            miInfo_start = f'<gost:miInfo>\n'
            singleMI_start = f'<gost:singleMI>\n'
            mitypeNumber_str = f'<gost:mitypeNumber>{mitypeNumber}</gost:mitypeNumber>\n'
            manufactureNum_str = f'<gost:manufactureNum>{manufactureNum}</gost:manufactureNum>\n'
            manufactureYear_str = f'<gost:manufactureYear>{manufactureYear}</gost:manufactureYear>\n'
            modification_str = f'<gost:modification>{modification}</gost:modification>\n'
            singleMI_close = f'</gost:singleMI>\n'
            miInfo_close = f'</gost:miInfo>\n'

            miInfo = miInfo_start + singleMI_start + mitypeNumber_str + manufactureNum_str + manufactureYear_str + modification_str + singleMI_close + miInfo_close

            signCipher_str = f'<gost:signCipher>{signCipher}</gost:signCipher>\n'
            vrfDate_str = f'<gost:vrfDate>{vrfDate}+03:00</gost:vrfDate>\n'
            validDate_str = f'<gost:validDate>{validDate}+03:00</gost:validDate>\n'

            valid = signCipher_str + vrfDate_str + validDate_str

            applicable_start = f'<gost:applicable>\n'
            certNum_str = f'<gost:certNum>{certNum}</gost:certNum>\n'
            signPass_str = f'<gost:signPass>{signPass}</gost:signPass>\n'
            signMi_str = f'<gost:signMi>{signMi}</gost:signMi>\n'
            applicable_close = f'</gost:applicable>\n'
            verification_res = applicable_start + certNum_str + signPass_str + signMi_str + applicable_close

            docTitle = f'<gost:docTitle>{method}</gost:docTitle>\n'

            means_start = f'<gost:means>\n'

            npe = ''
            uve = ''
            ses = ''
            mieta = ''
            mis = ''
            reagent = ''

            if npe_number != '':
                npe_start = f'<gost:npe>\n'
                npe_number_str = f'<gost:number>{npe_number}</gost:number>\n'
                npe_close = f'</gost:npe>\n'
                npe = npe_start + npe_number_str + npe_close

            if uve_number != '':
                uve_start = f'<gost:uve>\n'
                uve_number_str = f'<gost:number>{uve_number}</gost:number>\n'
                uve_close = f'</gost:uve>\n'
                uve = uve_start + uve_number_str + uve_close

            if ses_number != '':
                ses_start = f'<gost:ses>\n'
                se_start = f'<gost:se>\n'
                ses_number_str = f'<gost:typeNum>{ses_number}</gost:typeNum>\n'
                ses_manufactureYear_str = f'<gost:manufactureYear>{ses_manufactureYear}</gost:manufactureYear>\n'
                ses_manufactureNum_str = f'<gost:manufactureNum>{ses_manufactureNum}</gost:manufactureNum>\n'
                se_close = f'</gost:se>\n'
                ses_close = f'</gost:ses>\n'
                ses = ses_start + se_start + ses_number_str + ses_manufactureYear_str + ses_manufactureNum_str + se_close + ses_close

            if mieta_number != '':
                mieta_start = f'<gost:mieta>\n'
                mieta_number_str = f'<gost:number>{mieta_number}</gost:number>\n'
                mieta_close = f'</gost:mieta>\n'
                mieta = mieta_start + mieta_number_str + mieta_close

            if mis_number != '':
                mis_start =	f'<gost:mis>\n'
                mi_start = f'<gost:mi>\n'
                mis_number_str = f'<gost:typeNum>{mis_number}</gost:typeNum>\n'
                mis_manufactureNum_str = f'<gost:manufactureNum>{mis_manufactureNum}</gost:manufactureNum>\n'
                mi_close = f'</gost:mi>\n'
                mis_close =	f'</gost:mis>\n'
                mis = mis_start + mi_start + mis_number_str + mis_manufactureNum_str + mi_close + mis_close

            if reagent_number != '':
                reagent_start =	f'<gost:reagent>\n'
                reagent_number_str = f'<gost:number>{reagent_number}</gost:number>\n'
                reagent_close =	f'</gost:reagent>\n'
                reagent = reagent_start + reagent_number_str + reagent_close

            means_close = f'</gost:means>\n'
            result_close = f'</gost:result>\n'

            body = result_start + miInfo + valid + verification_res + docTitle + means_start + npe + uve + ses + mieta + mis + reagent + means_close + result_close
            sample_body.write(body)

        manufactureNum_string['изменяемая часть'] += 1
        certNum_string['изменяемая часть'] += 1

    with open (FileFullPath, 'a', encoding='utf-8') as sample:
        footer = f'</gost:application>\n'
        sample.write(footer)

    print('Формирование файла завершено!')

    return manufactureNum_string['изменяемая часть'], certNum_string['изменяемая часть']



if __name__ == "__main__":
    try:
        path_for_files = os.getcwd()
        path_for_files = os.getcwd() + '/' + folder + '/' + mitypeNumber
        os.makedirs(path_for_files)
    except OSError as e:
        print('Вы пытаетесь создать папку, которая уже существует.')
        print('Измените название папки, в строке "folder"')
        exit()


    parts = TOTAL_RESULTS // RESULTS_IN_APP

    for j in range(parts + 1):

        if TOTAL_RESULTS <= RESULTS_IN_APP:
            applic_constructor(TOTAL_RESULTS, j + 1)
        elif TOTAL_RESULTS > RESULTS_IN_APP:
            applic_constructor(RESULTS_IN_APP, j + 1)
            TOTAL_RESULTS -= RESULTS_IN_APP