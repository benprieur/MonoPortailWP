from flask import Flask, render_template, flash, request
import pywikibot
from pywikibot import pagegenerators

# source venv/bin/activate

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def entry():

    print("yolo")
    return render_template('form.html')


@app.route("/result", methods=['GET', 'POST'])
def result():

    if request.method == 'POST':

        catname = 'Catégorie:Portail:' + request.form['portal'] + '/Articles liés'

        wikisite = pywikibot.Site('fr', u'wikipedia')
        wikicat = pywikibot.Category(wikisite, catname)

        pages = pagegenerators.CategorizedPageGenerator(wikicat,recurse=False)

        listArticles = []

        for page in pages:

            title = page.title()
            print (title)

            # On recherche le contenu du modèle Portail
            paramscount = getTemplateContentCount('Portail', page)

            # Si le modèle n'a qu'un seul paramètre, on l'ajoute à la liste
            if paramscount == 1:

                    listArticles.append(title)
                    print("compteur : " + str(len(listArticles)))

        message = "Recherche récursive d'articles à un seul portail dans la Catégorie:" + catname + " : "
        message = message + str(len(listArticles)) + " article(s) concerné(s)"

        return render_template("result.html", message=message, articles=listArticles)



def getTemplateContentCount(templatename, page):

    pagetemplates = page.templatesWithParams()
    for (template, params) in pagetemplates:
        if template.title(with_ns=False) == templatename:
            return len(params)
    return 0


if __name__ == '__main__':
    app.run()