# (c) 2015 Magnus "Tuxie" Johnsson, magnusjjj@gmail.com
# Licensed under the BSD license, see LICENSE.TXT in the root folder.
# Revision 1
# Changelog:
# 2015-04-14 - Magnus Johnsson - Added the license header

from django.shortcuts import render,redirect
from page.models import Page, PageFile
from django.http import HttpResponseForbidden, HttpResponse
from django.http import JsonResponse
import bleach

	
def handle_save(request, page_id=None, parent_override=None, stripsettings=None):
	page = None
	if page_id is not None:
		# Load the page
		page = Page.objects.get(pk=page_id)
	else:
		# Create a new page
		page = Page()
	
	parent = None
	# Put in the values..
	if parent_override is not None or request.POST["parent"] != "NULL":
		if parent_override is None:
			parent = Page.objects.get(pk=request.POST["parent"])
		else:
			parent = parent_override
	
	page.name = request.POST["name"]
	page.content = request.POST["content"]
	
	if stripsettings is not None:
		page.content = bleach.clean(request.POST["howto"], stripsettings.ALLOWED_TAGS, stripsettings.ALLOWED_ATTRIBUTES, stripsettings.ALLOWED_STYLES)
	
	page.parent = parent
	
	# Save. Bamilybamaram.
	page.save()
	
	# Handle possible uploads
	if 'fileupload' in request.FILES:
		file = PageFile()
		file.page = page
		file.file = request.FILES['fileupload']
		file.save()
		
	return page


# The view that renders a text page. Its a view that views a page ;D
def page(request, slug):
	return render(request, "page.html", {"page": Page.objects.get(slug=slug)})

# The view that, uhm, deletes a page
def page_delete(request, page_id):
	if not request.user.is_superuser:
		return HttpResponseForbidden("You don't have access to this :(")
	Page.objects.get(pk=page_id).delete()
	return redirect("index")

# The view that handles editing and saving pages
def edit_page(request, page_id):
	# This is our placeholder security check, to be replaced with a bit more granular settings
	if not request.user.is_superuser:
		return HttpResponseForbidden("You don't have access to this :(")
	
	# The list of pages that come up in the 'parent' dropdown
	parents = Page.objects.all()
	
	# Empty placeloader before save
	page = Page.objects.get(pk=page_id)
	
	# Fetch associated files
	files = PageFile.objects.filter(page=page)
	
	# When saving:
	if request.method == "POST":
		page = handle_save(request, page_id)
		
	# Render the editor
	return render(request, "edit.html", {"page": page, "parents": parents, "files": files})
	
def delete_pagefile(request, pagefile_id):
	if not request.user.is_superuser:
		return HttpResponseForbidden("You don't have access to this :(")
	PageFile.objects.get(pk=pagefile_id).delete()
	return JsonResponse({"id": pagefile_id})


# The view that renders an editor for a new page
def new_page(request):
	# This is our placeholder security check, to be replaced with a bit more granular settings
	if not request.user.is_superuser:
		return HttpResponseForbidden("You don't have access to this :(")
	
	# The list of pages that come up in the 'parent' dropdown
	parents = Page.objects.all()
	
	# Empty placeloader before save :)
	page = Page()
	
	# When saving:
	if request.method == "POST":
		page = handle_save(request)
		return redirect(page)

			
	return render(request, "edit.html", {"page": page, "parents": parents})
