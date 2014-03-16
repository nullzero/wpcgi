$(document).ready(function(){
	autocompleteTitle("th", "#txt-title");

    $("#btn-openwiki").click(function(){
        var title = $('#txt-title').val();
        if(title){
            window.open("http://th.wikipedia.org/wiki/" + title, "child_window");
            return false;
        }
    });
   	$(document).scrollTop( $("#statpanel").offset().top ); // will make error
});