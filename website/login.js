let req  = new XMLHttpRequest()

$(document).ready(function (){

    $("#btn_login").click(function () {

        const apelido = $("#apelido")[0].value
        const senha = $("#senha")[0].value
        const params =  JSON.stringify({
            "apelido": apelido,
            "senha": senha
        })

        req.open('POST', 'http://127.0.0.1:5000/login')
        req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        req.onload = function () {
            const status = req.status
            let msg = ""
            switch (status){
                case 200:
                    sessionStorage.apelido = apelido
                    sessionStorage.cargo = JSON.parse(req.responseText).cargo
                    setTimeout(function () {
                        $(window).attr("location", "http://localhost:8000")
                    }, 1000);
                    return;

                case 400:
                    msg = "Preencha Todos os Campos"
                    break;

                case 404:
                    msg = "Verifique suas credencias"
                    break

                default:
                    msg = "Algo deu errado"
                    break
            }
            console.log(msg)
            $("#erro_login").text(msg)

        }


        req.send(params)

    })

})