from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
import markdown2, random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), "header": 'All Pages'
    })


def page(request, name):
    content = util.get_entry(name)
    if content is None:
        return redirect(error, args="No Article found")
    content = markdown2.markdown(content)
    return render(request, "encyclopedia/page.html", {
        "article": content, "title": name.upper()
    })


def editpage(request, name):
    content = util.get_entry(name)
#    #content = markdown2.markdown(content)
    return render(request, "encyclopedia/editpage.html", {
        "article": content, "title": name.upper()
    })


def newpage(request):
    return render(request, "encyclopedia/editpage.html", {
        "article": "", "title": None
    })


@ensure_csrf_cookie
def save(request, name):
    content = str(request.POST.get("content", ""))
    dummynewpage = False
    try:
        if eval(name) is None:
            name = str(request.POST.get("newpagetitle", ""))
            dummynewpage = True
    except (NameError, SyntaxError):
        name = name
    if name == "":
        return redirect(error, args="No name has been specified for the article")
    if dummynewpage is True and util.get_entry(name) is not None:
        return redirect(error, args="Article with defined name already exists")
    util.save_entry(name, content)
    return redirect(page, name=name)


def randompage(request):
    articleslist = [article for article in util.list_entries()]
    return redirect(page, name=articleslist[random.randint(0, len(articleslist)-1)])


@ensure_csrf_cookie
def searchwiki(request):
    name = request.POST.get("q", "")
    content = util.get_entry(name)
    if content is None:
        articleslist = [article for article in util.list_entries() if name.upper() in article.upper()]
        i = "Search Results" if len(articleslist) > 0 else "No Articles found"
        return render(request, "encyclopedia/index.html", {
            "entries": articleslist, "header": i})
    return redirect(page, name=name)


def error(request, args):
    return render(request, "encyclopedia/error.html", {
        "message": args
    })