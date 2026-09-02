const chatBox = document.getElementById("chatBox");

async function sendMessage(){

const input = document.getElementById("message");

const text = input.value;

if(text==="") return;

chatBox.innerHTML +=
`<div class="user">${text}</div>`;

const response = await fetch("/api/chat",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({

message:text

})

});

const data = await response.json();

chatBox.innerHTML +=
`<div class="bot">${data.reply}</div>`;

chatBox.scrollTop=chatBox.scrollHeight;

input.value="";

}