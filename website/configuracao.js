const base_addr = "http://192.168.0.109:80"
const server_addr = "http://192.168.0.109:5000"

$(document).ready( () => {
	sessionStorage.apelido = "sudo";

    $("#atividade_duracao").on("input", (ev) => {
        let minutos = parseInt(ev.target.value);
        if (minutos < 60){
            $("#label_atividade_duracao")[0].innerText = "Duração: " +minutos+ "min";
        }
        else{
            let horas = Math.floor( minutos / 60);
            minutos = minutos - horas*60;

            if (minutos === 0){
                $("#label_atividade_duracao")[0].innerText = "Duração: " +horas+ "h";
            }
            else {
                $("#label_atividade_duracao")[0].innerText = "Duração: " +horas+ "h"+minutos+ "min";
            }
        }
    });


    $("#atividade_porcentagem").on("input", (ev) =>
        $("#label_atividade_porcentagem")[0].innerText = "Porcentagem: "+ev.target.value+ "%"
    );

    setInterval(function(){
        const currentDate = new Date();
        const options = {
            year: 'numeric', month: 'numeric', day: 'numeric',
            hour: 'numeric', minute: 'numeric', second: 'numeric',
        };
        const dateTimeFormat = new Intl.DateTimeFormat('pt-BR', options);

        $("#momento_atual")[0].innerText = dateTimeFormat.format(currentDate);
    },1000);


	$("#salvar_dados").click( _ => {
		erro = 0;
		
		const momento = $("#momento_atual")[0].innerText;
		console.log(momento)
		const eM = enviarMomento(momento)
		eM.onload = () => {
			if(eM.status != 200){
				alert("Erro ao enviar o horário");
				erro = 1;
			}
		}
		if(erro == 1) return;
		
	});


});

function enviarMomento(momento){
    let req  = new XMLHttpRequest()
	const apelido = sessionStorage.apelido
    const params =  JSON.stringify({
        apelido,
        momento
    })

    req.open('POST', server_addr+'/settime')
    req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    req.send(params)
    
    return req;
}


















