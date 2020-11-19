
// function writeTable(){
// 	var trHTML = '';
// 	$.get("descricao", function (data) {
// 		// console.log(data['Name']);
// 		$.each(data['Name'], function(i, item) {
// 			console.log(item);
// 			trHTML +='<tr>'
// 			trHTML += '<th width="1%"> <img width="40px" id="statusConn' + item +'"  class= "statusConn' + item.split("/")[0] +'"  src="static/icon-fail.svg"> </th>';
// 			trHTML += '<th>'  + item +'</th>';
// 			trHTML += '<th class="text-center"> <div id="status-Conclusao-' + item + '" class="lbl"></div>';
// 			trHTML += '<th width="30%">';
// 			$.each(data['Botoes'][i],function(j,botoes){
// 				// console.log(botoes)
// 				trHTML += '			 <button id ="botao-forcar-' + item + "-" + j + '"class="btn btn-primary btn-sm" onclick="ForceLogic(this.id , &quot;' + data['Topicos'][i][j] + 
// 				'&quot; , &quot;'+ data['Mensagens'][i][j] +'&quot; )">' + botoes +'</button> ';
// 			});
			
// 			trHTML += '</tr>'
// 			// console.log(trHTML);
// 		});			    		
// 		$('#JavascriptTable').append(trHTML);
// 	});
	
	
// }

// function writeTable(){
// 	var trHTML = '';
// 	$.get("descricao", function (data) {
// 		// console.log(data['Name']);
// 		$.each(data['Name'], function(i, item) {
// 			console.log(item);
// 			trHTML +='<tr>'
// 			trHTML += '<td width="1%">'+ item.split("/")[1] +  '<img width="40px" id="statusConn' + item +'"  class= "statusConn' + item.split("/")[0] +'"  src="static/icon-fail.svg"> </td>';
// 			// trHTML += '<td>'  + item +'</td>';
// 			trHTML += '<td width="10%"> <div  id="status-Conclusao-' + item + '" class="dot"></div>';
// 			trHTML += '<td >';
// 			$.each(data['Botoes'][i],function(j,botoes){
// 				// console.log(botoes)
// 				trHTML += '			 <button id ="botao-forcar-' + item + "-" + j + '"class="btn btn-primary" onclick="ForceLogic(this.id , &quot;' + data['Topicos'][i][j] + 
// 				'&quot; , &quot;'+ data['Mensagens'][i][j] +'&quot; )">' + botoes +'</button> ';
// 			});
// 			trHTML += '</td>'
// 			trHTML += '</tr>'
// 			// console.log(trHTML);
// 		});			    		
// 		$('#TabelaLogicas').append(trHTML);
// 	});
	
	
// }






// function toggleConnStatusON(id){
// 	$('.statusConn' + id).attr("src", "static/icon-ok.svg");
// }	
// function toggleConnStatusOFF(id){
// 	$('.statusConn' + id).attr("src", "static/icon-fail.svg");
// }


// function toggleStatusON(id){
// 	// console.log(id)
// 	document.getElementById("status-Conclusao-"+id).className = "dot dotVerde";
// }
// function toggleStatusOFF(id){
// 	// console.log(id)
// 	document.getElementById("status-Conclusao-"+id).className = "dot dotCinza";
// }


// function checkConnStatus(){
// 	$.get("ping", function (data) {
// 			// console.log(data[0][0]['Name']);
// 		$.each(data, function(i, item) {
// 			// console.log(data[i][0]['Name']);
// 			// console.log(data[i][0]['Status']);
// 			if(data[i][0]['Status'] == 1){
// 				toggleConnStatusON(data[i][0]['Name']);
// 			} else if(data[i][0]['Status'] == 0 ){
// 				toggleConnStatusOFF(data[i][0]['Name']);
// 			}			    			
// 			// alert(data[i]);
// 		});			    		

//     });
// }

// function checkConclusionStatus(){
//     $.get("status", function (data) {
//     		// console.log(data[0][0]['Name']);
// 		$.each(data, function(i, item) {
// 			// console.log(data[i][0]['Name']);
// 			// console.log(data[i][0]['Status']);
// 			if(data[i]['Status']){
// 				toggleStatusON(data[i]['Name']);
// 				// console.log("CONCLUIDO");
// 			} else{
// 				// console.log("NAOCONCLUIDO");
// 				toggleStatusOFF(data[i]['Name']);
// 			}			    			
// 			// alert(data[i]);
// 		});			    		

//     });
// }

			// checkConnStatus()
			// checkConclusionStatus()
			// setInterval(checkConnStatus,5000);
			// setInterval(checkConclusionStatus,2000);



function ForceLogic(id,topic,message) {
	// var tabId = id.split("_").pop(); // => "Tabs1"
	$.get("send?topic=" + id.split("-")[2] + "/" + topic + "&msg=" + message, function (data) {
		console.log(id.split("-")[2]);
	// }
	});
}
function ResetAll(id){
	$.get("reset", function (data) {
		// console.log(data)
	});
}
