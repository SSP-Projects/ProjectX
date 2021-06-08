function show_notifications() {
    number = document.getElementById("notification_number").innerHTML;
    notification_panel = document.getElementById("notifications_dropdown");
    if(number=="0") {
        notification_panel.innerHTML = "";
        item = document.createElement("p");
        item.setAttribute("class", "m-0 dropdown-item");
        item.innerText = "No hay notificaciones";
        notification_panel.appendChild(item);
    }
    toggle_dropdown('notifications_dropdown')
}