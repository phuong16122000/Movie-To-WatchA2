"""(Incomplete) Tests for MovieCollection class."""
from movie import Movie
from moviecollection import MovieCollection


from movie import Movie
from moviecollection import MovieCollection


def run_tests():
    """Test MovieCollection class."""

    # Test empty MovieCollection (defaults)
    print("Test empty MovieCollection:")
    movie_collection = MovieCollection()
    print(movie_collection)
    assert not movie_collection.movies  # an empty list is considered False

    # Test loading movies
    print("Test loading movies:")
    movie_collection.load_movies('movies.csv')
    print(movie_collection)
    assert movie_collection.movies  # assuming CSV file is non-empty, non-empty list is considered True

    # Test adding a new Movie with values
    print("Test adding new movie:")
    movie_collection.add_movie(Movie("Chinatown", 1974, "Film Noir", False))
    print(movie_collection)

    # Test sorting movies
    print("Test sorting - year:")
    sorted_list = movie_collection.sort_movies("year", desc=True)
    print(MovieCollection.format_data(sorted_list))
    # TODO: Add more sorting tests

    # TODO: Test saving movies (check CSV file manually to see results)
    print("Test saving movie:")
    movie_collection.save_movies('movies.csv')

    # TODO: Add more tests, as appropriate, for each method
    print("Test unwatched count:")
    print(movie_collection.count_unwatch())
    print("Test watched count:")
    print(movie_collection.count_watch())

    # Add filter method
    print('Test filter method:')
    movie_collection.search_movies('star', 1977, 'action')
    print(MovieCollection.format_data(movie_collection.search_list))


run_tests()
