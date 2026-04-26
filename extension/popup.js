function analyze() {
    let text = document.getElementById("text").value;
    let resultDiv = document.getElementById("result");

    // show loader
    resultDiv.innerHTML = "<div class='loader'></div> Analyzing...";

    fetch("http://localhost:5000/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ text: text })
    })
    .then(res => {
        console.log("STATUS:", res.status);
        return res.json();
    })
    .then(data => {
        console.log("DATA:", data);

        if (data.error) {
            resultDiv.innerText = "Error: " + data.error;
            return;
        }

        let priorityClass = data.priority.toLowerCase();

        resultDiv.innerHTML =
            "📌 <b>Category:</b> " + data.category + "<br><br>" +
            "⚡ <b>Priority:</b> <span class='badge " + priorityClass + "'>" + data.priority + "</span><br><br>" +
            "🏢 <b>Department:</b> " + data.department;
    })
    .catch(err => {
        console.error("FETCH ERROR:", err);
        resultDiv.innerText = "Error connecting to backend";
    });
}

document.getElementById("analyzeBtn").addEventListener("click", analyze);