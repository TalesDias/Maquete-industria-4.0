const base_addr = "http://192.168.0.109:80"
const server_addr = "http://192.168.0.109:5000"

$(document).ready( () => {
	sessionStorage.cargo = "sudo";

	// Controla label do slider duracao
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

	
	// Controla label do porcentagem
    $("#atividade_porcentagem").on("input", (ev) =>
        $("#label_atividade_porcentagem")[0].innerText = "Porcentagem: "+ev.target.value+ "%"
    );

    const atualiza_label_historico = function (data) {
        const umDia = 24*60*60*1000;

        const options = {
            month: 'numeric', day: 'numeric',
        };
        const dateTimeFormat = new Intl.DateTimeFormat('pt-BR', options);

        $("#historico_data_hoje")[0].innerText = dateTimeFormat.format(data);

        for (let i = 5; i >= 0 ; i--) {
            data = new Date(data.getTime() - umDia);
            $("#historico_peca_"+i+"_label")[0].innerText = dateTimeFormat.format(data);
        }
    }

	//atualiza o momento atual e suas dependencias
    const horario = $("#horario_escolha")[0];
    const data = $("#data_escolha")[0];
    const momentoAtual =  $("#momento_atual")[0];
    setInterval(function() {
        const tresHoras = 3*60*60*1000;
        if (data.valueAsDate === null && horario.valueAsDate === null){
            const currentDate = new Date();
            const options = {
                year: 'numeric', month: 'numeric', day: 'numeric',
                hour: 'numeric', minute: 'numeric', second: 'numeric',
            };
            const dateTimeFormat = new Intl.DateTimeFormat('pt-BR', options);

            atualiza_label_historico(currentDate);
            momentoAtual.innerText = dateTimeFormat.format(currentDate);
        }
        else if (data.valueAsDate === null){
            const horarioDate = new Date(horario.valueAsNumber + tresHoras);
            const options = {
                hour: 'numeric', minute: 'numeric', second: 'numeric',
            };
            const dateTimeFormat = new Intl.DateTimeFormat('pt-BR', options);

            momentoAtual.innerText = "--/--/---- " + dateTimeFormat.format(horarioDate);
        }
        else if (horario.valueAsDate === null){
            const dataDate = data.valueAsDate;
            const options = {
                year: 'numeric', month: 'numeric', day: 'numeric',
            };
            const dateTimeFormat = new Intl.DateTimeFormat('pt-BR', options);

            atualiza_label_historico(dataDate);
            momentoAtual.innerText = dateTimeFormat.format(dataDate) + " --:--:--" ;
        }
        else {
            const customizadoDate = new Date(data.valueAsNumber + horario.valueAsNumber + tresHoras);
            const options = {
                year: 'numeric', month: 'numeric', day: 'numeric',
                hour: 'numeric', minute: 'numeric', second: 'numeric',
            };
            const dateTimeFormat = new Intl.DateTimeFormat('pt-BR', options);

            atualiza_label_historico(customizadoDate);
            momentoAtual.innerText = dateTimeFormat.format(customizadoDate);
        }
    },1000)


	//Inicia a Calibracao dos sensores
	$("#calibracao_rapida").click(_ => calibrar("Rapido"))
	$("#calibracao_regular").click(_ => calibrar("Moderado"))
	$("#calibracao_precisa").click(_ => calibrar("Lento"))

	// Envia os Dados necessarios
	$("#salvar_dados").click( _ => {
		let erro = -1;

        if ((data.valueAsDate !== null && horario.valueAsDate === null) || (data.valueAsDate === null && horario.valueAsDate !== null)){
            alert("Escolha a data e o horário para corrigir o horário!")
            return;
        }
		const momento = $("#momento_atual")[0].innerText;
		const eM = enviarMomento(momento)
		eM.onload = () => {
			if(eM.status !== 200){
				alert("Erro ao enviar o horário");
				erro = 1;
			}
			else erro = 0;
		}
		if(erro === 1) return;

		while (erro !== -1){
		    //Espera a request anterior concluir
        }

		const porcentagem = $("#atividade_porcentagem")[0].value
		const duracao = $("#atividade_duracao")[0].value
		const mA = modAtividade(porcentagem, duracao)
		mA.onload = () => {
			if(mA.status !== 200){
				alert("Erro ao enviar o alterar o tempo de atividade");
				erro = 1;
			}
		}
		if(erro === 1) return;

		erro = -1;
		const historico_pecas = [];
        for (let i = 0; i <= 5 ; i++) historico_pecas[i] = $("#historico_peca_"+i)[0].value;
        const conc =  $("#historico_hoje_concluidas")[0].value;
        const retr =  $("#historico_hoje_retrabalhadas")[0].value;
        const refu =  $("#historico_hoje_refugadas")[0].value;
        const mHP = modHistoricoPecas(historico_pecas,conc, retr, refu);
        mHP.onload = () => {
            if(mHP.status !== 200){
                alert("Erro ao enviar o alterar o historico de pecas");
                erro = 1;
            }
            else erro = 0;
        }

        while (erro !== -1){
            //Espera a request anterior concluir
        }
        alert("Envio concluido com sucesso");
    });
});


function calibrar(modo){
    let req  = new XMLHttpRequest()
	const cargo = sessionStorage.cargo
    const params =  JSON.stringify({
        cargo,
        modo
    })

    req.open('POST', server_addr+'/calibracaocor')
    req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    req.onload = () => {
			if(req.status !== 200){
				alert("Erro ao enviar o Calibrar o sensor");
			}
		}
    
    req.send(params)
    
    return req;
}


function enviarMomento(momento){
    let req  = new XMLHttpRequest()
	const cargo = sessionStorage.cargo
    const params =  JSON.stringify({
        cargo,
        momento
    })

    req.open('POST', server_addr+'/settime')
    req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    req.send(params)
    
    return req;
}


function modAtividade(porcentagem, duracao){
    let req  = new XMLHttpRequest()
    const cargo = sessionStorage.cargo
    const params =  JSON.stringify({
        cargo,
        porcentagem,
        duracao
    })

    req.open('POST', server_addr+'/modatividade')
    req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    req.send(params)

    return req;
}


function modHistoricoPecas(historico, concluidas, retrabalhads, refugadas){
    let req  = new XMLHttpRequest()
    const cargo = sessionStorage.cargo
    const params =  JSON.stringify({
        cargo,
        historico,
        concluidas,
        retrabalhads,
        refugadas,
    })

    req.open('POST', server_addr+'/modhistoricopecas')
    req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    req.send(params)

    return req;
}



















