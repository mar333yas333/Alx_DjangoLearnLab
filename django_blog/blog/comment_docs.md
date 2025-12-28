# Comment Functionality Documentation

## Overview
The Django blog project includes a comment system that allows users to leave comments on blog posts. Authenticated users can post, edit, and delete their own comments, while all users can view comments.

## Components

### 1. Models
- **Comment**: Links to Post and User, with content, created_at, and updated_at fields.

### 2. Forms
- **CommentForm**: ModelForm for comment content.

### 3. Views
- **PostDetailView**: Displays post with comments and comment form for authenticated users.
- **add_comment**: Function view to handle posting new comments.
- **CommentUpdateView**: Allows comment authors to edit their comments.
- **CommentDeleteView**: Allows comment authors to delete their comments.

### 4. URLs
- `/post/<int:pk>/comment/`: Adds a new comment to a post.
- `/comment/<int:pk>/update/`: Edits a comment.
- `/comment/<int:pk>/delete/`: Deletes a comment.

### 5. Templates
- **post_detail.html**: Shows post, comments, and add comment form.
- **comment_form.html**: Form for editing comments.
- **comment_confirm_delete.html**: Confirmation for deleting comments.

## Permissions
- Posting comments requires authentication.
- Editing and deleting comments require the user to be the comment author.

## Data Handling
- Comments are linked to posts and authors automatically.
- Forms validate content and handle submissions securely.

## Setup Instructions
1. Ensure Comment model is migrated.
2. Configure URLs and templates.
3. Test by posting, editing, and deleting comments.

## User Interaction
- View comments on post detail pages.
- Authenticated users can add comments directly on the page.
- Comment authors can edit or delete via links in the comment display.

## Testing Instructions
1. View comments on a post.
2. Log in and add a comment.
3. Edit your comment.
4. Delete your comment.
5. Try editing/deleting others' comments (should fail).