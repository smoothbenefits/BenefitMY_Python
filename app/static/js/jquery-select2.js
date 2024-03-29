
function movieFormatResult(movie) {
    var markup = "<table class='movie-result'><tr>";
    if (movie.posters !== undefined && movie.posters.thumbnail !== undefined) {
        markup += "<td class='movie-image' style='vertical-align: top'><img src='" + movie.posters.thumbnail + "' style='max-width: 60px; display: inline-block; margin-right: 10px; margin-left: 10px;' /></td>";
    }
    markup += "<td class='movie-info'><div class='movie-title' style='font-weight: 600; color: #000; margin-bottom: 6px;'>" + movie.title + "</div>";
    if (movie.critics_consensus !== undefined) {
        markup += "<div class='movie-synopsis'>" + movie.critics_consensus + "</div>";
    }
    else if (movie.synopsis !== undefined) {
        markup += "<div class='movie-synopsis'>" + movie.synopsis + "</div>";
    }
    markup += "</td></tr></table>";
    return markup;
}

function movieFormatSelection(movie) {
    return movie.title;
}

init.push(function () {
    // Single select
    $("#jquery-select2-example").select2({
        allowClear: true,
        placeholder: "Select a State"
    });

    // Multiselect
    $("#jquery-select2-multiple").select2({
        placeholder: "Select a State"
    });

    // External source
    $("#jquery-select2-external").select2({
        placeholder: "Search for a movie",
        minimumInputLength: 1,
        ajax: { // instead of writing the function to execute the request we use Select2's convenient helper
            url: "http://api.rottentomatoes.com/api/public/v1.0/movies.json",
            dataType: 'jsonp',
            data: function (term, page) {
                return {
                    q: term, // search term
                    page_limit: 10,
                    apikey: "ju6z9mjyajq2djue3gbvv26t" // please do not use so this example keeps working
                };
            },
            results: function (data, page) { // parse the results into the format expected by Select2.
                // since we are using custom formatting functions we do not need to alter remote JSON data
                return {results: data.movies};
            }
        },
        initSelection: function(element, callback) {
            // the input tag has a value attribute preloaded that points to a preselected movie's id
            // this function resolves that id attribute to an object that select2 can render
            // using its formatResult renderer - that way the movie name is shown preselected
            var id=$(element).val();
            if (id!=="") {
                $.ajax("http://api.rottentomatoes.com/api/public/v1.0/movies/"+id+".json", {
                    data: {
                        apikey: "ju6z9mjyajq2djue3gbvv26t"
                    },
                    dataType: "jsonp"
                }).done(function(data) { callback(data); });
            }
        },
        formatResult: movieFormatResult, // omitted for brevity, see the source of this page
        formatSelection: movieFormatSelection,  // omitted for brevity, see the source of this page
        dropdownCssClass: "bigdrop", // apply css that makes the dropdown taller
        escapeMarkup: function (m) { return m; } // we do not want to escape markup since we are displaying html in results
    });

    // Disabled state
    $(".select2-disabled-examples select").select2({ placeholder: 'Select option...' });

    // Colors
    $(".select2-colors-examples select").select2();
});
