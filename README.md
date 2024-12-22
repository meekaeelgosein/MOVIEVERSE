(っ◔◡◔)っ
# MEEKAEELFLASKAPP (The MovieTverse)

#### 𝕍𝕚𝕕𝕖𝕠 𝔻𝕖𝕞𝕠:  <𝕌ℝ𝕃 ℍ𝔼ℝ𝔼>

#### 𝔻𝕖𝕤𝕔𝕣𝕚𝕡𝕥𝕚𝕠𝕟:

My project is a dynamic movie search and filtering web application that uses the TMDB API to help users find movies based on their preferences, like genre, release year, or actor name. I built it using Flask for the backend, which handles the API calls, routes, and form submissions, while keeping things secure by storing my TMDB API key in a .env file. Users can interact with a clean, easy-to-use search form where they can pick a genre from a dropdown menu that’s populated dynamically using the Genre List API, select a year for the movie’s release date, or type in an actor’s name to search for movies they starred in.

To make it all work, I combined multiple TMDB endpoints—like /discover for filtering movies by genre, year, or actor, /search/person to convert actor names into IDs, and /genre/movie/list to fetch the genre options. These filters can work independently of one another, so users don’t need to fill out every field to get results. For example, they can search just by year or actor without selecting a genre. I also wrote helper functions, like fetch_movies_from_api_all and get_actor_id, to clean up and simplify my code by keeping all the logic for API calls in one place.

The results are displayed in a responsive grid layout, with each movie shown in its own card. Each card features the movie poster, title, release date, and overview, along with information about streaming availability—like whether the movie is on Amazon Prime, Apple TV, or other platforms—fetched directly from TMDB. If a movie doesn’t have a poster, I included a placeholder image so the layout always looks polished. I also added hover animations and fallback messages to handle cases where streaming data isn’t available. On the front end, I used Jinja templates to organize the layout and styled everything with CSS to create a clean, modern design that works on both desktop and mobile devices.

One of the challenges I faced was ensuring the filters worked properly on their own or together. I refined my backend logic to handle empty inputs gracefully, so users could perform searches without being forced to fill out all the fields. I also added error handling to display meaningful messages if no results matched the search criteria, ensuring a smooth and user-friendly experience.

The app is fast, functional, and scalable. If I wanted to add more features in the future, I could implement things like pagination for navigating multiple pages of search results, movie detail pages with trailers or reviews, user authentication for creating watchlists, or advanced filters for ratings, runtime, and popularity. I’m proud of how this app turned out because it demonstrates my ability to integrate third-party APIs, build a solid backend, and create a responsive front-end design that delivers a great user experience. It’s been a valuable project for me, and I think it really reflects my growth as a developer.# MOVIEVERSE
