console.log("Digital Board Bank frontend loaded");

async function fetchTables() {
    const res = await fetch('/api/tables');
    const tables = await res.json();
    renderTables(tables);
}

function renderTables(tables) {
    const container = document.querySelector('.tables ul');
    if (!container) return;
    container.innerHTML = '';
    tables.forEach(table => {
        const li = document.createElement('li');
        li.innerHTML = `<strong>${table.name}</strong> (макс. ${table.max_players})
            <ul>
                ${table.players.map(p => `<li>${p.name} — ${p.balance}₽</li>`).join('')}
            </ul>`;
        container.appendChild(li);
    });
}

async function fetchTransactions() {
    const res = await fetch('/api/transactions');
    const txs = await res.json();
    renderTransactions(txs);
}

function renderTransactions(txs) {
    const tbody = document.querySelector('table tbody');
    if (!tbody) return;
    tbody.innerHTML = '';
    txs.forEach(tx => {
        const tr = document.createElement('tr');
        tr.innerHTML = `<td>${tx.sender}</td><td>${tx.receiver}</td><td>${tx.amount}₽</td><td>${tx.timestamp}</td>`;
        tbody.appendChild(tr);
    });
}

setInterval(() => {
    fetchTables();
    fetchTransactions();
}, 5000);

document.addEventListener('DOMContentLoaded', () => {
    fetchTables();
    fetchTransactions();
});


