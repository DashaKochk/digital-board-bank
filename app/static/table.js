console.log("Table script loaded");

async function fetchPlayers() {
    if (!window.TABLE_ID) return;

    const res = await fetch(`/api/tables/${window.TABLE_ID}`);
    const table = await res.json();

    const ul = document.getElementById("players");
    ul.innerHTML = "";

    table.players.forEach(p => {
        const li = document.createElement("li");
        li.textContent = `${p.name} — ${p.balance}₽`;
        ul.appendChild(li);
    });
}

document.addEventListener("DOMContentLoaded", fetchPlayers);
setInterval(fetchPlayers, 2000);
