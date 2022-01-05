function goBack() {
  window.history.back();
}

function deleteUser(userId) {
  fetch(window.location.origin + "/delete-user", {
    method: "POST",
    body: JSON.stringify({ userId: userId }),
  }).then((_res) => {
    window.location.href = window.location.origin + "/login";
  });
}

function showDuel(duelId) {
  fetch(window.location.origin + "/get-duel-id", {
    method: "POST",
    body: JSON.stringify({ duelId: duelId }),
  }).then((_res) => {
    window.location.href = window.location.origin + "/update-duel";
  });
}

function showTournament(tournamentId) {
  if (this.event.target.parentElement.nodeName !== "BUTTON") {
    fetch(window.location.origin + "/set-tournament-id", {
      method: "POST",
      body: JSON.stringify({ tournamentId: tournamentId }),
    }).then((_res) => {
      window.location.href = window.location.origin + "/schedule";
    });
  }
}

function editTournament(tournamentId) {
    fetch(window.location.origin + '/set-tournament-id', {
        method: 'POST',
        body: JSON.stringify({ tournamentId: tournamentId }),
    }).then((_res) => {
        window.location.href = window.location.origin + "/edit-tournament";
    });
}

function showPublicTournament(tournamentId) {
    fetch(window.location.origin + '/set-temp-tournament-id', {
        method: 'POST',
        body: JSON.stringify({ tournamentId: tournamentId }),
    }).then((_res) => {
        window.location.href = window.location.origin + "/public-schedule";
    });
}
function showMyPublicTournament(tournamentId) {
  fetch(window.location.origin + '/set-tournament-id', {
      method: 'POST',
      body: JSON.stringify({ tournamentId: tournamentId }),
  }).then((_res) => {
      window.location.href = window.location.origin + "/joined-schedule";
  });
}

function deleteTournament(tournamentId) {
  fetch(window.location.origin + "/delete-tournament", {
    method: "POST",
    body: JSON.stringify({ tournamentId: tournamentId }),
  }).then((_res) => {
    window.location.href = window.location.origin + "/tournaments";
  });
}

function deletePlayer(playerId) {
  fetch(window.location.origin + "/delete-player", {
    method: "POST",
    body: JSON.stringify({ playerId: playerId }),
  }).then((_res) => {
    window.location.reload();
  });
}
