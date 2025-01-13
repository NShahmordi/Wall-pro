from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .forms import *
from .models import Advertisement, Users, Message, Room, AdvertisementImage, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import secrets 
import string 
from django.http import HttpResponseForbidden, JsonResponse

def generate_token(length=32): 
    characters = string.ascii_letters + string.digits + string.punctuation 
    token = ''.join(secrets.choice(characters) for _ in range(length))
    return token
# Chat Management
@login_required
def chat_history(request):
    rooms = Room.objects.filter(user1=request.user) | Room.objects.filter(user2=request.user)
    return render(request, 'Chat/chat_history.html', {'rooms': rooms})

@login_required
def create_or_get_room(request, ad_slug):
    advertisment = Advertisement.objects.get(slug=ad_slug)
    user1 = request.user
    user2 = advertisment.owner
    
    # Check if a room already exists between the two users
    room = Room.objects.filter(user1=user1, user2=user2).first() or Room.objects.filter(user1=user2, user2=user1).first()
    
    if room:
        return redirect('room_detail', token=room.token)
    
    if user2 != user1:
        token = generate_token()
        room, created = Room.objects.get_or_create(user1=user1, user2=user2, token=token)
        return redirect('room_detail', token=token)

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
    recommendations = suggest_ads_template(request, context_key='home_recommendations', as_dict=True)

    for product in products:
        product.first_image = AdvertisementImage.objects.filter(advertisement=product).first()

    context = {
        'home_recommendations': recommendations,
        'Advertisments': products,
    }

    return render(request, 'Market/product_list.html', context)


def product_detail(request, slug):
    advertisement = get_object_or_404(Advertisement, slug=slug)
    ad_slug = advertisement.slug
    image = AdvertisementImage.objects.filter(advertisement = advertisement)

    recommendations = suggest_ads_template(request, context_key='product_recommendations', as_dict=True)

    context = {
        'advertisement': advertisement,
        'product_recommendations': recommendations,
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
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'User registered successfully.')
                return redirect('login')
            else:
                messages.error(request, 'There was an error with your registration.')
        else:
            form = CustomUserCreationForm()
        return render(request, 'Main/signup.html', {'form': form})
    else:
        return redirect('home')

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data["username"]
                upass = form.cleaned_data["password"]
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in successfully.')
                    return redirect('home')
                else:
                    messages.error(request, 'Invalid username or password.')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            form = LoginForm()
        return render(request, 'Main/login.html', {'form': form})
    else:
        return redirect('home')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/login/")

# Advertisement Suggestions
def suggest_ads_template(request, context_key='recommendations', as_dict=False):
    search_query = request.GET.get('search', '')
    category_name = request.GET.get('category', '')

    if search_query:
        ads = Advertisement.objects.filter(title__icontains=search_query)
        context = {context_key: ads}
        return render(request, 'ads_list.html', context)  # Changed template to 'ads_list.html'

    if not category_name:
        if as_dict:
            return []
        return render(request, 'no_preferences.html')

    try:
        category = Category.objects.get(name__iexact=category_name)
    except Category.DoesNotExist:
        if as_dict:
            return []
        return render(request, 'no_preferences.html')

    ads = Advertisement.objects.filter(category=category)
    print(f"Total ads found in category '{category_name}': {ads.count()}")

    ad_data = [f"{ad.title} {ad.description}" for ad in ads]
    ad_data.append(category_name)
    context = {context_key: ad_data}
    return render(request, 'ads_list.html', context)  # Changed template to 'ads_list.html'

#Error Handling
def custom_403(request, exception=None):
    return render(request, 'errors/403.html', status=403)

def custom_404(request, exception=None):
    return render(request, 'errors/404.html', status=404)

def custom_500(request):
    return render(request, 'errors/500.html', status=500)
