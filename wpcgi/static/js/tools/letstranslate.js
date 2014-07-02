$(document).ready(function(){
    $("#txt-lang").keyup(function(){
        autocompleteTitle($("#txt-lang").val(), "#txt-title");
    });
    $("#txt-lang").keyup();
});
