function signIn() {
    let team = document.getElementById("team").value;
    if (team == "")
        team = "null";
    let username = document.getElementById("username").value;
    if (username == "")
        username = "null";
    let password = document.getElementById("password").value;
    if (password == "")
        password = "null";

    window.location.href = `/endpoint/signin/${team}/${username}/${password}`;
}