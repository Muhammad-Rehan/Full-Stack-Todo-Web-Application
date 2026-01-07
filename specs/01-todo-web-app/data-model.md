# Data Model: Todo Full-Stack Web Application (Phase II)

## User Entity
- **user_id**: UUID (Primary Key)
- **email**: String (Unique, Required)
- **password_hash**: String (Required)
- **created_at**: DateTime (Default: current timestamp)
- **updated_at**: DateTime (Default: current timestamp, Updates: on modification)

## Task Entity
- **id**: UUID (Primary Key)
- **title**: String (Required, Max length: 255)
- **description**: Text (Optional)
- **completed**: Boolean (Default: false)
- **created_at**: DateTime (Default: current timestamp)
- **updated_at**: DateTime (Default: current timestamp, Updates: on modification)
- **user_id**: UUID (Foreign Key to User.user_id, Required)

## Database Constraints
- All tasks must have a valid user_id reference
- Users cannot access tasks belonging to other users
- Task titles must not be empty
- User emails must be unique

## Indexes
- Index on Task.user_id for efficient user-based queries
- Index on Task.id for efficient individual task lookups
- Composite index on (Task.user_id, Task.created_at) for efficient user task listings with sorting