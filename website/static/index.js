function deletePlayer(playerId) {
    fetch('delete-player', {
        method: 'POST',
        body: JSON.stringify({ playerId: playerId }),
    }).then((_res) => {
        window.location.href = "/new-players";
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
function getTournamentId(tournamentId) {
    fetch('show-schedule', {
        method: 'POST',
        body: JSON.stringify({ tournamentId: tournamentId }),
    }).then((_res) => {
        window.location.href = "/schedule";
    }).catch(error=>{console.log(error)})
}