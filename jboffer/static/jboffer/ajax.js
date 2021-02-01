// Submit post on submit
function update_app(url) {
    $.ajax({
        url : url, // the endpoint
        dataType: 'json',
        type : "POST", // http method
        data : { comments : $('#id_comments').val(),
                 application_response: $('#id_application_response').is(':checked'),
                 response_content: $('#id_response_content').val(),
                 csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val() }, // data sent with the post request

        // handle a successful response
        success : function(data) {
            $('#edit-form').css("display","none")/// hide the form
            $('display').html(data)
            location.reload(); //fetch updated item and render page again
        },

        // handle a non-successful response
        error : function(xhr,errmsg, err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};

// Submit post on submit
function delete_app(url) {
    $.ajax({
        url : url, // the endpoint
        type : "POST", // http method
        data : { csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val() }, // data sent with the post request

        // handle a successful response
        success : function(data) {
            window.location = '/'/// hide the form
            ; //fetch updated item and render page again
        },

        // handle a non-successful response
        error : function(xhr,errmsg, err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};

$('#act-form').on('submit', function(e){
    e.preventDefault();
    console.log("form submitted!")
    update_app($(this).attr("data-href"));
});


$('#del-form').on('submit', function(e){
    e.preventDefault();
    console.log("sending delete!")
    delete_app($(this).attr("data-href"));
});
