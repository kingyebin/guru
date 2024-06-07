// 전역 변수 설정
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

// DOMContentLoaded 이벤트 리스너
document.addEventListener("DOMContentLoaded", () => {
    // 초기 데이터 로드
    loadTopRatingGames();
    showMainPage();
    loadStats('platforms'); // 기본적으로 플랫폼 통계 로드

    // 이벤트 리스너 설정
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
    document.querySelector('.recommend-actions button:nth-child(2)').addEventListener('click', recommendGames);

    // 통계 유형 버튼 클릭 이벤트 추가
    document.querySelectorAll('.stats-button').forEach(button => {
        button.addEventListener('click', event => {
            const statsType = event.target.dataset.type;
            loadStats(statsType);
        });
    });

    // 카테고리 클릭 이벤트 추가
    document.querySelectorAll('.dropdown-content a').forEach(item => {
        item.addEventListener('click', event => {
            event.preventDefault(); // 링크 기본 동작 방지
            const category = event.target.textContent.toLowerCase();
            loadCategoryData(category);
        });
    });
});

// 페이지 전환 함수
function showMainPage() {
    resetSelectedValues();
    displaySections(['hero', 'top-ratings']);
    hideSections(['search-results', 'upcoming', 'popular', 'recommend', 'category', 'stats']);
}

function showRecommendPage() {
    resetSelectedValues();
    displaySections(['recommend']);
    hideSections(['hero', 'top-ratings', 'search-results', 'upcoming', 'popular', 'category', 'stats']);
    loadUniqueValues('platforms');
}

function showStatsPage() {
    loadStats('platforms'); // 기본적으로 플랫폼 통계를 로드
    hideSections(['hero', 'top-ratings', 'search-results', 'upcoming', 'popular', 'recommend', 'category']);
    displaySections(['stats']);
}

function showCategoryPage() {
    resetSelectedValues();
    displaySections(['category']);
    hideSections(['hero', 'top-ratings', 'search-results', 'upcoming', 'popular', 'recommend', 'stats']);
}

// 데이터 로드 및 표시 함수
function loadStats(type) {
    fetch(`/stats/${type}`)
        .then(response => response.json())
        .then(data => {
            displayStats(data, type);
        })
        .catch(error => console.error('Error loading stats:', error));
}

function displayStats(data, type) {
    const statsContent = document.getElementById('stats-content');
    statsContent.innerHTML = ''; // 기존 내용을 비움

    const ctx = document.createElement('canvas');
    statsContent.appendChild(ctx);

    let datasets;
    let labels;

    if (type === 'social_media') {
        datasets = [
            {
                label: 'YouTube Count',
                data: data.youtube,
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            },
            {
                label: 'Twitch Count',
                data: data.twitch,
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            },
            {
                label: 'Reddit Count',
                data: data.reddit,
                backgroundColor: 'rgba(255, 206, 86, 0.2)',
                borderColor: 'rgba(255, 206, 86, 1)',
                borderWidth: 1
            }
        ];
        labels = data.labels;
    } else {
        datasets = [{
            label: 'Game Count',
            data: data.values,
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
        }];
        labels = data.labels;
    }

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: datasets
        },
        options: {
            tooltips: {
                titleFontSize: 16,
                bodyFontSize: 14,
                titleFontColor: '#FFFFFF',
                bodyFontColor: '#FFFFFF',
                backgroundColor: 'rgba(0, 0, 0, 0.7)',
                xPadding: 10,
                yPadding: 10,
                caretSize: 6,
                cornerRadius: 6
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function loadTopRatingGames() {
    fetch(`/games?page=${currentPage}&per_page=${perPage}`)
        .then(response => response.json())
        .then(data => {
            displayGames(data);
        })
        .catch(error => console.error('Error fetching top rating games:', error));
}

function searchGames() {
    const searchTerm = document.querySelector('.search-container input').value;
    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ search_term: searchTerm }),
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            displaySearchResults(data, searchTerm);
        })
        .catch(error => console.error('Error searching games:', error));
}

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

function loadGames(endpoint, section, title) {
    fetch(`/${endpoint}`)
        .then(response => response.json())
        .then(data => {
            displaySectionResults(data, section, title);
        })
        .catch(error => console.error('Error fetching games:', error));
}

function loadCategoryData(category) {
    fetch(`/category/${category}`)
        .then(response => response.json())
        .then(data => {
            displayCategoryData(category, data);
        })
        .catch(error => console.error('Error fetching category data:', error));
}

function loadGamesByCategoryValue(category, value) {
    fetch(`/category/${category}/${value}`)
        .then(response => response.json())
        .then(data => {
            displayGamesByCategoryValue(category, value, data);
        })
        .catch(error => console.error('Error fetching games by category value:', error));
}

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

// 데이터 표시 함수
function displayStats(data, type) {
    const statsContent = document.getElementById('stats-content');
    statsContent.innerHTML = ''; // 기존 내용을 비움

    const ctx = document.createElement('canvas');
    statsContent.appendChild(ctx);

    let datasets;
    let labels;

    if (type === 'social_media') {
        datasets = [
            {
                label: 'YouTube Count',
                data: data.youtube,
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            },
            {
                label: 'Twitch Count',
                data: data.twitch,
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            },
            {
                label: 'Reddit Count',
                data: data.reddit,
                backgroundColor: 'rgba(255, 206, 86, 0.2)',
                borderColor: 'rgba(255, 206, 86, 1)',
                borderWidth: 1
            }
        ];
        labels = data.labels;
    } else {
        datasets = [{
            label: 'Game Count',
            data: data.values,
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
        }];
        labels = data.labels;
    }

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: datasets
        },
        options: {
            tooltips: {
                titleFontSize: 16,
                bodyFontSize: 14,
                titleFontColor: '#FFFFFF',
                bodyFontColor: '#FFFFFF',
                backgroundColor: 'rgba(0, 0, 0, 0.7)',
                xPadding: 10,
                yPadding: 10,
                caretSize: 6,
                cornerRadius: 6
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function displaySearchResults(games, searchTerm) {
    resetSelectedValues();
    displaySections(['search-results']);
    hideSections(['hero', 'top-ratings', 'upcoming', 'popular', 'recommend', 'category', 'stats']);

    const searchResultsHeader = document.getElementById('search-results-header');
    searchResultsHeader.innerHTML = `<h2>Search: ${searchTerm}</h2>`;

    const searchGameList = document.getElementById('search-game-list');
    searchGameList.innerHTML = '';

    if (games.length === 0) {
        searchGameList.innerHTML = '<p>No results found.</p>';
        return;
    }

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

function displaySectionResults(games, section, title) {
    resetSelectedValues();
    hideSections(['hero', 'top-ratings', 'search-results', 'upcoming', 'popular', 'recommend', 'category', 'stats']);
    displaySections([section]);

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
}

function displayCategoryData(category, data) {
    const categorySection = document.getElementById('category');
    categorySection.innerHTML = `
        <div class="category-header" id="category-header">
            <h2>${category.charAt(0).toUpperCase() + category.slice(1)}</h2>
        </div>
    `;
    
    const categoryList = document.createElement('div');
    categoryList.className = 'category-list';
    const sortedData = Object.entries(data).sort((a, b) => b[1] - a[1]);

    sortedData.forEach(([key, value]) => {
        const uniqueBox = document.createElement('div');
        uniqueBox.className = 'unique-box';
        uniqueBox.innerHTML = `
            <div class="unique-name">${key}</div>
            <div class="unique-count">Total: ${value}</div>
        `;
        uniqueBox.addEventListener('click', () => {
            loadGamesByCategoryValue(category, key);
        });
        categoryList.appendChild(uniqueBox);
    });
    
    categorySection.appendChild(categoryList);
    showCategoryPage();
}

function displayGamesByCategoryValue(category, value, games) {
    const categorySection = document.getElementById('category');
    const categoryHeader = document.getElementById('category-header');
    categoryHeader.innerHTML = `<h2>${category.charAt(0).toUpperCase() + category.slice(1)}: ${value}</h2>`;
    
    const gameList = document.createElement('div');
    gameList.className = 'game-list';
    
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

    categorySection.appendChild(gameList);
    hideCategoryList(); // 추가
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

// 값 선택 및 제거 함수
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

function removeValue(value, category) {
    const index = selectedValues[category].indexOf(value);
    if (index > -1) {
        selectedValues[category].splice(index, 1);
    }
    displaySelectedValues();
}

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

// 슬라이더 표시 및 업데이트 함수
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

// 게임 상세 정보 표시 함수
function showGameDetails(game) {
    const modal = document.getElementById("game-modal");
    const modalGameInfo = document.getElementById("modal-game-info");

    const releaseDate = game.tba ? "TBA" : game.released;
    let platforms = game.platforms ? game.platforms : '';
    let genres = game.genre ? game.genre : '';
    let themes = game.theme ? game.theme : '';
    let developers = game.developers ? game.developers : '';
    let publishers = game.publishers ? game.publishers : '';
    let tags = game.tags ? game.tags : '';
    let esrbRating = game.esrb_rating || '';
    let website = game.website && game.website.trim() ? game.website : '';

    let modalContent = `
        <img src="${game.background_image}" alt="${game.name}">
        <div class="game-name">${game.name}</div>
        <div class="game-description"><strong>About</strong> <div>${game.description}</div></div>
        <div class="game-rating"><strong>Ratings:</strong> ${game.rating}<br><br></div>
    `;

    if (platforms) {
        modalContent += `
        <div class="game-platforms-genres">
            <strong>Platforms:</strong> ${platforms}<br>
            <strong>Genre:</strong> ${genres}<br>
            <strong>Themes:</strong> ${themes}
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

// 헬퍼 함수
function displaySections(sections) {
    sections.forEach(section => {
        document.getElementById(section).style.display = 'block';
    });
}

function hideSections(sections) {
    sections.forEach(section => {
        document.getElementById(section).style.display = 'none';
    });
}

function hideCategoryList() {
    const categoryList = document.querySelector('.category-list');
    if (categoryList) {
        categoryList.style.display = 'none';
    }
}
