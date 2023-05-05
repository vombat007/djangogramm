import Cookies from 'js-cookie';

$(function() {

    const csrftoken = Cookies.get('csrftoken');
    // Attach a click event handler to the like button
    $('.like-button').click(function() {
        var button = $(this); // Store the button element
        var postId = button.data('post-id');

        $.ajax({
            url: '/like',
            method: 'POST',
            data: {
                'post_id': postId,
                'csrfmiddlewaretoken': csrftoken
            },
            success: function(response) {
                // Update the like count
                $('#likes-count-' + postId).text(response.like_count);

                // Toggle the button text
                     if (button.text() === 'Like') {
                    button.removeClass('btn-primary').addClass('btn-secondary').text('Unlike');
                } else {
                    button.removeClass('btn-secondary').addClass('btn-primary').text('Like');
                }
            },
            error: function(xhr, status, error) {
                alert('An error occurred while liking the post.');
            }
        });
    });
});