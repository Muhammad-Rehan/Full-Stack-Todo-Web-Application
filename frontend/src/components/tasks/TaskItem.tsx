'use client';

import React, { useState, memo } from 'react';
import { Task } from '../../services/api';
import { useApp } from '../../contexts/AppContext';

interface TaskItemProps {
  task: Task;
  onDelete: (id: string) => void;
  onToggle: (id: string) => void;
}

const TaskItemComponent = ({ task, onDelete, onToggle }: TaskItemProps) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);
  const [editDescription, setEditDescription] = useState(task.description || '');
  const [isUpdating, setIsUpdating] = useState(false);

  const { updateTask } = useApp();

  const handleEdit = async () => {
    if (!editTitle.trim()) return;

    setIsUpdating(true);
    try {
      await updateTask(task.id, {
        title: editTitle,
        description: editDescription,
      });
      setIsEditing(false);
    } catch (error) {
      // Error updating task - error is handled by context
    } finally {
      setIsUpdating(false);
    }
  };

  return (
    <li className="p-4 hover:bg-gray-50" role="listitem">
      {isEditing ? (
        <div className="border rounded p-3 bg-white" role="form" aria-label={`Editing task: ${task.title}`}>
          <label htmlFor="edit-title" className="sr-only">Task Title</label>
          <input
            id="edit-title"
            type="text"
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            className="w-full p-2 border rounded mb-2 text-gray-900"
            placeholder="Task title"
            aria-label="Edit task title"
            autoFocus
          />
          <label htmlFor="edit-description" className="sr-only">Task Description</label>
          <textarea
            id="edit-description"
            value={editDescription}
            onChange={(e) => setEditDescription(e.target.value)}
            className="w-full p-2 border rounded mb-2 text-gray-900"
            placeholder="Task description"
            rows={2}
            aria-label="Edit task description"
          />
          <div className="flex flex-col sm:flex-row justify-end space-y-2 sm:space-y-0 sm:space-x-2">
            <button
              onClick={() => setIsEditing(false)}
              className="px-3 py-1 text-sm bg-gray-200 rounded hover:bg-gray-300 sm:w-auto"
              disabled={isUpdating}
              aria-label="Cancel editing"
            >
              Cancel
            </button>
            <button
              onClick={handleEdit}
              className="px-3 py-1 text-sm bg-indigo-600 text-white rounded hover:bg-indigo-700 sm:w-auto"
              disabled={isUpdating}
              aria-label="Save changes"
            >
              {isUpdating ? 'Saving...' : 'Save'}
            </button>
          </div>
        </div>
      ) : (
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="flex items-start sm:items-center">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={() => onToggle(task.id)}
              className="h-4 w-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500 mt-0.5 sm:mt-0"
              id={`task-checkbox-${task.id}`}
              aria-label={task.completed ? `Mark task "${task.title}" as incomplete` : `Mark task "${task.title}" as complete`}
            />
            <div className="ml-3 flex-1 min-w-0">
              <label
                htmlFor={`task-checkbox-${task.id}`}
                className={`text-sm font-medium block ${
                  task.completed ? 'text-gray-500 line-through' : 'text-gray-900'
                }`}
              >
                {task.title}
              </label>
              {task.description && (
                <p className="text-sm text-gray-500 mt-1 truncate" aria-label={`Description: ${task.description}`}>{task.description}</p>
              )}
            </div>
          </div>
          <div className="flex items-center justify-between sm:justify-end space-x-2">
            <span className="text-xs text-gray-500 sm:hidden" aria-label={`Created on ${new Date(task.created_at).toLocaleDateString()}`}>
              {new Date(task.created_at).toLocaleDateString()}
            </span>
            <span className="hidden sm:block text-xs text-gray-500" aria-label={`Created on ${new Date(task.created_at).toLocaleDateString()}`}>
              {new Date(task.created_at).toLocaleDateString()}
            </span>
            <button
              onClick={() => setIsEditing(true)}
              className="text-blue-600 hover:text-blue-900"
              aria-label={`Edit task "${task.title}"`}
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-5 w-5"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
              </svg>
            </button>
            <button
              onClick={() => onDelete(task.id)}
              className="text-red-600 hover:text-red-900"
              aria-label={`Delete task "${task.title}"`}
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-5 w-5"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fillRule="evenodd"
                  d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z"
                  clipRule="evenodd"
                />
              </svg>
            </button>
          </div>
        </div>
      )}
    </li>
  );
}

export const TaskItem = memo(TaskItemComponent, (prevProps, nextProps) =>
  prevProps.task.id === nextProps.task.id &&
  prevProps.task.title === nextProps.task.title &&
  prevProps.task.description === nextProps.task.description &&
  prevProps.task.completed === nextProps.task.completed &&
  prevProps.task.created_at === nextProps.task.created_at &&
  prevProps.task.updated_at === nextProps.task.updated_at
);