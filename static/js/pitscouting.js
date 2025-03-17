function selectEvent(event) {
    window.location.href = `/pitselectevent/${event}`;
}

function selectTeam(team) {
    window.location.href = `/pitselectteam/${team}`;
}

function unScout(level) {
    window.location.href = `/pitunscout/${level}`;
}

function submitData() {
    let data = {}
    data["L1"] = document.getElementById("L1").value;
    data["L2"] = document.getElementById("L2").value;
    data["L3"] = document.getElementById("L3").value;
    data["L4"] = document.getElementById("L4").value;
    data["Processor"] = document.getElementById("Processor").value;
    data["Net"] = document.getElementById("Net").value;
    data["Deep"] = document.getElementById("Deep").value;
    data["Shallow"] = document.getElementById("Shallow").value;
    data["Drivetrain"] = document.getElementById("Drive").value;
    data["DNP"] = document.getElementById("DNP").value;

    window.location.href = "/pitsubmit/" + JSON.stringify(data);
}