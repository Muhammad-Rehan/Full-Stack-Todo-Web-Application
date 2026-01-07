'use client';

import React, { useState, useEffect, memo } from 'react';
import { TaskItem } from './TaskItem';
import { LoadingSpinner } from '../common/LoadingSpinner';
import { useApp } from '../../contexts/AppContext';

const TaskListComponent = () => {
  const {
    user,
    tasks,
    loadingState,
    error,
    fetchTasks,
    deleteTask,
    toggleTaskCompletion,
  } = useApp();

  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all');

  /* Fetch tasks once when user is available */
  useEffect(() => {
    if (user?.user_id) {
      fetchTasks();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user?.user_id]);

  const filteredTasks = tasks.filter(task => {
    if (filter === 'active') return !task.completed;
    if (filter === 'completed') return task.completed;
    return true;
  });

  /* Initial loading (no tasks yet) */
  if (loadingState.tasks && tasks.length === 0) {
    return (
      <div className="flex justify-center items-center h-64">
        <LoadingSpinner size="lg" text="Loading tasks..." />
      </div>
    );
  }

  /* Error state */
  if (error) {
    return (
      <div className="bg-red-50 border-l-4 border-red-400 p-4 mb-4">
        <p className="text-sm text-red-700">
          <span className="font-medium">Error:</span> {error}
        </p>
        <button
          onClick={fetchTasks}
          className="mt-2 text-sm text-red-600 underline"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="bg-white shadow sm:rounded-md">
      <div className="p-4 border-b flex justify-between items-center">
        <h3 className="text-lg font-medium">Tasks</h3>

        <div className="flex space-x-2">
          {(['all', 'active', 'completed'] as const).map(f => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-3 py-1 text-sm rounded-md ${
                filter === f
                  ? 'bg-indigo-600 text-white'
                  : 'bg-gray-200 text-gray-700'
              }`}
            >
              {f[0].toUpperCase() + f.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {/* Background refresh */}
      {loadingState.tasks && tasks.length > 0 ? (
        <div className="p-4 flex justify-center">
          <LoadingSpinner size="sm" text="Updating tasks..." />
        </div>
      ) : filteredTasks.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          No tasks found.
        </div>
      ) : (
        <ul className="divide-y">
          {filteredTasks.map(task => (
            <TaskItem
              key={task.id}
              task={task}
              onDelete={deleteTask}
              onToggle={toggleTaskCompletion}
            />
          ))}
        </ul>
      )}
    </div>
  );
};

export const TaskList = memo(TaskListComponent);
