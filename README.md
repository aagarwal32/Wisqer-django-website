# WISQER
## A social media question-and-answer website built with Django.

This README outlines the features, deployment process, and CI/CD workflows for Wisqer. The project focuses on building a web application where users can ask questions and reply with answers all with secure user authentication, CRUD functionalities, and additional features that enhance the user experience.

### Update: Wisqer is back online! Now on AWS with new features and improvements!
#### www.wisqer.com or www.wisqer.net

## Features and Media:

### Optimized for mobile every step of the way.

![out (2)](https://github.com/user-attachments/assets/a181020d-d047-4def-9713-65f6d93f57b9) ![out 2](https://github.com/user-attachments/assets/3d3be886-3c4b-463d-9b82-b2de768c1b55)

![IMG_6169](https://github.com/user-attachments/assets/9067f0b5-2719-49c1-b18b-4e4a3e8f2382)

![IMG_6172](https://github.com/user-attachments/assets/8c7b82a3-8218-4f42-9f32-e860742f4d9e)

#### New Features (2025)

- Users can perform full, site-wide search on other users, questions, and replies.
- Users can request a summary of the replies from OpenAI's API. Number of requests are limited per hour.
- Users can follow other users.
- Users can bookmark questions and replies.
- Added left navigation menu for quick access to explore, following, bookmarks, etc. tabs.
- Users can attach images and preview them before posting.

#### Create Account, Email Verification, and Login
- Users can view questions, replies, and edit histories without an account.
- To create, update, or delete questions and replies, the user must have an account and be logged in.
- The user must verify their email in order to activate their account and log in.

#### Creating/Deleting Questions and Replies
- Logged in users can create questions. A question title is required but the body text (description) is optional.
- Logged in users can also create replies to questions. Both questions and replies can be deleted by their respective author.
- Deleting a question also deletes all replies associated with it.

#### Updating Questions and Edit History
- The edit history for a question becomes available when it has been modified. The newest edit is shown first in the modal.

#### Account Page and Account Deletion Handling
- Each user has their own account page that is viewable by anyone. The account page displays their past questions and replies.
- The account page can also be used to delete your account which deletes your user but re-assigns your posts under a common "deleted" user.


## DigitalOcean Deployment Process
- The Wisqer app is packaged into a Docker container that is distributed across clusters orchestrated via Kubernetes.
- DigitalOcean provides an abstraction to these deployment tools and also provides a connection to an online PostgreSQL database where user created data is securely held.
- Static files are served via DigitalOcean Spaces that operates via AWS S3 API

## DigitalOcean CI/CD workflows for automated deployments
In the actions tab, workflow scripts automatically...
1. Run Django tests to check proper functionality.
2. Build and push docker image to DigitalOcean's Private Container Registery.
3. Access secret production environment variables via GitHub secrets.
4. Updates the deployment image and waits for Kubernetes to terminate old pods.
5. Finally, the workflow accesses a single pod and performs migrations and collectstatic operations.
