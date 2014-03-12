$(document).ready(function(){
	/*
    bootstrap_alert = function() {};
    bootstrap_alert.warning = function(message){
        $('#alertBar').html('<div class="alert">' + 
        '<a class="close" data-dismiss="alert">×</a><span>' + 
        message + '</span></div>');
    };
	*/
    /*
    $("[id^='lang-']").click(function(){
        <?php $(this).attr("id"); ?>
    });
    * */
	$(function(){
	    $("[data-toogle='tooltip']").tooltip({
	    	placement: 'right',
	    });
	});
});

function autocompleteTitle(site, title){
	$(title).autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "http://" + site + ".wikipedia.org/w/api.php",
                dataType: "jsonp",
                data: {
                    'action': "query",
                    'list'  : "allpages",
                    'format': "json",
                    'apprefix': request.term,
                    'limit' : 10
                },
                success: function(data) {
                    var tmp = new Array();
                    data = data["query"]["allpages"];
                    for(var x in data) tmp.push(data[x]["title"]);
                    response(tmp);
                }
            });
        },
		open: function() { 
			$(title).autocomplete("widget").width(300) 
		} 
	});
}