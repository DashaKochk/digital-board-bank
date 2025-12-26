console.log("Table script loaded");

async function fetchPlayers() {
    if (!window.TABLE_ID) return;

    const res = await fetch(`/api/tables/${window.TABLE_ID}`);
    const table = await res.json();

    const ul = document.getElementById("players");
    ul.innerHTML = "";

    table.players.forEach(p => {
        const li = document.createElement("li");
        li.textContent = `ID: ${p.id} | ${p.name} — ${p.balance}₽`;
        ul.appendChild(li);
    });
}

async function sendMoney() {
    const receiverId = document.getElementById("player-id").value;
    const amount = document.getElementById("amount").value;

    if (!receiverId || !amount) {
        alert("Введите ID и сумму");
        return;
    }

    const senderId = prompt("Введите ВАШ ID");

    if (!senderId) return;

    const form = new FormData();
    form.append("sender_id", senderId);
    form.append("receiver_id", receiverId);
    form.append("amount", amount);

    const res = await fetch("/api/transfer", {
        method: "POST",
        body: form
    });

    if (!res.ok) {
        alert("Ошибка перевода");
    }

    fetchPlayers();
}

document.addEventListener("DOMContentLoaded", fetchPlayers);
setInterval(fetchPlayers, 2000);
