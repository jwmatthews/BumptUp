// Callback for bump up buttons
var bumpUp = function(event) {
    var user_uuid = $(this).attr("data-user-id");
    var category_uuid = $(this).attr("data-category-id");
    return bump(event, user_uuid, category_uuid, +1);
}

// Callback for bump down buttons
var bumpDown = function(event) {
    var user_uuid = $(this).attr("data-user-id");
    var category_uuid = $(this).attr("data-category-id");
    return bump(event, user_uuid, category_uuid, -1);
}

var bump = function(event, user_uuid, category_uuid, value) {
    $.ajax({
        url: '/users/'+ user_uuid +'/categories/' + category_uuid + '/ratings/',
        dataType: 'json',
        type: 'POST',
        data: '{"rater":"TO_BE_DETERMINED", "score":'+value+'}',
        success: function(data) {
            var user_name = $('#create_category_panel').attr("data-user-name");
            refresh_categories(user_uuid, user_name);
            },
            error: function(data, error) {
                alert("Error from ");
            },
        });
}

var category_to_html = function(category) {
    var category_entry = $("<div class='category_entry row-fluid' data-category-id='" + category["uuid"] + "' data-user-id='" + category['parent'] + "'></div>"); 
    category_entry.data("category", category);
    category_entry.append("<div class='name span2'>" + category["name"] + "</div>" +
            "<div class='description span2'>" + category['description'] + "</div>" +
            "<div class='last_rated span2'>" + category['last']['ctime'] + "</div>" +
            "<div class='num_ratings span2'>" + category['num_ratings'] + "</div>" +
            "<div class='total_score span2'>" + category['total_score'] + "</div>" +
            "<div class='bump_buttons span1'>" +
                "<a class='btn btn-mini' id='bump_down' data-user-id='" + category["parent"] +
                    "' data-category-id='" + category["uuid"] + "'><i class='icon-thumbs-down'></i></a>" +
                "<a class='btn btn-mini' id='bump_up' data-user-id='" + category["parent"] +
                    "' data-category-id='" + category["uuid"] + "'><i class='icon-thumbs-up'></i></a>" +
            "</div>");
    return category_entry;
};

var user_to_html = function(user) {
    var name = user["lastname"] + ", " + user["firstname"];
    var user_entry = $("<div class='user_entry row-fluid' data-user-id='" + user["uuid"] + "' data-user-name='" + name + "'></div>"); 
    user_entry.data("user", user);
    user_entry.append("<div class='name span6'>" + name + "</div>" +
           "<div class='email span6'>" + user["email"] + "</div>" );
    return user_entry;
};

// Called to fetch data from the server and populate the categories panel
var refresh_categories = function(user_uuid, user_name) {
    $('#create_user_panel').hide();
    $('#create_category_panel').hide();
    $.ajax({
        url: '/users/'+ user_uuid +'/categories/',
        dataType: 'json',
        data: "",
        success: function(data) {
            $("#categories-content").empty();
            $("#categories-panel").show();
            if ($.isEmptyObject(data)) {
                $("#categories-content").append($("<div class='empty_categories'>No categories have been created for " + user_name + "</div>"));
            }
            else {
                $.each(data, function(i, item) {
                    $("#categories-content").append(category_to_html(item));
                    });
                }
            },
            error: function(data, error) {
                alert("Error from ");
            },
    });
};

// Called to fetch data from the server and populate the users panel
var refresh_users = function() {
    $("#categories-panel").hide();
    $('#create_user_panel').hide();
    $('#create_category_panel').hide();
    $.ajax({
        url: '/users/',
        dataType: 'json',
        data: "",
        success: function(data) {
            $("#users-panel").empty();
            $("#categories-content").empty();
            $.each(data, function(i, item) {
                $("#users-panel").append(user_to_html(item));
            });
        },
        error: function(data, error) {
            $("#users-panel").empty();
            $("#users-panel").append("Unable to refresh user information");
        },
    });
};

// Called when create new user button is clicked, 
// job is to display the form for creating a new user
var create_new_user_CB = function(event) {
    $("#categories-panel").hide();
    $('#create_category_panel').hide();
    $('#create_user_panel').show();
};

// Called when the form for a new user is being submitted
// job is to read the input variables and submit the new user info
var submit_new_user_CB = function(event) {
    $('#create_user_panel').hide();
    var firstname = $('input.firstname', '.create_new_user_form').val();
    var lastname = $('input.lastname', '.create_new_user_form').val();
    var email = $('input.email', '.create_new_user_form').val();
    // TODO:
    //  Validate form variables and show info on an error
    submit_new_user(firstname, lastname, email);
    return false;
};

var submit_new_user = function(firstname, lastname, email) {
    $.ajax({
        url: '/users/',
        dataType: 'json',
        type: 'POST',
        data: '{"first":"'+firstname+'", "last":"'+lastname+'", "email":"'+email+'"}',
        success: function(data) {
            refresh_users();
        },
        error: function(xhr, ajaxOptions, thrownError) {
            alert("Error, unable to submit new user request, status = " + xhr.status + ", ajaxOptions = " + ajaxOptions + ", thrownError = " + thrownError);
        },
    });
}

// Called when create new category button is clicked, 
// job is to display the form for creating a new category
var create_new_category_CB = function(event) {
    $("#categories-panel").hide();
    $('#create_user_panel').hide();
    $('#create_category_panel').show();
};

// Called when the form for a new category is being submitted
// job is to read the input variables and submit the new category info
var submit_new_category_CB = function(event) {
    $('#create_category_panel').hide();
    var category_name = $('input.name', '.create_new_category_form').val();
    var category_description = $('input.description', '.create_new_category_form').val();
    var user_uuid = $('#create_category_panel').attr("data-user-id");
    var user_name = $('#create_category_panel').attr("data-user-name");
    // TODO:
    //  Validate form variables and show info on an error
    submit_new_category(user_uuid, user_name, category_name, category_description);
    return false;
};

var submit_new_category = function(user_uuid, user_name, category_name, category_description) {
    $.ajax({
        url: '/users/' + user_uuid + '/categories/',
        dataType: 'json',
        type: 'POST',
        data: '{"name":"'+category_name+'", "description":"'+category_description+'", "display":"true"}',
        success: function(data) {
            refresh_categories(user_uuid, user_name);
        },
        error: function(xhr, ajaxOptions, thrownError) {
            alert("Error, unable to submit new category request, status = " + xhr.status + ", ajaxOptions = " + ajaxOptions + ", thrownError = " + thrownError);
        },
    });
}

//
//
// Register event handlers below in the document ready handler
//
//
$(document).ready(function() {
    $.ajaxSetup({
        cache: false
    });
    //
    // Note:  the .live() handlers are needed on dynamic elements we create
    //
    $('#bump_down').live('click', bumpDown);
    $('#bump_up').live('click', bumpUp);
    $('#create_new_user_button').live('click', create_new_user_CB);
    $('#create_new_category_button').live('click', create_new_category_CB);
    $('#submit_new_user_button').live('click', submit_new_user_CB);
    $('#submit_new_category_button').live('click', submit_new_category_CB);

    // When a user entry is clicked, display the associated categories
    $('.user_entry').live('click', 
        function(event){
            var user_uuid = $(this).attr("data-user-id");
            var user_name = $(this).attr("data-user-name");
            // Update the create_category_panel to record the current user
            // TODO:    This is likely something we should refactor out later, 
            //          Feels like there is a potential for a problem relying on this data to be written for category creation.
            //
            $('#create_category_panel').attr("data-user-id", user_uuid);
            $('#create_category_panel').attr("data-user-name", user_name);
            if (typeof user_uuid === "undefined") {
                return;
            }
            refresh_categories(user_uuid, user_name);
        }
    );
    //
    // Only use .click() handlers on elements we create in the base HTML delivered from the server
    //
    $("#load_users").click(function(){
        return refresh_users();
    });
    
    // Hide the dynamic panels initially
    $("#categories-panel").hide();
    $('#create_user_panel').hide();
    $('#create_category_panel').hide();

    // Populate User Panel
    refresh_users();
});




