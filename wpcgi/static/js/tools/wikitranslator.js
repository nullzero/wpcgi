$(document).ready(function(){
	$(function() {
	    $('#text').click(function() {
			var text = $("#text")[0];
		    if (document.body.createTextRange) {
		        var range = document.body.createTextRange();
		        range.moveToElementText(text);
		        range.select();
		    } else if (window.getSelection) {
		        var selection = window.getSelection();
		        var range = document.createRange();
		        range.selectNodeContents(text);
		        selection.removeAllRanges();
		        selection.addRange(range);
		    }
	    });
	});
    $("#btn-clear").click(function(){
        $('#txt-title').val("");
        $('#txt-siteSource').val("");
        $('#txt-siteDest').val("");
        $('#txt-content').val("");
    });
    $("#tab-link-page").click(function(){
        $("#tab-active").val("page");
    });
    $("#tab-link-content").click(function(){
        $("#tab-active").val("content");
    });
	$("#txt-siteSource").change(function(){
		autocompleteTitle($("#txt-siteSource").val(), "#txt-title");
	});
	$("#txt-siteSource").change();
});
