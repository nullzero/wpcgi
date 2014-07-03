$(document).ready(function(){
    $("#txt-lang").keyup(function(){
        autocompleteTitle($("#txt-lang").val(), "#txt-ftitle", 0, $("#txt-fam").val());
    });
    $("#txt-lang").keyup();
    $("#txt-fam").keyup();
});
