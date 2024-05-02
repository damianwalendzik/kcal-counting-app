let nav = 0;
let clicked = null;
let events = localStorage.getItem('events') ? JSON.parse(localStorage.getItem('events')) : [];

const kcalRequirement = "{{ kcal_requirement }}";

const calendar = document.getElementById('calendar');
const newEventModal = document.getElementById('newEventModal');
const deleteEventModal = document.getElementById('deleteEventModal');
const backDrop = document.getElementById('modalBackDrop');
const eventTitleInput = document.getElementById('eventTitleInput');
const weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];


function handleDayClick(year, month, day) {
    const formattedDate = `${year}-${month.toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`;
    const username = window.location.pathname.split('/')[3];
    const url = `/api/profile/${username}/food_consumption/${formattedDate}/`;
    console.log("Generated URL:", url);
    window.location.href = url; // Redirect to the URL associated with the clicked date

}

// Modify the load function to pass year, month, and day to the handleDayClick function
function load() {
    const dt = new Date();

    if (nav !== 0) {
        dt.setMonth(new Date().getMonth() + nav);
    }

    const day = dt.getDate();
    const month = dt.getMonth() + 1; // Adjust month to 1-based index
    const year = dt.getFullYear();

    const firstDayOfMonth = new Date(year, month - 1, 1); // Adjust month to 0-based index
    const daysInMonth = new Date(year, month, 0).getDate();

    const dateString = firstDayOfMonth.toLocaleDateString('en-us', {
        weekday: 'long',
        year: 'numeric',
        month: 'numeric',
        day: 'numeric',
    });
    const paddingDays = weekdays.indexOf(dateString.split(', ')[0]);

    document.getElementById('monthDisplay').innerText =
        `${dt.toLocaleDateString('en-us', { month: 'long' })} ${year}`;

    calendar.innerHTML = '';

    for (let i = 1; i <= paddingDays + daysInMonth; i++) {
        const daySquare = document.createElement('div');
        daySquare.classList.add('day');

        if (i > paddingDays) {
            const dayOfMonth = i - paddingDays;
            daySquare.innerText = dayOfMonth;

            const additionalDataSpan = document.createElement('span');
            additionalDataSpan.textContent = kcalRequirement;
            additionalDataSpan.style.fontSize = 'small';
            daySquare.appendChild(additionalDataSpan);
            if (dayOfMonth === day && nav === 0) {
                daySquare.id = 'currentDay';
            }

            daySquare.addEventListener('click', () => handleDayClick(year, month, dayOfMonth));
        } else {
            daySquare.classList.add('padding');
        }

        calendar.appendChild(daySquare);
    }
}

function initButtons() {
  document.getElementById('nextButton').addEventListener('click', () => {
    nav++;
    load();
  });

  document.getElementById('backButton').addEventListener('click', () => {
    nav--;
    load();
  });
}

initButtons();
load();