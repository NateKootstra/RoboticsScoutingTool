function checkCookie(cookie) {
    regex = RegExp('^(.*;)?\\s*' + cookie + '\\s*=\\s*[^;]+(.*)?$');
    return document.cookie.match(regex);
}