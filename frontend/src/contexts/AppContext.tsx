'use client';

import React, {
  createContext,
  useContext,
  useReducer,
  ReactNode,
  useEffect,
} from 'react';
import { Task } from '../types/task';
import { apiService } from '../services/api';

/* =======================
   Types
======================= */

interface User {
  user_id: string;
  email: string;
}

interface LoadingState {
  auth: boolean;
  tasks: boolean;
}

interface AppState {
  user: User | null;
  token: string | null;
  tasks: Task[];
  loadingState: LoadingState;
  error: string | null;
}

type AppAction =
  | { type: 'SET_USER'; payload: { user: User; token: string } }
  | { type: 'LOGOUT' }
  | { type: 'SET_TASKS'; payload: Task[] }
  | { type: 'ADD_TASK'; payload: Task }
  | { type: 'UPDATE_TASK'; payload: Task }
  | { type: 'DELETE_TASK'; payload: string }
  | { type: 'SET_LOADING'; payload: { section: keyof LoadingState; value: boolean } }
  | { type: 'SET_ERROR'; payload: string | null };

/* =======================
   Initial State
======================= */

const initialState: AppState = {
  user: null,
  token: null,
  tasks: [],
  loadingState: {
    auth: false,
    tasks: false,
  },
  error: null,
};

/* =======================
   Reducer
======================= */

const appReducer = (state: AppState, action: AppAction): AppState => {
  switch (action.type) {
    case 'SET_USER':
      return {
        ...state,
        user: action.payload.user,
        token: action.payload.token,
        error: null,
      };

    case 'LOGOUT':
      return { ...initialState };

    case 'SET_TASKS':
      return {
        ...state,
        tasks: action.payload,
        loadingState: { ...state.loadingState, tasks: false },
      };

    case 'ADD_TASK':
      return { ...state, tasks: [...state.tasks, action.payload] };

    case 'UPDATE_TASK':
      return {
        ...state,
        tasks: state.tasks.map(task =>
          task.id === action.payload.id ? action.payload : task
        ),
      };

    case 'DELETE_TASK':
      return {
        ...state,
        tasks: state.tasks.filter(task => task.id !== action.payload),
      };

    case 'SET_LOADING':
      return {
        ...state,
        loadingState: {
          ...state.loadingState,
          [action.payload.section]: action.payload.value,
        },
      };

    case 'SET_ERROR':
      return {
        ...state,
        error: action.payload,
        loadingState: { auth: false, tasks: false },
      };

    default:
      return state;
  }
};

/* =======================
   Context
======================= */

interface AppContextType extends AppState {
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (email: string, password: string) => Promise<void>;
  signOut: () => void;
  fetchTasks: () => Promise<void>;
  createTask: (taskData: Omit<Task, 'id' | 'user_id' | 'created_at'>) => Promise<void>;
  updateTask: (id: string, taskData: Partial<Task>) => Promise<void>;
  deleteTask: (id: string) => Promise<void>;
  toggleTaskCompletion: (id: string) => Promise<void>;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

/* =======================
   Provider
======================= */

export const AppProvider = ({ children }: { children: ReactNode }) => {
  const [state, dispatch] = useReducer(appReducer, initialState);

  /* Restore auth on load */
  useEffect(() => {
    const token = localStorage.getItem('token');
    const user = localStorage.getItem('user');

    if (token && user) {
      try {
        dispatch({
          type: 'SET_USER',
          payload: { token, user: JSON.parse(user) },
        });
      } catch {
        localStorage.clear();
      }
    }
  }, []);

  /* =======================
     Auth Actions
  ======================= */

  const signIn = async (email: string, password: string) => {
    dispatch({ type: 'SET_LOADING', payload: { section: 'auth', value: true } });
    try {
      const data = await apiService.signIn(email, password);

      localStorage.setItem('token', data.token);
      localStorage.setItem(
        'user',
        JSON.stringify({ user_id: data.user_id, email: data.email })
      );

      dispatch({
        type: 'SET_USER',
        payload: {
          token: data.token,
          user: { user_id: data.user_id, email: data.email },
        },
      });
    } catch (err: any) {
      dispatch({ type: 'SET_ERROR', payload: err.message });
      throw err;
    } finally {
      dispatch({ type: 'SET_LOADING', payload: { section: 'auth', value: false } });
    }
  };

  const signUp = async (email: string, password: string) => {
    dispatch({ type: 'SET_LOADING', payload: { section: 'auth', value: true } });
    try {
      const data = await apiService.signUp(email, password);

      localStorage.setItem('token', data.token);
      localStorage.setItem(
        'user',
        JSON.stringify({ user_id: data.user_id, email: data.email })
      );

      dispatch({
        type: 'SET_USER',
        payload: {
          token: data.token,
          user: { user_id: data.user_id, email: data.email },
        },
      });
    } catch (err: any) {
      dispatch({ type: 'SET_ERROR', payload: err.message });
      throw err;
    } finally {
      dispatch({ type: 'SET_LOADING', payload: { section: 'auth', value: false } });
    }
  };

  const signOut = () => {
    localStorage.clear();
    dispatch({ type: 'LOGOUT' });
  };

  /* =======================
     Task Actions
  ======================= */

  const fetchTasks = async () => {
    if (!state.token) return;

    dispatch({ type: 'SET_LOADING', payload: { section: 'tasks', value: true } });
    try {
      const tasks = await apiService.getTasks(state.token);
      dispatch({ type: 'SET_TASKS', payload: tasks });
    } catch (err: any) {
      dispatch({ type: 'SET_ERROR', payload: err.message });
    }
  };

  const createTask = async (taskData: any) => {
    if (!state.token) return;
    const task = await apiService.createTask(taskData, state.token);
    dispatch({ type: 'ADD_TASK', payload: task });
  };

  const updateTask = async (id: string, taskData: Partial<Task>) => {
    if (!state.token) return;
    const task = await apiService.updateTask(id, taskData, state.token);
    dispatch({ type: 'UPDATE_TASK', payload: task });
  };

  const deleteTask = async (id: string) => {
    if (!state.token) return;
    await apiService.deleteTask(id, state.token);
    dispatch({ type: 'DELETE_TASK', payload: id });
  };

  const toggleTaskCompletion = async (id: string) => {
    if (!state.token) return;
    const task = await apiService.toggleTaskCompletion(id, state.token);
    dispatch({ type: 'UPDATE_TASK', payload: task });
  };

  return (
    <AppContext.Provider
      value={{
        ...state,
        signIn,
        signUp,
        signOut,
        fetchTasks,
        createTask,
        updateTask,
        deleteTask,
        toggleTaskCompletion,
      }}
    >
      {children}
    </AppContext.Provider>
  );
};

/* =======================
   Hook
======================= */

export const useApp = () => {
  const ctx = useContext(AppContext);
  if (!ctx) throw new Error('useApp must be used inside AppProvider');
  return ctx;
};
