from datetime import datetime

import requests
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from .models import SavedEvents


def search(request):

    if request.POST.get('search'):
        classification_name = request.POST['classification_name']
        city = request.POST['city']
        sort = "date,asc"

        if not classification_name:
            messages.info(request, 'Search term cannot be empty. Please enter a search term.')
            return redirect('search-results')
        elif not city:
            messages.info(request, 'City cannot be empty. Please enter a city.')
            return redirect('search-results')

        search_results = get_ticketmaster_search(classification_name, city, sort)
        if search_results is None:
            messages.info(request, 'The server encountered an issue while fetching data. Please try again later.')
            return redirect('search-results')

        events_found = search_results['page']['totalElements']
        if events_found > 20:
            events_found = 20  # the ticketMasterAPI only allows 20 results per page by default

        if events_found == 0:
            messages.info(request, 'Sorry... no results were found for the entered search term and city.')
            return redirect('search-results')

        else:
            events = search_results['_embedded']['events']
            event_list = []
            for event in events:
                event_name = event['name']
                event_image = event['images'][0]['url']
                for image in event['images']:
                    if image['height'] == 1152:
                        event_image = image['url']

                #  Some events don't have a date, so return nothing if one of these events show up
                try:
                    event_date = event['dates']['start']['dateTime']
                    date_object = datetime.strptime(event_date[:10], "%Y-%m-%d")
                    event_date = date_object.strftime("%a %b %d %Y")
                except KeyError:
                    event_date = ""
                try:
                    event_time = event['dates']['start']['localTime']
                    event_time = event_time[:-4]
                    time_object = datetime.strptime(event_time, "%H:%M")
                    event_time = time_object.strftime("%I:%M %p")
                except KeyError:
                    event_time = ""

                venue = event['_embedded']['venues'][0]
                venue_name = venue['name']
                venue_city = venue['city']['name']
                venue_state = venue['state']['name']
                venue_address = venue['address']['line1']
                ticket_link = event['url']

                event_details = {
                    'event_name': event_name,
                    'event_image': event_image,
                    'event_date': event_date,
                    'event_time': event_time,
                    'venue_name': venue_name,
                    'venue_city': venue_city,
                    'venue_state': venue_state,
                    'venue_address': venue_address,
                    'ticket_link': ticket_link
                }
                event_list.append(event_details)

            print(event_list)
            form = SavedEventsForm(initial={
                'name': event_list[0],
                'image': "test",
                'date': event_list[3]
            })
            context = {'events': event_list, 'events_found': events_found, 'form': form}

            return render(request, 'search-results.html', context)

    return render(request, 'search-results.html')


def get_ticketmaster_search(classification_name, city, sort):
    try:
        url = "https://app.ticketmaster.com/discovery/v2/events.json?apikey=uR0EVsl1GNv6kaCf2DggXqQURjGEw1fe"
        params = {
            "classificationName": classification_name,
            "city": city,
            "sort": sort,
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    context = {'form': form}
    return render(request, 'landing.html', context)


def view_events(request):  # view saved events
    events = SavedEvents.objects.all()
    context = {'events': events}
    return render(request, 'saved-events.html', context)


def add_event(request):
    form = SavedEventsForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('view-events')
    return render(request, 'search-results.html', {'form': form})


def update_event(request, event_id):  # favorite events that are saved
    event = SavedEvents.objects.get(id=event_id)
    form = SavedEventsForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('view-events')
    return render(request, 'search-results.html', {'form': form})


def delete_event(request, event_id):  # delete events from saved database
    event = SavedEvents.objects.get(id=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('view-events')
    return render(request, 'saved-events.html')
