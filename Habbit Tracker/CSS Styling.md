## Step 3: CSS Styling

Add this to your `obsidian.css` file (in `.obsidian/snippets/`):

```css
/* Habit Dashboard Styles */
.habit-dashboard {
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
}

.habit-controls {
    display: flex;
    gap: 10px;
    margin-bottom: 30px;
    justify-content: center;
}

.habit-controls button {
    padding: 10px 20px;
    border: 2px solid var(--interactive-accent);
    background: transparent;
    color: var(--text-normal);
    border-radius: 8px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.2s;
}

.habit-controls button:hover {
    background: var(--interactive-accent);
    color: var(--text-on-accent);
}

.habit-controls button.active {
    background: var(--interactive-accent);
    color: var(--text-on-accent);
}

.streak-container {
    margin-bottom: 40px;
}

.streak-container h3 {
    text-align: center;
    margin-bottom: 20px;
}

.streak-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 15px;
}

.streak-card {
    background: var(--background-secondary);
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    border: 2px solid var(--background-modifier-border);
}

.streak-label {
    font-size: 0.9em;
    color: var(--text-muted);
    margin-bottom: 10px;
}

.streak-current {
    font-size: 2.5em;
    font-weight: bold;
    color: var(--interactive-accent);
    margin-bottom: 5px;
}

.streak-max {
    font-size: 0.85em;
    color: var(--text-muted);
}

.chart-container {
    margin-bottom: 40px;
    background: var(--background-secondary);
    padding: 20px;
    border-radius: 12px;
}

.chart-container h3 {
    margin-bottom: 20px;
    text-align: center;
}

.chart-container canvas {
    max-height: 400px;
}
```
