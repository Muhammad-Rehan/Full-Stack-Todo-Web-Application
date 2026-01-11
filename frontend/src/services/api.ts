// frontend/services/api.ts

export interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
  user_id: string;
}

class ApiService {
  private baseUrl =
    process.env.NEXT_PUBLIC_API_BASE_URL ?? "https://todo-backend-delta-six.vercel.app/api";

  private async request(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<any> {
    const controller = new AbortController();
    const url = `${this.baseUrl}${endpoint}`;

    const headers: HeadersInit = {
      ...(options.headers || {}),
    };

    // Only set JSON header when body exists
    if (options.body) {
      headers["Content-Type"] = "application/json";
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers,
        signal: controller.signal,
      });

      if (!response.ok) {
        let message = `HTTP ${response.status}`;

        try {
          const data = await response.json();
          message = data.detail || message;
        } catch {
          // ignore JSON parse error
        }

        if (response.status === 401) {
          throw new Error("Unauthorized");
        }

        throw new Error(message);
      }

      if (response.status === 204) return null;
      return response.json();
    } catch (error: any) {
      if (error.name === "AbortError") return;
      throw error;
    }
  }

  // ------------------------------
  // Authentication
  // ------------------------------
  signIn(email: string, password: string) {
    return this.request("/auth/signin", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });
  }

  signUp(email: string, password: string) {
    return this.request("/auth/signup", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });
  }

  signOut() {
    return Promise.resolve();
  }

  // ------------------------------
  // Tasks
  // ------------------------------
  getTasks(token: string) {
    return this.request("/tasks", {
      headers: { Authorization: `Bearer ${token}` },
    });
  }

  getTaskById(taskId: string, token: string) {
    return this.request(`/tasks/${taskId}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
  }

  createTask(
    taskData: Omit<Task, "id" | "created_at" | "updated_at" | "user_id">,
    token: string
  ) {
    return this.request("/tasks", {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
      body: JSON.stringify(taskData),
    });
  }

  updateTask(taskId: string, taskData: Partial<Task>, token: string) {
    return this.request(`/tasks/${taskId}`, {
      method: "PUT",
      headers: { Authorization: `Bearer ${token}` },
      body: JSON.stringify(taskData),
    });
  }

  deleteTask(taskId: string, token: string) {
    return this.request(`/tasks/${taskId}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    });
  }

  toggleTaskCompletion(taskId: string, token: string) {
    return this.request(`/tasks/${taskId}/toggle`, {
      method: "PATCH",
      headers: { Authorization: `Bearer ${token}` },
    });
  }
}

export const apiService = new ApiService();
