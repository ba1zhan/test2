from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import CreateView, ListView
import math
from series.forms import CreateSeriesForm, SearchForm
from series.models import Category, Series



class SeriesListView(ListView):
    model = Series
    template_name = "series/series_list.html"
    context_object_name = "series"
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["forms"] = SearchForm()
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        category_id = self.request.GET.get("category_id")
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        tags = self.request.GET.getlist("tags")
        if tags:
            queryset = queryset.filter(tags__in=tags)
        return queryset
    

class SeriesCreateView(CreateView):
    model = Series
    template_name = "series/series_create.html"
    form_class = CreateSeriesForm
    success_url = "/series/"
    



@login_required(login_url="/login/")
def series_list(request):
    limit = 3
    if request.method == "GET":
        series = Series.objects.all()
        forms = SearchForm()
        if request.GET.get("search"):
            search = request.GET.get("search")

            series = Series.objects.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        category_id = request.GET.get("category_id")
        if category_id:
            series = Series.objects.filter(category_id=category_id)
        price_choice = request.GET.get("price_choice")
        if price_choice:
            if price_choice == "1":
                series = Series.objects.filter(price__gt=100)
            elif price_choice == "2":
                series = Series.objects.filter(price__lt=100)
        tags = request.GET.getlist("tags")
        if tags:
            series = Series.objects.filter(tags__in=tags)

        page = int(request.GET.get("page")) if request.GET.get("page") else 1
        max_page = math.ceil(len(series) / limit)
        start = (page - 1) * limit
        stop = page * limit
        list_pages = range(1, max_page + 1)
        series = series[start:stop]
        return render(
            request,
            "series/series_list.html",
            context={"series": series, "forms": forms, "list_pages": list_pages},
        )


@login_required(login_url="/login/")
def series_detail(request, series_id):
    if request.method == "GET":
        series = Series.objects.get(id=series_id)
        return render(
            request, "series/series_detail.html", context={"series": series}
        )




@login_required(login_url="/login/")
def series_create(request):

    if request.method == "GET":
        forms = CreateSeriesForm()
        return render(request, "series/series_create.html", context={"forms": forms})
    elif request.method == "POST":
        forms = CreateSeriesForm(request.POST, request.FILES)
        if forms.is_valid():
            Series.objects.create(
                profile=request.user.profile,
                name=forms.cleaned_data.get("name"),
                description=forms.cleaned_data.get("description"),
                image=forms.cleaned_data.get("image"),
            )
            return redirect("/series/")
        else:
            return render(request, "series/series_create.html", context={'forms': forms})
        
def base(request):
    return render(request, "base.html")

def delete_series(request, series_id):
    series = Series.objects.get(id=series_id)
    if request.user.profile != series.profile:
        return HttpResponse("Permission denied")
    series.delete()
    return redirect("/series/")

def base(request):
    if request.method == "GET":
        categories = Category.objects.all()
        return render(request, "base.html", context={"categories": categories})