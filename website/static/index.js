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
function showDual(dualId) {
  fetch(window.location.origin + "/get-dual-id", {
    method: "POST",
    body: JSON.stringify({ dualId: dualId }),
  }).then((_res) => {
    window.location.href = window.location.origin + "/update-dual";
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
    window.location.href = window.location.origin + "/new-players";
  });
}
