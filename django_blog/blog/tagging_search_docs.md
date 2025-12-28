# Tagging and Search Functionality Documentation

## Overview
The Django blog project includes tagging and search features to enhance content organization and discoverability. Users can tag posts and search by keywords in titles, content, or tags.

## Components

### 1. Models
- **Post**: Includes a `tags` field using django-taggit for many-to-many tag associations.

### 2. Views
- **search_posts**: Handles search queries, filtering posts by title, content, or tags using Q objects.
- **posts_by_tag**: Displays posts filtered by a specific tag.

### 3. Forms
- **PostForm**: Automatically includes tag input via django-taggit.

### 4. URLs
- `/search/`: Processes search queries.
- `/tags/<str:tag>/`: Shows posts with a specific tag.

### 5. Templates
- **post_list.html**: Includes search form and displays post tags with links.
- **post_detail.html**: Shows tags for each post with links to filtered views.

## Tagging Usage
- When creating or editing a post, enter tags as comma-separated values.
- Tags are displayed on post list and detail pages.
- Clicking a tag links to posts with that tag.

## Search Usage
- Use the search bar on the post list page.
- Enter keywords to filter posts by title, content, or tags.
- Results display matching posts.

## Setup Instructions
1. Install django-taggit and add to INSTALLED_APPS.
2. Run migrations to add tag fields.
3. Ensure templates include tag display and search form.

## Testing Instructions
1. Create a post with tags and verify display.
2. Search for posts using keywords in title/content/tags.
3. Click tags to filter posts.
4. Edit posts to add/remove tags.