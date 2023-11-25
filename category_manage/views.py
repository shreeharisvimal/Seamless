from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect,get_object_or_404
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from .models import Category
from django.contrib import messages







@cache_control(no_cache=True, must_revalidate=True, max_age=0,no_store = True)
@login_required(login_url='authentication:login_handler')
def category_main(request):
    try:
        if request.user.is_authenticated and not request.user.is_superuser:
            return redirect('user_side:landing')       
    except:
        pass
    cat = Category.objects.all()
    context = {
        'categories': cat
    }
    print(cat)
    return render(request, 'admin/dashboard/category.html', context)





@cache_control(no_cache=True, must_revalidate=True, max_age=0,no_store = True)
@login_required(login_url='authentication:login_handler')
def add_category(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        return redirect('user_side:landing')
    if request.method == 'POST':
        name = request.POST.get('category_name')
        parent = None if request.POST.get('parent') == 'None' else Category.objects.get(category_name=request.POST.get('parent'))
        description = request.POST.get('description')
        images = request.FILES.get('imgs')
        print(name)
        print(parent)
        print(description)
        print(images)


        Category.objects.create(
            category_name=name,
            parent=parent,
            description=description,
            category_img=images
        )
        messages.success(request,'Category added successfully')
   
    print(Category.objects.get(category_name=name))

    return redirect('category_manage:category_handler')


@cache_control(no_cache=True, must_revalidate=True, max_age=0,no_store = True)
@login_required(login_url='authentication:login_handler')
def delete_category(request, slug):
    if request.user.is_authenticated and not request.user.is_superuser:
        return redirect('user_side:landing')
    try:
        category = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        messages.error(request, "Category does not exist.")
        return redirect('category_manage:category_list')
    category.delete()
    messages.error(request, "Category Deleted ❌")
    return redirect('category_manage:category_handler')


@cache_control(no_cache=True, must_revalidate=True, max_age=0,no_store = True)
@login_required(login_url='authentication:login_handler')
def edit_category(request, id):
    if request.user.is_authenticated and not request.user.is_superuser:
        return redirect('user_side:landing')
    
    cat = get_object_or_404(Category, id=id)

    if request.method == "POST":
        cat.category_name = request.POST.get('category_name')
        cat.description = request.POST.get('description')
        if request.FILES.get('imgs'):
            cat.category_img = request.FILES.get('imgs')

        try:
            cat.save()
            messages.success(request, f'The category {cat.category_name} has been updated successfully')
            return redirect('category_manage:category_handler')
        except Exception as e:
            messages.error(request, f'Error updating category: {str(e)}')
            # Handle the error as needed

    context = {'cat': cat}
    return render(request, 'admin/dashboard/category_edit.html', context)
        
@cache_control(no_cache=True, must_revalidate=True, max_age=0,no_store = True)
@login_required(login_url='authentication:login_handler')
def status_category(request, id):
    if request.user.is_authenticated and not request.user.is_superuser:
        return redirect('user_side:landing')
    if request.method == "POST":
        cat = get_object_or_404(Category, id=id)
        if cat.is_available == True:
            cat.is_available = False
            cat.save()
            messages.info(request,'The status has been changed to inactive successfully')
        else:
            cat.is_available =True
            cat.save()
            messages.info(request,'The status has been changed active successfully')
        return redirect('category_manage:category_handler')