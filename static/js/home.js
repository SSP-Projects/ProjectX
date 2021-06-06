var textToShowInModal = "default";
var data = {};
var workingStatus;

function confirmation_modal_event_function(event) {
    //var button = $(event.relatedTarget) // Button that triggered the modal
    //var recipient = button.data('whatever') // Extract info from data-* attributes
    //document.getElementById("type").value = recipient
    //var modal = $(this)
    //console.log(modal.find('.modal-title'))
    $("#modal_title").text(textToShowInModal);
}

function on_click_work_button_event_function(event) {
    console.log(workingStatus);
    if (workingStatus == "isntWorking") {
        data = {
            state: 0,
            interaction_type: "work",
        };
        textToShowInModal = "¿Entrar al trabajo?";
    } else if (workingStatus == "isWorking") {
        data = {
            state: 1,
            interaction_type: "work",
        };
        textToShowInModal = "¿Salir del trabajo?";
        $("#break-button").prop("disabled", false);
    } else if (workingStatus == "breaking") {
        alert("No puedes salir del trabajo sin haber salido del descanso");
    }
}

function on_click_break_button_event_function(event) {
    if (workingStatus == "isntWorking") {
        alert("No puedes entrar al descanso si no estas trabajando");
    } else if (workingStatus == "isWorking") {
        data = {
            state: 0,
            interaction_type: "break",
        };
        textToShowInModal = "¿Entrar al descanso?";
    } else if (workingStatus == "breaking") {
        data = {
            state: 1,
            interaction_type: "break",
        };
        textToShowInModal = "¿Salir del descanso?";
    }
}

function on_click_confirmation_button_event_function(event) {
    console.log("asdgkljerkfgearklgjergbnearjkgbae")
    ajax_to_post_data("insert_job_interaction/", data, success_function=on_success_on_click_confirmation_button_event_function);
}
function on_error_submit_interaction(error){
    show_feedback_to_user("error",error, true, 15000, "rgba(0,0,123,0.4)", text =error)
}

function on_success_refresh_interactions(data) {
    $("#register_container").empty()                                            
    data.forEach(interaction => {
        //RESOLV FIELDS

        date = new Date(interaction.fields.date_time);
        year = date.getFullYear();
        month = date.getMonth() + 1;
        dt = date.getDate();

        if (dt < 10) {
            dt = "0" + dt;
        }
        if (month < 10) {
            month = "0" + month;
        }
        dateResolved = dt + "-" + month + "-" + year;
        timeResolved = date.toLocaleTimeString("es-ES");

        interactionTypeResolved = "";
        if (interaction.fields.interaction_type == "work") {
            interactionTypeResolved = "Trabajo";
        } else {
            interactionTypeResolved = "Descanso";
        }

        stateResolved = "";
        if (interaction.fields.state == 0) {
            stateResolved = "Entrada";
        } else {
            stateResolved = "Salida";
        }

        $("#register_container").append(
            ` 
        <div class="container-fluid text-dark row">
            <p class="col-4">` +
                dateResolved +
                `</p> 
            <p class="col-4">` +
                stateResolved +
                `</p>
            <p class="col-4">` +
                timeResolved +
                `</p>
        </div>`
        );
    });
}
//GET DE LAS INTERACCIONES
function refreshInteractions() {
    ajax_to_get_data("get_employee_job_interactions/", data, (success_function = on_success_refresh_interactions));
}

function on_success_on_click_confirm_send_event_function() {
    desc = document.getElementById("ticket_description");
    show_feedback_to_user("success", "Enviado, ¡gracias!", false, 1500, "rgba(80,80,80,0.4)");
    desc.value = "";
    toggle_modal("#sendNotification");
}

function on_click_confirm_send_event_function(event) {
    dnis = [];
    checkboxes = document.getElementsByClassName("select_user");
    Array.from(checkboxes).forEach((checkbox) => {
        if (checkbox.checked) {
            dni = checkbox.parentNode.parentNode.parentNode.childNodes[3].innerText;
            dnis.push(dni);
        }
    });
    n = document.getElementById("ticket_type");
    desc = document.getElementById("ticket_description");
    data = {
        dnis: dnis,
        notification_type: n.options[n.selectedIndex].value,
        notification_desc: desc.value,
    };
    ajax_to_post_data("notification_ad/", data, (success_function = on_success_on_click_confirm_send_event_function));
}

function on_success_refresh_notifications(data) {
    notification_panel = document.getElementById("notifications_dropdown");
    notification_panel.innerHTML = "";
    notification_number = document.getElementById("notification_number");
    notification_number.innerText = data.length;
    data.forEach((notification) => {
        item = document.createElement("a");
        item.setAttribute("class", "dropdown-item");
        item.setAttribute("id", notification.id);
        item.setAttribute("onclick", "show_notification(this)");
        item.setAttribute("data-toggle", "modal");
        item.setAttribute("data-target", "#showNotification");
        item.innerText = notification.date + " " + notification.type;
        notification_panel.appendChild(item);
    });
}

function refresh_notifications() {
    ajax_to_get_data("get_notifications/", "", (success_function = on_success_refresh_notifications));
}

function on_success_show_notification(data) {
    notification_type = document.getElementById("show_notification_type");
    notification_desc = document.getElementById("show_notification_description");
    set_as_viewed = document.getElementById("set_as_viewed");
    notification_type.innerHTML = data.type;
    notification_desc.value = data.desc;
    set_as_viewed.value = data.notification;
}

function show_notification(notification) {
    data = {
        id: notification.id,
    };
    ajax_to_get_data("get_notification_to_show_/", data, (success_function = on_success_show_notification));
}

function on_success_on_click_set_as_viewed_notification() {
    show_feedback_to_user("success", "Listo, ¡gracias!", false, 1500, "rgba(80,80,80,0.4)");
}

function on_click_set_as_viewed_notification() {
    data = {
        id: document.getElementById("set_as_viewed").value,
    };
    ajax_to_post_data("set_notification_as_viewed/", data, (success_function = on_success_on_click_set_as_viewed_notification));
}

refreshInteractions();
refresh_notifications();
setInterval(refresh_notifications, 300000);
