# User Authentication System Documentation

## Overview
The Django blog project includes a comprehensive user authentication system that allows users to register, log in, log out, and manage their profiles. This system uses Django's built-in authentication framework for security and reliability.

## Components

### 1. Forms
- **UserRegistrationForm**: Extends Django's UserCreationForm to include an email field for user registration.

### 2. Views
- **register**: Handles user registration. Displays the registration form and saves new users upon valid submission, redirecting to the login page.
- **profile**: Allows authenticated users to view and edit their profile information, specifically their email address.

### 3. URLs
- `/register/`: Maps to the register view.
- `/login/`: Uses Django's LoginView with a custom template.
- `/logout/`: Uses Django's LogoutView with a custom template.
- `/profile/`: Maps to the profile view, requiring login.

### 4. Templates
- **login.html**: Displays the login form.
- **register.html**: Displays the registration form.
- **logout.html**: Confirms logout and provides a link to log in again.
- **profile.html**: Shows user details and a form to update the email.

## Security Features
- All forms include CSRF tokens to prevent cross-site request forgery attacks.
- Passwords are securely hashed using Django's built-in algorithms.
- Profile editing requires user authentication via the @login_required decorator.

## Setup Instructions
1. Ensure the blog app is installed and configured in settings.py.
2. Run migrations if any model changes are made.
3. Start the development server and navigate to the authentication URLs.

## User Interaction
- **Registration**: Users fill out the form at /register/ and are redirected to /login/.
- **Login**: Users enter credentials at /login/ and are redirected to /profile/.
- **Profile Management**: Authenticated users can update their email at /profile/.
- **Logout**: Users log out at /logout/ and are redirected to the home page.

## Testing Instructions
1. **Registration**: Submit the registration form with valid data and verify redirection to login.
2. **Login**: Log in with registered credentials and check redirection to profile.
3. **Profile Update**: Change the email and verify it saves correctly.
4. **Logout**: Log out and confirm the logout message appears.
5. **Security**: Attempt to access /profile/ without logging in and verify redirection to login.