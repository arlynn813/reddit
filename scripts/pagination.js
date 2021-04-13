$(document).ready(function() {
    let page = $('#page');
    let page_display = $('#page_display');
    let previous_button = $('#previous');
    let next_button = $('#next');
    paginate();

    function paginate() {
        let page_idx = parseInt(page.attr('content'));
        let posts = $('.feed-post');

        posts.each(function (i) {
            if (i >= 5 * page_idx && i < 5 * (page_idx + 1)) {
                $(this).css('display', 'inline');
            } else {
                $(this).css('display', 'none');
            }
        });

        previous_button.prop('disabled', false);
        next_button.prop('disabled', false);
        if (page_idx <= 0) {
            previous_button.prop('disabled', true);
        }
        if (page_idx * 5 >= posts.length - 1) {
            next_button.prop('disabled', true);
        }
    }

    previous_button.click(function() {
        let page_idx = parseInt(page.attr('content'));
        page.attr('content', (page_idx - 1).toString());
        page_display.text(page_idx);
        paginate();
    });

    next_button.click(function () {
        let page_idx = parseInt(page.attr('content'));
        page.attr('content', (page_idx + 1).toString());
        page_display.text(page_idx + 2);
        paginate();
    });
});