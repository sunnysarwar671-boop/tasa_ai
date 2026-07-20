async function send(){

let prompt=document.getElementById("prompt").value;

let box=document.getElementById("messages");

box.innerHTML+="<p><b>You:</b> "+prompt+"</p>";

box.innerHTML+="<p><b>Tasa:</b> Hello Sunny 🥰</p>";

document.getElementById("prompt").value="";

}
