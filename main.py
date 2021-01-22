"""
Name: Vu Le Nguyen Phuong
Date:18/01/2020
Brief Project Description: My small project to store the list of movies. I have add extra functionality
    including sort by ascending and descending order and search movie from the list :)
GitHub URL:https://github.com/phuong16122000/Movie-To-WatchA2
"""
# TODO: Create your main program in this file, using the MoviesToWatchApp class

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.uix.button import Button
from movie import Movie
from moviecollection import MovieCollection
from string import capwords


class MoviesToWatchApp(App):
    """Class for GUI movie app"""
    # Initiate string and list properties
    sort_by = StringProperty()
    category = ListProperty()
    order = ListProperty()
    current_order = StringProperty()

    def __init__(self, **kwargs):
        """Constructor that initiate my collection and movie list"""
        super(MoviesToWatchApp, self).__init__(**kwargs)
        self.my_collection = MovieCollection()
        # Create another list to not TOUCH the original list, in case for back-up or error
        self.movie_to_show = []

    def build(self):
        """Build from the root kv file"""
        Window.size = (1000, 800)
        self.title = "Movie To Watch 2.0 by Van Phuong Nguyen"
        self.root = Builder.load_file('app.kv')
        # Set category list
        self.category = ['Title', 'Year', 'Category', 'Unwatch']
        # Default sorting option
        self.sort_by = self.category[0]
        # Set order list
        self.order = ['Ascending Order', 'Descending Order']
        # Set default order
        self.current_order = self.order[0]
        return self.root

    def on_start(self):
        """Start when program start"""
        self.my_collection.load_movies('movies.csv')
        # Separate movie list to not change to original list
        self.movie_to_show = self.my_collection.movies
        # Make sure the height is such that there is something to scroll.
        self.root.ids.movie_list.bind(minimum_height=self.root.ids.movie_list.setter('height'))
        # Show welcome message
        self.root.ids.message.text = 'Let\'s watch some movies :)'
        # Load movies
        self.load_movies()
        # Show watch and unwatch count
        self.count_watch()

    def on_stop(self):
        """Close program and save movies to the file"""
        self.my_collection.save_movies('movies.csv')

    def count_watch(self):
        """Count movie based on watch and unwatch"""
        self.root.ids.watch_count.text = 'To watch: {}. Watched: {}'.format(self.my_collection.count_unwatch(),
                                                                            self.my_collection.count_watch())

    def sort_movies(self, key):
        """Sort movie based on key"""
        # Change current sort_by key based on the key from the sort spinner
        self.sort_by = key
        # Load movies based on key provided
        self.load_movies()

    def handle_order(self, element):
        """Sort movie based on order"""
        # Change current order for loading
        self.current_order = element
        # Load movie based on current order
        self.load_movies()

    def handle_add_movie(self, title, year, category):
        """Add movie to movie list"""
        # Only add movie when title, year, category are provided
        if title and year and category:
            # Make sure that title input is correct
            title_check = self.handle_input(title, is_title=True)
            # Make sure that category is on category list
            category_check = self.handle_input(category, is_category=True)
            # Make sure that year is a number >= 0
            year_check = self.handle_input(year, is_year=True)
            if year_check and category_check and title_check:
                # Make the input prettier
                clean_title = ' '.join(title.split())
                pretty_title = capwords(clean_title)
                pretty_category = capwords(category)
                # Check if  movie is already exist
                if self.check_exist(title_check, year_check, category_check):
                    self.show_popup_message('The movie is already exist')
                else:
                    # Add movie to list, then reload movie list
                    self.my_collection.add_movie(Movie(title_check, year_check, category_check))
                    self.load_movies()
                    self.show_popup_message('{} have been add to movie list'.format(pretty_title))
                    self.handle_clear_button(is_add=True)

        else:
            # Show error if any field blank
            self.show_popup_message('All fields are required')

    def load_movies(self):
        """Load movie to the GUI movie list"""
        # First clear the current movie on list
        self.root.ids.movie_list.clear_widgets()
        # Check the current order
        desc = self.current_order == 'Descending Order'
        # Add movies based on current sort_by and order to movie to show list
        self.movie_to_show = self.my_collection.sort_movies(self.sort_by, desc)
        # Add buttons based on movie list
        for index, movie in enumerate(self.movie_to_show):
            watch_mark = 'watched' if movie.is_watched else ''
            btn = Button(text='{} ({} from {}) {}'.format(movie.title, movie.category, movie.year, watch_mark),
                         size_hint_y=None, height=30)
            # Save movie object to btn
            btn.movie = movie
            # If pressed, execute handle_watch_movie function
            btn.bind(on_press=self.handle_watch_movie)
            # If movie is watched, change background color
            if watch_mark:
                btn.background_color = (1, 0.5, 0.5, 1)
            # Add btn to movie_list id
            self.root.ids.movie_list.add_widget(btn)

    def handle_watch_movie(self, instance):
        """Handle watch movie if user click on movie"""
        # Movie object is saved to btn.movie >> instance.movie
        current_movie = instance.movie
        # Toggle between watch/unwatch
        current_movie.is_watched = not current_movie.is_watched
        # Load movie to the GUI list for immediate sorting
        self.load_movies()
        # Show message and reload the count watch
        watch_mark = 'watched' if current_movie.is_watched else 'unwatched'

        self.root.ids.message.text = 'You have {} {}'.format(watch_mark, current_movie.title)
        self.count_watch()

    def show_popup_message(self, text):
        """Handle show popup message"""
        self.root.ids.popup_message.text = text
        self.root.ids.popup.open()

    def handle_close_popup(self):
        """Close the popup"""
        self.root.ids.popup_message.text = ''
        self.root.ids.popup.dismiss()

    def handle_clear_button(self, is_add=False, is_search=False):
        """Clear input when pressed"""
        # If is_add, clear the add movie input
        if is_add:
            self.root.ids.title.text = ''
            self.root.ids.year.text = ''
            self.root.ids.category.text = ''
        # If is_search, clear the search input
        elif is_search:
            self.root.ids.title_search.text = ''
            self.root.ids.year_search.text = ''
            self.root.ids.category_search.text = ''
            self.root.ids.watch_search.text = ''
        # Else clear all
        else:
            self.root.ids.title.text = ''
            self.root.ids.year.text = ''
            self.root.ids.category.text = ''
            self.root.ids.title_search.text = ''
            self.root.ids.year_search.text = ''
            self.root.ids.category_search.text = ''
            self.root.ids.watch_search.text = ''

    def handle_search(self, title, year, category, watch):
        """Search for movie in list"""
        # Only search when at least on field is provided
        if title or category or watch or year:
            # Check for valid year, category and title
            title_check = self.handle_input(title, is_title=True, blank=True)
            year_check = self.handle_input(year, is_year=True, blank=True)
            category_check = self.handle_input(category, is_category=True, blank=True)
            watch_check = self.handle_input(watch, is_watch=True, blank=True)
            # If all are valid, then search
            if title_check and year_check and category_check and watch_check:
                # If is_watched is provided, change to bool, else None
                is_watched = None
                if watch:
                    is_watched = watch.lower() == 'y'
                # Search movie method
                self.my_collection.search_movies(title.strip(), year, category, is_watched)
                # If found, show movie count and display in GUI movie list
                if self.my_collection.search_list:
                    self.movie_to_show = self.my_collection.search_list
                    self.show_popup_message('We have found: {} movies'.format(len(self.movie_to_show)))
                    self.load_movies()
                    # Clear the input when completed
                    self.handle_clear_button(is_search=True)
                # If no movie found, show error message
                else:
                    self.show_popup_message('No movie found!')
        else:
            # If no field is fill in, show error message
            self.show_popup_message('Your must at least fill in one field')

    def handle_clear_search(self):
        """Clear the search and return the original list"""
        # Set search list to empty
        self.my_collection.search_list = []
        self.handle_clear_button(is_search=True)
        self.load_movies()

    def check_exist(self, title, year, category):
        """Check if movie is existed"""
        # Filter method based on title, year, category
        def find_duplicate(movie):
            filter_title = title.lower() == movie.title.lower()
            filter_year = int(movie.year) == int(year)
            filter_category = movie.category.lower() == category.lower()
            return filter_title and filter_year and filter_category

        return list(filter(find_duplicate, self.my_collection.movies))

    def handle_input(self, input_data, is_title=False, is_year=False, is_category=False, is_watch=False, blank=False):
        """Handle input data"""
        # Check if year > 0 and is a number
        if blank and not input_data:
            return True
        else:
            if is_year:
                try:
                    year = int(input_data)
                    if year < 0:
                        raise ValueError()
                    return input_data.strip()
                except ValueError:
                    self.show_popup_message('Your year must be a number and greater than 0')
            # Check if input in category list
            elif is_category:
                # Check if category is in the category list
                if input_data.lower().strip() not in ['action', 'comedy', 'documentary', 'drama', 'fantasy',
                                                      'thriller']:
                    self.show_popup_message('Please enter a correct category '
                                            '(Action, Comedy, Documentary, Drama, Fantasy, Thriller)')
                else:
                    return input_data.strip()
            # Check if valid watch
            elif is_watch:
                if input_data.lower() not in ['y', 'n']:
                    self.show_popup_message('Your watch field must be Y or N')
                else:
                    return True
            # Check if title is blank
            elif not input_data.strip() and is_title:
                self.show_popup_message('Your title must not be blank')
            else:
                return input_data.strip()


if __name__ == '__main__':
    # Execute GUI program
    MoviesToWatchApp().run()
