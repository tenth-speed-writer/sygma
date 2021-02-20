function load_statuses_table(){
    // Get the ID from the form
    var grant_id = $("#id_id").val() ? $("#id_id").val() : null;

    // If it's specified, populate the statuses table
    if (grant_id !== null) {
        var populate = function(data) {
            // On success, replace the HTML of the div
            // with the table HTML provided by the server.
            //$("#grant-statuses").html($(data).html())
//            for (status in data) {
//                $("#grant-statuses").append(data)
//            }
            $("#grant-statuses").html(data)
        };

        var on_err = function(err) {
            // TODO: Express the error to the user more gracefully
            alert(err);
        };

        var req_data = {
            grant: grant_id
        };

        $.ajax({
            url: "/sygma/statuses",
            type: "GET",
            success: populate,
            error: on_err,
            data: req_data
        });
    }
}

function make_status_editable(id){
    // TODO: Hide grant selector and replace it with currently selected grant
    // Replace a row with an editable form
    var populate = function(data) {
        // On success, replace the HTML of the row
        // with the HTML given in the response.
        $("#status-" + id).html(data);
    };

    var on_err = function(err) {
        // TODO: Express the error to the user more gracefully
        alert(err)
    };

    var req_data = {
        id: id
    };

    $.ajax({
        url: "/sygma/status",
        type: "GET",
        success: populate,
        error: on_err,
        data: req_data
    });
}

function new_blank_status() {
    // TODO: Auto-hide the Grant selector and set it to current grant
    // Fetches a blank status form and puts it at the top of the status list
    var on_success = function(data) {
        // Prepend the empty form to the grant_statuses div
        $("#grant-statuses").prepend(data);
    }

    var on_err = function(err) {
        // TODO: Express the error to the user more gracefully
        alert(err);
    }

    $.ajax({
        url: "/sygma/status/",
        type: "GET",
        success: on_success,
        error: on_err
    });
}

function load_obligations_table(){
    // Get the ID from the form
    var grant_id = $("#id_id").val() ? $("#id_id").val() : null;

    // If it's specified, populate the statuses table
    if (grant_id !== null) {
        var populate = function(data) {
            // On success, replace the HTML of the div
            // with the table HTML provided by the server.
            alert(data)
            $("#grant-obligations").html(data)
        };

        var on_err = function(err) {
            // TODO: Express the error to the user more gracefully
            alert(err);
        };

        var req_data = {
            grant: grant_id
        };

        $.ajax({
            url: "/sygma/obligations",
            type: "GET",
            success: populate,
            error: on_err,
            data: req_data
        });
    }
}

function make_obligation_editable(id){
    // TODO: Hide grant selector and replace it with currently selected grant
    // Replace a row with an editable form
    var populate = function(data) {
        // On success, replace the HTML of the row
        // with the HTML given in the response.
        $("#obligation-" + id).html(data);
    };

    var on_err = function(err) {
        // TODO: Express the error to the user more gracefully
        alert(err)
    };

    var req_data = {
        id: id
    };

    $.ajax({
        url: "/sygma/obligation",
        type: "GET",
        success: populate,
        error: on_err,
        data: req_data
    });
}

function new_blank_obligation() {
    // TODO: Auto-hide the Grant selector and set it to current grant
    // Fetches a blank status form and puts it at the top of the status list
    var on_success = function(data) {
        // Prepend the empty form to the grant_statuses div
        $("#grant-obligations").prepend(data);
    }

    var on_err = function(err) {
        // TODO: Express the error to the user more gracefully
        alert(err);
    }

    $.ajax({
        url: "/sygma/obligation",
        type: "GET",
        success: on_success,
        error: on_err
    });
}

// Populate the statuses & obligations once the rest is loaded and ready
var on_doc_ready = function() {
    load_statuses_table();
    load_obligations_table();
}
$(document).ready(on_doc_ready);