
import { useCallback, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

const emptyForm = {
  title: "",
  description: "",
  completed: false,
};

export default function Dashboard() {
  const navigate = useNavigate();

  const [tasks, setTasks] = useState([]);
  const [form, setForm] = useState(emptyForm);
  const [editingId, setEditingId] = useState(null);
  const [editForm, setEditForm] = useState(emptyForm);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const handleUnauthorized = useCallback((err) => {
    if (err.response?.status === 401) {
      sessionStorage.removeItem("access_token");
      navigate("/login", { replace: true });
      return true;
    }
    return false;
  }, [navigate]);

  const fetchTasks = useCallback(async () => {
    setLoading(true);
    setError("");

    try {
      const response = await api.get("/tasks/");
      setTasks(response.data);
    } catch (err) {
      if (!handleUnauthorized(err)) {
        setError(err.response?.data?.detail || "Could not load tasks.");
      }
    } finally {
      setLoading(false);
    }
  }, [handleUnauthorized]);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  async function handleCreate(event) {
    event.preventDefault();
    setSaving(true);
    setError("");
    setMessage("");

    try {
      await api.post("/tasks/", {
        ...form,
        title: form.title.trim(),
        description: form.description.trim() || null,
      });

      setForm(emptyForm);
      setMessage("Task created successfully.");
      await fetchTasks();
    } catch (err) {
      if (!handleUnauthorized(err)) {
        setError(err.response?.data?.detail || "Could not create task.");
      }
    } finally {
      setSaving(false);
    }
  }

  function startEditing(task) {
    setEditingId(task.id);
    setEditForm({
      title: task.title,
      description: task.description || "",
      completed: task.completed,
    });
    setError("");
    setMessage("");
  }

  async function handleUpdate(event) {
    event.preventDefault();
    setSaving(true);
    setError("");
    setMessage("");

    try {
      await api.put(`/tasks/${editingId}`, {
        ...editForm,
        title: editForm.title.trim(),
        description: editForm.description.trim() || null,
      });

      setEditingId(null);
      setMessage("Task updated successfully.");
      await fetchTasks();
    } catch (err) {
      if (!handleUnauthorized(err)) {
        setError(err.response?.data?.detail || "Could not update task.");
      }
    } finally {
      setSaving(false);
    }
  }

  async function handleToggle(task) {
    setError("");
    setMessage("");

    try {
      await api.put(`/tasks/${task.id}`, {
        completed: !task.completed,
      });

      await fetchTasks();
    } catch (err) {
      if (!handleUnauthorized(err)) {
        setError(err.response?.data?.detail || "Could not update task status.");
      }
    }
  }

  async function handleDelete(taskId) {
    if (!window.confirm("Are you sure you want to delete this task?")) {
      return;
    }

    setError("");
    setMessage("");

    try {
      await api.delete(`/tasks/${taskId}`);
      setTasks((current) => current.filter((task) => task.id !== taskId));
      setMessage("Task deleted successfully.");
    } catch (err) {
      if (!handleUnauthorized(err)) {
        setError(err.response?.data?.detail || "Could not delete task.");
      }
    }
  }

  function handleLogout() {
    sessionStorage.removeItem("access_token");
    navigate("/login", { replace: true });
  }

  return (
    <main className="min-h-screen bg-slate-50 px-4 py-8 sm:px-8">
      <div className="mx-auto max-w-4xl space-y-6">
        <header className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">
              My Task Dashboard
            </h1>
            <p className="mt-1 text-sm text-slate-600">
              Organize your work, one task at a time.
            </p>
          </div>

          <Button variant="outline" onClick={handleLogout}>
            Logout
          </Button>
        </header>

        {error && (
          <p role="alert" className="rounded-md bg-red-50 p-3 text-sm text-red-700">
            {error}
          </p>
        )}

        {message && (
          <p role="status" className="rounded-md bg-green-50 p-3 text-sm text-green-700">
            {message}
          </p>
        )}

        <Card>
          <CardHeader>
            <CardTitle>Create a new task</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleCreate} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="new-title">Title</Label>
                <Input
                  id="new-title"
                  placeholder="e.g. Learn FastAPI"
                  value={form.title}
                  onChange={(event) =>
                    setForm({ ...form, title: event.target.value })
                  }
                  minLength={1}
                  maxLength={200}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="new-description">Description</Label>
                <Input
                  id="new-description"
                  placeholder="Optional details"
                  value={form.description}
                  onChange={(event) =>
                    setForm({ ...form, description: event.target.value })
                  }
                />
              </div>

              <Button type="submit" disabled={saving}>
                {saving ? "Saving..." : "Create task"}
              </Button>
            </form>
          </CardContent>
        </Card>

        <section className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold">Your tasks</h2>
            <Button
              variant="outline"
              size="sm"
              onClick={fetchTasks}
              disabled={loading}
            >
              Refresh
            </Button>
          </div>

          {loading ? (
            <p className="text-sm text-slate-600">Loading tasks...</p>
          ) : tasks.length === 0 ? (
            <Card>
              <CardContent className="py-10 text-center text-slate-600">
                No tasks yet. Create your first task above.
              </CardContent>
            </Card>
          ) : (
            tasks.map((task) => (
              <Card key={task.id}>
                <CardContent className="space-y-4 py-5">
                  {editingId === task.id ? (
                    <form onSubmit={handleUpdate} className="space-y-4">
                      <div className="space-y-2">
                        <Label htmlFor={`edit-title-${task.id}`}>Title</Label>
                        <Input
                          id={`edit-title-${task.id}`}
                          value={editForm.title}
                          onChange={(event) =>
                            setEditForm({
                              ...editForm,
                              title: event.target.value,
                            })
                          }
                          minLength={1}
                          maxLength={200}
                          required
                        />
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor={`edit-description-${task.id}`}>
                          Description
                        </Label>
                        <Input
                          id={`edit-description-${task.id}`}
                          value={editForm.description}
                          onChange={(event) =>
                            setEditForm({
                              ...editForm,
                              description: event.target.value,
                            })
                          }
                        />
                      </div>

                      <label className="flex items-center gap-2 text-sm">
                        <input
                          type="checkbox"
                          checked={editForm.completed}
                          onChange={(event) =>
                            setEditForm({
                              ...editForm,
                              completed: event.target.checked,
                            })
                          }
                        />
                        Completed
                      </label>

                      <div className="flex gap-2">
                        <Button type="submit" disabled={saving}>
                          {saving ? "Saving..." : "Save changes"}
                        </Button>
                        <Button
                          type="button"
                          variant="outline"
                          onClick={() => setEditingId(null)}
                          disabled={saving}
                        >
                          Cancel
                        </Button>
                      </div>
                    </form>
                  ) : (
                    <>
                      <div className="flex items-start gap-3">
                        <input
                          type="checkbox"
                          className="mt-1 size-4"
                          checked={task.completed}
                          onChange={() => handleToggle(task)}
                          aria-label={`Mark ${task.title} as ${
                            task.completed ? "incomplete" : "completed"
                          }`}
                        />

                        <div className="min-w-0 flex-1">
                          <h3
                            className={`font-semibold ${
                              task.completed
                                ? "text-slate-500 line-through"
                                : ""
                            }`}
                          >
                            {task.title}
                          </h3>
                          <p className="mt-1 whitespace-pre-wrap break-words text-sm text-slate-600">
                            {task.description || "No description"}
                          </p>
                          <p className="mt-2 text-xs text-slate-500">
                            {task.completed ? "Completed" : "Pending"}
                          </p>
                        </div>
                      </div>

                      <div className="flex gap-2">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => startEditing(task)}
                        >
                          Edit
                        </Button>
                        <Button
                          variant="destructive"
                          size="sm"
                          onClick={() => handleDelete(task.id)}
                        >
                          Delete
                        </Button>
                      </div>
                    </>
                  )}
                </CardContent>
              </Card>
            ))
          )}
        </section>
      </div>
    </main>
  );
}
