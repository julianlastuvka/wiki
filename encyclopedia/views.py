from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from random import randrange

from . import util

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content", widget=forms.Textarea)


def index(request):

    q = request.GET.get('q', '')
    if q:
        return HttpResponseRedirect(reverse('search', args=[q]))

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):

    q = request.GET.get('q', '')
    if q:
        return HttpResponseRedirect(reverse('search', args=[q]))

    entry = util.get_entry(title)

    if entry:
        entry = util.markdown(entry)
    else:
        return HttpResponseRedirect(reverse('not_found', args=[title]))

    return render(request, "encyclopedia/entry.html", {
        "entry": entry,
        "title": title
    })

def search(request, query):

    q = request.GET.get('q', '')
    if q:
        return HttpResponseRedirect(reverse('search', args=[q]))

    entries = util.list_entries()
    results = []

    if query in entries:
        return HttpResponseRedirect(reverse('entry', args=[query]))

    for entry in entries:
        if query in entry:
            results.append(entry)

    return render(request, "encyclopedia/results.html", {
        "results": results
    })


def create(request):

    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            if title in util.list_entries():
                return render(request, "encyclopedia/create.html", {
                    "form": NewPageForm(),
                    "error": f"{title} page already exist. Try with a different title."
                })
            else:
                util.save_entry(title, form.cleaned_data["content"])
                return HttpResponseRedirect(reverse('entry', args=[title]))
        else:
            return render(request, "encyclopedia/create.html", {
                    "form": NewPageForm(),
                    "error": form
                })

    q = request.GET.get('q', '')
    if q:
        return HttpResponseRedirect(reverse('search', args=[q]))

    return render(request, "encyclopedia/create.html", {
        "form": NewPageForm()
    })


def edit(request, title):

    q = request.GET.get('q', '')
    if q:
        return HttpResponseRedirect(reverse('search', args=[q]))
    
    if request.method == "POST":
        new_content = request.POST.get('new_content')
        util.save_entry(title, new_content)
        return HttpResponseRedirect(reverse('entry', args=[title]))

    # GET
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "old_content": util.get_entry(title)
    })


def random(request):

    titles = util.list_entries()
    title_index = randrange(0, len(titles))

    return HttpResponseRedirect(reverse('entry', args=[titles[title_index]]))


def not_found(request, title):

    q = request.GET.get('q', '')
    if q:
        return HttpResponseRedirect(reverse('search', args=[q]))

    return render(request, "encyclopedia/not_found.html", {
        "error": f"Error: There isn't a entry that matches '{title}'"
    })
