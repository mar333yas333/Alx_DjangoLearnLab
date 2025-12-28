# Blog Post Management Features Documentation

## Overview
The Django blog project includes comprehensive CRUD (Create, Read, Update, Delete) operations for blog posts, allowing authenticated users to manage their content and all users to view posts.

## Components

### 1. Forms
- **PostForm**: A ModelForm for the Post model, handling title and content fields.

### 2. Views
- **PostListView**: Displays a list of all blog posts.
- **PostDetailView**: Shows details of a single post.
- **PostCreateView**: Allows authenticated users to create new posts, automatically setting the author.
- **PostUpdateView**: Enables post authors to edit their posts.
- **PostDeleteView**: Allows post authors to delete their posts.

### 3. URLs
- `/posts/`: Lists all posts.
- `/posts/new/`: Creates a new post.
- `/posts/<int:pk>/`: Views a specific post.
- `/posts/<int:pk>/edit/`: Edits a specific post.
- `/posts/<int:pk>/delete/`: Deletes a specific post.

### 4. Templates
- **post_list.html**: Lists posts with titles, content snippets, author, and date.
- **post_detail.html**: Displays full post details with edit/delete links for authors.
- **post_form.html**: Form for creating or editing posts.
- **post_confirm_delete.html**: Confirmation page for deleting posts.

## Permissions and Access Control
- Create, update, and delete operations require user authentication (LoginRequiredMixin).
- Update and delete operations check that the current user is the post author (UserPassesTestMixin).
- List and detail views are accessible to all users.

## Data Handling
- Author is automatically set to the logged-in user during post creation.
- Forms validate data and handle submission securely with CSRF tokens.

## Setup Instructions
1. Ensure the Post model is defined and migrations are applied.
2. Configure URLs and templates as specified.
3. Start the server and test the features.

## User Interaction
- **Viewing Posts**: Navigate to /posts/ to see all posts.
- **Creating Posts**: Authenticated users can create posts at /posts/new/.
- **Editing/Deleting Posts**: Authors can edit or delete their posts from the detail view.

## Testing Instructions
1. **List View**: Access /posts/ and verify posts are displayed.
2. **Detail View**: Click on a post title and check full details.
3. **Create**: Log in, create a post, and verify it appears in the list.
4. **Update**: Edit a post and confirm changes save.
5. **Delete**: Delete a post and ensure it's removed.
6. **Permissions**: Try accessing edit/delete as a different user and verify denial.