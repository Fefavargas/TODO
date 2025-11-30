from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseNotAllowed
from .models import Task
from datetime import date


def home(request):
    # Allow creating a task from the home page POST
    if request.method == "POST":
        title = request.POST.get("title")
        due_date_str = request.POST.get("due_date")
        due_date = None
        if due_date_str:
            try:
                due_date = date.fromisoformat(due_date_str)
            except Exception:
                due_date = None
        if title:
            Task.objects.create(title=title, due_date=due_date)
        return redirect("home")

    tasks = Task.objects.all()
    return render(request, "home.html", {"tasks": tasks})


def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    # Only accept POST for updates; the single-page UI posts here
    if request.method == "POST":
        task.title = request.POST.get("title", task.title)
        due_date_str = request.POST.get("due_date")
        if due_date_str:
            try:
                task.due_date = date.fromisoformat(due_date_str)
            except Exception:
                task.due_date = None
        else:
            task.due_date = None
        # resolved checkbox: present when checked
        task.resolved = True if request.POST.get("resolved") in ["on", "true", "1"] else False
        task.save()
        return redirect("home")
    # For non-POST, just redirect to home (no separate update page)
    return redirect("home")

def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect("home")

def toggle_complete(request, pk):
    """Toggle completed state. Accepts POST (AJAX or form). For GET, redirect home.

    Returns JSON {ok: true, completed: bool} for POST requests.
    """
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.resolved = not task.resolved
        task.save()
        return JsonResponse({"ok": True, "resolved": task.resolved})
    # fallback for non-POST (e.g., browser link) keep redirect behavior
    return redirect("home")