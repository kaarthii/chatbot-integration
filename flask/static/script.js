document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("sendBtn").addEventListener("click", function() {
        sendMessage();
    });

    document.getElementById("voiceBtn").addEventListener("click", function() {
        fetch("/voice")
        .then(response => response.json())
        .then(data => {
            document.getElementById("responseText").innerText = "Bot: " + data.answer;
            let audio = document.getElementById("audioResponse");
            audio.src = data.audio_url;
            audio.play();
        });
    });
});

function sendMessage() {
    let userInput = document.getElementById("userInput").value;
    fetch("/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: userInput })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("responseText").innerText = "Bot: " + data.answer;
    });
}
