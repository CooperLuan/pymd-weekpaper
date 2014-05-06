$(function() {
    // code highlight
    if (typeof(hljs) != "undefined") {
        hljs.initHighlightingOnLoad();
    }
    // json format
    $.each($("pre.json"), function(i, pre) {
        $(pre).html(JSON.stringify($.parseJSON($(pre).html()), null, 4));
    })
    // nav group
    $.each($("h3"), function(i, sub) {
        if (!$(sub).attr("id")) {
            $(sub).attr("id", parseInt(Math.random() * 1000).toString());
        }
        $("<a>", {
            "class": "btn",
            "html": $(sub).html(),
            "href": "#" + $(sub).attr("id")
        }).appendTo($(".btn-group"));
        if ((i + 1) % 7 == 0) {
            $("<br>").appendTo($(".btn-group"));
        }
    })
    // add remove button
    $("<a>", {
        "class": "btn",
        "html": "<i class='icon-remove'></i>"
    }).click(function() {
        if ($(this).find("i").hasClass("icon-remove")) {
            $(".btn-group a[href]").hide();
            $(this).find("i").attr("class", "icon-th-large");
        } else {
            $(".btn-group a:hidden").show();
            $(this).find("i").attr("class", 'icon-remove');
        }
    }).appendTo($(".btn-group"));
})