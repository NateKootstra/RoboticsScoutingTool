settings = {
    alignVert: true,
    alignHoriz: true,
    multiLine: false,
    detectMultiLine: true,
    minFontSize: 2,
    maxFontSize: 80,
    reProcess: true,
    widthOnly: false,
    alignVertWithFlexbox: false
};
settings2 = {
    alignVert: true,
    alignHoriz: true,
    detectMultiLine: true,
    minFontSize: 2,
    maxFontSize: 80,
    reProcess: true,
    widthOnly: false,
    alignVertWithFlexbox: false
};

window.onload = function fit() {
    textFit(document.getElementsByClassName('teaminfo'), settings);
    textFit(document.getElementsByClassName('teamsite'), settings2);
}