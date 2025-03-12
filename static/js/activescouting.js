var timer = [2, 30, 3, 10]
var time = 0

function scout(name, event) {
    let location = name.startsWith("TL") ? 1 : name.startsWith("TR") ? 2 : name.startsWith("BL") ? 3 : 4;
    document.getElementById("divider" + location).replaceChildren(document.getElementById(name).content.cloneNode(true));
    process(event)
}

async function runTimer() {
    let run = true
    while (run) {
        if (timer[1] < 10)
            document.getElementById("timer").textContent = timer[0] + ":0" + timer[1];
        else
            document.getElementById("timer").textContent = timer[0] + ":" + timer[1];

        await new Promise(r => setTimeout(r, 1000));

        if (timer[0] == 2 && timer[1] == 15 && timer[2] > 0) {
            timer[2]--;
        }
        else
            timer[1]--;
        if (timer[1] == -1) {
            timer[0]--;
            timer[1] = 59;
        }
        if (timer[0] == 0 && timer[1] == 0) {
            run = false;
            document.getElementById("timer").textContent = "0:00";
        }
    }
    for (var i = 0; i < timer[3]; i++) {
        await new Promise(r => setTimeout(r, 1000));
    }
    document.getElementById("midgame").replaceWith(document.getElementById("postgame").content.cloneNode(true));
}
async function runStampTimer() {
    while (true) {
        await new Promise(r => setTimeout(r, 10));
        time++
    }
}


var events = []
var unfinished = {}
function process(event) {
    event = event.split("|");

    if (event[1] == "f")
        events.push([event[0], time]);
    else {
        if (event[2] == "s")
            unfinished[event[1]] = [event[0], time]
        else if (event[2] == "m" || event[2] == "e")
            unfinished[event[1]][0] = unfinished[event[1]][0] + " | " + event[0]
        if (event[2] == "e")
            events.push(unfinished[event[1]])
    }
}

var stars = {}
function updateStars(item, number) {
    if (stars[item] == number)
        number = 0
    stars[item] = number;
    let container = document.getElementById(item);
    if (number >= 1) {
        container.childNodes[2].className = "star hidden";
        container.childNodes[3].className = "star";
    }
    else {
        container.childNodes[2].className = "star";
        container.childNodes[3].className = "star hidden";
    }
    if (number >= 2) {
        container.childNodes[4].className = "star hidden";
        container.childNodes[5].className = "star";
    }
    else {
        container.childNodes[4].className = "star";
        container.childNodes[5].className = "star hidden";
    }
    if (number >= 3) {
        container.childNodes[6].className = "star hidden";
        container.childNodes[7].className = "star";
    }
    else {
        container.childNodes[6].className = "star";
        container.childNodes[7].className = "star hidden";
    }
    if (number >= 4) {
        container.childNodes[8].className = "star hidden";
        container.childNodes[9].className = "star";
    }
    else {
        container.childNodes[8].className = "star";
        container.childNodes[9].className = "star hidden";
    }
    if (number >= 5) {
        container.childNodes[10].className = "star hidden";
        container.childNodes[11].className = "star";
    }
    else {
        container.childNodes[10].className = "star";
        container.childNodes[11].className = "star hidden";
    }
}

function submitData() {
    let postgame = {}
    postgame["endgame"] = document.getElementById("endgame").value;
    postgame["major"] = document.getElementById("major").value;
    postgame["minor"] = document.getElementById("minor").value;
    postgame["robot"] = stars["robotstars"] == undefined ? 0 : stars["robotstars"]
    postgame["drivers"] = stars["driverstars"] == undefined ? 0 : stars["driverstars"]

    let finalData = {
        "events": events,
        "postgame": postgame
    };
    window.location.href = "/submit/" + JSON.stringify(finalData);
}