function getUserId() {
    let userId = localStorage.getItem("digital_bank_user_id");

    if (!userId) {
        userId = crypto.randomUUID();
        localStorage.setItem("digital_bank_user_id", userId);
    }

    return userId;
}

const USER_ID = getUserId();
console.log("User ID:", USER_ID);

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
