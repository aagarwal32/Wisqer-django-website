# Wisqer - A social media question-and-answer website built with Django.

This README outlines the current development progress and upcoming features for Wisqer. This project focuses on building a web application where users can ask questions and reply with answers all with secure user authentication, CRUD functionalities, and additional features that enhance user experience.

## Below are video demos showcasing the current progress of Wisqer:

## Register and Login
- Users can view questions, replies, and edit histories without an account. Additionally, they can also sort questions and report.
- To create, update, or delete questions and replies the user must have an account and be logged in.

https://github.com/user-attachments/assets/c3f3a9c5-d927-4999-a6ec-e1ee2ec3b44b

## Checking Edit History and Replying
- The edit history is only shown to users when a question has been modified. The newest edit is shown first in the modal.
- Logged in users can leave replies in the detailed question view.

https://github.com/user-attachments/assets/01debe2c-b168-4d9c-bf19-eac31dddf405

## Creating Questions and Sorting
- Logged in users can create questions. A question title is required but the body text (description) is optional.
- All users can sort questions and switch to different pages.

https://github.com/user-attachments/assets/c6938742-1526-43cf-b9af-9be10f874f0c

## Updating (Editing) Questions
- Logged in users can only update (edit) their questions. Upon updating, previous edits can be viewed in the edit history.

https://github.com/user-attachments/assets/75ab370c-50cf-4283-ad2b-9c1553bf934d

## Deleting Questions and Replies
- Logged in users can only delete their questions and/or replies.
- Deleting a question also deletes all the replies to it.

https://github.com/user-attachments/assets/66787f23-f23f-4e3d-8034-9a0fd9ac06de

# Upcoming Features
1. Options to create polls, tags, and body text along with questions. Polls will only be visible if created.
2. Migrate the database to PostgreSQL for enhanced performance and security.
3. User account page where users can delete their accounts and view past replies and questions.
4. Rating system for questions and replies, and display the number of comments.
5. Comment sorting and filtering capabilities to improve user interaction.
6. Expand navigation options with categories like Search, Top, Hot, and other relevant filters.
7. Integrate an AI model for content classification and categorization to enhance content organization.
8. Home landing page view to welcome users and highlight key features.
9. Deploy the site using Docker for consistent and efficient deployment across different environments.
10. Implement a React frontend to create a more dynamic and responsive user interface.
