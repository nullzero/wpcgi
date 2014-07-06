$(document).ready(function(){
    $("#txt-catfrom").keyup(function(){
        autocompleteTitle($("#txt-lang").val(), "#txt-catfrom", 14, $("#txt-fam").val());
    });
    $("#txt-catfrom").keyup();
});