function getUserId() {
    let userId = localStorage.getItem("digital_bank_user_id");

    if (!userId) {
        userId = crypto.randomUUID();
        localStorage.setItem("digital_bank_user_id", userId);
    }

    return userId;
}

window.USER_ID = getUserId();
