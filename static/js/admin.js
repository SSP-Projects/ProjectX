var dniToEdit = {};
var inputName = document.getElementById("id_name");
var inputSurname = document.getElementById("id_surnames");
var inputDNI = document.getElementById("id_dni");
var inputSS = document.getElementById("id_ss_number");
var inputPhone = document.getElementById("id_phone_number");
var inputEmail = document.getElementById("id_email");
var editButton = document.getElementById("editButton");
var onlyModalEdit = document.getElementById("only-edit-form");
var last_sign = ""

get_employees_by_name("");


function on_success_search_date_button_action(data) {
    
    document.getElementById("register_container").innerHTML = "";
    $("#register_container").empty();
    data.forEach((interaction) => {
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
        dateResolved = year + "-" + month + "-" + dt;
        timeResolved = date.toLocaleTimeString("es-ES");
        if (timeResolved.length < 8) {
            timeResolved = "0" + timeResolved;
        }

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
        <div  class="container-fluid background-grey font-black row m-1 g-0 py-1">
        <h5 class="col-3">` +
                interactionTypeResolved +
                `</h5> 
        <h5 class="col-3">` +
                stateResolved +
                `</h5>
        
        <input type="time" class="col-3 text-center " onblur="updateInteraction(` +
                interaction.pk +
                `, this.value, 'time' )" value="` +
                timeResolved +
                `" />
        <input type="date" class="col-3 text-center " onblur="updateInteraction(` +
                interaction.pk +
                `, this.value, 'date' )" value="` +
                dateResolved +
                `" />
        </div>`
        );
    });
    show_feedback_to_user("success", "¡Búsqueda realizada con éxito!", 750, "rgba(80,80,80,0.4)");
}
function on_click_check_if_employee_have_interactions(event){

    var data = {
        employee_dni: $("#input_dni").val(),
        month: $("#monthDatePDF").val(),
    };
    ajax_to_get_data("get_pdf_from_month/", data,success_function = on_success_get_month_employee_interactions, error_function = on_error_get_month_employee_interactions);

}
function on_success_get_month_employee_interactions(data){
    var binaryData = [];
    binaryData.push(data);
    var url = window.URL.createObjectURL(new Blob(binaryData, {type: "application/zip"}))
    var a = document.createElement('a');
    a.href = url;
    a.download = "Registro_jornada.pdf";
    document.body.append(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
}
function on_error_get_month_employee_interactions(error){
    show_feedback_to_user("error","No existen interacciones en este mes", true, 15000, "rgba(70,70,70,0.4)")
}

function on_click_show_details(trigger) {
    day = trigger.parentNode.parentNode.childNodes[0].innerHTML;
    dni = document.getElementById("hidden-dni").value;
    console.log(dni)
    data = { day: day, "dni": dni};
    ajax_to_get_data("get_hours_from_desired_day_and_user/", data, (success_function = on_success_get_interactions_by_day));
    title = document.getElementById("showDetailsTitle");
    title.innerHTML = "Registros del día " + day;
    toggle_modal("#showDetailsTable");
}

function on_success_get_interactions_by_day(data) {
    container = document.getElementById("showDetailsContainer");
    container.innerHTML = "";
    Array.from(data).forEach((interaction) => {
        pk = interaction.pk
        state = interaction.fields.state;
        type = interaction.fields.interaction_type;
        hour = interaction.fields.date_time.substring(11, 16);
        day = interaction.fields.date_time.substring(0, 10);
        symbol = '<i class="exit-arrow fas fa-arrow-circle-up"></i>';
        text_state = "Descanso";
        if (state == 0) {
            symbol = '<i class="entrance-arrow fas fa-arrow-circle-down"></i>';
        }
        if (type == "work") {
            text_state = "Trabajo";
        }
        container.innerHTML +=
            '<tr class"table-home-row"><td class="symbol-table text-center p-0 m-0 align-middle"><p style="display:none;">' + pk + '</p><p class="p-0 m-0">' +
            symbol +
            '</p></td><td class="details-text text-center p-0 m-0 align-middle">' +
            text_state +
            '</td><td class="details-text text-center p-0 m-0 align-middle"><input type="date" class="text-center" value=' + day + ' onblur="updateInteractionDetailsDay(this)"><input type="time" class="text-center" value=' +
            hour +
            ' onblur="updateInteractionDetailsTime(this)"></td><td class="symbol-table text-center p-0 m-0 align-middle"><p class="p-0 m-0">' +
            symbol +
            '</p>';
    });
}

function search_date_button_action(event) {
    var startDate = document.getElementById("startDate").value;
    var endDate = document.getElementById("endDate").value;
    var dni = document.getElementById("hidden-dni").value;
    var data = {
        dni: dni,
        startDate: startDate,
        endDate: endDate,
    };
    $("#register_container").append(`<h2>No hay resultados </h2>`);
    ajax_to_get_data("get_employee_job_interactions_date_range/", data, success_function = on_success_search_date_button_action);
}

function changeAll() {
    state = document.getElementsByClassName("select_all")[0].checked;
    checkboxes = document.getElementsByClassName("select_user");
    Array.from(checkboxes).forEach((checkbox) => {
        if(checkbox.disabled == false){
            checkbox.checked = state
        }
    });
}

function changeOne() {
    general = document.getElementsByClassName("select_all")[0];
    checkboxes = document.getElementsByClassName("select_user");
    all_checked = true;
    Array.from(checkboxes).forEach((checkbox) => {
        if (checkbox.checked == false) {
            general.checked = false;
            all_checked = false;
        }
    });
    if (all_checked) {
        general.checked = true;
    }
}



function user_modal_event_function(event) {
    var button = $(event.relatedTarget); 
    var recipient = button.data("whatever"); 
    var dni = button.parents()[0].parentNode.childNodes[3].innerText;
    var data = {
        dni: dni,
    };
    
    if (recipient === "Crear Usuario") {
       // document.getElementsByClassName("only-edit-form").style.visibility = "hidden";
        editButton.style.visibility = "hidden";
        onlyModalEdit.style.display = "none";
        inputName.disabled = false;
        inputSurname.disabled = false;
        inputDNI.disabled = false;
        inputSS.disabled = false;
        inputPhone.disabled = false;
        inputEmail.disabled = false;
        document.getElementById("user_signature").innerHTML = '<input style="width: 60%;" type="file" name="signature" accept="image/*" class="form-control" id="id_signature" required></input>'

        document.getElementById("id_name").value = "";
        document.getElementById("id_surnames").value = "";
        document.getElementById("id_dni").value = "";
        document.getElementById("id_ss_number").value = "";
        document.getElementById("id_phone_number").value = "";
        document.getElementById("id_email").value = "";
     
    } else {
        editButton.style.visibility = "visible";
        onlyModalEdit.style.display = "block";
        month_date = document.getElementById("monthDatePDF");
        
        if (month_date.value == ""){
            month_date.valueAsDate = new Date();
        }
        //document.getElementsByClassName("only-edit-form").style.visibility = "visible";        
        inputName.disabled = true;
        inputSurname.disabled = true;
        inputDNI.disabled = true;
        inputSS.disabled = true;
        inputPhone.disabled = true;
        inputEmail.disabled = true;
        
        ajax_to_get_data("get_user/", data, success_function = on_success_user_modal_event_function);
    }
    document.getElementById("type").value = recipient
    document.getElementById("createUserModalLabel").innerHTML = recipient
}

function on_success_user_interaction_modal_event_function(data) {
    $("#register_container").empty();
    interactions = Object.entries(data);
    if(interactions.length == 0) {
        $("#register_container").append(
            '<tr class"table-home-row"><td></td><td class="text-center">No hay registros</td><td></td></tr>'
        );
    }
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

function user_interaction_modal_event_function(event) {
    var button = $(event.relatedTarget); // Button that triggered the modal
    var dni = button.parents()[0].parentNode.childNodes[3].innerText;
    console.log(dni)
    document.getElementById("hidden-dni").value = dni;
    console.log(document.getElementById("hidden-dni").value)
    var data = {
        'dni': dni,
    };
    console.log(data)
    ajax_to_get_data("get_employee_job_interactions_dni/", data, success_function = on_success_user_interaction_modal_event_function);
}

function updateInteraction(key, value, type) {
    console.log("Updating key(" + key + "): " + value);

    var newInput = {
        type: type,
        key: key,
        value: value,
    };

    changeInteraction(newInput);
}

function updateInteractionDetailsTime(trigger) {
    hour = trigger.value;
    pk = trigger.parentNode.parentNode.childNodes[0].childNodes[0].innerHTML;
    ajax_to_post_data("change_interaction_time/", {'pk':pk, 'hour':hour}, success_function = on_success_change_interaction)
}

function updateInteractionDetailsDay(trigger) {
    day = trigger.value;
    pk = trigger.parentNode.parentNode.childNodes[0].childNodes[0].innerHTML;
    ajax_to_post_data("change_interaction_day/", {'pk':pk, 'day':day}, success_function = on_success_change_interaction)
}

function on_success_change_interaction() {
    show_feedback_to_user("success", "¡Modificado con éxito!", false, 750, "rgba(80,80,80,0.4)");
}

function on_error_change_interaction() {
    show_feedback_to_user(
        "error",
        "Oops...",
        false,
        750,
        "rgba(70,70,70,0.3)",
        (text = "¡Algo ha salido mal!"),

    );
}

function changeInteraction(newInput) {
    ajax_to_post_data("modifyInteraction/", newInput, on_success_change_interaction, on_error_change_interaction);
}

function on_success_confirm_desactivate_modal_event_function(data) {
    $("#userToDesactivate").text(data[0].fields.name + " " + data[0].fields.surnames);
}
function on_success_confirm_activate_user_modal_event_function(data){
    $("#userToActivate").text(data[0].fields.name + " " + data[0].fields.surnames);
}
function confirm_desactivate_modal_event_function(event) {
    var button = $(event.relatedTarget);
    var dni = button.parents()[0].parentNode.childNodes[3].innerText;
    var data = {
        dni: dni,
    };
    ajax_to_get_data("get_user/", data, success_function = on_success_confirm_desactivate_modal_event_function);
    dniToEdit = data;
}
function confirm_activate_user_modal_event_function(event){
    var button = $(event.relatedTarget);
    var dni = button.parents()[0].parentNode.childNodes[3].innerText;
    var data = {
        dni: dni,
    };
    ajax_to_get_data("get_user/", data, success_function = on_success_confirm_activate_user_modal_event_function);
    dniToEdit = data;
}

function on_click_desactivate_user_confirmation_button(event) {
    ajax_to_post_data("desactivate_user/", dniToEdit, success_function = document.location.reload());
}
function on_click_activate_user_confirmation_button(event) {
    ajax_to_post_data("activate_user/", dniToEdit, success_function = document.location.reload());
}


function on_success_get_employees_by_name(data) {
    $("#tableContent").empty();
    if (data.length == 0) {
        $("#tableContent").append(` <div class="table-data"><h5 class="text-center">No se ha encontrado empleados</h5></div>`);
    }
   
    data.forEach(function (employee, i) {
        rowColor = `<div class="table-row-2">`;
        if (i % 2 == 0) {
            rowColor = `<div class="table-row-1">`;
        }
        buttons = `<button class="btn delete-button" data-toggle="modal" data-target="#confirmActivateUserModal"><i class="fas fa-unlock-alt"></i></button>`
        checkbox =` <div id="table-data-checkbox" class="table-data">
        <div class="form-check col-2 justify-content-center align-items-center">
            <input disabled ="true" class="select_user form-check-input position-static m-0 p-0" style="background-color:#BF1414;" type="checkbox" id="blankCheckbox" value="option1" aria-label="...">

            </div>
    </div>`
        if(employee.fields.is_active == true){
         buttons=`<button class="btn  delete-button" data-toggle="modal" data-target="#confirmDesactivateModal"><i class="fas fa-user-slash"></i></button>`
            checkbox =` <div id="table-data-checkbox" class="table-data">
            <div class="form-check col-2 justify-content-center align-items-center">
                <input class="select_user form-check-input position-static m-0 p-0" type="checkbox" id="blankCheckbox" value="option1" aria-label="...">
              
            </div>
        </div>`
        }
        $("#tableContent").append(
            rowColor + checkbox+
                `

        <div class="table-data">
            <h5 id="DNI{{ forloop.counter }}">` +
                employee.fields.dni +
                `</h5>
        </div>
        <div class="table-data">
            <h5>` +
                employee.fields.name +
                " " +
                employee.fields.surnames +
                `</h5>
        </div>
        <div class="table-data">
            <h5>` +
                employee.fields.email +
                `</h5>
        </div>
        <div class="table-data">
            <h5>` +
                employee.fields.phone_number +
                `</h5>
        </div>
        <div class="table-data d-inline" name="prueba">
            <button class="btn" data-toggle="modal" data-target="#UserModal" data-whatever="Editar Usuario"><i
                class="fas fa-user-edit"></i></button>
            <button data-toggle="modal" data-target="#userInteractions" class="btn"><i
                class="fas fa-clipboard-list"></i></button>
                `+buttons+` 

        </div>
        </div> `
        );
    });
}

function get_employees_by_name(name) {
    data = { name: name };
    ajax_to_get_data("get_users_by_name/", data, success_function = on_success_get_employees_by_name);
}

function on_input_search_input(event) {
    var nameToSearch = $("#searchInput").val();
    get_employees_by_name(nameToSearch);
    document.getElementsByClassName("select_all")[0].checked = false;
    checkboxes = document.getElementsByClassName("select_user");
    Array.from(checkboxes).forEach((checkbox) => {
        checkbox.checked = false;
    })
}

function check_if_employees_are_selected_to_send_notifications(event){
    checkboxes = document.getElementsByClassName("select_user");
    isAnyCheckboxChecked = false
    Array.from(checkboxes).forEach((checkbox) => {
        if (checkbox.checked) {
            isAnyCheckboxChecked = true
        }
    })
    if(isAnyCheckboxChecked){
        $('#sendNotification').modal('show')
        document.getElementById('ticket_description').value = ""
        send_notification_modal_event_function(event)
    }else{
        Swal.fire({
            title: 'Aviso',
            text: "Selecciona al menos un empleado para ver mandar notificaciones",
            icon: 'warning',
            showCancelButton: false,
        })
    }
}

function send_notification_modal_event_function(event) {
    n = document.getElementById("ticket_type")
    n.options[0].selected = true
    check_select_option()
    checkboxes = document.getElementsByClassName("select_user");
    users_div = document.getElementById("users_to_notify");
    users_div.innerHTML = "";
    Array.from(checkboxes).forEach((checkbox) => {
        if (checkbox.checked) {
            a = document.createElement("a");
            name = checkbox.parentNode.parentNode.parentNode.childNodes[5].innerText;
            dni = checkbox.parentNode.parentNode.parentNode.childNodes[3].innerText;
            a.appendChild(document.createTextNode("(" + dni + ") " + name));
            users_div.appendChild(a);
        }
    });
}
function check_if_employees_are_selected(event){
    checkboxes = document.getElementsByClassName("select_user");
    isAnyCheckboxChecked = false
    Array.from(checkboxes).forEach((checkbox) => {
        if (checkbox.checked) {
            isAnyCheckboxChecked = true
        }
    })
    if(isAnyCheckboxChecked){
       
        $('#userHours').modal('show')
        on_watch_hours_model(event)


      
    }else{
        Swal.fire({
            title: 'Aviso',
            text: "Selecciona al menos un empleado para ver sus horas",
            icon: 'warning',
            showCancelButton: false,
        })
    }
}

function on_watch_hours_model(){

    checkboxes = document.getElementsByClassName("select_user");
    users_div = document.getElementById("users_to_notify");
    month_date = document.getElementById("monthDateHours");
    if (month_date.value == ""){
        month_date.valueAsDate = new Date();
    }

    var info = [];
    $("#user_hours_container").empty();
    Array.from(checkboxes).forEach((checkbox) => {
        if (checkbox.checked) {
            document.getElementById("user_hours_container").innerHTML += "";
            var name = checkbox.parentNode.parentNode.parentNode.childNodes[5].innerText;
            dni = checkbox.parentNode.parentNode.parentNode.childNodes[3].innerText;
            
            var data = {
                "dni" : dni,
                "month_to_search" : month_date.value
            }
            
            ajax_to_get_data("get_hours_from_range", data, success_function = function (data) {
                info.push({"name": name, "hours" : data.hours});
                fill_hours_sorted(info);
            });
        }
    });
};

function fill_hours_sorted(hours){
    $("#user_hours_container").empty();
    
    hours.sort(function(a, b){
        return b.hours - a.hours;
    });

    jQuery.each(hours, function(i, val) {
        $("#user_hours_container").append(`
            <tr>
                <td><h5>` + val.name + `</h5></td>
                <td class="text-center"><h5>` + val.hours + `</h5></td>
            </tr>
        `);
    });
}


function on_success_on_click_confirm_send_event_function() {
    desc = document.getElementById("ticket_description");
    show_feedback_to_user("success", "Enviado, ¡gracias!", false, 1500, "rgba(80,80,80,0.4)");
    toggle_modal("#sendNotification");
    desc.value = "";
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
    if(n.options[n.selectedIndex].value == "Tipo de Notificación") {
        show_feedback_to_user("error", "Selecciona un tipo de notificación", false, 1500, "rgba(0,0,123,0.4)");
        return
    }
    desc = document.getElementById("ticket_description");
    data = {
        dnis: dnis,
        notification_type: n.options[n.selectedIndex].value,
        notification_desc: desc.value,
    };
    n.options[0].selected = true
    check_select_option()
    ajax_to_post_data("notification_ad/", data, success_function = on_success_on_click_confirm_send_event_function);
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
    ajax_to_get_data("get_notifications/", "", success_function = on_success_refresh_notifications);
}

function on_success_show_notification(data) {
    sent_by = document.getElementById("send_by_text_show_notification");
    notification_type = document.getElementById("show_notification_type");
    notification_desc = document.getElementById("show_notification_description");
    set_as_viewed = document.getElementById("set_as_viewed");
    sent_by.innerHTML = "Enviado por " + data.sender_name;
    notification_type.innerHTML = data.type;
    notification_desc.value = data.desc;
    set_as_viewed.value = data.notification;
    document.getElementById("response_to").value = data.sender;
}

function show_notification(notification) {
    data = {
        id: notification.id,
    };
    ajax_to_get_data("get_notification_to_show/", data, success_function = on_success_show_notification);
}

function on_click_make_a_response_notification(event) {
    n = document.getElementById("response_ticket_type");
    n.options[0].selected = true
    check_select_option()
    toggle_modal("#showNotification");
    receiver = document.getElementById("send_to_text_response_notification");
    receiver.innerHTML = "Enviar respuesta a " + document.getElementById("send_by_text_show_notification").innerHTML.substring(12);
    toggle_modal("#responseNotification");
}

function on_success_on_click_send_response_notification() {
    show_feedback_to_user("success", "Enviado, ¡gracias!", false, 1500, "rgba(80,80,80,0.4)");
    toggle_modal("#responseNotification")
}

function on_click_send_response_notification(event) {
    receiver = document.getElementById("send_to_text_response_notification");
    n = document.getElementById("response_ticket_type");
    desc = document.getElementById("response_ticket_description");
    if(n.options[n.selectedIndex].value == "Tipo de Notificación") {
        show_feedback_to_user("error", "Selecciona un tipo de notificación", false, 1500, "rgba(0,0,123,0.4)");
        return
    } 
    data = {
        dnis: [receiver.innerHTML.match(/\(([^)]+)\)/)[1]],
        notification_type: n.options[n.selectedIndex].value,
        notification_desc: desc.value,
    };
    ajax_to_post_data("notification_ad/", data, success_function = on_success_on_click_send_response_notification);
}

function on_success_on_click_set_as_viewed_notification() {
    toggle_dropdown('notifications_dropdown')
    show_feedback_to_user("success", "Listo, ¡gracias!", false, 1500, "rgba(80,80,80,0.4)");
    refresh_notifications()
}

function on_click_set_as_viewed_notification() {
    data = {
        id: document.getElementById("set_as_viewed").value,
    };
    refresh_notifications()
    ajax_to_post_data("set_notification_as_viewed/", data, success_function = on_success_on_click_set_as_viewed_notification);
}

function on_success_user_modal_event_function(data) {
    document.getElementById("id_name").value = data[0].fields.name;
    document.getElementById("id_surnames").value = data[0].fields.surnames;
    document.getElementById("id_dni").value = data[0].fields.dni;
    document.getElementById("input_dni").value = data[0].fields.dni;
    document.getElementById("id_ss_number").value = data[0].fields.ss_number;
    document.getElementById("id_phone_number").value = data[0].fields.phone_number;
    document.getElementById("id_email").value = data[0].fields.email;
    url = window.location.protocol + "//" + window.location.hostname + ":"  + window.location.port + "/media/"
    image_path = "<img style=\"max-width: 40%;\" src=\"" + url + data[0].fields.signature + "\">"
    document.getElementById("user_signature").innerHTML = image_path;
    last_sign = image_path
    if(!data[0].fields.is_active){
        $("#editButton").prop( "disabled", true )
    }
}

function on_click_edit_button(event) {
    if (inputName.disabled == true){
        inputName.disabled = false;
        inputSurname.disabled = false;
        inputDNI.disabled = false;
        inputSS.disabled = false;
        inputPhone.disabled = false;
        inputEmail.disabled = false;
        document.getElementById("user_signature").innerHTML = '<input style="width: 60%;" type="file" name="signature" accept="image/*" class="form-control" id="id_signature"></input>'
    } else {
        inputName.disabled = true;
        inputSurname.disabled = true;
        inputDNI.disabled = true;
        inputSS.disabled = true;
        inputPhone.disabled = true;
        inputEmail.disabled = true;
        document.getElementById("user_signature").innerHTML = last_sign
    }
}

function check_select_option() {
    select = document.getElementById("response_ticket_type")
    selected_text = select.options[select.selectedIndex].text
    if(selected_text == "Tipo de Notificación") {
        select.style.color = "grey";
    } else {
        select.style.color = "black";
    }
    Array.from(select.options).forEach(option => {
        if(option.text=="Tipo de Notificación") {
            option.style.color = "grey";
        } else {
            option.style.color = "black"
        }
    })
    select = document.getElementById("ticket_type")
    selected_text = select.options[select.selectedIndex].text
    if(selected_text == "Tipo de Notificación") {
        select.style.color = "grey";
    } else {
        select.style.color = "black";
    }
    Array.from(select.options).forEach(option => {
        if(option.text=="Tipo de Notificación") {
            option.style.color = "grey";
        } else {
            option.style.color = "black"
        }
    })
}

function first_load() {
    select = document.getElementById("response_ticket_type")
    option = document.createElement("option")
    option.innerHTML = "Tipo de Notificación";
    option.setAttribute("selected", true)
    inner = select.innerHTML;
    select.innerHTML = ""
    select.appendChild(option)
    select.innerHTML += inner
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
refresh_notifications();
setInterval(refresh_notifications, 300000);