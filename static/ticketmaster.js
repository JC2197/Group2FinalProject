$('button').click(function () {

    // Clear before adding in case the user clicks the button twice
    $('#card-container').empty();
    $('#warning').empty();
    // Get the search term and location from the input elements
    const searchTerm = $('input[name=param1]').val();
    const location = $('input[name=param2]').val();
    const API_KEY = 'quU5tiOXflAPKAoI2tFbvXXZ3SkwwhOR'

    if(searchTerm === '' || location ===''){
        if(searchTerm ===''){
            $('#warning').append(''+
            '   <div class="bg-danger-subtle border border-danger rounded p-2 m-1 text-danger fw-bold">'+
            '    Please enter a search term.'+
            '   </div>')
        }else{
            $('#warning').append(''+
            '   <div class="bg-danger-subtle border border-danger rounded p-2 m-1 text-danger fw-bold">'+
            '    City cannot be empty. Please enter a city.'+
            '   </div>')
        }
    } else{
        $.ajax({
        url:`https://app.ticketmaster.com/discovery/v2/events.json?size=20&sort=date,asc&keyword=${searchTerm}&city=${location}&apikey=${API_KEY}`,
        dataType: 'json',
        method: 'GET',
        success: function (data) {
            const totalResults = data.page.totalElements;
            if (totalResults > 0) {
                const events = data._embedded.events
                $('#card-container').append('' +
                    `    <h1 class="h3 text-secondary m-3 p-3">Total Results: ${totalResults}</h1>`)
                $.each(events, function (i) {

                    const item = events[i]
                    console.log(item)
                    const name = item.name
                    const image = item.images[0].url
                    const startDate = new Date(item.dates.start.dateTime).toDateString();
                    const startTime = convertTo12HourFormat(item.dates.start.localTime)
                    const venue = item._embedded.venues[0].name
                    const venueCity = item._embedded.venues[0].city.name
                    const venueState = item._embedded.venues[0].state.name
                    const link = item.url
                    const address = item._embedded.venues[0].address.line1
                    console.log(name)
                    console.log(image)
                    console.log(venue)
                    console.log(venueCity)
                    console.log(venueState)
                    console.log(link)

                    //Store each business's object in a variable
                    //Append our result into our page
                    $('#card-container').append('' +
                        '      <div class="shadow">\n' +
                        '            <div class="card mb-3">\n' +
                        '                        <div class="row">\n' +
                        '                            <div class="col-md-4 align-items-center">\n' +
                        `                                <img src="${image}" class="card-img rounded p-1" alt="business-image">\n` +
                        '                            </div>\n' +
                        '                            <div class="col-md-4 col-6 align-items-center ">\n' +
                        '                                <div class="card-body">\n' +
                        '                                    <div class="row">\n' +
                        '                                        <div>\n' +
                        `                                            <h4 class="card-title text-wrap">${name}</h4>\n` +
                        '                                        </div>\n' +
                        '                                    </div>\n' +
                        `                                    <h4 class="card-text text-muted">${venue}</h4>\n` +
                        `                                    <p class="card-text text-muted">${address}</p>\n` +
                        `                                    <p class="card-text text-muted">${venueCity}, ${venueState}</p>\n` +
                        `                                    <a href="${link}">\n` +
                        '                                       <button class="btn btn-primary">Find Tickets</button>\n' +
                        '                                    </a>\n' +
                        '                                </div>\n' +
                        '                            </div>\n' +
                        '                            <div class="col-md-4 col-6 p-3 ">\n' +
                        '                                    <div class="row">\n' +
                        `                                         <h2 style="text-align: right;" class="text-success">${startDate}</h2>\n` +
                        '                                    </div>\n' +
                        '                                    <div class="row d-flex">\n' +
                        `                                         <p style="text-align: right;" class=" text-success">${startTime}</p>\n` +
                        '                                    </div>\n' +
                        '                            </div>\n' +
                        '                        </div>\n' +
                        '                    </div');
                 });
            } else {
                $('#card-container').append('<h5>No results were found!</h5>');
            }
        }
    });
    }
});
function convertTo12HourFormat(time24Hour) {
  const [hours, minutes] = time24Hour.split(":");
  const parsedHours = parseInt(hours, 10);
  const parsedMinutes = parseInt(minutes, 10);
  const period = parsedHours >= 12 ? "PM" : "AM";
  const hours12Hour = parsedHours === 0 ? 12 : parsedHours > 12 ? parsedHours - 12 : parsedHours;
  const time12Hour = `${hours12Hour.toString().padStart(2, "0")}:${minutes.padStart(2, "0")} ${period}`;
  return time12Hour;
}
