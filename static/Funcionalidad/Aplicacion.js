function login(usuario,password){
    lanzar_cargar()
    $.ajax({
        url: "/Usuario/login-register/",
        type: "POST",
        data: {
            usuario: usuario,
            password: password
        },
        cache: false,
        success: function(result) {
            setTimeout(function(){
                console.log(result)
                window.location="/";
            },1500)
        }
    });
}
function lanzar_cargar(){
    $("#formModal").addClass("in")
    $("#formModal").css("display","block")
}

function comprobar_password(password,password1,usuario,nombres,apellidos,email){
    if (password==password1){
        $("#error").css("display","none")
        return true
    }
    else{
        $("#error").css("display","block")
        console.log(password+" , "+password1)
        return false
    }
    if (usuario==null){
        $("#errorusuario").css("display","block")
        console.log("usuario esta vacio")
        return false
    }
    else{
        $("#errorusuario").css("display","none")
        return true
    }
    if (nombres==null){
        $("#errornombres").css("display","block")
        console.log("nombres esta vacio")
        return false
    }
    else{
        $("#errornombres").css("display","none")
        return true
    }
    if (apellidos==null){
        console.log("apellidos esta vacio")
        $("#errorapellidos").css("display","block")
        return false
    }
    else{
        $("#error").css("display","none")
        return true
    }
    if (email==null){
        console.log("email esta vacio")
        $("#erroremail").css("display","block")
        return false
    }
    else{
        $("#erroremail").css("display","none")
        return true
    }
}
function registrar_usuario(usuario,nombres,apellidos,email,password,password1){
    if (comprobar_password(password,password1,nombres,apellidos,email,usuario)) {
        lanzar_cargar()
        $.ajax
        (
            {
                url: "/Usuario/login-register/register/",
                type: "POST",
                data: {
                    usuario: usuario,
                    nombres: nombres,
                    apellidos: apellidos,
                    password: password,
                    email: email
                },
                cache: false,
                success: function (result) {
                    setTimeout(function () {
                        console.log(result)
                        window.location = "/Usuario/login-register/";
                    }, 3000)
                }
            }
        );

    }
}

function add_carrito(nproducto,pagina,cantidad){
    lanzar_cargar()
    try {
        $.ajax
        (
            {
                url: "/Productos/al-carrito/add/" + nproducto + "/",
                type: "POST",
                data: {
                    cantidad: cantidad
                },
                cache: false,
                success: function (result) {
                    setTimeout(function () {
                        console.log(result)
                        if(result=="render"){
                            window.location="/Usuario/login-register/"
                        }
                        else{
                            window.location = "/" + pagina;
                        }
                    }, 3000)
                }
            }
        );
    }catch (ex){
        console.log(ex)
    }

}