var dniToEdit = {};
var inputName = document.getElementById("id_name");
var inputSurname = document.getElementById("id_surnames");
var inputDNI = document.getElementById("id_dni");
var inputSS = document.getElementById("id_ss_number");
var inputPhone = document.getElementById("id_phone_number");
var inputEmail = document.getElementById("id_email");
var inputSignature = document.getElementById("id_signature");
var editButton = document.getElementById("editButton");
var onlyModalEdit = document.getElementById("only-edit-form");


refresh_notifications();
setInterval(refresh_notifications, 300000);
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

function on_success_user_modal_event_function(data) {
    document.getElementById("id_name").value = data[0].fields.name;
    document.getElementById("id_surnames").value = data[0].fields.surnames;
    document.getElementById("id_dni").value = data[0].fields.dni;
    document.getElementById("input_dni").value = data[0].fields.dni;
    document.getElementById("id_ss_number").value = data[0].fields.ss_number;
    document.getElementById("id_phone_number").value = data[0].fields.phone_number;
    document.getElementById("id_email").value = data[0].fields.email;
    
    //document.getElementById("id_signature").value = data[0].fields.signature;
    

    if(!data[0].fields.is_active){
        $("#editButton").prop( "disabled", true )
        
    }
}

function user_modal_event_function(event) {
    var button = $(event.relatedTarget); // Button that triggered the modal
    var recipient = button.data("whatever"); // Extract info from data-* attributes
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
        inputSignature.disabled = false;

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
        inputSignature.disabled = true;
        
        ajax_to_get_data("get_user/", data, success_function = on_success_user_modal_event_function);
    }
    
    document.getElementById("type").value = recipient;
    var modal = $(this);
    modal.find(".modal-title").text(recipient);
}

function on_success_user_interaction_modal_event_function(data) {
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
}

function user_interaction_modal_event_function(event) {
    var button = $(event.relatedTarget); // Button that triggered the modal
    var recipient = button.data("whatever"); // Extract info from data-* attributes
    var dni = button.parents()[0].parentNode.childNodes[3].innerText;
    document.getElementById("hidden-dni").value = dni;

    var data = {
        dni: dni,
    };
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

function on_success_change_interaction() {
    show_feedback_to_user("success", "¡Modificado con éxito!", false, 750, "rgba(80,80,80,0.4)");
}

function on_error_change_interaction() {
    show_feedback_to_user(
        "error",
        "Oops...",
        false,
        750,
        "rgba(80,80,80,0.4)",
        (text = "¡Algo ha salido mal!"),
        (footer = "<a href>¿Porque he tenido este problema?</a>")
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
    console.log("Data: " + JSON.stringify(data))
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
}

function send_notification_modal_event_function(event) {
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

function on_watch_hours_model(event){

    checkboxes = document.getElementsByClassName("select_user");
    users_div = document.getElementById("users_to_notify");
    month_date = document.getElementById("monthDateHours");
    if (month_date.value == ""){
        month_date.valueAsDate = new Date();
    }
    console.log("asd", month_date.value)

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
            console.log(data);
            ajax_to_get_data("get_hours_from_range", data, success_function = function (data) {
                console.log("HOLAAAAAAAAAAAAAAAAAAAAAAAA", data)
                $("#user_hours_container").append(`
                <tr>
                    <td><h5>` + name + `</h5></td>
                    <td><h5>` + data.hours + `</h5></td>
                </tr>
                `);
            });
            
        }
    });
   
   
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
    data = {
        dnis: [receiver.innerHTML.match(/\(([^)]+)\)/)[1]],
        notification_type: n.options[n.selectedIndex].value,
        notification_desc: desc.value,
    };
    ajax_to_post_data("notification_ad/", data, success_function = on_success_on_click_send_response_notification);
}

function on_success_on_click_set_as_viewed_notification() {
    show_feedback_to_user("success", "Listo, ¡gracias!", false, 1500, "rgba(80,80,80,0.4)");
}

function on_click_set_as_viewed_notification() {
    data = {
        id: document.getElementById("set_as_viewed").value,
    };
    ajax_to_post_data("set_notification_as_viewed/", data, success_function = on_success_on_click_set_as_viewed_notification);
}

function on_click_edit_button(event) {
    if (inputName.disabled == true){
        inputName.disabled = false;
        inputSurname.disabled = false;
        inputDNI.disabled = false;
        inputSS.disabled = false;
        inputPhone.disabled = false;
        inputEmail.disabled = false;
        inputSignature.disabled = false;
    } else {
        inputName.disabled = true;
        inputSurname.disabled = true;
        inputDNI.disabled = true;
        inputSS.disabled = true;
        inputPhone.disabled = true;
        inputEmail.disabled = true;
        inputSignature.disabled = true;
    }
}