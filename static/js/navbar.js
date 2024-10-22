function hide() {
    document.getElementsByClassName("alert")[0].style.visibility = "hidden";
    document.body.style.overflow = "visible";
}
function show() {
    document.getElementsByClassName("alert")[0].style.visibility = "visible";
    document.body.style.overflow = "hidden";
}



function viewHome() {
    window.location.href = "/";
}
function viewRankings() {
    let loggedIn = false;
    if (loggedIn) {
        window.location.href = "rankings";
    }
    else {
        show()
    }
}
function viewAccount() {
    let loggedIn = false;

    if (loggedIn)
        window.location.href = "account";
    else
        window.location.href = "signin";
}
function viewData() {
    let loggedIn = false;

    if (loggedIn)
        window.location.href = "data";
    else
        show()
}
function viewScout() {
    let loggedIn = false;

    if (loggedIn)
        window.location.href = "rankings";
    else
        show()
}
function viewRankings() {
    let loggedIn = false;

    if (loggedIn)
        window.location.href = "rankings";
    else
        show()
}