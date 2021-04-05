$(document).ready(function() {
    let post_id = $('#post_id').attr('content');

    $('#upvote').click(function() {
       $.ajax({
           url: '/posts/' + post_id + '/vote',
           type: 'POST',
           data: {'value': 1},
           success: function(response) {
               update_vote_count(response['vote_value']);
           }
       });
    });

    $('#downvote').click(function() {
       $.ajax({
           url: '/posts/' + post_id + '/vote',
           type: 'POST',
           data: {'value': -1},
           success: function(response) {
               update_vote_count(response['vote_value']);
           }
       });
    });

    function update_vote_count(vote_value) {
        $('#vote_count').text(vote_value);
    }
});