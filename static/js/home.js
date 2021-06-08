var textToShowInModal = "default";
var data = {};
var workingStatus;

function on_click_show_details(trigger) {
    day = trigger.parentNode.parentNode.childNodes[0].innerHTML;
    data = { day: day };
    ajax_to_get_data("get_hours_from_desired_day/", data, (success_function = on_success_get_interactions_by_day));
    title = document.getElementById("showDetailsTitle");
    title.innerHTML = "Registros del día " + day;
    toggle_modal("#showDetailsTable");
}


function check_select_option() {
    select = document.getElementById("ticket_type")
    console.log(select.options)
    selected_text = select.options[select.selectedIndex].text
    if(selected_text == "Tipo de Notificación") {
        select.style.color = "grey";
    } else {
        select.style.color = "black";
    }
    Array.from(select.options).forEach(option => {
        if(option.text=="Tipo de Notificación") {
            select.style.color = "grey";
        } else {
            option.style.color = "black"
        }
    })
}

function first_load() {
    select = document.getElementById("ticket_type")
    option = document.createElement("option")
    option.innerHTML = "Tipo de Notificación";
    option.setAttribute("selected", true)
    inner = select.innerHTML;
    select.innerHTML = ""
    select.appendChild(option)
    select.innerHTML += inner
}

first_load()
check_select_option()

function on_success_get_interactions_by_day(data) {
    container = document.getElementById("showDetailsContainer");
    container.innerHTML = "";
    number = Array.from(data).length;
    if(number == 0) {
        //TODO: NO HAY NOTIFICCIONES
    }

    Array.from(data).forEach((interaction) => {
        state = interaction.fields.state;
        type = interaction.fields.interaction_type;
        hour = interaction.fields.date_time.substring(11, 16);
        symbol = '<i class="exit-arrow fas fa-arrow-circle-up"></i>';
        text_state = "Descanso";
        if (state == 0) {
            symbol = '<i class="entrance-arrow fas fa-arrow-circle-down"></i>';
        }
        if (type == "work") {
            text_state = "Trabajo";
        }
        container.innerHTML +=
            '<tr class"table-home-row"><td class="symbol-table text-center p-0 m-0 align-middle"><p class="p-0 m-0">' +
            symbol +
            '</p></td><td class="details-text text-center p-0 m-0 align-middle">' +
            text_state +
            '</td><td class="details-text text-center p-0 m-0 align-middle">' +
            hour +
            '</td><td class="symbol-table text-center p-0 m-0 align-middle"><p class="p-0 m-0">' +
            symbol +
            '</p>';
    });
}

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
    console.log("asdgkljerkfgearklgjergbnearjkgbae");
    ajax_to_post_data("insert_job_interaction/", data, (success_function = on_success_on_click_confirmation_button_event_function));
}
function on_error_submit_interaction(error) {
    show_feedback_to_user("error", error, true, 15000, "rgba(0,0,123,0.4)", (text = error));
}

function on_success_refresh_interactions(data) {
    $("#register_container").empty();
    for (const [key, value] of Object.entries(data)) {
        $("#register_container").append(
            '<tr class"table-home-row"><td class="text-center p-0 m-0 align-middle">' +
                key +
                '</td><td class="text-center p-0 m-0 align-middle">' +
                value +
                '</td><td class="text-center p-0 m-0 align-middle"><button class="col-4 btn notification-button p-0 m-0" onclick="on_click_show_details(this)">' +
                '<i class="details-button fas fa-info-circle"></i></button></td></tr>'
        );
    }
}

//GET DE LAS INTERACCIONES
function refreshInteractions() {
    ajax_to_get_data("get_hours_from_current_month/", data, (success_function = on_success_refresh_interactions));
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
