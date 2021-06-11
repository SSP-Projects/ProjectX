function generic_success() {
    console.log("SUCCESS");
}

function generic_error(text) {
    console.log(text);
}

function ajax_to_post_data(url, data, success_function = generic_success, error_function = generic_error) {
    $.ajax({
        url: "/ajax/" + url,
        type: "POST",
        data: data,
        headers: {"X-CSRFToken": get_token()},
        success: function(data) {
            success_function(data);
        },
        error: function(data) {
            error_function(data);
        }
    });
}

function ajax_to_get_data(url, data, success_function = generic_success, error_function = generic_error) {
    $.ajax({
        url: "/ajax/" + url,
        type: "GET",
        data_type: "json",
        data: data,
        headers: {"X-CSRFToken": get_token()},
        success: function(data) {
            success_function(data);
        },
        error: function(error) {
            error_function(error);
        }
    });
}

function bind_event(trigger_id, event_to_bind, action_to_dispatch) {

        $(trigger_id).on(event_to_bind, function(event) {
            action_to_dispatch(event)
        })

}

function set_prop(element_id, prop, value) {
    $(element_id).prop(prop, value)
}

function on_click_show_help_alert(event){
   
    //ESTA HARDCODEADO EL SWAL PORQUE NO FINCIONA LA VARIABLE TEXT EN EL METODO SHOE FEEDBACK TOL USER :)
    Swal.fire({
        icon: "info",
        title: "Ayuda",
        text: event.target.parentNode.childNodes[1].childNodes[0].innerHTML,
        //$("#helpText").text()
       
      })
    //show_feedback_to_user("info","Ayuda",text = $("#helpText").text())
}

function show_feedback_to_user(icon, title, confirmation, timer, backdrop, action_on_end = generic_success, text = undefined, footer = undefined) {
    options = {
        icon: icon,
        title: title,
        showConfirmButton: confirmation,
        timer: timer,
        backdrop: backdrop
    }

    if(text != undefined) {
        options["text"] = text
    }

    if(footer != undefined) {
        options["footer"] = footer
    }

    Swal.fire(options).then(() => {
        action_on_end()
    });
}

function toggle_dropdown(dropdown_id) {
    document.getElementById(dropdown_id).classList.toggle("show");
}

function toggle_modal(modal_id) {
    $(modal_id).modal('toggle');
}

window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}