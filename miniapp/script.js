async function fetchLeaderboard() {
    try {
        const response = await fetch("/miniapp/data");
        const data = await response.json();
        const tbody = document.querySelector("#leaderboard tbody");
        tbody.innerHTML = "";
        data.forEach((row, index) => {
            const tr = document.createElement("tr");
            tr.innerHTML = `<td>${index + 1}</td><td>${row.username}</td><td>${row.score}</td>`;
            tbody.appendChild(tr);
        });
    } catch (e) {
        console.error("Ошибка загрузки таблицы рекордов:", e);
    }
}

fetchLeaderboard();
