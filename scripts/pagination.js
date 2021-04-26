$(document).ready(function() {
    let page = $('#page');
    let page_display = $('#page_display');
    let previous_button = $('#previous');
    let next_button = $('#next');
    let page_idx = 0;
    let posts = $('.feed-post');
    paginate();

    function paginate() {
        posts.each(function (i) {
            if (i >= 5 * page_idx && i < 5 * (page_idx + 1)) {
                $(this).css('display', 'inline');
            } else {
                $(this).css('display', 'none');
            }
        });
    }

    previous_button.click(function() {
        if (page_idx > 0) {
            page_idx--;
            page_display.text(page_idx + 1);
            paginate();
        }
    });

    next_button.click(function () {
        if (page_idx * 5 < posts.length - 1) {
            page_idx++;
            page_display.text(page_idx + 1);
            paginate();
        }
    });
});