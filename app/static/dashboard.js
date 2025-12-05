console.log("Dashboard script loaded");

async function fetchTables() {
    const res = await fetch('/api/tables');
    const tables = await res.json();
    renderTables(tables);
}

function renderTables(tables) {
    const container = document.querySelector('.tables ul');
    if (!container) return;

    container.innerHTML = '';

    tables.forEach(t => {
        const li = document.createElement('li');
        li.innerHTML = `
            <strong>${t.name}</strong> (макс. ${t.max_players})
            <a href="/tables/${t.id}" class="btn">Открыть</a>
            <ul>${t.players.map(p => `
                <li>${p.name} — ${p.balance}₽</li>
            `).join('')}</ul>
        `;
        container.appendChild(li);
    });
}

document.addEventListener("DOMContentLoaded", fetchTables);
setInterval(fetchTables, 4000);

