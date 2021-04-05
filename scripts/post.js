$(document).ready(function() {
    let post_id = $('#post_id').attr('content');
    let upvote_button = $('#upvote');
    let downvote_button = $('#downvote');

    upvote_button.click(function() {
        $.ajax({
            url: '/posts/' + post_id + '/vote',
            type: 'POST',
            data: {'value': 1},
            success: function(response) {
               update_vote_count(response['vote_value']);
               upvote_button.css('background-color', 'red');
               downvote_button.css('background-color', 'white');
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
               downvote_button.css('background-color', 'red');
               upvote_button.css('background-color', 'white');
           }
       });
    });

    function update_vote_count(vote_value) {
        $('#vote_count').text(vote_value);
    }
});