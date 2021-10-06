function deleteUser(userId) {
    fetch('delete-user', {
        method: 'POST',
        body: JSON.stringify({ userId: userId }),
    }).then((_res) => {
        window.location.href = "/login";
    });
}
function showDual(dualId) {
    fetch('get-dual-id', {
        method: 'POST',
        body: JSON.stringify({ dualId: dualId }),
    }).then((_res) => {
        window.location.href = "/update-dual";
    });
}
function showTournament(tournamentId) {
    fetch('show-tournament', {
        method: 'POST',
        body: JSON.stringify({ tournamentId: tournamentId }),
    }).then((_res) => {
        window.location.href = "/schedule";
    });
}
function deleteTournament(tournamentId) {
    fetch('delete-tournament', {
        method: 'POST',
        body: JSON.stringify({ tournamentId: tournamentId }),
    }).then((_res) => {
        window.location.href = "/tournaments";
    });
}
function deletePlayer(playerId) {
    fetch('delete-player', {
        method: 'POST',
        body: JSON.stringify({ playerId: playerId }),
    }).then((_res) => {
        window.location.href = "/new-players";
    });
}