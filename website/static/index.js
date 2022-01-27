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

function deleteOpponent(opponentId) {
  fetch(window.location.origin + "/delete-opponent", {
    method: "POST",
    body: JSON.stringify({ opponentId: opponentId }),
  }).then((_res) => {
    window.location.href = window.location.origin + "/new-opponents";

  });
}

// PasswordFunction SHOW/HIDE

function PasswordFunction() {
  var x = document.getElementById("password");
  if (x.type === "password") {
      x.type = "text";
      document.getElementById('hide').style.display = "inline-block";
      document.getElementById('show').style.display = "none";
  }
  else {
      x.type = "password";
      document.getElementById('hide').style.display = "none";
      document.getElementById('show').style.display = "inline-block";
  }
}
