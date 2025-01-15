# WISQER
## A social media question-and-answer website built with Django.

This README outlines the features, deployment process, and CI/CD workflows for Wisqer. The project focuses on building a web application where users can ask questions and reply with answers all with secure user authentication, CRUD functionalities, and additional features that enhance the user experience.

### WISQER is now live at www.wisqer.com !

## Features:

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


## Deployment Process
- The Wisqer app is packaged into a Docker container that is distributed across clusters orchestrated via Kubernetes.
- DigitalOcean provides an abstraction to these deployment tools and also provides a connection to an online PostgreSQL database where user created data is securely held.
- Static files are served via DigitalOcean Spaces that operates via AWS S3 API

## CI/CD workflows for automated deployments via GitHub Actions
- In the actions tab, workflow scripts automatically...
  1. Run Django tests to check proper functionality.
  2. Build and push docker image to DigitalOcean's Private Container Registery.
  3. Access secret production environment variables via GitHub secrets.
  4. Updates the deployment image and waits for Kubernetes to terminate old pods.
  5. Finally, the workflow accesses a single pod and performs migrations and collectstatic operations.
