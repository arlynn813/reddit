# Team: TacoSamurai
### Andrew Lynn and Amogh Shanbhag

# APIs

## Register: /register
User can create an account by providing a username, email, and optionally a profile picture. After user is created, the user is routed to the feed API.

## Feed: /{hashedcode}/feed
Displays all posts created by other users. The user can click any post to redirect to the post API.

## Profile: /{hashedcode}/profile
Displays all posts created by the current user. The user can click any post to redirect to the post API. The user can also delete any of their posts.

## Create: /{hashedcode}/create
User can create a post by providing a title and body. After a post is created, user is routed to the profile API.

## Post: /posts/{postid}
Displays a detail view of a post. Users can also upvote or downvote a post.

## Database Dump: /getTSVdump
Displays buttons to download each database table's data. Files are formatted as tab separated values.

# Internal APIs
These APIs are used internally using AJAX

## /{hashedcode}/profile/{postid}/delete
Internal API to delete a post. This deletes the given post from the database.

## /posts/{postid}/vote
Internal API to vote on a post. This updates the vote count in the database and returns the new vote *value* to display to the user.