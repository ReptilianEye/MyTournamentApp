function deletePlayer(playerId) {
    fetch('delete-player', {
        method: 'POST',
        body: JSON.stringify({ playerId: playerId }),
    }).then((_res) => {
        window.location.href = "/generator";
    });
}
function deleteUser(userId) {
    fetch('delete-user', {
        method: 'POST',
        body: JSON.stringify({ userId: userId }),
    }).then((_res) => {
        window.location.href = "/login";
    });
}