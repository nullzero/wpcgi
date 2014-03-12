$(document).ready(function(){
	autocompleteTitle("th", "#txt-title");
	
    $("#btn-openwiki").click(function(){
        var title = $('#txt-title').val();
        if(title){
            window.open("http://th.wikipedia.org/wiki/" + title, "child_window");
            return false;
        }
    });
    var icons = {
        header: "ui-icon-triangle-1-e",
        activeHeader: "ui-icon-triangle-1-s"
    };
    $('#statpanel').accordion({heightStyle: "content", 
                               icons: icons, 
                               active: 0,
                               collapsible: true});
   	$(document).scrollTop( $("#statpanel").offset().top ); // will make error
});