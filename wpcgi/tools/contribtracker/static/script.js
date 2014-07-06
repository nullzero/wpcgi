$(document).ready(function(){
    autocompleteTitle("th", "#txt-title");

    $("#tab-link-page").click(function(){
        $("#tab-active").val("page");
    });
    $("#tab-link-content").click(function(){
        $("#tab-active").val("content");
    });

    $("#btn-openwiki").click(function(){
        var title = $('#txt-title').val();
        if(title){
            window.open("http://th.wikipedia.org/wiki/" + title, "child_window");
            return false;
        }
    });
});
