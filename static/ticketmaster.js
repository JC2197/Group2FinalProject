const emptySearchTerm = $('#classification-empty');
const emptySearchCity = $('#city-empty');
const resultsContainer = $('#results-container');
const desiredImageHeight = 1152;

$('button').on('click',function () {

    emptySearchTerm.addClass("d-none");
    emptySearchCity.addClass("d-none");
    $('#results').empty();

    const classificationName = $('input[aria-label=classificationName]').val();
    const city = $('input[aria-label=city]').val();
    const sort = "date,asc";
    const apiKey = "uR0EVsl1GNv6kaCf2DggXqQURjGEw1fe";

    if (classificationName === "") {
        emptySearchTerm.removeClass("d-none");
        resultsContainer.addClass("d-none");
        return;
    }
    if (city === "") {
        emptySearchCity.removeClass("d-none");
        resultsContainer.addClass("d-none");
        return;
    }

    $.ajax({
        type: "GET",
        url: 'https://app.ticketmaster.com/discovery/v2/events.json?apikey=' + apiKey,
        async: true,
        dataType: "json",
        data: {'classificationName': classificationName, 'city': city, 'sort': sort},
        success: function (data) {
            resultsContainer.removeClass("d-none");
            let eventsFound = data.page.totalElements;
            if (eventsFound > 20) {eventsFound = 20}    // the ticketMasterAPI only allows 20 results per page by default
            if (eventsFound <= 0) {
                $('#results').append('<h4>Sorry... no results were found for the entered search term and city.</h4>');
            } else {
                $('#results').append('<h4 class="text-secondary">' + eventsFound + ' events found</h4>');
                $.each(data._embedded.events, function (i, event) {

                    const eventName = event.name;

                    let eventImage = event.images[0].url;
                    for (const image of event.images) {
                        if (image.height === desiredImageHeight) {
                            eventImage = image.url;
                            break;
                        }
                    }

                    let eventDate = event.dates.start.dateTime;
                    eventDate = new Date(eventDate).toDateString();

                    let eventTime = event.dates.start.localTime;
                    const eventTimeArray = eventTime.split(':');
                    const hours = eventTimeArray[0];
                    const minutes = eventTimeArray[1];
                    if (hours === 0 || hours === 24) {
                        eventTime = "12:" + minutes + " AM";
                    } else if (hours === 12) {
                        eventTime = "12:" + minutes + " PM";
                    } else if (hours > 12) {
                        eventTime = hours - 12 + ":" + minutes + " PM";
                    } else {
                        eventTime = hours + ":" + minutes + " AM";
                    }

                    const venue = event._embedded.venues[0];
                    const venueName = venue.name;
                    const venueCity = venue.city.name;
                    const venueState = venue.state.name;
                    const venueAddress = venue.address.line1;

                    const ticketLink = event.url;

                    $('#results').append('' +
                        '<div class="card mb-3 shadow">\n' +
                        '    <div class="row g-0">\n' +
                        '        <div class="col-md-4 d-flex align-items-center">\n' +
                        '            <img src="' + eventImage + '" class="card-img p-1" alt="event image">\n' +
                        '        </div>\n' +
                        '        <div class="col-md-8">\n' +
                        '            <div class="card-body">\n' +
                        '                <div class="row">\n' +
                        '                    <div class="col-6 d-flex align-items-center">\n' +
                        '                        <h4>' + eventName + '</h4>\n' +
                        '                    </div>\n' +
                        '                    <div class="col-6 text-success text-end">\n' +
                        '                        <h4>' + eventDate + '</h4>\n' +
                        '                        <h5>' + eventTime + '</h5>\n' +
                        '                    </div>\n' +
                        '                </div>\n' +
                        '                <h4 class="text-secondary">' + venueName + '</h4>\n' +
                        '                <p class="text-secondary mt-4">' + venueAddress + '<br>' + venueCity + ', ' + venueState + '</p>\n' +
                        '                <a href="' + ticketLink + '" class="btn btn-primary">Find tickets</a>\n' +
                        '            </div>\n' +
                        '        </div>\n' +
                        '    </div>\n' +
                        '</div>'
                    );
                });
            }
        },
    });
});