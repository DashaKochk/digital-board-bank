const API_BASE = "https://digital-bank-backend.onrender.com/api";

async function getTables() {
    const response = await fetch(`${API_BASE}/tables`);
    const tables = await response.json();
    console.log(tables);
}

async function getPlayers() {
    const response = await fetch(`${API_BASE}/players`);
    const players = await response.json();
    console.log(players);
}

async function getTransactions() {
    const response = await fetch(`${API_BASE}/transactions`);
    const transactions = await response.json();
    console.log(transactions);
}

async function getTableById(tableId) {
    const response = await fetch(`${API_BASE}/tables/${tableId}`);
    const table = await response.json();
    console.log(table);
}

getTables();
getPlayers();
getTransactions();
