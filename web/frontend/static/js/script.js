let apiBaseURL = 'http://localhost:5000/api';
let currentPage = 1;
let moviesPerPage = 10;

function loadAllMovies(page = 1, perPage = 10) {
    fetch(`${apiBaseURL}/movies/all?page=${page}&per_page=${perPage}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const moviesList = document.getElementById('all-movies-list');
            if (moviesList) {
                moviesList.innerHTML = '';  // נקה את הרשימה לפני הוספת פריטים חדשים
                data.movies.forEach(movie => {
                    const li = document.createElement('li');
                    li.innerHTML = `<a href="/movie/${movie.movieId}">${movie.movieTitle}</a>`;
                    moviesList.appendChild(li);
                });
                updatePagination(data.total_pages, data.current_page);
            }
        })
        .catch(error => {
            console.error('Fetch error:', error);
        });
}

function updatePagination(totalPages, currentPage) {
    const pagination = document.getElementById('pagination');
    if (pagination) {
        pagination.innerHTML = '';  // נקה את האלמנט לפני הוספת פריטים חדשים

        // הוספת כפתור לעמוד הראשון
        const firstPage = document.createElement('span');
        firstPage.innerText = '<<';
        firstPage.classList.add('page-item');
        firstPage.addEventListener('click', () => loadAllMovies(1, moviesPerPage));
        pagination.appendChild(firstPage);

        // הוספת כפתור לעמוד הקודם
        if (currentPage > 1) {
            const prevPage = document.createElement('span');
            prevPage.innerText = '<';
            prevPage.classList.add('page-item');
            prevPage.addEventListener('click', () => loadAllMovies(currentPage - 1, moviesPerPage));
            pagination.appendChild(prevPage);
        }

        // חישוב העמודים להצגה
        let startPage = Math.max(1, currentPage - 2);
        let endPage = Math.min(totalPages, currentPage + 3);

        if (endPage - startPage < 5) {
            if (startPage === 1) {
                endPage = Math.min(6, totalPages);
            } else if (endPage === totalPages) {
                startPage = Math.max(1, totalPages - 5);
            }
        }

        // הוספת מספרי העמודים
        for (let i = startPage; i <= endPage; i++) {
            const pageItem = document.createElement('span');
            pageItem.innerText = i;
            pageItem.classList.add('page-item');
            if (i === currentPage) {
                pageItem.classList.add('active');
            }
            pageItem.addEventListener('click', () => loadAllMovies(i, moviesPerPage));
            pagination.appendChild(pageItem);
        }

        // הוספת כפתור לעמוד הבא
        if (currentPage < totalPages) {
            const nextPage = document.createElement('span');
            nextPage.innerText = '>';
            nextPage.classList.add('page-item');
            nextPage.addEventListener('click', () => loadAllMovies(currentPage + 1, moviesPerPage));
            pagination.appendChild(nextPage);
        }

        // הוספת כפתור לעמוד האחרון
        const lastPage = document.createElement('span');
        lastPage.innerText = '>>';
        lastPage.classList.add('page-item');
        lastPage.addEventListener('click', () => loadAllMovies(totalPages, moviesPerPage));
        pagination.appendChild(lastPage);
    }
}

function changeMoviesPerPage(perPage) {
    moviesPerPage = perPage;
    loadAllMovies(1, moviesPerPage);  // טען את העמוד הראשון עם מספר הסרטים החדש
}

function searchMovies(query) {
    fetch(`${apiBaseURL}/search_movies?q=${query}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const moviesList = document.getElementById('all-movies-list');
            if (moviesList) {
                moviesList.innerHTML = '';  // נקה את הרשימה לפני הוספת פריטים חדשים
                data.forEach(movie => {
                    const li = document.createElement('li');
                    li.innerHTML = `<a href="/movie/${movie.movieId}">${movie.movieTitle}</a>`;
                    moviesList.appendChild(li);
                });
                document.getElementById('pagination').innerHTML = '';  // נקה את הפאגינציה
            }
        })
        .catch(error => {
            console.error('Fetch error:', error);
        });
}

function loadMovieDetail(movieId) {
    fetch(`${apiBaseURL}/movie/${movieId}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('movie-title').textContent = data.movieTitle;
            document.getElementById('movie-year').textContent = data.movieYear;
            document.getElementById('movie-rating').textContent = data.rating;
            document.getElementById('critic-score').textContent = data.critic_score;
            document.getElementById('critic-sentiment').textContent = data.critic_sentiment;
            document.getElementById('audience-score').textContent = data.audience_score;
            document.getElementById('audience-sentiment').textContent = data.audience_sentiment;
            document.getElementById('release-date-theaters').textContent = data.release_date_theaters;
            document.getElementById('release-date-streaming').textContent = data.release_date_streaming;
            document.getElementById('original-language').textContent = data.original_language;
            document.getElementById('runtime').textContent = data.runtime;
            document.getElementById('movie-quote').textContent = data.quote;
        })
        .catch(error => {
            console.error('Error fetching movie details:', error);
        });
}