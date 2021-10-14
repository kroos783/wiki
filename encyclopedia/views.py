from django.http.response import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from random import randint
from django import forms
from . import util
from markdown2 import Markdown


class searchPage(forms.Form):
    title = forms.CharField(required=True, label="", widget=forms.TextInput(attrs={"placeholder": "Search encyclopedia"}))

class editPost(forms.Form):
    content = forms.CharField(required=True, label="Edit content ", widget=forms.Textarea())

class postNew(forms.Form):
    title = forms.CharField(required=True, label="Title", widget=forms.TextInput())
    content = forms.CharField(required=True, label="Content", widget=forms.Textarea())

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "formSearch": searchPage()
    })

def wiki(request, title):
    entries = util.list_entries()
    page = util.get_entry(title)
    if title.lower() not in entries:
        return render(request, "encyclopedia/error.html", {"title": "Error 404", "formSearch": searchPage(), "message": "Page not found", "codeError": "ERROR 404"})
    return render(request, "encyclopedia/wiki.html", {"title": title, "list_entries": entries,"content": Markdown().convert(page), "formSearch": searchPage()})

def search(request):
    if request.method == "POST":
        form = searchPage(request.POST)
        if form.is_valid():
            query = form.cleaned_data["title"].lower()
            search_md = util.list_entries()
            page = util.get_entry(query)
            print('search request: ', query)
            if query in search_md:
                context = {"formSearch": searchPage(), "title": query, "content": Markdown().convert(page), "message": "Page found"}
                return render(request, "encyclopedia/wiki.html", context)
            else:    
                if any(query in s for s in search_md):
                    matching = [s for s in search_md if query in s]
                    if len(matching) == 1:
                        title = matching[0]
                        page = util.get_entry(title)
                        return render(request, "encyclopedia/searchPage.html", {"query": query, "list_entries": search_md, "formSearch": searchPage(), "matching": matching})
                else:
                    return render(request, "encyclopedia/searchPage.html", {"query": query, "list_entries": search_md, "formSearch": searchPage(), 'messageNotFound': "messageNotFound"})
    else:
        return redirect(reverse('index'))

def new(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html", {"form": postNew(), "formSearch": searchPage()})
    form = postNew(request.POST)
    if form.is_valid():
        title = form.cleaned_data["title"]
        content = form.cleaned_data["content"]
        entries = util.list_entries()
        if title.lower() in entries:
            return render(request, "encyclopedia/new.html", {"form": form, "formSearch": searchPage(), "message": "Page already exist"})
        else:
            util.save_entry(title,content)
            page = util.get_entry(title)
            context = {"formSearch": searchPage(), "title": title, "content": Markdown().convert(page), "message": "New page created"}
            return render(request, "encyclopedia/wiki.html", context)
    else:
        return render(request, "encyclopedia/new.html", {"form": form, "formSearch": searchPage()})

def editPage(request, title):
    if request.method == "GET":
        content = util.get_entry(title)
        context = {'formSearch': searchPage(), 'form': editPost(initial={'content': content}), 'title': title}
        return render(request, "encyclopedia/editPage.html", context)
    form = editPost(request.POST)
    if form.is_valid():
        page = form.cleaned_data["content"]
        util.save_entry(title=title, content=page)
        context = {"formSearch": searchPage(), "title": title, "content": Markdown().convert(page), "message": "Page has been modified"}
        return render(request, "encyclopedia/wiki.html", context)

def randomPage(request):
    if request.method == 'GET':
        entries = util.list_entries()
        entryRandom = entries[randint(0, len(entries) - 1)]
        return redirect("wiki", entryRandom)

