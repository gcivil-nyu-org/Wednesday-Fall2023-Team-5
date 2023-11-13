let cityField = document.getElementById("city-create-field");
let countryField = document.getElementById("country-create-field");

const CITY_CHOICES = {
    "INDIA": [
        "Ahmedabad",
        "Bangalore",
        "Chennai",
        "Hyderabad",
        "Jaipur",
        "Kolkata",
        "Mumbai",
        "New Delhi",
        "Pune"
    ],
    "UK": [
        "Bristol",
        "Glasgow",
        "Leeds",
        "Liverpool",
        "London",
        "Newcastle",
        "Nottingham",
        "Sheffield"
    ],
    "US": [
        "Chicago",
        "Dallas",
        "Houston",
        "Los Angeles",
        "New York City",
        "Phoenix",
        "Philadelphia",
        "San Antonio",
        "San Diego"
    ],
    "CANADA": [
        "Calgary",
        "Edmonton",
        "Hamilton",
        "Mississauga",
        "Montreal",
        "Niagara Falls",
        "Ottawa",
        "Quebec City",
        "Toronto",
        "Vancouver"
    ],
    "MEXICO": [
        "Cancun",
        "Chichen Itza",
        "Guadalajara",
        "Los Cabos",
        "Mexico City",
        "Oaxaca City",
        "Playa del Carmen",
        "Puerto Vallarte"
    ],
    "FRANCE": [
        "Burgundy",
        "Bordeaux",
        "Cannes",
        "Corsica",
        "Eze",
        "Marseille",
        "Nice",
        "Normandy",
        "Paris",
        "Toulouse"
    ],
    "ITALY": [
        "Florence",
        "Genoa",
        "Milan",
        "Naples",
        "Palermo",
        "Rome",
        "Venice"
    ]
}

countryField.addEventListener('change', (e) => {

    let inUse;

    switch (countryField.value) {
        case 'India':
            inUse = CITY_CHOICES["INDIA"];
            break;
        case 'United Kingdom':
            inUse = CITY_CHOICES["UK"];
            break;
        case 'United States':
            inUse = CITY_CHOICES["US"];
            break;
        case 'Canada':
            inUse = CITY_CHOICES["CANADA"];
            break;
        case 'Mexico':
            inUse = CITY_CHOICES["MEXICO"];
            break;
        case 'Italy':
            inUse = CITY_CHOICES["ITALY"];
            break;
        case 'France':
            inUse = CITY_CHOICES["FRANCE"];
            break;
        default:
            inUse = null;
            break;
    }

    if (inUse != null) {
        for (let child of cityField.children) {
            if (!inUse.includes(child.innerHTML)) {
                child.style.display = 'none';
            } else {
                child.style.display = 'block';
            }
        }
    }
})

