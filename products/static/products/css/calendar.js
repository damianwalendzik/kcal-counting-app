let nav = 0;
let clicked = null;
let events = localStorage.getItem('events') ? JSON.parse(localStorage.getItem('events')) : [];

const kcalRequirement = document.currentScript.getAttribute('kcal_requirement');
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
    window.location.href = url; 

}


function load() {
    const dt = new Date();
    if (nav !== 0) {
        dt.setMonth(new Date().getMonth() + nav);
    }

    const day = dt.getDate();
    const month = dt.getMonth() + 1; 
    const year = dt.getFullYear();
    const formattedDate = `${year}-${month.toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`;
    const firstDayOfMonth = new Date(year, month - 1, 1); 
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

            // Check if the formattedDate matches any date key in kcal_consumed_on_date
            const formattedDate = `${year}-${month.toString().padStart(2, '0')}-${dayOfMonth.toString().padStart(2, '0')}`;
            const value = kcalConsumedOnDate[formattedDate] || 0; // Default value is 0 if no data for the date
            const output = value.toFixed(0).toString() + " / " + kcalRequirement.split('.')[0];
            const additionalDataSpan = document.createElement('span');
            additionalDataSpan.textContent = output;
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