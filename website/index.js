const base_addr = "http://192.168.0.109:80"
const server_addr = "http://192.168.0.109:5000"

$(document).ready(function (){

    if (sessionStorage.apelido){
        let login = $("#login")
        login.after("<span class=\"navbar_link\" id=\"logout\">Sair ("+sessionStorage.apelido +")</span>")
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
    },500)

})

function parada(tipo){
    let req  = new XMLHttpRequest()
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
    let req  = new XMLHttpRequest()
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
    const req  = new XMLHttpRequest();
    req.open('GET', server_addr);
    req.onload = function () {
        const data = JSON.parse(req.responseText);

        preencherEstado(data.estado_atual);
        preencherPizzaEstados(data.estados);

        let pecasMes = new Map();
        for (const peca of data.pecas) {
            const key = (new Date(peca.data)).getDate();
            const dia = pecasMes.get(key)
            if(!dia){
                pecasMes.set(key, [peca.resultado])
            } else {
                dia.push(peca.resultado);
            }
        }

        preencherBarrasPecas(pecasMes);
        preencherPizzaPecas(pecasMes.get((new Date()).getDate()));
    }
    req.send();
}

function preencherEstado(estado){
    if(estado === "Ativo") {
        $('#txt_estado').text("Estado Atual: Ativo");
        $('#box_estado').css('background-color','#40F500')
    }
    else if(estado === "Manutencao") {
        $('#txt_estado').text("Estado Atual: Manutenção");
        $('#box_estado').css('background-color','#FFF500')
    }
    else if(estado === "Emergencia") {
        $('#txt_estado').text("Estado Atual: Emergência");
        $('#box_estado').css('background-color','#FF162D')
    }
    else if(estado === "Inativo") {
        $('#txt_estado').text("Estado Atual: Inativo");
        $('#box_estado').css('background-color','#5089DE')
    }
    else{
        $('#txt_estado').text("Estado Atual: Inválido");
        $('#box_estado').css('background-color','#8F8F8F')
    }

    if (estado !== "Manutencao") {
        $("#btn_manutencao").css('display', 'block')
        $("#btn_retomada").css('display', 'none')
    }
    else {
        $("#btn_manutencao").css('display', 'none')
        $("#btn_retomada").css('display', 'block')
    }
}

function preencherPizzaEstados(estados) {
    let canvas = document.getElementById("c_estados");
    let ctx = canvas.getContext('2d');
    canvas.height = window.innerHeight;
    ctx.save();
    ctx.fillStyle = "#F5F5F6";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.restore();

    let ativo = 0, inativo = 0;
    let anterior = estados.shift();
    anterior.data = new Date(anterior.data);
    estados.push({data: new Date(), nome:"Invalido"})
    for (const estado of estados) {
        estado.data = new Date(estado.data);
        let delta = anterior.data - estado.data;

        if(anterior.nome === "Ativo"){
            ativo += delta;
        }
        else if (anterior.nome === "Inativo"){
            inativo += delta;
        }
		else continue
        anterior = estado;

    }

    let delta = anterior.data - new Date();;
    if(anterior.nome === "Ativo"){
        ativo += delta;
    }
    else if (anterior.nome === "Inativo"){
        inativo += delta;
    }

    const tot = ativo + inativo;

    ativo = ativo === 0 ? 0 : ativo/tot;
    inativo = inativo === 0 ? 0 : inativo/tot;

    const dados = [ativo, inativo];
    {
        canvas.height = 300;
        const raio = canvas.width / 8;
        const espessura = 60;
        const centro = {
            x: canvas.width / 2,
            y: raio + espessura / 2,
        }
        const cores = ["#40F500","#5089DE",];

        let stackedAngle = 0;
        ctx.save();
        for (let i = 0; i < 2; i++) {
            ctx.beginPath();
            ctx.arc(centro.x, centro.y,
                raio, stackedAngle * 2 * Math.PI,
                (stackedAngle + dados[i]) * 2 * Math.PI);

            ctx.strokeStyle = cores[i];
            ctx.lineWidth = espessura;
            ctx.stroke();
            stackedAngle += dados[i];
        }
        ctx.restore();

        ctx.save();
        const nomes = ["Ativo", "Inativo"];
        for (let i = 0; i < 2; i++) {
            ctx.beginPath();
            ctx.fillStyle = cores[i];
            ctx.fillRect(centro.x - raio - 30, centro.y + 2 * raio + 50 * i, 20, 20);
            ctx.beginPath();
            ctx.fillStyle = "black";
            ctx.font = "bold 18px Georgia";
            ctx.fillText(nomes[i], centro.x - raio, centro.y + 2 * raio + 50 * i + 17);
        }
        ctx.restore();
    }
}

function preencherPizzaPecas(pecasDia){
    if (pecasDia === undefined){
        let canvas = document.getElementById("c_pecas");
        let ctx = canvas.getContext('2d');
        ctx.save();
        ctx.fillStyle = "#F5F5F6";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "#000";
        ctx.font = "bold 18px Georgia";
        ctx.fillText("Sem Dados", 10, canvas.width/2);
        ctx.restore();
        return;
    }

    let conc = 0, retr = 0, refu = 0;
    for (const peca of pecasDia) {
        if (peca === "concluida") {
            conc += 1;
            continue;
        }

        if (peca === "retrabalhada") {
            retr += 1;
            continue;
        }

        if (peca === "refugada") {
            refu += 1;
        }
    }

    let tot = conc + retr + refu;
    conc = conc === 0 ? 0 : conc/tot;
    retr = retr === 0 ? 0 : retr/tot;
    refu = refu === 0 ? 0 : refu/tot;

    const dados = [conc, retr, refu];
    {
        let canvas = document.getElementById("c_pecas");
        let ctx = canvas.getContext('2d');
        canvas.height = 300;

        ctx.fillStyle = "#F5F5F6";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        const raio = canvas.width / 8;
        const espessura = 60;
        const centro = {
            x: canvas.width / 2,
            y: raio + espessura / 2,
        }
        const cores = [ "#40F500","#FFF500", "#FF162D"];

        let stackedAngle = 0;
        ctx.save();
        for (let i = 0; i < 3; i++) {
            ctx.beginPath();
            ctx.arc(centro.x, centro.y,
                raio, stackedAngle * 2 * Math.PI,
                (stackedAngle + dados[i]) * 2 * Math.PI);

            ctx.strokeStyle = cores[i];
            ctx.lineWidth = espessura;
            ctx.stroke();
            stackedAngle += dados[i];
        }
        ctx.restore();

        ctx.save();
        const nomes = ["Concluidas", "Retrabalhadas", "Refugadas"];
        for (let i = 0; i < 3; i++) {
            ctx.beginPath();
            ctx.fillStyle = cores[i];
            ctx.fillRect(centro.x - raio - 30 , centro.y + 2 * raio + 50 * i, 20, 20);
            ctx.beginPath();
            ctx.fillStyle = "black";
            ctx.font = "bold 20px Georgia";
            ctx.fillText(nomes[i], centro.x - raio, centro.y + 2 * raio + 50 * i + 17);
        }
        ctx.restore();
    }
}

function preencherBarrasPecas(pecasMes){
    let canvas = document.getElementById("c_producao");
    let ctx = canvas.getContext('2d');
    ctx.save();
    ctx.fillStyle = "#F5F5F6";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.restore();

    let data = []
    for (let i = 0; i < 7; i++) {
        const pecasDia = pecasMes.get((new Date()).getDate() - i);
        const dia = new Date((new Date()).setDate((new Date()).getDate()-i));
        data[i] = {
            nome: "" + (dia.getDate()) + "/" + (dia.getMonth()+1),
            quantidade: pecasDia === undefined ? 0 : pecasDia.length
        }
    }
    data = data.reverse();



    // Public properties and methods

    this.width = 300;
    this.height = 150;
    this.maxValue;
    this.margin = 5;
    this.colors = ["purple", "red", "green", "yellow"];
    this.curArr = data;
    this.animationSteps = 10;

    let numOfBars = data.length;
    let barWidth;
    let barHeight;
    let border = 2;
    let ratio;
    let maxBarHeight;
    let gradient;
    let graphAreaWidth = this.width;
    let graphAreaHeight = this.height;
    let i;




    // Calcula as Dimensões
    barWidth = graphAreaWidth / numOfBars - this.margin * 2;
    maxBarHeight = graphAreaHeight - 25;


    let largestValue = 0;
    for (i = 0; i < data.length; i += 1) {
        data[i].quantidade += 1; // Evitando barras nulas
        if (data[i].quantidade > largestValue) {
            largestValue = data[i].quantidade;
        }
    }

    for (i = 0; i < data.length; i += 1) {
        // Set the ratio of current bar compared to the maximum
        if (this.maxValue) {
            ratio = data[i].quantidade / this.maxValue;
        } else {
            ratio = data[i].quantidade / largestValue;
        }

        barHeight = ratio * maxBarHeight;

        // Turn on shadow
        ctx.shadowOffsetX = 2;
        ctx.shadowOffsetY = 2;
        ctx.shadowBlur = 2;
        ctx.shadowColor = "#999";

        // Draw bar background
        ctx.fillStyle = "#333";
        ctx.fillRect(this.margin + i * this.width / numOfBars,
            graphAreaHeight - barHeight,
            barWidth,
            barHeight);

        // Turn off shadow
        ctx.shadowOffsetX = 0;
        ctx.shadowOffsetY = 0;
        ctx.shadowBlur = 0;

        // Draw bar color if it is large enough to be visible
        if (barHeight > border * 2) {
            // Create gradient
            gradient = ctx.createLinearGradient(0, 0, 0, graphAreaHeight);
            gradient.addColorStop(1-ratio, this.colors[i % this.colors.length]);
            gradient.addColorStop(1, "#ffffff");

            ctx.fillStyle = gradient;
            // Fill rectangle with gradient
            ctx.fillRect(this.margin + i * this.width / numOfBars + border,
                graphAreaHeight - barHeight + border,
                barWidth - border * 2,
                barHeight - border * 2);
        }

        // Write bar value
        ctx.fillStyle = "#333";
        ctx.font = "bold 10px sans-serif";
        ctx.textAlign = "center";
        // Use try / catch to stop IE 8 from going to error town
        try {
            ctx.fillText(parseInt(data[i].quantidade-1,10),
                i * this.width / numOfBars + (this.width / numOfBars) / 2,
                graphAreaHeight - barHeight - 10);
        } catch (ex) {}
        // Draw bar label if it exists
        if (data[i].nome) {
            // Use try / catch to stop IE 8 from going to error town
            ctx.fillStyle = "#333";
            ctx.font = "bold 9px sans-serif";
            ctx.textAlign = "center";
            try{
                ctx.fillText(data[i].nome,
                    i * this.width / numOfBars + (this.width / numOfBars) / 2,
                    this.height - 10);
            } catch (ex) {}
        }
    }
}


function preencherLog(){
	let req  = new XMLHttpRequest()
    const params =  JSON.stringify({
        "cargo": sessionStorage.cargo
    })

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
    }
    req.send(params)
}


