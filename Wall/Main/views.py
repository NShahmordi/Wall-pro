from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import Advertisement, Message, Room, AdvertisementImage, Category, Bookmark
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import string 
from django.http import JsonResponse
# Utility Functions
def generate_token(length=32):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Chat Management
@login_required
def chat_history(request):
    rooms = Room.objects.filter(user1=request.user) | Room.objects.filter(user2=request.user)
    return render(request, 'Chat/chat_history.html', {'rooms': rooms})

@login_required
def create_or_get_room(request, ad_slug):
    ad = get_object_or_404(Advertisement, slug=ad_slug)
    room, created = Room.objects.get_or_create(user1=request.user, user2=ad.owner)
    return redirect('room_detail', token=room.token)

@login_required
def room_detail(request, token):
    room = get_object_or_404(Room, token=token)
    
    if request.user != room.user1 and request.user != room.user2:
        return render(request, 'Error_codes/403.html', status=403)
    
    messages = Message.objects.filter(room=room).order_by('timestamp')
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.room = room
            message.sender = request.user
            message.save()
            return redirect('room_detail', token=token)
    else:
        form = MessageForm()
    return render(request, 'Chat/chatPage.html', {'room': room, 'form': form, 'messages': messages})

# Advertisement Management
def HomePage(request):
    products = Advertisement.objects.all()

    # Filtering by city
    city = request.GET.get('city')
    if city:
        products = products.filter(city__city_name__icontains=city)

    # Filtering by category
    category = request.GET.get('category')
    if category:
        products = products.filter(category__category_name__icontains=category)

    # Filtering by price range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price and max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)

    # Filtering by status
    status = request.GET.get('status')
    if status:
        products = products.filter(status=status)

    # Searching by title
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(title__icontains=search_query)

    for product in products:
        product.first_image = AdvertisementImage.objects.filter(advertisement=product).first()

    if request.user.is_authenticated:
        bookmarks = Bookmark.objects.filter(user=request.user)
        bookmarked_ads = [bookmark.advertisement for bookmark in bookmarks]
        suggested_ads = Advertisement.objects.filter(category__in=[ad.category for ad in bookmarked_ads]).exclude(id__in=[ad.id for ad in bookmarked_ads])
    else:
        suggested_ads = Advertisement.objects.none()

    context = {
        'Advertisments': products,
        'suggested_ads': suggested_ads,
    }

    return render(request, 'Market/product_list.html', context)


@login_required
def product_detail(request, slug):
    product = get_object_or_404(Advertisement, slug=slug)
    is_bookmarked = False
    if request.user.is_authenticated:
        is_bookmarked = product.bookmarks.filter(id=request.user.id).exists()
    ad_slug = product.slug
    image = AdvertisementImage.objects.filter(advertisement = product)
    context = {
        'advertisement': product,
        'is_bookmarked': is_bookmarked,
        'image' : image,
        'slug' : ad_slug
    }
    return render(request, 'Market/product_detail.html', context)

@login_required
def create_advertisement(request):
    if request.method == 'POST':
        advertisement_form = AdvertisementForm(request.POST)
        image_form = AdvertismentImageForm(request.POST, request.FILES)

        if advertisement_form.is_valid():
            advertisement = advertisement_form.save(commit=False)
            advertisement.owner = request.user
            advertisement.save()

            images = request.FILES.getlist('image')
            for image in images:
                AdvertisementImage.objects.create(advertisement=advertisement, image=image)

            return redirect('home')

    else:
        advertisement_form = AdvertisementForm()
        image_form = AdvertismentImageForm()

    categories = Category.objects.exclude(parent__isnull=True)

    return render(request, 'Market/create_ad.html', {
        'advertisement_form': advertisement_form,
        'image_form': image_form,
        'categories': categories
    })

@login_required
def edit_ad(request, slug, message=None):
    ad = get_object_or_404(Advertisement, slug=slug)
    ad_image = AdvertisementImage.objects.filter(advertisement=ad)

    if request.method == 'POST':
        form = AdvertisementForm(request.POST, request.FILES, instance=ad)

        if form.is_valid():
            try:
                advertisement = form.save()
                images = request.FILES.getlist('images')

                if images:
                    AdvertisementImage.objects.filter(advertisement=advertisement).delete()
                    for image in images:
                        AdvertisementImage.objects.create(advertisement=advertisement, image=image)
                elif not ad_image.exists():
                    raise ValueError("At least one image is required for the advertisement.")
                
                messages.success(request, 'Advertisement updated successfully.')
            except Exception as e:
                messages.error(request, f'There was an error updating the advertisement: {str(e)}')
            return redirect('edit_ad', slug=advertisement.slug)
        else:
            messages.error(request, 'There was an error updating the advertisement.')
    else:
        form = AdvertisementForm(instance=ad)

    context = {
        'form': form,
        'ad': ad,
        'categories': Category.objects.all(),
        'ad_image': ad_image
    }

    return render(request, 'Market/edit_ad.html', context)

@login_required
def delete_advertisement(request, slug):
    ad = get_object_or_404(Advertisement, slug=slug)
    if request.method == 'POST':
        try:
            ad.delete()
            messages.success(request, 'Advertisement deleted successfully.')
            return redirect('home')
        except Exception as e:
            messages.error(request, f'Error deleting advertisement: {str(e)}')
            return redirect('edit_ad', slug=slug)
    return render(request, 'Market/delete_ad.html', {'ad': ad})

@login_required
def delete_image(request, image_id):
    image = get_object_or_404(AdvertisementImage, id=image_id)
    ad = image.advertisement

    if request.method == 'POST':
        try:
            if ad.images.count() > 1:
                image.delete()
                return JsonResponse({'success': True})
            else:
                raise ValueError('At least one image is required for an advertisement.')
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)

# User Authentication
def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully.')
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'Main/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'Main/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')
#Error Handling
def custom_403(request, exception=None):
    return render(request, 'Error_codes/403.html', status=403)

def custom_404(request, exception=None):
    return render(request, 'Error_codes/404.html', status=404)

def custom_500(request):
    return render(request, 'Error_codes/500.html', status=500)

# Bookmark Management
@login_required
def add_bookmark(request, ad_id):
    advertisement = get_object_or_404(Advertisement, id=ad_id)
    Bookmark.objects.get_or_create(user=request.user, advertisement=advertisement)
    return redirect('product_detail', slug=advertisement.slug)

@login_required
def view_bookmarks(request):
    bookmarks = Bookmark.objects.filter(user=request.user)
    return render(request, 'Market/bookmarks.html', {'bookmarks': bookmarks})

@login_required
def toggle_bookmark(request, ad_id):
    advertisement = get_object_or_404(Advertisement, id=ad_id)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, advertisement=advertisement)
    if not created:
        bookmark.delete()
    return redirect('product_detail', slug=advertisement.slug)
