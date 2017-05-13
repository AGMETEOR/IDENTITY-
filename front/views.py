# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from haystack.query import SearchQuerySet
from .forms import SearchForm

    

def product_list(request, category_slug=None):
    category = None
    pagnate = True
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        pagnate=False
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, available=True)
        paginator = Paginator(products,4)
        page =request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            if request.is_ajax():
                return HttpResponse('')
            products = paginator.page(paginator.num_pages)
        if request.is_ajax():
            return render(request, 'front/list_ajax.html',{'category':category,'products':products})
    
        
        
    return render(request, 'front/list.html',{'pagnate':pagnate,'category':category, 'categories':categories,'products':products})




def product_detail(request, id, slug):
    categories = Category.objects.all()
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'front/detail.html',{'product':product,'cart_product_form':cart_product_form,'categories':categories})
    

def product_search(request):    
    form = SearchForm()
    if 'query' in request.GET:        
        form = SearchForm(request.GET)
        page = request.GET.get('page')
        if form.is_valid():
            
            cd = form.cleaned_data
            results = SearchQuerySet().models(Product).filter(content=cd['query']).load_all()
            paginator = Paginator(results,2)
            page = request.GET.get('page')
            try:
                prods = paginator.page(page)
            except PageNotAnInteger:
                prods = paginator.page(1)
            except:
                prods = paginator.page(paginator.num_pages)
            total_results = results.count()
        return render(request,'front/search.html',{'form': form,'cd': cd,'page':page,'prods': prods,'total_results': total_results})
    return render(request, 'front/search.html', {'form': form})





















































    


