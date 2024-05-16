var pass = document.getElementById("password");
isChecked( event ) {
    if(event.checked){
        pass.innerHTML = "Hide password";
    }else{
        pass.innerHTML = "Show password";
    }
}