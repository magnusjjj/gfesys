from django.shortcuts import render,redirect
from page.models import Page
from django.http import HttpResponseForbidden


# Create your views here.
def page(request, page_id):
	return render(request, "page.html", {"page": Page.objects.get(pk=page_id)})
	
def edit_page(request, page_id):
	if not request.user.is_superuser:
		return HttpResponseForbidden("You don't have access to this :(")
	
	parents = Page.objects.all()
	
	page = Page.objects.get(pk=page_id)
	if request.method == "POST":
		parent = None
		if request.POST["parent"] != "NULL":
			parent = Page.objects.get(pk=request.POST["parent"])
		page.name = request.POST["name"]
		page.content = request.POST["content"]
		page.parent = parent
		page.save()
	return render(request, "edit.html", {"page": page, "parents": parents})
	
def new_page(request):
	if not request.user.is_superuser:
		return HttpResponseForbidden("You don't have access to this :(")
	page = Page()
	
	parents = Page.objects.all()
	
	if request.method == "POST":
		parent = None
		if request.POST["parent"] != "NULL":
			parent = Page.objects.get(pk=request.POST["parent"])
		page = Page(name=request.POST["name"], content=request.POST["content"], parent=parent)
		page.save()
		return redirect(page)
	return render(request, "edit.html", {"page": page, "parents": parents})