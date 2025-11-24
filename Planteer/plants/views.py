from django.shortcuts import render, redirect
from .models import Benefit, Contact, Plant , Comment , Countries
from django.db.models import Q

def get_plant_or_none(plant_id):
    try:
        return Plant.objects.get(id=plant_id)
    except Plant.DoesNotExist:
        return None


def plant_list(request):
    plants = Plant.objects.all().order_by("-created_at")

    current_category = request.GET.get("category", "")
    current_edible = request.GET.get("is_edible", "")
    current_country = request.GET.get("country", "")

    if current_country: 
        plants = plants.filter(native_to__id=current_country)

    if current_category:
        plants = plants.filter(category=current_category)

    if current_edible == "yes":
        plants = plants.filter(is_edible=True)
    elif current_edible == "no":
        plants = plants.filter(is_edible=False)

    categories = Plant.objects.values_list("category", flat=True).distinct()
    countries = Countries.objects.all() 

    context = {
        "plants": plants,
        "categories": categories,
        "countries": countries, 
        "current_category": current_category,
        "current_edible": current_edible,
        "current_country": current_country,
    }
    return render(request, "plants/plant_list.html", context)


def plant_detail(request, plant_id):
    plant = get_plant_or_none(plant_id)
    if plant is None:
        return render(request, "plants/not_found.html", status=404)

    if request.method == "POST":
        name = request.POST.get("name")
        content = request.POST.get("content")

        if name and content:
            Comment.objects.create(
                plant=plant,
                name=name,
                content=content
            )
            return redirect("plants:plant_detail", plant_id=plant.id)

    related_plants = Plant.objects.filter(
        category=plant.category
    ).exclude(id=plant.id)[:3]

    comments = plant.comments.all().order_by('-created_at')

    context = {
        "plant": plant,
        "related_plants": related_plants,
        "native_to": getattr(plant, "native_to", "Not specified"),
        "is_edible": plant.is_edible,
        "used_for": plant.used_for,
        "comments": comments
    }

    return render(request, "plants/plant_detail.html", context)


def plant_create(request):
    all_benefits = Benefit.objects.all()
    all_countries = Countries.objects.all() 

    if request.method == "POST":
        new_plant = Plant.objects.create(
            name=request.POST.get("name"),
            about=request.POST.get("about"),
            used_for=request.POST.get("used_for"),
            category=request.POST.get("category"),
            is_edible=request.POST.get("is_edible") == "on",
            image=request.FILES.get("image")
        )

        selected_benefits = request.POST.getlist("benefits")
        new_plant.benefits.set(selected_benefits)
        
        new_benefit_name = request.POST.get("new_benefit_name")
        new_benefit_desc = request.POST.get("new_benefit_desc")
        
        if new_benefit_name:   
            benefit_obj = Benefit.objects.create(
                name=new_benefit_name, 
                description=new_benefit_desc or "" 
            )
            new_plant.benefits.add(benefit_obj)
        
        selected_countries = request.POST.getlist("native_to") 
        new_plant.native_to.set(selected_countries)    

        new_country_name = request.POST.get("new_country_name")
        new_country_flag = request.FILES.get("new_country_flag") 

        if new_country_name:
            country_obj, created = Countries.objects.get_or_create(name=new_country_name)
            
            if created and new_country_flag:
                country_obj.flag = new_country_flag
                country_obj.save()

            new_plant.native_to.add(country_obj)

        return redirect("plants:plant_list")

    context = {
        "benefits": all_benefits,
        "countries": all_countries
    }
    return render(request, "plants/plant_form.html", context)


def plant_update(request, plant_id):
    plant = get_plant_or_none(plant_id)
    if plant is None:
        return render(request, "plants/not_found.html")

    all_benefits = Benefit.objects.all()
    all_countries = Countries.objects.all() 

    if request.method == "POST":
        plant.name = request.POST.get("name")
        plant.about = request.POST.get("about")
        plant.used_for = request.POST.get("used_for")
        plant.category = request.POST.get("category")
        plant.is_edible = request.POST.get("is_edible") == "on"

        if request.FILES.get("image"):
            plant.image = request.FILES.get("image")

        plant.save()

        selected_benefits = request.POST.getlist("benefits")
        plant.benefits.set(selected_benefits)

        new_benefit_name = request.POST.get("new_benefit_name")
        new_benefit_desc = request.POST.get("new_benefit_desc")

        if new_benefit_name:
            benefit_obj = Benefit.objects.create(
                name=new_benefit_name, 
                description=new_benefit_desc or ""
            )
            plant.benefits.add(benefit_obj)

        selected_countries = request.POST.getlist("native_to")
        plant.native_to.set(selected_countries)

        new_country_name = request.POST.get("new_country_name")
        new_country_flag = request.FILES.get("new_country_flag") 

        if new_country_name:
            country_obj, created = Countries.objects.get_or_create(name=new_country_name)
            
            if created and new_country_flag:
                country_obj.flag = new_country_flag
                country_obj.save()

            plant.native_to.add(country_obj)

        return redirect("plants:plant_detail", plant_id=plant.id)

    context = {
        "plant": plant, 
        "benefits": all_benefits,
        "countries": all_countries
    }
    return render(request, "plants/plant_form.html", context)


def plant_delete(request, plant_id):
    plant = get_plant_or_none(plant_id)

    if plant is None:
        return render(request, "plants/not_found.html")

    plant.delete()
    return redirect("plants:plant_list")


def plant_search(request):
    query = request.GET.get("q", "").strip()

    plants = Plant.objects.all()
    if query:
        plants = plants.filter(
            Q(name__icontains=query) |
            Q(category__icontains=query) |
            Q(about__icontains=query) |
            Q(used_for__icontains=query)
        )

    context = {
        "plants": plants,
        "query": query,
    }
    
    return render(request, "plants/plant_search.html", context)


def contact_view(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        Contact.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            message=message,
        )
        return redirect("home:home_page")


    return render(request, "plants/contact.html")


def contact_messages_view(request):
    q = request.GET.get("q", "")

    messages_qs = Contact.objects.all().order_by("-created_at")
    if q:
        messages_qs = messages_qs.filter(
            Q(first_name__icontains=q)
            | Q(last_name__icontains=q)
            | Q(email__icontains=q)
            | Q(message__icontains=q)
        )

    context = {
        "messages_list": messages_qs,
        "query": q,
    }
    
    return render(request, "plants/contact_messages.html", context)


def plants_by_country(request, country_id):
    try:
        country = Countries.objects.get(id=country_id)
    except Countries.DoesNotExist:
        return render(request, "plants/not_found.html")

    plants = country.plants.all()
    
    context = {
        "country": country,
        "plants": plants
    }
    return render(request, "plants/plants_by_country.html", context)