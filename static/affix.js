$(function() {
    $('#header').html('<h3>affix</h3>');

    var cursor = 0;
    var affix = $('<div/>', {
        'class': 'bs-sidebar affix',
        'data-spy': 'affix',
        'html': $('<ul/>', {
            'class': 'nav bs-sidenav',
        })
    });
    $.each($('h2,h3'), function(i, tag) {
        $(tag).attr('id', cursor++);
        if(tag.tagName == 'H2') {
            var li = $('<li/>');
            $('<a/>', {
                'href': '#' + (cursor - 1),
                'html': tag.textContent
            }).appendTo(li);
            $('<ul/>', {
                'class': 'nav'
            }).appendTo(li);
            li.appendTo($(affix).find('ul.bs-sidenav'));
        } else if (tag.tagName == 'H3') {
            $('<li/>', {
                'html': $('<a/>', {
                    'href': '#' + (cursor - 1),
                    'html': tag.textContent
                })
            }).appendTo($(affix).find('ul.bs-sidenav>li').last().find('ul'));
        } else {
            console.log('wrong tagName');
        }
    });
    $('#header').html(affix);

    setTimeout(function() {
        $('body').scrollspy({
            target: '.bs-sidebar',
            // offset: 150
        });
        $('body').scrollspy('refresh');
        $('.bs-sidebar').affix({
            offset: {
                top: 20
            }
        });
    }, 200);
});