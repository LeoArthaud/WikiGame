# -*-coding:Utf-8 -*
from bs4 import BeautifulSoup
import urllib.request
import Display


Display.affichageHeader()

#global
histo = []
coup=0
victoir = False
choice = 0
startUrl = urllib.request.urlopen('https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard').url
endUrl = urllib.request.urlopen('https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard').url


# Fonction qui tri tout les liens qui ne sont pas pertinant
# return une soupe avec le main content de la page
def filtreSoupAction(url):
    histo.append(url)
    with urllib.request.urlopen(url) as response:
        webpage = response.read()
        soup = BeautifulSoup(webpage, 'html.parser')
        for anchor in soup.find_all(True,{'class':
                                         ['infobox_v3',
                                          'infobox_v2',
                                          'mw-editsection',
                                          'noprint',
                                          'references-small',
                                          'reference',
                                          'extiw',
                                          'external text',
                                          'wd_identifiers',
                                          'bandeau-article',
                                          'incomplet']
                                     }):
            anchor.decompose()
        for anchor in soup.find_all(True,{'id':['toc']}):
            anchor.decompose()
        for anchor in soup.find_all('div',{'class':'mw-parser-output'}):
            filteredSoup = anchor
        return filteredSoup


# recupere une soup, trouve tout les liens et les mes dans une liste
# return la list
def getAllLinks(soup):
    linkList = []
    for anchor in soup.find_all('a'):
            if anchor.get_text():
                linkList.append(anchor.get_text())

    return linkList


# Return le titre de la page
def getPageTitle(url):
    with urllib.request.urlopen(url) as response:
        webpage = response.read()
        soup = BeautifulSoup(webpage, 'html.parser')
        for anchor in soup.find_all('h1', {"id": "firstHeading"}):
            pageTitle = anchor.get_text()

            return pageTitle


# gere l'affichage
def affichage(page, coup, choice):
    verif = len(histo)
    if(verif>1):
        print(str(coup)+' coup')
        print('00 - RETOUR')
    if choice==98:
        stop = len(page)
    elif len(page)>20:
        stop = 20
    else:
        stop = len(page)
    i = 1
    for link in range(0,stop):
        print(str(i)+' - '+page[link])
        i = i+1
    if stop == 20:
        print('98 - VOIR PLUS')
    print('99 - QUITTER')


def formatUrl(urlPiece):
    # charToReplace = ['é', 'è', ' ', 'à', 'ù', '?']
    # for char in charToReplace:
    #     urlPiece = urlPiece.replace(char, '')
    urlPiece= urlPiece.replace(' ', '_').replace('é', 'e').replace('è', 'e').replace('à', 'a').replace('ó', 'o').replace('ê', 'e')
    return urlPiece


def creatNewUrl(page,choice):
    if(choice == 00):
        newUrl = histo[-2]
    elif(choice == 98):
        newUrl = histo[-1]
    else:
        choice = choice -1
        urlPiece = page[choice]
        urlPiece = formatUrl(urlPiece)
        str(urlPiece)
        newUrl = 'https://fr.wikipedia.org/wiki/'+urlPiece
        str(newUrl)

    return newUrl


# prend en param la liste des lien 'page' et la reponse du joueur 'choice'
def redirect(newUrl):
    soup = filtreSoupAction(newUrl)
    newUrlLinks = getAllLinks(soup)

    return newUrlLinks


def affichageObjectif(startUrl, endUrl):
    nameStartPage = getPageTitle(startUrl)
    finalPage = getPageTitle(endUrl)
    Display.objectif(nameStartPage, finalPage)


def gameOver(newUrl,endUrl):
    if newUrl == endUrl:
        return True
    else:
        return False


def sauvegarde(coup,victoir):
    if victoir is not True:
        status = ' (Partie non teminée)'
    else:
        status = ' (Partie finit)'
    fichier = open("heighScore",'a')
    fichier.write('Pour allai de la page '+startUrl+' a la page '+endUrl+' , '+input('Votre nom/pseudo: ')+' as mis '+str(coup)+status+'\n')


soup = filtreSoupAction(startUrl)
page = getAllLinks(soup)
Display.chargement()
affichageObjectif(startUrl, endUrl)
affichage(page,coup,choice)
choice = int(input('aller au lien numero : '))


while(choice != 99 ):
    # choice = int(input('aller au lien numero : '))
    Display.chargement()
    newUrl = creatNewUrl(page,choice)
    victoir = gameOver(newUrl,endUrl)
    if victoir is False:
        if choice == 98:
            affichage(page, coup, choice)
        page = redirect(newUrl)
        if choice != 00:
            coup = coup+1
        Display.status(newUrl,endUrl)
        affichage(page,coup,choice)
        choice = int(input('aller au lien numero : '))
    else:
        choice = 99
        Display.bravo()
sauvegarde(coup,victoir)
Display.end()







