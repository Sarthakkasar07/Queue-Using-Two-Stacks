import tkinter as tk
from tkinter import messagebox
from dataclasses import dataclass


class QueueUsingTwoStacks:
    """Queue implementation using two stacks (Python lists)."""

    def __init__(self):
        self.stack1 = []  # Enqueue stack
        self.stack2 = []  # Dequeue stack

    def enqueue(self, value):
        self.stack1.append(value)

    def _move_if_needed(self):
        if not self.stack2:
            while self.stack1:
                self.stack2.append(self.stack1.pop())

    def dequeue(self):
        self._move_if_needed()
        if not self.stack2:
            return None
        return self.stack2.pop()

    def peek(self):
        self._move_if_needed()
        if not self.stack2:
            return None
        return self.stack2[-1]

    def is_empty(self):
        return not self.stack1 and not self.stack2

    def clear(self):
        self.stack1.clear()
        self.stack2.clear()

    def queue_items(self):
        # Front to rear: stack2 top-to-bottom, then stack1 bottom-to-top.
        return list(reversed(self.stack2)) + self.stack1


class QueueVisualizerApp:
    BG = "#101827"
    PANEL = "#182438"
    PANEL_ALT = "#202f46"
    TEXT = "#edf3ff"
    MUTED = "#a8b7d0"
    BLUE = "#4f8cff"
    GREEN = "#28c997"
    ORANGE = "#ffb454"
    RED = "#ff6b78"
    PURPLE = "#a78bfa"
    BORDER = "#31415c"

    def __init__(self, root):
        self.root = root
        self.root.title("Queue Using Two Stacks | DS Visualizer")
        self.root.geometry("1120x790")
        self.root.minsize(950, 700)
        self.root.configure(bg=self.BG)

        self.queue = QueueUsingTwoStacks()
        self.next_value = 10
        self.steps = [
            "1. Enqueue: push the new element onto Stack 1.",
            "2. Dequeue: if Stack 2 is empty, transfer all Stack 1 items to Stack 2.",
            "3. Pop Stack 2 to remove the queue's front element (FIFO).",
        ]
        self.step_index = 0

        self._build_ui()
        self.refresh()
        self._set_step(0, "Ready. Add an item to start the visualization.")

    def _label(self, parent, text, size=10, color=None, bold=False, **kwargs):
        return tk.Label(
            parent, text=text, bg=kwargs.pop("bg", self.PANEL),
            fg=color or self.TEXT, font=("Segoe UI", size, "bold" if bold else "normal"),
            **kwargs
        )

    def _build_ui(self):
        header = tk.Frame(self.root, bg=self.BG)
        header.pack(fill="x", padx=22, pady=(18, 12))

        left = tk.Frame(header, bg=self.BG)
        left.pack(side="left", fill="x", expand=True)
        self._label(left, "DATA STRUCTURES LAB", 9, self.GREEN, True, bg=self.BG).pack(anchor="w")
        self._label(left, "Queue Using Two Stacks", 25, self.TEXT, True, bg=self.BG).pack(anchor="w", pady=(3, 0))
        self._label(left, "Interactive algorithm visualizer • Python + Tkinter", 10, self.MUTED, bg=self.BG).pack(anchor="w", pady=(4, 0))

        pill = tk.Frame(header, bg="#183c3b", padx=12, pady=8)
        pill.pack(side="right", anchor="n")
        self._label(pill, "FIFO  •  FIRST IN, FIRST OUT", 9, self.GREEN, True, bg="#183c3b").pack()

        # Control strip
        controls = tk.Frame(self.root, bg=self.PANEL, highlightbackground=self.BORDER, highlightthickness=1)
        controls.pack(fill="x", padx=22, pady=(0, 14))
        self._label(controls, "OPERATIONS", 9, self.MUTED, True).grid(row=0, column=0, padx=(14, 10), pady=(12, 4), sticky="w")

        self.value_var = tk.StringVar()
        self.value_entry = tk.Entry(
            controls, textvariable=self.value_var, width=15, font=("Segoe UI", 11),
            bg="#0f1725", fg=self.TEXT, insertbackground=self.TEXT,
            relief="flat", highlightthickness=1, highlightbackground=self.BORDER,
            highlightcolor=self.BLUE
        )
        self.value_entry.grid(row=1, column=0, padx=(14, 8), pady=(0, 13), ipady=8)
        self.value_entry.insert(0, "Enter value")
        self.value_entry.bind("<FocusIn>", self._clear_placeholder)
        self.value_entry.bind("<Return>", lambda event: self.enqueue())

        self._button(controls, "＋  Enqueue", self.enqueue, self.BLUE).grid(row=1, column=1, padx=5, pady=(0, 13), ipady=5)
        self._button(controls, "−  Dequeue", self.dequeue, self.RED).grid(row=1, column=2, padx=5, pady=(0, 13), ipady=5)
        self._button(controls, "◎  Peek Front", self.peek, self.PURPLE).grid(row=1, column=3, padx=5, pady=(0, 13), ipady=5)
        self._button(controls, "↻  Next Example", self.next_example, self.GREEN, fg="#071a18").grid(row=1, column=4, padx=5, pady=(0, 13), ipady=5)
        self._button(controls, "Clear", self.clear, self.PANEL_ALT).grid(row=1, column=5, padx=(5, 14), pady=(0, 13), ipady=5)
        for col in range(6):
            controls.grid_columnconfigure(col, weight=1 if col == 0 else 0)

        # Status strip
        status = tk.Frame(self.root, bg=self.PANEL_ALT, padx=14, pady=10)
        status.pack(fill="x", padx=22, pady=(0, 14))
        self._label(status, "CURRENT STATUS", 8, self.MUTED, True, bg=self.PANEL_ALT).pack(anchor="w")
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = self._label(status, "", 10, self.TEXT, bg=self.PANEL_ALT, justify="left", wraplength=1030)
        self.status_label.configure(textvariable=self.status_var)
        self.status_label.pack(anchor="w", pady=(4, 0))

        # Main visual panels
        self._label(self.root, "LIVE VISUALIZATION", 9, self.MUTED, True, bg=self.BG).pack(anchor="w", padx=24, pady=(0, 8))
        panels = tk.Frame(self.root, bg=self.BG)
        panels.pack(fill="both", expand=True, padx=22)
        panels.grid_columnconfigure(0, weight=3, uniform="visual")
        panels.grid_columnconfigure(1, weight=2, uniform="visual")
        panels.grid_rowconfigure(0, weight=1)
        panels.grid_rowconfigure(1, weight=1)

        queue_panel = self._panel(panels, "QUEUE", "Front  →  Rear", self.GREEN)
        queue_panel.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 10), pady=(0, 10))
        self.queue_canvas = tk.Canvas(queue_panel, bg=self.PANEL, highlightthickness=0, height=390)
        self.queue_canvas.pack(fill="both", expand=True, padx=10, pady=(2, 10))
        self.queue_canvas.bind("<Configure>", lambda event: self._draw_queue())

        s1_panel = self._panel(panels, "STACK 1", "PUSH / ENQUEUE", self.BLUE)
        s1_panel.grid(row=0, column=1, sticky="nsew", pady=(0, 10))
        self.s1_canvas = tk.Canvas(s1_panel, bg=self.PANEL, highlightthickness=0, height=190)
        self.s1_canvas.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self.s1_canvas.bind("<Configure>", lambda event: self._draw_stack(self.s1_canvas, self.queue.stack1, self.BLUE, "BOTTOM", "TOP"))

        s2_panel = self._panel(panels, "STACK 2", "POP / DEQUEUE", self.ORANGE)
        s2_panel.grid(row=1, column=1, sticky="nsew")
        self.s2_canvas = tk.Canvas(s2_panel, bg=self.PANEL, highlightthickness=0, height=190)
        self.s2_canvas.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self.s2_canvas.bind("<Configure>", lambda event: self._draw_stack(self.s2_canvas, self.queue.stack2, self.ORANGE, "BOTTOM", "TOP"))

        # Explanation / complexity footer
        footer = tk.Frame(self.root, bg=self.BG)
        footer.pack(fill="x", padx=22, pady=(0, 16))
        expl = tk.Frame(footer, bg=self.PANEL, highlightbackground=self.BORDER, highlightthickness=1, padx=13, pady=10)
        expl.pack(side="left", fill="both", expand=True, padx=(0, 8))
        self._label(expl, "ALGORITHM STEP", 8, self.MUTED, True).pack(anchor="w")
        self.step_var = tk.StringVar()
        self._label(expl, "", 10, self.TEXT, bg=self.PANEL, wraplength=560, justify="left").pack(anchor="w", pady=(4, 0))
        self.step_label = expl.winfo_children()[-1]
        self.step_label.configure(textvariable=self.step_var)

        complexity = tk.Frame(footer, bg=self.PANEL, highlightbackground=self.BORDER, highlightthickness=1, padx=13, pady=10)
        complexity.pack(side="right", fill="y")
        self._label(complexity, "COMPLEXITY", 8, self.MUTED, True).pack(anchor="w")
        self._label(complexity, "Enqueue: O(1)", 9, self.BLUE, True).pack(anchor="w", pady=(4, 0))
        self._label(complexity, "Dequeue: amortized O(1)", 9, self.ORANGE, True).pack(anchor="w", pady=(2, 0))
        self._label(complexity, "Space: O(n)", 9, self.GREEN, True).pack(anchor="w", pady=(2, 0))

    def _button(self, parent, text, command, color, fg="#ffffff"):
        return tk.Button(
            parent, text=text, command=command, bg=color, fg=fg,
            activebackground=color, activeforeground=fg, relief="flat",
            bd=0, cursor="hand2", font=("Segoe UI", 9, "bold"),
            padx=11, pady=7
        )

    def _panel(self, parent, title, subtitle, accent):
        panel = tk.Frame(parent, bg=self.PANEL, highlightbackground=self.BORDER, highlightthickness=1)
        top = tk.Frame(panel, bg=self.PANEL)
        top.pack(fill="x", padx=12, pady=(10, 3))
        tk.Frame(top, bg=accent, width=4, height=30).pack(side="left", padx=(0, 9))
        txt = tk.Frame(top, bg=self.PANEL)
        txt.pack(side="left", fill="x", expand=True)
        self._label(txt, title, 11, self.TEXT, True).pack(anchor="w")
        self._label(txt, subtitle, 8, self.MUTED).pack(anchor="w", pady=(1, 0))
        return panel

    def _clear_placeholder(self, _event=None):
        if self.value_entry.get() == "Enter value":
            self.value_entry.delete(0, tk.END)

    def _set_step(self, index, status):
        self.step_index = index
        self.step_var.set(self.steps[index])
        self.status_var.set(status)

    def enqueue(self):
        value = self.value_var.get().strip()
        if not value or value == "Enter value":
            messagebox.showwarning("Value required", "Please enter a value to enqueue.")
            self.value_entry.focus_set()
            return
        self.queue.enqueue(value)
        self.value_var.set("")
        self.refresh()
        self._set_step(0, f"ENQUEUE SUCCESS: '{value}' was pushed onto Stack 1. The queue order is preserved.")
        self.value_entry.focus_set()

    def dequeue(self):
        if self.queue.is_empty():
            self._set_step(2, "QUEUE EMPTY: there is no item to dequeue.")
            messagebox.showinfo("Queue Empty", "Add an item before using Dequeue.")
            return
        moved = not self.queue.stack2 and bool(self.queue.stack1)
        item = self.queue.dequeue()
        self.refresh()
        if moved:
            self._set_step(1, f"TRANSFER + DEQUEUE: Stack 2 was empty, so items were transferred from Stack 1. '{item}' was then removed from the front.")
        else:
            self._set_step(2, f"DEQUEUE SUCCESS: '{item}' was popped from Stack 2 (the front of the queue).")

    def peek(self):
        item = self.queue.peek()
        if item is None:
            self._set_step(2, "QUEUE EMPTY: there is no front item to peek at.")
        else:
            self._set_step(2, f"PEEK: the front item is '{item}'. No item was removed.")

    def clear(self):
        self.queue.clear()
        self.refresh()
        self._set_step(0, "QUEUE CLEARED: both stacks are now empty.")

    def next_example(self):
        examples = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        value = examples[self.next_value % len(examples)]
        self.next_value += 1
        self.queue.enqueue(value)
        self.refresh()
        self._set_step(0, f"DEMO ENQUEUE: '{value}' was added to Stack 1. Try Dequeue to watch the two-stack transfer.")

    def refresh(self):
        self._draw_queue()
        self._draw_stack(self.s1_canvas, self.queue.stack1, self.BLUE, "BOTTOM", "TOP")
        self._draw_stack(self.s2_canvas, self.queue.stack2, self.ORANGE, "BOTTOM", "TOP")

    def _draw_queue(self):
        if not hasattr(self, "queue_canvas"):
            return
        c = self.queue_canvas
        c.delete("all")
        w = max(c.winfo_width(), 300)
        h = max(c.winfo_height(), 300)
        items = self.queue.queue_items()
        c.create_text(18, 18, text="FRONT", fill=self.GREEN, font=("Segoe UI", 9, "bold"), anchor="w")
        c.create_text(w - 18, 18, text="REAR", fill=self.PURPLE, font=("Segoe UI", 9, "bold"), anchor="e")
        c.create_line(58, 42, w - 58, 42, fill=self.BORDER, width=2, arrow=tk.LAST)
        if not items:
            c.create_rectangle(22, 70, w - 22, h - 28, outline=self.BORDER, width=2, dash=(5, 4))
            c.create_text(w / 2, h / 2, text="Queue is empty\nEnqueue an item to begin", fill=self.MUTED, font=("Segoe UI", 12), justify="center")
            return
        margin = 24
        gap = 8
        available = w - 2 * margin
        box_w = min(82, max(42, (available - gap * (len(items) - 1)) / max(len(items), 1)))
        total = len(items) * box_w + (len(items) - 1) * gap
        start_x = (w - total) / 2
        y1 = max(88, h / 2 - 30)
        y2 = y1 + 62
        for i, item in enumerate(items):
            x1 = start_x + i * (box_w + gap)
            x2 = x1 + box_w
            color = self.GREEN if i == 0 else self.PANEL_ALT
            outline = self.GREEN if i == 0 else self.BORDER
            c.create_rectangle(x1, y1, x2, y2, fill=color, outline=outline, width=2)
            c.create_text((x1+x2)/2, (y1+y2)/2, text=str(item)[:12], fill="#071a18" if i == 0 else self.TEXT, font=("Segoe UI", 10, "bold"))
            c.create_text((x1+x2)/2, y2 + 18, text="FRONT" if i == 0 else ("REAR" if i == len(items)-1 else str(i+1)), fill=self.MUTED, font=("Segoe UI", 8))
        c.create_text(w / 2, h - 28, text=f"{len(items)} item(s)  •  FIFO order", fill=self.MUTED, font=("Segoe UI", 9))

    def _draw_stack(self, canvas, values, accent, bottom_label, top_label):
        if not canvas.winfo_exists():
            return
        canvas.delete("all")
        w = max(canvas.winfo_width(), 220)
        h = max(canvas.winfo_height(), 140)
        x1, x2 = w * 0.27, w * 0.73
        y_top, y_bottom = 24, h - 25
        canvas.create_line(x1 - 10, y_bottom, x2 + 10, y_bottom, fill=self.BORDER, width=3)
        canvas.create_text(x1 - 18, y_bottom, text=bottom_label, fill=self.MUTED, font=("Segoe UI", 7), anchor="e")
        canvas.create_text(x2 + 18, y_top, text=top_label, fill=accent, font=("Segoe UI", 7, "bold"), anchor="w")
        if not values:
            canvas.create_text(w / 2, h / 2, text="Empty stack", fill=self.MUTED, font=("Segoe UI", 10))
            return
        box_h = min(28, max(18, (h - 42) / max(len(values), 1)))
        visible = values[-max(1, int((h - 44) / box_h)):]
        for i, value in enumerate(visible):
            y2 = y_bottom - i * (box_h + 3)
            y1b = y2 - box_h
            canvas.create_rectangle(x1, y1b, x2, y2, fill=accent, outline=accent, width=1)
            canvas.create_text(w / 2, (y1b + y2) / 2, text=str(value)[:12], fill="#101827", font=("Segoe UI", 9, "bold"))
        canvas.create_text(w - 10, 12, text=f"{len(values)} item(s)", fill=self.MUTED, font=("Segoe UI", 8), anchor="e")


def main():
    root = tk.Tk()
    QueueVisualizerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
