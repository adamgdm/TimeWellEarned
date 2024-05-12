# TimeWellEarned

## Description

This project is a productivity-focused session manager designed to help users effectively manage their tasks and earn rewards for their accomplishments. It rewards users with 45 minutes of screen time upon completing their assigned tasks. Stay focused, accomplish your goals, and enjoy the well-deserved break with TimeWellEarned.

## Content

- [Plan](#plan)
- [Technologies That Will Be Used](#technologies-that-will-be-used)
- [Database Schema](#database-schema)


## Plan

Building an app that locks the user's screen showing a bunch of tasks that they need to complete. When pressing a task, we will be forwarded to capture an image or a video of the task being completed. After the task whole tasks are completed, the user will be rewarded with 45 minutes of screen time. The user can also set a timer for the task to be completed. This app will be compatible with Windows. When booting up the computer and logging to a user. This app will be the first thing to load up. The user will have to complete the tasks to unlock the screen and use the computer normally.

## Technologies That Will Be Used

- Python
- OpenCV
- Windows API
- MySQL
- Docker

## Database Schema

- Task
  - id
  - name
  - description
  - submited_image_or_video
  - created_at
  - updated_at


