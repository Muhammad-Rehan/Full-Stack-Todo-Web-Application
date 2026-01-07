'use client';

import React, { useState, memo, useCallback } from 'react';
import { useApp } from '../../contexts/AppContext';


interface TaskFormProps {
  onClose?: () => void;
}

const TaskFormComponent = ({ onClose }: TaskFormProps) => {
  const { createTask, loadingState, error } = useApp();
  const { tasks: loading } = loadingState;
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim()) {
      alert('Title is required');
      return;
    }

    try {
      await createTask({
        title: title.trim(),
        description: description.trim(),
        completed: false,
        updated_at: ''
      });

      setTitle('');
      setDescription('');

      if (onClose) {
        onClose();
      }
    } catch (err) {
      // Error creating task - error is handled by context
    }
  };

  return (
    <div className="bg-white shadow rounded-lg p-4 sm:p-6" role="region" aria-labelledby="task-form-title">
      <h3 id="task-form-title" className="text-lg font-medium text-gray-900 mb-4">Create New Task</h3>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert" aria-live="polite">
          <span className="block sm:inline">{error}</span>
        </div>
      )}

      <form onSubmit={handleSubmit} role="form" aria-label="Create new task form">
        <div className="mb-4">
          <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
            Title *
          </label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md p-2 text-gray-900"
            placeholder="Task title"
            required
            aria-describedby="title-error"
          />
          <div id="title-error" className="sr-only" aria-live="polite">
            {title.trim() ? '' : 'Title is required'}
          </div>
        </div>

        <div className="mb-4">
          <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
            Description
          </label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={3}
            className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md p-2 text-gray-900"
            placeholder="Task description (optional)"
            aria-label="Task description"
          />
        </div>

        <div className="flex flex-col sm:flex-row sm:justify-end space-y-2 sm:space-y-0 sm:space-x-3">
          {onClose && (
            <button
              type="button"
              onClick={onClose}
              className="inline-flex items-center justify-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:w-auto"
              aria-label="Cancel creating task"
            >
              Cancel
            </button>
          )}
          <button
            type="submit"
            disabled={loading}
            className="inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 sm:w-auto"
            aria-busy={loading}
          >
            {loading ? 'Creating...' : 'Create Task'}
          </button>
        </div>
      </form>
    </div>
  );
}

export const TaskForm = memo(TaskFormComponent);