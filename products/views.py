import uuid
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from .models import Product,ProductVariant,AttributeValue,VariantImage
from django.contrib import messages
from .forms import ProductForm,AttributeForm,AttributeValueForm
from django.db.models import Q
from django.shortcuts import get_object_or_404

# Create your views here.





@cache_control(no_cache=True, must_revalidate=True, max_age=0,no_store = True)
@login_required(login_url='authentication:login_handler')
def product_adding(request):
    if not request.user.is_authenticated:
        if not request.user.is_superuser:
            return redirect('admin_side:admin_login_handler')
        return redirect('user_side:landing')


    form = ProductForm()
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'the product added succesfully')
            return redirect('products:view_product')
    else:
        form = ProductForm()
    return render(request, 'admin/dashboard/product/add_product.html',{'form':form} )




@cache_control(no_cache=True, must_revalidate=True, max_age=0,no_store = True)
@login_required(login_url='authentication:login_handler')
def attribute(request):
    if not request.user.is_authenticated:
        if not request.user.is_superuser:
            return redirect('admin_side:admin_login_handler')
        return redirect('user_side:landing')
 

    form = AttributeForm()
    if request.method == "POST":
        form = AttributeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'the attribute added successfully')
            return redirect('products:add_attribute')
    else:
        form = AttributeForm()
    return render(request, 'admin/dashboard/product/attribute/product_attribute.html', {'form': form})



@cache_control(no_cache=True, must_revalidate=True, max_age=0,no_store = True)
@login_required(login_url='authentication:login_handler')
def attribute_value(request):
    if not request.user.is_authenticated:
        if not request.user.is_superuser:
            return redirect('admin_side:admin_login_handler')
        return redirect('user_side:landing')
    form = AttributeValueForm()
    if request.method =="POST":
        form = AttributeValueForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'the attribute value added succesfully')
            return redirect('products:add_attribute_value')
    else:
        form = AttributeValueForm()


    return render (request, 'admin/dashboard/product/product_values.html',{'form':form})



@cache_control(no_cache=True, must_revalidate=True, max_age=0,no_store = True)
@login_required(login_url='authentication:login_handler')
def product_variant(request):
    if not request.user.is_authenticated:
        if not request.user.is_superuser:
            return redirect('admin_side:admin_login_handler')
        return redirect('user_side:landing')
    try:
        if request.method == 'POST':
            max_price = request.POST['max_price']
            sale_price =  request.POST['sale_price']
            uu_order_id = int(uuid.uuid4().hex[:8],16)
            uu_order_id = f"#{uu_order_id}"
            model_id = uu_order_id
            stock = request.POST['stock']
            if '-' in str(max_price) or  '-' in str(sale_price) or  '-' in str(stock):
                messages.warning(request,'cant add negative values')
                return redirect('products:product_variant')
            if  str(max_price) == '0' or  str(sale_price)=='0' or  str(stock)=='0' :
                messages.warning(request,'cant add only 0 as values ')
                return redirect('products:product_variant')
            else:
                images = request.FILES.getlist('images')
                color = get_object_or_404(AttributeValue, id=request.POST['color'])
                ram =  get_object_or_404(AttributeValue, id=request.POST['ram'])
                storage = get_object_or_404(AttributeValue, id= request.POST['rom'])
                os = get_object_or_404(AttributeValue, id=request.POST['os'])
                screen_size = get_object_or_404(AttributeValue, id=request.POST['size'])
                print(color)
                print(os)
                print(storage)
                variant_new = ProductVariant.objects.create(
                    product = get_object_or_404(Product, id=request.POST['product']),
                    model_id = model_id,
                    color = color.Attribute_value,
                    ram =  ram.Attribute_value,
                    storage = storage.Attribute_value,
                    os = os.Attribute_value,
                    screen_size = screen_size.Attribute_value,
                    max_price = max_price,
                    sale_price = sale_price,
                    stock = stock,
                    description =  request.POST['description'],
                )
                variant_new.save()
                for image in images:
                    VariantImage.objects.create(variant = variant_new, images = image,)
                messages.success(request, f'the product variant has added succesfully')
                return redirect('products:product_variant')
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        messages.warning(request,f'{str(e)}')
        return redirect('products:product_variant')
    
    print(request.POST)
    product = Product.objects.filter(is_active = True)
    print(product)
    color = AttributeValue.objects.filter(Q(Attribute_id =4) & Q(is_active = True))
    ram = AttributeValue.objects.filter(Q(Attribute_id =1) & Q(is_active = True))
    storage = AttributeValue.objects.filter(Q(Attribute_id =2) & Q(is_active = True))
    os = AttributeValue.objects.filter(Q(Attribute_id =5) & Q(is_active = True))
    size = AttributeValue.objects.filter(Q(Attribute_id =3) & Q(is_active = True))

    context = {
        'product' : product,
        'color' : color,
        'ram' : ram,
        'storage' : storage,
        'os' : os,
        'size' : size,
            }

    return render(request, 'admin/dashboard/product/product_varient.html',context)


@cache_control(no_cache=True, must_revalidate=True, max_age=0,no_store = True)
@login_required(login_url='authentication:login_handler')
def view_attribute(request):
    if not request.user.is_authenticated:
        if not request.user.is_superuser:
            return redirect('admin_side:admin_login_handler')
        return redirect('user_side:landing')
    att = AttributeValue.objects.all()

    context = {
        'att' : att,
    }
    return render (request, 'admin/dashboard/product/attribute/attribute_view.html', context)



@cache_control(no_cache=True, must_revalidate=True, max_age=0,no_store = True)
@login_required(login_url='authentication:login_handler')
def attribute_status(request, id):
    if not request.user.is_authenticated:
        if not request.user.is_superuser:
            return redirect('admin_side:admin_login_handler')
        return redirect('user_side:landing')
    if request.method =="POST":
        att = AttributeValue.objects.get(id = id)
        if att.is_active == True:
            att.is_active=False
            att.save()
            messages.info(request, f'The Attribute {att.Attribute} - {att.Attribute_value}  has been set to inactive')
        else:
            att.is_active=True
            att.save()
            messages.info(request, f'The Attribute {att.Attribute} - {att.Attribute_value}  has been set to active')


    return redirect('products:view_att')



@cache_control(no_cache=True, must_revalidate=True, max_age=0,no_store = True)
@login_required(login_url='authentication:login_handler')
def attribute_delete(request, id):
    if not request.user.is_authenticated:
        if not request.user.is_superuser:
            return redirect('admin_side:admin_login_handler')
        return redirect('user_side:landing')
    att = AttributeValue.objects.get(id = id)
    att.delete()
    messages.info(request, 'The attibute has been deleted')
    return redirect('products:view_att')

# --------------------------------------------------------------------------------------


@cache_control(no_cache=True, must_revalidate=True, max_age=0,no_store = True)
@login_required(login_url='authentication:login_handler')
def view_variant(request):
    if not request.user.is_authenticated:
        if not request.user.is_superuser:
            return redirect('admin_side:admin_login_handler')
        return redirect('user_side:landing')

    variant = ProductVariant.objects.all()
    context = {
        'variant' : variant,
    }
    return render (request, 'admin/dashboard/product/variant_view.html', context)


@cache_control(no_cache=True, must_revalidate=True, max_age=0,no_store = True)
@login_required(login_url='authentication:login_handler')
def variant_status(request, id):
    if not request.user.is_authenticated:
        if not request.user.is_superuser:
            return redirect('admin_side:admin_login_handler')
        return redirect('user_side:landing')
    if request.method =="POST":
        var = ProductVariant.objects.get(id = id)
        if var.is_active == True:
            var.is_active = False
            messages.info(request,f"the product variant has been set to inactive { var.product}")
            var.save()
        else:
            var.is_active = True
            messages.info(request,f"the product variant has been set to active { var.product }")
            var.save()


    return redirect("products:view_variant")


@cache_control(no_cache=True, must_revalidate=True, max_age=0,no_store = True)
@login_required(login_url='authentication:login_handler')
def variant_delete(request,id):
    if not request.user.is_authenticated:
        if not request.user.is_superuser:
            return redirect('admin_side:admin_login_handler')
        return redirect('user_side:landing')
    var = ProductVariant.objects.get(id = id)
    var.delete()
    messages.info(request, "Product Variant Deleted Successfully!")
    return redirect("products:view_variant")


@cache_control(no_cache=True, must_revalidate=True, max_age=0,no_store = True)
@login_required(login_url='authentication:login_handler')
def variant_edit(request,id):
    if not request.user.is_authenticated:
        if not request.user.is_superuser:
            return redirect('admin_side:admin_login_handler')
        return redirect('user_side:landing')
    var = get_object_or_404(ProductVariant, id=id)

    if request.method =="POST":
        var.color = request.POST['color']
        var.ram = request.POST['ram']
        var.storage = request.POST['rom']
        var.screen_size = request.POST['size']
        var.max_price = request.POST['max_price']
        var.sale_price = request.POST['sale_price']
        var.stock = request.POST['stock']
        var.description = request.POST['description']
        try: 
            var.save()
            if  request.FILES.getlist('images'):
                new_images = request.FILES.getlist('images')
                for image in new_images:
                    VariantImage.objects.create(variant = var, images = image)
            
            messages.success(request, f'the product variant {var.product} has added succesfully')
            return redirect("products:view_variant")
        except:
            pass

    else:
        color = AttributeValue.objects.filter(Q(Attribute_id =4) & Q(is_active = True))
        ram = AttributeValue.objects.filter(Q(Attribute_id =1) & Q(is_active = True))
        storage = AttributeValue.objects.filter(Q(Attribute_id =2) & Q(is_active = True))
        size = AttributeValue.objects.filter(Q(Attribute_id =3) & Q(is_active = True))
        context = {
            'var': var,
            'color' : color,
            'ram' : ram,
            'storage' : storage,
            'size' : size,
        }
        return render (request, 'admin/dashboard/product/variant_edit.html', context)


# --------------------------------------------------------------------------------------


@cache_control(no_cache=True, must_revalidate=True, max_age=0,no_store = True)
@login_required(login_url='authentication:login_handler')
def view_product(request):
    if not request.user.is_authenticated:
        if not request.user.is_superuser:
            return redirect('admin_side:admin_login_handler')
        return redirect('user_side:landing')
    pro = Product.objects.all()
    context = {
        'pro' : pro,
    }
    return render (request, 'admin/dashboard/product/product_view.html', context)

@cache_control(no_cache=True, must_revalidate=True, max_age=0,no_store = True)
@login_required(login_url='authentication:login_handler')
def product_status(request, id):
    if not request.user.is_authenticated:
        if not request.user.is_superuser:
            return redirect('admin_side:admin_login_handler')
        return redirect('user_side:landing')
    pro = Product.objects.get(id =id)
    if pro.is_active == True:
        pro.is_active = False
        pro.save()
        messages.info(request,f"the product variant has been set to inactive {pro.product_name}")
    else:
        pro.is_active = True
        pro.save()
        messages.info(request,f"the product variant has been set to active {pro.product_name}")

    return redirect("products:view_product")



@cache_control(no_cache=True, must_revalidate=True, max_age=0,no_store = True)
@login_required(login_url='authentication:login_handler')
def product_edit(request, id):
    if not request.user.is_authenticated:
        if not request.user.is_superuser:
            return redirect('admin_side:admin_login_handler')
        return redirect('user_side:landing')
    pro = get_object_or_404(Product, id=id)
    if request.method=="POST":
        form = ProductForm( request.POST, request.FILES,instance=pro)
        if form.is_valid():
            form.save()
            messages.info(request, f'The product{pro.product_name} has been updated successfully')
            return redirect('products:view_product')
    else:
        form = ProductForm(instance = pro)

        context = {
            "form" : form,
            "pro" : pro
        }
    return render(request, 'admin/dashboard/product/product_edit.html', context )


@cache_control(no_cache=True, must_revalidate=True, max_age=0,no_store = True)
@login_required(login_url='authentication:login_handler')
def product_delete(request, id):
    if not request.user.is_authenticated:
        if not request.user.is_superuser:
            return redirect('admin_side:admin_login_handler')
        return redirect('user_side:landing')
    pro = Product.objects.get(id =id)
    pro.delete()
    messages.info(request,f"the product variant has been deleted {pro.product_name}")

    return redirect("products:view_product")



def variant_image_edit(request,id, var_id):
    image = get_object_or_404(VariantImage, id=id, variant = var_id)
    image.delete()
    messages.info(request,'the image has been deleted')
    return redirect('products:variant_edit', id=var_id)


def product_select_variant(request, id):
    variant = ProductVariant.objects.filter(product = id)
    context = {
        'variant':variant,
    }
    return render (request, 'admin/dashboard/product/variant_view.html', context)
