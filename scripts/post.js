$(document).ready(function() {
    let post_id = $('#post_id').attr('content');
    let arrow_url = $('#arrow_url').attr('content');
    let arrow_active_url = $('#arrow_active_url').attr('content');
    let upvote_button = $('#upvote');
    let downvote_button = $('#downvote');

    upvote_button.click(function() {
        $.ajax({
            url: '/posts/' + post_id + '/vote',
            type: 'POST',
            data: {'value': 1},
            success: function(response) {
               update_vote_count(response['vote_value']);
               upvote_button.attr('src', arrow_active_url);
               downvote_button.attr('src', arrow_url);
            }
        });
    });

    downvote_button.click(function() {
       $.ajax({
           url: '/posts/' + post_id + '/vote',
           type: 'POST',
           data: {'value': -1},
           success: function(response) {
               update_vote_count(response['vote_value']);
               downvote_button.attr('src', arrow_active_url);
               upvote_button.attr('src', arrow_url);
           }
       });
    });

    function update_vote_count(vote_value) {
        $('#vote_count').text(vote_value);
    }
});