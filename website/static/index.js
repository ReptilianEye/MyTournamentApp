function deleteUser(userId) {
    fetch(window.location.origin + '/delete-user', {
        method: 'POST',
        body: JSON.stringify({ userId: userId }),
    }).then((_res) => {
        window.location.href = "/login";
    });
}
function showDual(dualId) {
    fetch(window.location.origin + '/get-dual-id', {
        method: 'POST',
        body: JSON.stringify({ dualId: dualId }),
    }).then((_res) => {
        window.location.href = "/update-dual";
    });
}
function showTournament(tournamentId) {
    fetch(window.location.origin + '/show-tournament', {
        method: 'POST',
        body: JSON.stringify({ tournamentId: tournamentId }),
    }).then((_res) => {
        window.location.href = "schedule";
    });
}
function deleteTournament(tournamentId) {
    fetch(window.location.origin + '/delete-tournament', {
        method: 'POST',
        body: JSON.stringify({ tournamentId: tournamentId }),
    }).then((_res) => {
        window.location.href = "/tournaments";
    });
}
function deletePlayer(playerId) {
    fetch(window.location.origin + '/delete-player', {
        method: 'POST',
        body: JSON.stringify({ playerId: playerId }),
    }).then((_res) => {
        window.location.href = "/new-players";
    });
}