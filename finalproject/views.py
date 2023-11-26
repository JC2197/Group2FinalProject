from datetime import datetime

import requests
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import *


def search(request):
    if request.method == 'POST':
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
            # print the response for testing purpose (open "Run" at the bottom to see what is printed)
            print(search_results)
            # Store each user's information in a variable
            events = search_results['_embedded']['events']

            # Initialize an empty list to store user data
            event_list = []

            # Iterate through each user in the 'users' list coming from the api
            # Rather than directly passing the "users" array to the template,
            # the following approach allows server-side processing and formatting of specific data (e.g., date).
            # So, the template only needs to plug in the preprocessed information.
            for event in events:
                # Extract relevant information from the user dictionary
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

                # Create a new dictionary to store user details
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

                # Append the user details dictionary to the user_list
                event_list.append(event_details)

            # Create a context dictionary with the user_list and render the 'index.html' template
            context = {'events': event_list, 'events_found': events_found}
            return render(request, 'search-results.html', context)

    # all other cases, just render the page without sending/passing any context to the template
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

