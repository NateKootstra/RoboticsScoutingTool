function addUser() {
    let username = document.getElementById("username").value;
    if (username == "")
        username = "null";
    let name = document.getElementById("name").value;
    if (name == "")
        name = "null";
    let password = document.getElementById("password").value;
    if (password == "")
        password = "null";

    window.location.href = `/adduser/${username}/${name}/${password}`;
}

function deleteUser(username) {
    window.location.href = `/deleteuser/${username}`;
}


function addEvent() {
    window.location.href = `/addevent`;
}

function removeEvent() {
    window.location.href = `/removeevent`;
}

function updateEvents(events) {
    window.location.href = `/updateevents/${events}`;
}