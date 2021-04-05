$(document).ready(function() {
    $('button[name="delete"]').click(function() {
        let post_id = $(this).val();
        let user_id = $('#user_id').attr('content');
        $.ajax({
            url: '/' + user_id + '/profile/' + post_id + '/delete',
            type: 'GET',
            success: function() {
                $('#' + post_id).remove();
            }
        });
    })
});
