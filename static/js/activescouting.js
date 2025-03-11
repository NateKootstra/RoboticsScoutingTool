var timer = [2, 30, 3]
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
}
async function runStampTimer() {
    while (true) {
        await new Promise(r => setTimeout(r, 10));
        time++
    }
}


var events = []
var unfinished = {
    "Coral": [],
    "Algae": [],
    "Defense": [],
    "Other": []
}

function process(event) {
    event = event.split("|");
    if (event[2] == "u" || event[2] == "ue")
        unfinished[event[0]][unfinished[event[0]].length - 1][0] += "|" + event[1];
    if (event[2] == "t" || event[2] == "te")
        unfinished[event[0]].push([event[1], time]);
    if (event[2] == "ue" || event[2] == "te") {
        events.push([event[0], unfinished[event[0]]]);
        unfinished[event[0]] = [];
    }
    console.log(events);
}