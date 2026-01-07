'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useApp } from '../../contexts/AppContext';
import { TaskForm } from '../../components/tasks/TaskForm';
import { TaskList } from '../../components/tasks/TaskList';

const DashboardPage = () => {
  const router = useRouter();
  const { user, loadingState, signOut } = useApp();
  const [showForm, setShowForm] = useState(false);

  // Redirect if user is not authenticated
  useEffect(() => {
    if (!loadingState.auth && !user) {
      router.push('/');
    }
  }, [user, loadingState.auth, router]);

  const handleSignOut = () => {
    signOut();
    router.push('/');
  };

  // Show loading while auth state is being determined
  if (loadingState.auth || !user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        Loading...
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
          <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4">
            <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">Todo Dashboard</h1>
            <div className="flex items-center justify-between w-full sm:w-auto gap-4">
              <span className="text-gray-700 text-sm sm:text-base">
                Welcome, {user.email.split('@')[0]}
              </span>
              <button
                onClick={() => setShowForm(!showForm)}
                className="sm:hidden bg-indigo-600 text-white px-3 py-1.5 rounded-md text-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
              >
                {showForm ? 'Cancel' : '+'}
              </button>
              <button
                onClick={handleSignOut}
                className="bg-red-600 text-white px-3 py-1.5 rounded-md text-sm hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 whitespace-nowrap"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center mb-6 gap-4">
          <h2 className="text-xl sm:text-2xl font-semibold text-gray-800">Your Tasks</h2>
          <button
            onClick={() => setShowForm(!showForm)}
            className="hidden sm:block bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
          >
            {showForm ? 'Cancel' : 'Add New Task'}
          </button>
        </div>

        {showForm && (
          <div className="mb-6">
            <TaskForm onClose={() => setShowForm(false)} />
          </div>
        )}

        <TaskList />
      </main>
    </div>
  );
};

export default DashboardPage;
