const addTaskForm = document.getElementById("addTaskForm");
const newTaskInput = document.getElementById("newTaskInput");
const taskList = document.getElementById("taskList");

addTaskForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const title = newTaskInput.value.trim();
  if (!title) return;

  const formData = new FormData();
  formData.append("title", title);

  const res = await fetch("/api/add", { method: "POST", body: formData });
  const task = await res.json();
  appendTask(task);
  newTaskInput.value = "";
});

function appendTask(task) {
  const li = document.createElement("li");
  li.dataset.id = task.id;
  li.className = task.completed ? "completed" : "";
  li.innerHTML = `
    <span class="task-title" contenteditable="true">${task.title}</span>
    <div class="task-actions">
      <button class="toggle-btn">✔</button>
      <button class="delete-btn">🗑</button>
    </div>
  `;
  taskList.appendChild(li);
  bindTaskEvents(li);
}

function bindTaskEvents(li) {
  const id = li.dataset.id;
  const toggleBtn = li.querySelector(".toggle-btn");
  const deleteBtn = li.querySelector(".delete-btn");
  const titleSpan = li.querySelector(".task-title");

  toggleBtn.addEventListener("click", async () => {
    const res = await fetch(`/api/toggle/${id}`, { method: "POST" });
    const data = await res.json();
    li.classList.toggle("completed", data.completed);
  });

  deleteBtn.addEventListener("click", async () => {
    await fetch(`/api/delete/${id}`, { method: "POST" });
    li.remove();
  });

  titleSpan.addEventListener("blur", async () => {
    const newTitle = titleSpan.textContent.trim();
    if (!newTitle) return;
    await fetch(`/api/edit/${id}`, {
      method: "POST",
      body: new URLSearchParams({ title: newTitle }),
    });
  });

  titleSpan.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      titleSpan.blur();
    }
  });
}

// Initialize existing tasks on page load
document.querySelectorAll("#taskList li").forEach(bindTaskEvents);
