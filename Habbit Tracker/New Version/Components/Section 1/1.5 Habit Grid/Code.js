const folder = "2. Daily Reflection";
const startDate = dv.date("2025-11-22");
const endDate = dv.date("2025-11-28");

/* --------------------------------------------------
   ICON HELPERS
-------------------------------------------------- */
const createIcon = (path) =>
  `<svg viewBox="0 0 512 512" width="18" height="18">
     <path d="${path}"/>
   </svg>`;

const checkIcon =
  `<svg viewBox="0 0 448 512" width="14" height="14">
     <path d="M438.6 105.4c12.5 12.5 12.5 32.8 0 45.3l-256 256c-12.5 12.5-32.8 12.5-45.3 0l-128-128c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0L160 338.7 393.4 105.4z"/>
   </svg>`;

/* --------------------------------------------------
   HABITS (icons unchanged) - TRUNCATED FOR BREVITY
-------------------------------------------------- */
const habitsMap = [ 
  { name: "Exercise", icon: "M176 48a48 48 0 1 0 0 96 48 48 0 1 0 0-96zM110.8 221l-36.6 62.4c-8.9 15.1-4.7 34.6 9.8 44.4s35.3 5.9 44.2-9.2L162 260.7l23 60.3L95.5 457.7c-6.2 16.5 2 34.9 18.5 41.1s34.9-2 41.1-18.5l94.1-149.2c6.6-10.5 7.9-23.5 3.4-35.1l-22.9-60 52.6 30.5c15.2 8.8 34.7 3.6 43.5-11.6s3.6-34.7-11.6-43.5l-82.5-47.9c-11.8-6.9-26.6-6-37.6 2.1L128 214.3l17.2-29.4c8.9-15.1 4.7-34.6-9.8-44.4s-35.3-5.9-44.2 9.2L42 219c-8.5 14.5-4 33.1 10.1 42s33.7 4.5 42.3-9.9L110.8 221z" }, 
  { name: "Read", icon: "M472.9 64h-384C62.8 64 32 88 32 118v345.1c0 30 30.8 53.6 57 42.6 24-10.1 42-20.3 64-20.3 22 0 40 10.2 64 20.3 24 10.1 42 20.3 64 20.3 22 0 40-10.2 64-20.3 24-10.1 42-20.3 64-20.3 24 0 52.1 19.3 71.3 7.8 17.6-10.5 31.7-27.1 31.7-52.1V128c0-35.3-28.7-64-64-64zM240 432c-23.2 0-41.2 9.5-64 20.3-22.8 10.8-51.2 12.8-59.5 6.6V124.6c13.7-6 32-8.6 48-8.6 34.2 0 75.5 14.8 75.5 14.8V432z" }, 
  { name: "Drink water", icon: "M256 512A128 128 0 1 0 256 256a128 128 0 1 0 0 256zM368.4 206c11.9 14.2 10 35.3-4.2 47.2s-35.3 10-47.2-4.2C300.9 230 281.3 216 256 216c-18.4 0-35.3 7.8-53.7 16.2C182.2 241.3 164.7 250 144 250c-26.2 0-45.3-15-58.2-31.5-11.7-15-9.3-36.6 5.7-48.3s36.6-9.3 48.3 5.7c2.4 3 8 9.5 18.5 12.8 13.9 4.4 30.7-3.2 49.3-11.8C228.6 167 252 156.3 282.8 162.7c17.6 3.7 34.5 13 49.8 24.3 12.4 9.1 23.3 12.3 35.8 19z" }, 
  { name: "Meditate", icon: "M175 160c-26.5 0-48-21.5-48-48S148.5 64 175 64s48 21.5 48 48-21.5 48-48 48zM337 160c-26.5 0-48-21.5-48-48S310.5 64 337 64s48 21.5 48 48-21.5 48-48 48zM413 252c-21.6 3.1-39.6 18.4-53.6 34-31.8 35.5-62.8 40.5-91.8 41.5-5.1.2-10.2.3-15.3.3-32.9 0-61.9-9.1-85.3-26.6-26.2-19.5-35.5-38.3-42.3-51.9-4.7-9.3-12.8-16.1-22.5-18.7l-49.8-13.4C26 210.8-.2 233.1 7.1 259.6l23.5 86.8c5.4 19.9 20.3 35.7 39.4 41.8l63.5 20.2c21.8 7 45.4-.5 57.3-19l7.7-12c11.6-18 36-21.5 52.4-8.8 15.3 11.9 23.3 18.1 33.1 20 22.8 4.4 38.2-22.3 26.5-41l-9-14.4c-9.5-15.1-5.1-35.2 9.8-44.9l60.2-39.2c16-10.4 20.6-31.7 10.3-47.6l-8.5-13.1c-13.7-21.2-40.4-27.4-61.3-17.4z" }, 
  { name: "Journal", icon: "M362.7 19.3L314.3 67.7 444.3 197.7l48.4-48.4c25-25 25-65.5 0-90.5L453.3 19.3c-25-25-65.5-25-90.5 0zm-71 71L58.6 323.5c-10.4 10.4-18 23.3-22.2 37.4L1 481.2C-1.5 489.7 .8 498.8 7 505s15.3 8.5 23.7 6.1l120.3-35.4c14.1-4.2 27-11.8 37.4-22.2L421.7 220.3 291.7 90.3z" }, 
  { name: "Sleep", icon: "M223.5 32C100 32 0 132.3 0 256S100 480 223.5 480c60.6 0 115.5-24.2 155.8-63.4 5-4.9 6.3-12.5 3.1-18.7s-10.1-9.7-17-8.5c-9.8 1.7-19.8 2.6-30.1 2.6-96.9 0-175.5-78.8-175.5-176 0-65.8 36-123.1 89.3-153.3 6.1-3.5 9.2-10.5 7.7-17.3s-7.3-11.9-14.3-12.5c-6.3-.5-12.6-.8-19-.8z" }, 
  { name: "Healthy meals", icon: "M208 0c-29.9 0-54.7 20.5-61.8 48.2-.8 3-1.2 6.1-1.2 9.2 0 22.1 17.9 40 40 40H303c22.1 0 40-17.9 40-40 0-3.1-.4-6.2-1.2-9.2C334.7 20.5 309.9 0 280 0H208zM192 256A128 128 0 1 0 192 0 128 128 0 1 0 192 256zM32 245.3C32 376.6 130.2 485.4 257.2 494.6c6.2 .5 11.2-4.4 11.2-10.6s-5-11.1-11.2-11.6C142 463.7 54.4 366.5 54.4 245.3c0-36.2 7.7-70.5 21.4-101.9 2.5-5.7 .3-12.4-5.2-15.3s-12.4-1-15.6 4.3C40 167.3 32 205.4 32 245.3z" }, 
  { name: "No phone", icon: "M64 0C28.7 0 0 28.7 0 64V448c0 35.3 28.7 64 64 64H384c35.3 0 64-28.7 64-64V64c0-35.3-28.7-64-64-64H64zM224 400a32 32 0 1 1 0 64 32 32 0 1 1 0-64z" }, 
  { name: "Deep work", icon: "M512 256c0 141.4-114.6 256-256 256S0 397.4 0 256 114.6 0 256 0s256 114.6 256 256zM256 64C150 64 64 150 64 256s86 192 192 192 192-86 192-192S362 64 256 64zm0 256a64 64 0 1 1 0-128 64 64 0 1 1 0 128zm0-96a32 32 0 1 0 0 64 32 32 0 1 0 0-64z" }, 
  { name: "Social connection", icon: "M224 256A128 128 0 1 0 224 0a128 128 0 1 0 0 256zm-45.7 48C79.8 304 0 383.8 0 482.3c0 16.4 13.3 29.7 29.7 29.7H326.3c16.4 0 29.7-13.3 29.7-29.7C356 383.8 276.2 304 178.3 304h-18.6zM480 304c-19.4 0-37.9 3.2-55.2 8.9 9.9 14.8 17.6 31.4 22.3 49.3 22.1 4.2 38.6 23.9 38.6 47.7v28.8c0 12.3-5 24.1-14.1 32.7H544c26.5 0 48-21.5 48-48V392c0-48.6-39.4-88-88-88h-24z" }, 
  { name: "Tidy space", icon: "M377 105L279.1 7c-4.5-4.5-10.6-7-17-7H256c-13.3 0-24 10.7-24 24V64h45.7L132.3 234.3c-23.7 23.7-28 60-11 88.5l-63 63c-36 36-22.3 97.4 24.4 109.1l-10-10c-9.1-9.1-12.7-22-9.6-34.4 2.5-9.9 11.5-16.9 21.8-16.9H85c17.7 0 32-14.3 32-32s-14.3-32-32-32H32c-17.7 0-32 14.3-32 32 0 48.3 28.3 92.4 72.8 108.6l10 3.7c33.9 12.4 72.2-6.5 83.2-40.9l63-63c28.5 17 64.8 12.7 88.5-11L377 151c4.5-4.5 7-10.6 7-17v-6c0-13.3-10.7-24-24-24h-39.7l56.7-56.7c9.4-9.4 9.4-24.6 0-33.9z" }, 
  { name: "Learn something", icon: "M256 0c76.8 0 146.4 35.8 196 91.8 32.3 36.6 54.3 84 59.9 133.2 2.9 25.1-13.3 54.1-41.9 76.9-38.3 30.7-61.9 83.1-61.9 143.5 0 25.2-16.7 47-40.8 53-15.1 3.7-30.8 5.7-46.6 5.8-9 4.3-19.1 6.8-29.6 6.8h-70.3c-10.6 0-20.7-2.5-29.6-6.8-15.8-.1-31.4-2-46.6-5.8-24.1-6-40.8-27.9-40.8-53 0-60.4-23.6-112.9-61.9-143.5-28.7-22.8-44.8-51.8-41.9-76.9 5.6-49.3 27.6-96.6 59.9-133.2C109.6 35.8 179.2 0 256 0z" }, 
  { name: "Creative work", icon: "M512 256c0 141.4-114.6 256-256 256S0 397.4 0 256 114.6 0 256 0s256 114.6 256 256zM269.7 136.9c-29.6-12-63.5-9.3-89.9 8.2l-34.9 23.3c-2.3 1.5-3.6 4.1-3.6 6.8v81.1c0 24.5-15.7 46.5-39.1 54.5-4.4 1.5-7.4 5.7-7.4 10.3 0 26.5 21.5 48 48 48 20.3 0 38.8-12.7 45.4-31.8 1.9-5.5 8-8.4 13.5-6.5l30 10.4c6.2 2.1 9.5 8.9 7.4 15.1-4.7 13.6-7.3 28.1-7.3 43.1 0 6.6 5.4 12 12 12h20.6c24 0 46-15 54.4-37.1l6.7-17.6c1.6-4.2 6.6-6 10.5-3.9l46.1 24.5c6.3 3.3 14 .9 17.3-5.3l12.4-23.2c5.9-11 5.4-24.3-1.4-34.8l-15.3-25c-2.1-3.5-2.2-7.8-.3-11.4l15-28.3c4.1-7.7 2.4-17.2-4.1-23.2l-36.9-34.1c-13.8-12.8-32.9-19-51.8-17z" }, 
  { name: "Strength training", icon: "M112 112c0 35.3-28.7 64-64 64V336c35.3 0 64 28.7 64 64H464c0-35.3 28.7-64 64-64V176c-35.3 0-64-28.7-64-64H112zM0 128C0 92.7 28.7 64 64 64H448c35.3 0 64 28.7 64 64V384c0 35.3-28.7 64-64 64H64c-35.3 0-64-28.7-64-64V128z" }, 
  { name: "Walk outside", icon: "M28.6 150.9C10.7 135 7.1 107.8 20.3 88.1l22.6-33.9c13.2-19.8 39.4-25 58.7-11.8l61.5 42c16 10.9 44.9 3.4 53-15.1 3-6.9 6.2-13.6 9.6-20.2 6.4-12.3 21-19.2 34.4-16.1l70.6 16.5c16.3 3.8 28.3 17.8 29.5 34.6 .4 5.3 .5 10.6 .5 15.9 0 46.5-29.3 88-72.9 103l-64 22c-8.9 3.1-15.8 10.6-18.4 19.8l-25.1 88.1c-2.1 7.4-8.8 12.6-16.5 12.8L93.5 347.1c-22 .6-39.7 18.9-38.6 40.9 .8 15.9 11.6 30 27.2 34.5l141.6 41c14.6 4.2 30.1 .7 41.3-9.5l70.4-64c12.3-11.2 19.3-27 19.3-43.6V264.8C421.3 234.3 448 207 448 176c0-35.3-28.7-64-64-64-1.2 0-2.3 0-3.5 .1-30.8-21-72.6-18.3-100.8 7l-5.7 5.1-19.9-13.6c-4.3-2.9-9.1-4.9-14.1-5.7l-47.5-7.7c-9-1.5-18.2 2-25.2 8.7L28.6 150.9z" }, 
  { name: "Review goals", icon: "M32 32C14.3 32 0 46.3 0 64v384c0 17.7 14.3 32 32 32h448c17.7 0 32-14.3 32-32V64c0-17.7-14.3-32-32-32H32zM128 96h256c17.7 0 32 14.3 32 32v256c0 17.7-14.3 32-32 32H128c-17.7 0-32-14.3-32-32V128c0-17.7 14.3-32 32-32zM96 128v256 16-16-256zm64 48c0-8.8-7.2-16-16-16s-16 7.2-16 16v32c0 8.8 7.2 16 16 16s16-7.2 16-16v-32zm64 0c0-8.8-7.2-16-16-16s-16 7.2-16 16v64c0 8.8 7.2 16 16 16s16-7.2 16-16v-64zm64 0c0-8.8-7.2-16-16-16s-16 7.2-16 16v128c0 8.8 7.2 16 16 16s16-7.2 16-16v-128zm64 0c0-8.8-7.2-16-16-16s-16 7.2-16 16v96c0 8.8 7.2 16 16 16s16-7.2 16-16v-96z" }, 
  { name: "No social media", icon: "M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zM175 175c9.4-9.4 24.6-9.4 33.9 0l47 47 47-47c9.4-9.4 24.6-9.4 33.9 0s9.4 24.6 0 33.9l-47 47 47 47c9.4 9.4 9.4 24.6 0 33.9s-24.6 9.4-33.9 0l-47-47-47 47c-9.4 9.4-24.6 9.4-33.9 0s-9.4-24.6 0-33.9l47-47-47-47c-9.4-9.4-9.4-24.6 0-33.9z" }, 
  { name: "No junk food", icon: "M208 0c-29.9 0-54.7 20.5-61.8 48.2-.8 3-1.2 6.1-1.2 9.2 0 22.1 17.9 40 40 40H303c22.1 0 40-17.9 40-40 0-3.1-.4-6.2-1.2-9.2C334.7 20.5 309.9 0 280 0H208zM192 256A128 128 0 1 0 192 0 128 128 0 1 0 192 256zM464 256a208 208 0 1 1 -416 0 208 208 0 1 1 416 0zM128 256a40 40 0 1 0 -80 0 40 40 0 1 0 80 0zm256 0a40 40 0 1 0 -80 0 40 40 0 1 0 80 0z" }, 
  { name: "Call family", icon: "M164.9 24.6c-7.7-18.6-28-28.5-47.4-23.2l-88 24C12.1 30.2 0 46 0 64C0 311.4 200.6 512 448 512c18 0 33.8-12.1 38.6-29.5l24-88c5.3-19.4-4.6-39.7-23.2-47.4l-96-40c-16.3-6.8-35.2-2.1-46.3 11.6L304.7 368C234.3 334.7 177.3 277.7 144 207.3L193.3 167c13.7-11.2 18.4-30 11.6-46.3l-40-96z" }, 
  { name: "Brain training", icon: "M208 0c-26.5 0-48 21.5-48 48s21.5 48 48 48 48-21.5 48-48-21.5-48-48-48zM167.3 117.8C180 114.5 193.6 112 208 112c33.5 0 65 6.9 92.9 19.3 12 5.3 24.6 3.1 34.6-5.2 6.5-5.4 17.5-13 20-29.4-37.4-18.3-77-29.6-119.5-31.9-5-7.3-11.9-13.6-20.1-16.8l-8.6 3.6c-4.2 1.8-13 5.4-16.2 8.7-2.6-1.5-5.3-3-8.2-4.1-19.1-7.7-39.7-12-61-12.5C108.6 54.7 96 66.8 96 82c0 23.3 11.5 44 29.1 57.6l21.3-8.6c5.8-2.4 12.3-3.6 19.1-3.6c2.5 0 4.9 .2 7.2 .4l-5.4-9.9zm-49 32.7L96 160c-17.7 0-32 14.3-32 32 0 15 10.3 27.6 24.3 30.9l7.1-23.9c1.9-6.3 7.8-10.7 14.4-10.8 .2 0 .4 0 .7 0l21.3 2.1c.3-14.7 2.1-29.5 5.2-44l-18.7-15.8zM415.8 153c17.7 17.7 30 41.5 34.1 68l-23-23c-7-7-18.2-7.5-25.9-1.2l-1.4 1.2c-7.9 6.5-8.8 18.2-1.9 25.7l61.2 66.9c7.2 7.9 18.2 8 25.5 .1l63-67.9c6.9-7.5 5.9-19.1-2-25.7l-1.4-1.2c-7.7-6.4-19-5.8-26 1.2l-22 22c-5.8-37.1-23-70.5-47.9-95.7-1.4-1.4-3.1-2.5-4.8-3.4l-21.7 24.8c-1.7 1.9-3.7 4.5-5.8 8.1zm-89.5 67c13.7 15 36.8 14.8 50.3 .1l1.7-1.9c6.4-7.2 18-6.9 23.8 1l.5 .7c4.6 6.3 3.9 14.9-1.5 20.4l-76 76c-4 4-12.3 8.3-21.2 7-9-1.3-16-7.8-20.7-14.1l-18.5-24.7c-5-6.6-4.5-15.8 1.2-21.9l.6-.7c6-6.4 15.9-6.6 22-1.4l7.1 6 30.7-46.5zM76.1 270.3l-22.3-35.3c-2.3-3.7-6.2-6.1-10.6-6.6-4.4-.5-8.8 .9-12.2 3.8l-1.6 1.4C10.6 250 0 274.6 0 300.9s10.6 50.9 29.5 67.3l1.5 1.3c3.6 3.1 8.2 4.4 12.8 3.7s8.6-3.8 11-7.8l20.2-34 26-61.9-24.9 .2zm63.4 153.1l20.8-20.8c5.4-5.4 6-13.8 1.6-19.9-4.8-6.6-14-17-27.1-17-7.9 0-14.7 3.8-19.9 7.6L102 382.4c-3.1 2.3-7.2 3.3-11 2.6-3.8-.7-7.3-3.1-9.4-6.4L54 336.9c1.5-6.6 2.3-13.5 2.3-20.5 0-16.1-4.2-31.2-11.6-44.4l29.4 46.5c8.7 13.8 23.8 22.1 40.2 22.1 3.5 0 7.1-.4 10.6-1.2 19.9-4.6 35-21 37.3-41.3 1.9-17 10.1-32.3 22.6-43.6l31.8-29.1c7.5-6.8 7.3-18.6-.5-25.1l-.7-.6c-7.2-6-17.9-5-23.9 2.2l-23 27.6c-17.9 16.1-30 38.6-33 63.6l-6.2 51.6 8.5 76.5 1.5 1.5z" }
];

/* --------------------------------------------------
   DATA
-------------------------------------------------- */
const pages = dv.pages(`"${folder}"`)
  .where(p =>
    p.date &&
    p.date >= startDate &&
    p.date <= endDate &&
    !p.file.name.includes("Dashboard")
  )
  .sort(p => p.date, "asc");

/* --------------------------------------------------
   ROOT CONTAINER
-------------------------------------------------- */
const container = dv.el("div", "", { cls: "habit-grid-root" });

/* --------------------------------------------------
   STYLES
-------------------------------------------------- */
container.innerHTML = `
<style>
/* Scroll ownership */
.habit-grid-wrapper {
  width: 100%;
  overflow-x: auto;
  position: relative;
}

/* Table base */
.habit-table {
  width: 100%;
  min-width: fit-content;
  border-collapse: separate;
  border-spacing: 0;
  table-layout: fixed;
}

/* IMPORTANT: allow tooltips to escape table */
.habit-table,
.habit-table thead,
.habit-table tbody,
.habit-table tr,
.habit-table th,
.habit-table td {
  overflow: visible !important;
}

/* Cell base */
.habit-table th,
.habit-table td {
  padding: 8px 6px;
  text-align: center;
  box-sizing: border-box;
}

/* Uniform background for ALL habit columns */
.habit-table th:not(.habit-date-col),
.habit-table td:not(.habit-date-col) {
  background-color: var(--background-secondary);
}

/* Sticky header */
.habit-table th {
  position: sticky;
  top: 0;
  z-index: 20;
}

/* Sticky date column */
.habit-date-col {
  width: 100px;
  min-width: 100px;
  max-width: 100px;
  position: sticky;
  left: 0;
  z-index: 30;
  background-color: var(--background-primary);
  text-align: left;
  font-weight: 600;
}

/* Icon columns */
.habit-icon-col {
  width: 45px;
  min-width: 45px;
  max-width: 45px;
}

/* Icon wrapper */
.habit-icon-wrapper {
  display: inline-block;
  position: relative;
  fill: rgba(255,255,255,0.6);
  overflow: visible !important;
  cursor: pointer;
}
.habit-icon-wrapper:hover {
  fill: #FFD60A;
}

/* Tooltip - FIXED VERSION */
.tooltip-tag {
  position: fixed;
  background: var(--background-secondary);
  border: 1px solid #FFD60A;
  padding: 6px 12px;
  font-size: 12px;
  border-radius: 6px;
  white-space: nowrap;
  
  /* Opacity-based hiding for proper dimension calculation */
  opacity: 0;
  z-index: 9999;
  
  /* Force proper width calculation */
  width: max-content;
  max-width: 200px;
  
  /* Prevent interaction while invisible */
  pointer-events: none;
  
  /* Smooth fade effect */
  transition: opacity 0.15s ease-in-out;
  
  /* Make sure it's on top of everything */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* Status */
.status-done {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  border: 1px solid #FFD60A;
  background: rgba(255,214,10,0.15);
  display: flex;
  align-items: center;
  justify-content: center;
}
.status-done svg { fill: #FFD60A; }
.status-miss { opacity: 0.25; }
</style>
`;

/* --------------------------------------------------
   BUILD TABLE
-------------------------------------------------- */
let header = `<tr><th class="habit-date-col">Date</th>`;
habitsMap.forEach(h => {
  header += `
    <th class="habit-icon-col">
      <div class="habit-icon-wrapper" data-habit="${h.name}">
        ${createIcon(h.icon)}
        <div class="tooltip-tag">${h.name}</div>
      </div>
    </th>`;
});
header += `</tr>`;

let body = "";
pages.forEach(p => {
  body += `<tr>`;
  body += `
    <td class="habit-date-col">
      <a href="${p.file.path}" class="internal-link">
        ${p.date.toFormat("EEE dd")}
      </a>
    </td>`;

  habitsMap.forEach(h => {
    const task = p.file.tasks.find(t => t.text.includes(h.name));
    body += `
      <td class="habit-icon-col">
        ${task && task.completed
          ? `<div class="status-done">${checkIcon}</div>`
          : `<div class="status-miss">•</div>`}
      </td>`;
  });

  body += `</tr>`;
});

/* --------------------------------------------------
   RENDER
-------------------------------------------------- */
container.innerHTML += `
<div class="habit-grid-wrapper">
  <table class="habit-table">
    <thead>${header}</thead>
    <tbody>${body}</tbody>
  </table>
</div>
`;

/* --------------------------------------------------
   TOOLTIP POSITIONING - SIMPLIFIED AND FIXED
-------------------------------------------------- */
// Wait for DOM to be ready
setTimeout(() => {
  const wrappers = container.querySelectorAll(".habit-icon-wrapper");
  
  wrappers.forEach(wrapper => {
    const tooltip = wrapper.querySelector(".tooltip-tag");
    if (!tooltip) return;
    
    // Pre-calculate tooltip dimensions while hidden
    const tooltipWidth = tooltip.offsetWidth;
    const tooltipHeight = tooltip.offsetHeight;
    
    wrapper.addEventListener("mouseenter", (e) => {
      // Get current position of the icon
      const rect = wrapper.getBoundingClientRect();
      const viewportWidth = window.innerWidth;
      const viewportHeight = window.innerHeight;
      
      // Calculate position - center horizontally above the icon
      let left = rect.left + (rect.width / 2);
      let top = rect.top - tooltipHeight - 8; // 8px gap instead of 12
      
      // Boundary checks - keep tooltip on screen
      
      // Horizontal boundaries
      const minLeft = 10 + (tooltipWidth / 2);
      const maxLeft = viewportWidth - 10 - (tooltipWidth / 2);
      
      if (left < minLeft) left = minLeft;
      if (left > maxLeft) left = maxLeft;
      
      // Vertical boundaries (if near top of screen)
      if (top < 10) {
        // Position below instead
        top = rect.bottom + 8;
      }
      
      // Apply position
      tooltip.style.left = `${left}px`;
      tooltip.style.top = `${top}px`;
      tooltip.style.transform = "translateX(-50%)";
      
      // Show tooltip
      tooltip.style.opacity = "1";
    });
    
    wrapper.addEventListener("mouseleave", () => {
      tooltip.style.opacity = "0";
    });
    
    // Handle scroll and resize
    let hideTimeout;
    const hideTooltip = () => {
      if (tooltip.style.opacity === "1") {
        tooltip.style.opacity = "0";
      }
    };
    
    window.addEventListener("scroll", () => {
      clearTimeout(hideTimeout);
      hideTooltip();
      hideTimeout = setTimeout(() => {}, 100);
    }, true);
    
    window.addEventListener("resize", hideTooltip);
  });
  
  console.log(`Tooltips initialized for ${wrappers.length} habit icons`);
}, 100);
