const API = "https://tasa-ai.onrender.com/chat";

async function send() {

    const input = document.getElementById("prompt");
    const box = document.getElementById("messages");

    const prompt = input.value.trim();

    if (!prompt) return;

    box.innerHTML += `
    <div class="user message">
        <b>You:</b><br>${prompt}
    </div>
    `;

    input.value = "";

    box.innerHTML += `
    <div id="typing" class="ai message">
        🤖 Tasa is typing...
    </div>
    `;

    box.scrollTop = box.scrollHeight;

    try {

        const response = await fetch(API,{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                message:prompt
            })
        });

        const data = await response.json();

        document.getElementById("typing").remove();

        box.innerHTML += `
        <div class="ai message">
            <b>Tasa:</b><br>${data.reply}
        </div>
        `;

    }

    catch(e){

        document.getElementById("typing").remove();

        box.innerHTML += `
        <div class="ai message">
        ❌ ${e}
        </div>
        `;

    }

    box.scrollTop = box.scrollHeight;

          }
