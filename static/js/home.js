
//var workingStatus = "isntWorking";
var workingStatus = '{{workingStatus}}';
$("#work-button").click(function() {
    alert("{{ workingStatus }}")
    if(workingStatus == "isntWorking"){
        alert("Entras del trabajo")
        workingStatus = "working"
    }else if(workingStatus == "working"){
        alert("Has salido del trabajo")
        workingStatus = "isntWorking"
    }else if(workingStatus == "breaking"){
        alert("No puedes salir del trabajo sin haber salido del descanso")
    }

});

$("#break-button").click(function() {

    if(workingStatus == "isntWorking"){
        alert("No puedes entrar al descanso si no estas trabajando")
    }else if(workingStatus == "working"){
        alert("Entras al descanso")
        workingStatus = "breaking"
    }else if(workingStatus == "breaking"){
        alert("Has salido del descanso")
        workingStatus = "working"
    }
});