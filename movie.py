"""..."""


# TODO: Create your Movie class in this file


class Movie:
    """Movie class"""
    def __init__(self, title='', year=0, category='', is_watched=False):
        """Constructor of movie class"""
        self.title = title
        self.category = category
        self.year = year
        self.is_watched = is_watched

    def __str__(self):
        """Return movie info"""
        watch_check = 'watched' if self.is_watched else 'unwatched'
        return '{} - {} ({}) ({})'.format(self.title, self.year, self.category, watch_check)

    def mark_watched(self):
        """Changing movie to watched"""
        self.is_watched = True

    def mark_unwatched(self):
        """Changing movie to unwatched"""
        self.is_watched = False
