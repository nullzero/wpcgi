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

    $("[data-toogle='tooltip']").tooltip({
        placement: 'right',
    });

    setTimeout(function() {
        $('.alert').fadeOut(1000);
    }, 5000);

    $('.dropdown-menu li').click(function(e){
      e.preventDefault();
      var selected = $(this).children(":first").attr('href').substring(1);
      $("#" + $(this).parent().data("id")).val(selected);
    });
});

function defaultFor(arg, val) { return typeof arg !== 'undefined' ? arg : val; }

function autocompleteTitle(site, title, ns, fam){
    ns = defaultFor(ns, 0);
    fam = defaultFor(fam, 'wikipedia');
    site = defaultFor(site, 'th');
    $(title).autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "http://" + site + "." + fam + ".org/w/api.php",
                dataType: "jsonp",
                data: {
                    'action': "query",
                    'list'  : "allpages",
                    'format': "json",
                    'apprefix': request.term,
                    'apnamespace': ns,
                    'limit' : 10
                },
                success: function(data) {
                    var tmp = new Array();
                    data = data["query"]["allpages"];
                    for(var x in data) tmp.push(data[x]["title"].replace(/.*?:/, ''));
                    response(tmp);
                }
            });
        },
        open: function() {
            $(title).autocomplete("widget").width(300)
        }
    });
}