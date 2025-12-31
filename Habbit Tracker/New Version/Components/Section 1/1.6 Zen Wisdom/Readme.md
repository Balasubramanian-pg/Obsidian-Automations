// Quotes Database
const quotes = [
    { text: "We suffer more often in imagination than in reality.", author: "Seneca" },
    { text: "Well-being is realized by small steps, but is truly no small thing.", author: "Zeno" },
    { text: "The discipline of desire is the background of character.", author: "John Locke" },
    { text: "First say to yourself what you would be; and then do what you have to do.", author: "Epictetus" },
    { text: "Focus on the process, not the outcome.", author: "Zen Proverb" },
    { text: "How you do anything is how you do everything.", author: "Zen Proverb" },
    { text: "Discipline is choosing what you want most over what you want now.", author: "Abraham Lincoln" }
];

// Random Selector
const random = quotes[Math.floor(Math.random() * quotes.length)];

// FIX: Create empty container first, then set innerHTML
const container = dv.el("div", "", { cls: "zen-footer" });

container.innerHTML = `
    <div style="text-align: center; margin-top: 60px; padding: 40px 0; border-top: 1px solid var(--background-modifier-border); opacity: 0.7;">
        <div style="font-family: 'Outfit', serif; font-size: 18px; font-style: italic; margin-bottom: 10px; color: var(--text-normal);">"${random.text}"</div>
        <div style="font-family: 'Outfit', sans-serif; font-size: 12px; text-transform: uppercase; letter-spacing: 2px; color: #FFD60A;">— ${random.author}</div>
    </div>
`;
