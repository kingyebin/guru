let currentPage = 1;
const perPage = 6; // 한 페이지에 표시할 게임 수
let loading = false;
let selectedValues = {
    platforms: [],
    genre: [],
    theme: [],
    mode: [],
    rating: [],
    year: [],
    tags: []
};
let rating = 0.0; // 전역 변수 rating 추가
const currentYear = new Date().getFullYear(); // 현재 년도 가져오기

document.addEventListener("DOMContentLoaded", () => {
    loadTopRatingGames();
    showMainPage();
    document.querySelector('.search-container input').addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            searchGames();
        }
    });
    document.querySelector('.logo').addEventListener('click', showMainPage);
    document.querySelector('.search-container button').addEventListener('click', searchGames);
    document.querySelector('.recommend-button').addEventListener('click', showRecommendPage);
    document.querySelector('nav a.active').addEventListener('click', showMainPage);
    document.querySelector('.recommend-actions button:nth-child(1)').addEventListener('click', function() {
        resetSelectedValues();
        showRecommendPage();
    });
    document.querySelector('.recommend-actions button:nth-child(2)').addEventListener('click', recommendGames); // Recommend 버튼 클릭 시
});

function resetSelectedValues() {
    selectedValues = {
        platforms: [],
        genre: [],
        theme: [],
        mode: [],
        rating: [],
        year: [],
        tags: []
    };
    rating = 0.0; // 초기화 시 rating도 초기화
    displaySelectedValues();
    clearRecommendedGames(); // 추천된 게임 목록 초기화
}

function clearRecommendedGames() {
    const recommendedGamesSection = document.getElementById('recommended-games');
    recommendedGamesSection.innerHTML = '';
}

function showMainPage() {
    resetSelectedValues();
    document.getElementById('hero').style.display = 'block';
    document.getElementById('top-ratings').style.display = 'block';
    document.getElementById('search-results').style.display = 'none';
    document.getElementById('upcoming').style.display = 'none';
    document.getElementById('popular').style.display = 'none';
    document.getElementById('recommend').style.display = 'none';
}

function showRecommendPage() {
    resetSelectedValues();
    document.getElementById('hero').style.display = 'none';
    document.getElementById('top-ratings').style.display = 'none';
    document.getElementById('search-results').style.display = 'none';
    document.getElementById('upcoming').style.display = 'none';
    document.getElementById('popular').style.display = 'none';
    document.getElementById('recommend').style.display = 'block';
    loadUniqueValues('platforms');
}

// Top Rating Games
function loadTopRatingGames() {
    fetch(`/games?page=${currentPage}&per_page=${perPage}`)
        .then(response => response.json())
        .then(data => {
            displayGames(data);
        })
        .catch(error => console.error('Error fetching top rating games:', error));
}

// Search
function searchGames() {
    const searchTerm = document.querySelector('.search-container input').value;
    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ search_term: searchTerm }),
    })
        .then(response => response.json())
        .then(data => {
            displaySearchResults(data, searchTerm);
        })
        .catch(error => console.error('Error searching games:', error));
}

function displaySearchResults(games, searchTerm) {
    resetSelectedValues();
    document.getElementById('hero').style.display = 'none';
    document.getElementById('top-ratings').style.display = 'none';
    document.getElementById('search-results').style.display = 'block';
    document.getElementById('upcoming').style.display = 'none';
    document.getElementById('popular').style.display = 'none';
    document.getElementById('recommend').style.display = 'none';

    const searchResultsHeader = document.getElementById('search-results-header');
    searchResultsHeader.innerHTML = `<h2>Search: ${searchTerm}</h2>`;

    const searchGameList = document.getElementById('search-game-list');
    searchGameList.innerHTML = '';

    games.forEach(game => {
        const gameItem = document.createElement('div');
        gameItem.className = 'game-item';
        gameItem.innerHTML = `
            <div class="game-content">
                <div class="game-image" style="background-image: url(${game.background_image});"></div>
                <div class="game-name">${game.name}</div>
            </div>
        `;
        gameItem.addEventListener('click', () => showGameDetails(game));
        searchGameList.appendChild(gameItem);
    });

    document.getElementById('search-results').style.display = 'block';
}

// Load Unique Values
function loadUniqueValues(column) {
    console.log(`Loading unique values for column: ${column}`);
    fetch(`/unique_values?column=${column}`)
        .then(response => response.json())
        .then(data => {
            console.log(`Received data for ${column}:`, data);
            displayUniqueValues(data, column);
        })
        .catch(error => console.error('Error fetching unique values:', error));
}

function displayUniqueValues(values, column) {
    console.log(`Displaying unique values for ${column}:`, values);
    const uniqueValuesContainer = document.getElementById('unique-values');
    uniqueValuesContainer.innerHTML = '';

    values.forEach(value => {
        const button = document.createElement('button');
        button.className = 'unique-value-button';
        button.innerText = value;
        button.onclick = () => toggleValueSelection(value, column);
        uniqueValuesContainer.appendChild(button);
    });
}

function toggleValueSelection(value, column) {
    if (!selectedValues[column]) {
        selectedValues[column] = [];
    }

    const index = selectedValues[column].indexOf(value);
    if (index > -1) {
        selectedValues[column].splice(index, 1);
    } else {
        selectedValues[column].push(value);
    }

    displaySelectedValues();
    updateButtonState(column, value); // 버튼 상태 업데이트
}

function updateButtonState(column, value) {
    const buttons = document.querySelectorAll('.unique-value-button');
    buttons.forEach(button => {
        if (button.innerText === value) {
            if (selectedValues[column].includes(value)) {
                button.classList.add('selected');
            } else {
                button.classList.remove('selected');
            }
        }
    });
}

function showRatingSliders() {
    document.getElementById('unique-values').innerHTML = `
        <div class="rating-slider" id="rating-slider-container">
            <label for="rating-slider">Rating</label>
            <input type="range" min="0.0" max="5.0" step="0.1" value="${rating}" id="rating-slider" oninput="updateRating(this.value)">
            <span id="slider-value">${rating}</span>
        </div>
    `;
    document.getElementById('unique-values').style.display = 'block';
}

function showYearSliders() {
    document.getElementById('unique-values').innerHTML = `
        <div class="year-slider" id="year-slider-container">
            <label for="year-slider">Year</label>
            <input type="range" min="1900" max="${currentYear}" step="1" value="${currentYear}" id="year-slider" oninput="updateYear(this.value)">
            <span id="year-slider-value">${currentYear}</span>
        </div>
    `;
    document.getElementById('unique-values').style.display = 'block';
}

function updateRating(value) {
    rating = parseFloat(value);
    document.getElementById('slider-value').innerText = rating;
    selectedValues.rating = [rating]; // selectedValues에 rating 추가
    displaySelectedValues();
}

function updateYear(value) {
    const year = parseInt(value);
    document.getElementById('year-slider-value').innerText = year;
    selectedValues.year = [year]; // selectedValues에 year 추가
    displaySelectedValues();
}

function displaySelectedValues() {
    document.getElementById('selected-platforms').innerText = selectedValues.platforms.join(',');
    document.getElementById('selected-genres').innerText = selectedValues.genre.join(',');
    document.getElementById('selected-themes').innerText = selectedValues.theme.join(',');
    document.getElementById('selected-modes').innerText = selectedValues.mode.join(',');
    document.getElementById('selected-tags').innerText = selectedValues.tags.join(',');
    document.getElementById('selected-ratings').innerText = selectedValues.rating.join(',');
    document.getElementById('selected-years').innerText = selectedValues.year.join(',');

    const selectedUniqueValuesContainer = document.getElementById('selected-unique-values');
    selectedUniqueValuesContainer.innerHTML = '';
    Object.keys(selectedValues).forEach(category => {
        selectedValues[category].forEach(value => {
            const span = document.createElement('span');
            span.className = 'selected-unique-value';
            span.innerText = value;
            const removeButton = document.createElement('button');
            removeButton.innerText = 'X';
            removeButton.onclick = () => removeValue(value, category);
            span.appendChild(removeButton);
            selectedUniqueValuesContainer.appendChild(span);
        });
    });

    if (rating > 0) {
        const ratingSpan = document.createElement('span');
        ratingSpan.className = 'selected-unique-value';
        ratingSpan.innerText = `${rating}`;
        const removeButton = document.createElement('button');
        removeButton.innerText = 'X';
        removeButton.onclick = () => {
            rating = 0.0;
            document.getElementById('rating-slider').value = rating;
            document.getElementById('slider-value').innerText = rating;
            selectedValues.rating = [];
            displaySelectedValues();
        };
        ratingSpan.appendChild(removeButton);
        if (!selectedUniqueValuesContainer.querySelector('.selected-unique-value:contains("Rating")')) {
            selectedUniqueValuesContainer.appendChild(ratingSpan);
        }
    }

    if (selectedValues.year.length > 0) {
        const yearSpan = document.createElement('span');
        yearSpan.className = 'selected-unique-value';
        yearSpan.innerText = selectedValues.year.join(', ');
        const removeButton = document.createElement('button');
        removeButton.innerText = 'X';
        removeButton.onclick = () => {
            selectedValues.year = [];
            document.getElementById('year-slider').value = currentYear;
            document.getElementById('year-slider-value').innerText = currentYear;
            displaySelectedValues();
        };
        yearSpan.appendChild(removeButton);
        if (!selectedUniqueValuesContainer.querySelector('.selected-unique-value:contains("Year")')) {
            selectedUniqueValuesContainer.appendChild(yearSpan);
        }
    }
}

function removeValue(value, category) {
    const index = selectedValues[category].indexOf(value);
    if (index > -1) {
        selectedValues[category].splice(index, 1);
    }
    displaySelectedValues();
}

// Upcoming, Popular
function loadGames(endpoint, section, title) {
    fetch(`/${endpoint}`)
        .then(response => response.json())
        .then(data => {
            displaySectionResults(data, section, title);
        })
        .catch(error => console.error('Error fetching games:', error));
}

function displaySectionResults(games, section, title) {
    resetSelectedValues();
    document.getElementById('hero').style.display = 'none';
    document.getElementById('top-ratings').style.display = 'none';
    document.getElementById('search-results').style.display = 'none';
    document.getElementById('upcoming').style.display = 'none';
    document.getElementById('popular').style.display = 'none';
    document.getElementById('recommend').style.display = 'none';

    const sectionHeader = document.getElementById(`${section}-header`);
    sectionHeader.innerHTML = `<h2>${title}</h2>`;

    const sectionGameList = document.getElementById(`${section}-game-list`);
    sectionGameList.innerHTML = '';

    games.forEach(game => {
        const gameItem = document.createElement('div');
        gameItem.className = 'game-item';
        gameItem.innerHTML = `
            <div class="game-content">
                <div class="game-image" style="background-image: url(${game.background_image});"></div>
                <div class="game-name">${game.name}</div>
            </div>
        `;
        gameItem.addEventListener('click', () => showGameDetails(game));
        sectionGameList.appendChild(gameItem);
    });

    document.getElementById(section).style.display = 'block';
}

// Recommend
function recommendGames() {
    const selectedValuesString = {
        platforms: selectedValues.platforms.join(","),
        genre: selectedValues.genre.join(","),
        theme: selectedValues.theme.join(","),
        mode: selectedValues.mode.join(","),
        rating: selectedValues.rating.length > 0 ? selectedValues.rating[0] : 0,
        year: selectedValues.year.length > 0 ? selectedValues.year[0] : new Date().getFullYear(),
        tags: selectedValues.tags.join(",")
    };

    fetch('/recommend', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(selectedValuesString),
    })
    .then(response => response.json())
    .then(data => {
        displayRecommendedGames(data);
    })
    .catch(error => console.error('Error recommending games:', error));
}

function displayRecommendedGames(games) {
    const recommendSection = document.getElementById('recommend');
    recommendSection.style.display = 'block';

    const recommendedGamesSection = document.getElementById('recommended-games');
    recommendedGamesSection.innerHTML = '';

    games.forEach(game => {
        const gameItem = document.createElement('div');
        gameItem.className = 'game-item';
        gameItem.innerHTML = `
            <div class="game-content">
                <div class="game-image" style="background-image: url(${game.background_image});"></div>
                <div class="game-name">${game.name}</div>
            </div>
        `;
        gameItem.addEventListener('click', () => showGameDetails(game));
        recommendedGamesSection.appendChild(gameItem);
    });

    document.getElementById('recommend').scrollIntoView({ behavior: 'smooth' }); // 스크롤을 이동하여 추천 섹션을 보이게 함
}

// Game Info
function displayGames(games) {
    const gameList = document.getElementById('game-list');
    gameList.innerHTML = '';

    games.forEach(game => {
        const gameItem = document.createElement('div');
        gameItem.className = 'game-item';
        gameItem.innerHTML = `
            <div class="game-content">
                <div class="game-image" style="background-image: url(${game.background_image});"></div>
                <div class="game-name">${game.name}</div>
            </div>
        `;
        gameItem.addEventListener('click', () => showGameDetails(game));
        gameList.appendChild(gameItem);
    });
}

function showGameDetails(game) {
    const modal = document.getElementById("game-modal");
    const modalGameInfo = document.getElementById("modal-game-info");

    const releaseDate = game.tba ? "TBA" : game.released;
    let platforms = game.platforms ? game.platforms : '';
    let genres = game.genre ? game.genre : '';
    let developers = game.developers ? game.developers : '';
    let publishers = game.publishers ? game.publishers : '';
    let tags = game.tags ? game.tags : '';
    let esrbRating = game.esrb_rating || '';
    let website = game.website && game.website.trim() ? game.website : '';

    let modalContent = `
        <img src="${game.background_image}" alt="${game.name}">
        <div class="game-name">${game.name}</div>
        <div class="game-description"><strong>About</strong> <div>${game.description}</div></div>
        <div class="game-rating"><strong>Ratings:</strong> ${game.rating}</div>
    `;

    if (platforms) {
        modalContent += `
        <div class="game-platforms-genres">
            <strong>Platforms:</strong> ${platforms}<br>
            <strong>Genre:</strong> ${genres}
        </div>`;
    }

    if (developers) {
        modalContent += `
        <div class="game-developer-publisher">
            <strong>Developer:</strong> ${developers}<br>
            <strong>Publisher:</strong> ${publishers}
        </div>`;
    }

    modalContent += `
        <div class="game-release-date"><strong>Release date:</strong> ${releaseDate}</div>
    `;

    if (esrbRating) {
        modalContent += `
        <div class="game-age-rating"><strong>Age rating:</strong> ${esrbRating}</div>
        `;
    }

    if (tags) {
        modalContent += `
        <div class="game-tags"><strong>Tags:</strong> ${tags}</div>
        `;
    }

    if (website) {
        modalContent += `
        <div class="game-website"><strong>Website:</strong> <a href="${website}" target="_blank">${website}</a></div>
        `;
    }

    modalGameInfo.innerHTML = modalContent;
    modal.style.display = "block";
}

function closeModal() {
    const modal = document.getElementById("game-modal");
    modal.style.display = "none";
}

window.onclick = function(event) {
    const modal = document.getElementById("game-modal");
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

function nextPage() {
    currentPage++;
    loadTopRatingGames();
}

function prevPage() {
    if (currentPage > 1) {
        currentPage--;
    loadTopRatingGames();
    }
}
