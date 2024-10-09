# Wisqer - A forum website built w/ Django

This README outlines the development timeline and features for the Wisqer Forum application. This project focuses on building a web application where users can ask questions and reply with answers all with secure user authentication, CRUD functionalities, and additional features that enhance user experience.

## Current Progress Video DEMO

https://github.com/user-attachments/assets/f8557abf-1c35-42ef-a3b4-b4c972b3cef4

## Wisqer Forum Development Timeline

---

### Completed Features

#### Saturday 9/14
- [x] **Create a simple top navigation bar** with links to signup and login.
- [x] **Associate users with their questions and replies** via the database and frontend.
- [x] **Add user registration and login functionality.**

#### Sunday 9/15
- [x] **Restrict non-logged-in users** from creating questions and replies (they can still view them).
- [x] **Apply Bootstrap styling** to the entire application for a consistent look and feel.

#### Tuesday 9/17
- [x] **Add a back button** for improved navigation.
- [x] **Revise and fix test cases** for the poll app to ensure reliability.

#### Sunday 9/22
- [x] **Switch to class-based views** and adhere to RESTful practices. Run and fix test cases as needed.
- [x] **Implement pagination** to improve data handling and user experience on list views.

#### Thursday 9/26
- [x] **Enable users to delete their questions.**
- [x] **Add additional tests** to check authentication and deletion of objects (ensure cascade deletion works).

#### Tuesday 10/01
- [x] **Add the ability to delete questions and replies via a menu** (under three dots for more options).

#### Tuesday 10/08
- [x] **Added ability to create optional body text** for more detailed questions.
- [x] **Added sorting functionality** for questions.

---

### Upcoming Features

#### Thursday 10/10
- [ ] **Allow users to delete their accounts** from the user settings.
- [ ] **Implement email verification** during user registration.
- [ ] **Remove the results view** -- view results in the detail page.

---

### Future Enhancements

- **Options to create polls, tags, and body text** along with questions. Polls will only be visible if created.
- **Migrate the database to PostgreSQL** for enhanced performance and security.
- **User account page** where users can delete their accounts and view past replies and questions.
- **Rating system** for questions and replies, and display the number of comments.
- **Comment sorting and filtering capabilities** to improve user interaction.
- **Expand navigation options** with categories like Search, Top, Hot, and other relevant filters.
- **Integrate an AI model for content classification and categorization** to enhance content organization.
- **Home landing page view** to welcome users and highlight key features.
- **Deploy the site using Docker** for consistent and efficient deployment across different environments.
- **Implement a React frontend** to create a more dynamic and responsive user interface.
