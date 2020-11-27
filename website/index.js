let req  = new XMLHttpRequest()
let base_addr = "http://192.168.1.9:80"
let server_addr = "http://192.168.1.9:5000"

$(document).ready(function (){

    if (sessionStorage.apelido){
        let login = $("#login")
        login.after("<span class=\"navbar-link\" id=\"logout\">Sair ("+sessionStorage.apelido +")</span>")
        login.remove()
    }

    $("#logout").click(function (){
        logout()
    })

    $("#btn_manutencao").click(function (){
        parada("manutencao")
    })


    $("#btn_retomada").click(function (){
        parada("retomada")
    })

    if(sessionStorage.apelido){
        $("#buttons").css('display', 'block')
        if(sessionStorage.cargo === "administrador" ){
            $("#log_div").css('display', 'block')
            setInterval(function (){
                preencherLog()
            },2500)
        }
    }
    setInterval(function (){
        preencherDados()
    },2500)

})

function parada(tipo){
    const apelido = sessionStorage.apelido
    const params =  JSON.stringify({
        "apelido": apelido,
        "tipo": tipo
    })

    req.open('POST', server_addr+'/parada')
    req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    req.onload = function () {
        $(window).attr("location", base_addr)
    }
    req.send(params)
}

function logout(){
    const apelido = sessionStorage.apelido
    const params =  JSON.stringify({
        "apelido": apelido
    })

    req.open('POST', server_addr+'/logout')
    req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    req.onload = function () {
        sessionStorage.removeItem('apelido')
        $(window).attr("location", base_addr)
    }
    req.send(params)
}

function preencherDados(){

    req.open('GET', server_addr)
    req.onload = function () {
        let data = JSON.parse(req.responseText)

        let estado = data.estado

        let concluidas = 0
        let retrabalhadas = 0
        let refugadas = 0
        for (const peca of data.pecas) {
            if (peca === "concluida") concluidas++
            else if (peca === "retrabalhada") retrabalhadas++
            else if (peca === "refugada") refugadas++
        }

        $("#estado").text("Arrumar Aqui")
        $("#prod_dia").text(concluidas + retrabalhadas)

        $("#normais").text(concluidas)
        $("#retrabalhadas").text(retrabalhadas)
        $("#refugadas").text(refugadas)

        $("#prod_mes").text(data.producao_mes)
        $("#ultima_manutencao").text(data.ultima_manutencao)

        switch (estado) {
            case "Ativo":
                $("#btn_manutencao").css('display', 'none')
                $("#btn_retomada").css('display', 'block')
                break;
            case "Manutenção":
                $("#btn_manutencao").css('display', 'block')
                $("#btn_retomada").css('display', 'none')
                break;
        }

        if (refugadas > 10 || retrabalhadas > 15) {
            $("#precisa_manutencao").text("O sistema necessita de manutenção")
        } else {
            $("#precisa_manutencao").text("O sistema não necessita de manutenção")
        }
    }
    req.send();
}

function preencherLog(){
    const apelido = sessionStorage.apelido
    const params =  JSON.stringify({
        "apelido": apelido
    })

    //
    console.log("fix")

    req.open('POST', server_addr+'/log')
    req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    req.onload = function () {
        let log = $("#log_div")
        log.text("")

        let contents = JSON.parse(req.responseText).contents
        for (const line of contents) {
            log.append(line)
            log.append("<br>")
        }
        console.log(JSON.parse(req.responseText))
    }
    req.send(params)
}


