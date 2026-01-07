# API Contracts: Todo Full-Stack Web Application (Phase II)

## Authentication Endpoints

### POST /api/auth/signup
**Description**: Create a new user account
**Request**:
- Body: { "email": "string", "password": "string" }
**Response**:
- 201: { "user_id": "uuid", "email": "string", "token": "jwt" }
- 400: Validation error
- 409: User already exists

### POST /api/auth/signin
**Description**: Authenticate user and return JWT token
**Request**:
- Body: { "email": "string", "password": "string" }
**Response**:
- 200: { "user_id": "uuid", "email": "string", "token": "jwt" }
- 401: Invalid credentials

## Task Endpoints

### GET /api/tasks
**Description**: Get all tasks for authenticated user
**Headers**: Authorization: Bearer {token}
**Response**:
- 200: [{ "id": "uuid", "title": "string", "description": "string", "completed": "boolean", "created_at": "datetime", "user_id": "uuid" }]
- 401: Unauthorized

### POST /api/tasks
**Description**: Create a new task for authenticated user
**Headers**: Authorization: Bearer {token}
**Request**:
- Body: { "title": "string", "description": "string", "completed": "boolean" }
**Response**:
- 201: { "id": "uuid", "title": "string", "description": "string", "completed": "boolean", "created_at": "datetime", "user_id": "uuid" }
- 400: Validation error
- 401: Unauthorized

### GET /api/tasks/{task_id}
**Description**: Get a specific task by ID
**Headers**: Authorization: Bearer {token}
**Response**:
- 200: { "id": "uuid", "title": "string", "description": "string", "completed": "boolean", "created_at": "datetime", "user_id": "uuid" }
- 401: Unauthorized
- 404: Task not found (or not owned by user)

### PUT /api/tasks/{task_id}
**Description**: Update a specific task by ID
**Headers**: Authorization: Bearer {token}
**Request**:
- Body: { "title": "string", "description": "string", "completed": "boolean" }
**Response**:
- 200: { "id": "uuid", "title": "string", "description": "string", "completed": "boolean", "created_at": "datetime", "updated_at": "datetime", "user_id": "uuid" }
- 400: Validation error
- 401: Unauthorized
- 404: Task not found (or not owned by user)

### DELETE /api/tasks/{task_id}
**Description**: Delete a specific task by ID
**Headers**: Authorization: Bearer {token}
**Response**:
- 204: Success (no content)
- 401: Unauthorized
- 404: Task not found (or not owned by user)

### PATCH /api/tasks/{task_id}/toggle
**Description**: Toggle completion status of a task
**Headers**: Authorization: Bearer {token}
**Response**:
- 200: { "id": "uuid", "title": "string", "description": "string", "completed": "boolean", "created_at": "datetime", "updated_at": "datetime", "user_id": "uuid" }
- 401: Unauthorized
- 404: Task not found (or not owned by user)