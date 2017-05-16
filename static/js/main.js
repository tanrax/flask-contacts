$('[data-toggle=confirmation]').confirmation({
    rootSelector: '[data-toggle=confirmation]',
    btnOkLabel: 'Ok',
    btnCancelLabel: 'No',
    'placement': 'top',
});
var dismissAlerts = function() {
    var alertElements = Array(document.querySelectorAll(".alert"));
    alertElements.forEach(function(e) {
        setTimeout(function() {
            $(e).remove();
        }, 2500)
    });
};
$(document).ready(function() {
    dismissAlerts();
});