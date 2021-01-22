"""..."""
# TODO: Copy your first assignment to this file, then update it to use Movie class
# Optionally, you may also use MovieCollection class

from movie import Movie

REMAINDER = [1]
TOTAL_MOVIE = [0]
movie_list = open('movies.csv', 'r')
FILE_LIST = movie_list.readlines()

'''This is the main function of the program, here the main_menu function is triggered, lead the users to the main 
menu for interaction.  '''


def main():
    """..."""
    print("Movies To Watch 2.0 - by Phuong Vu")
    main_menu()


'''The main_menu function will display the options for users to choose and go directly to the three main functions, 
show lists (L), watch a movie(W), add a movie(A) and Quit(Q). After interacting with the programs, the Quit option 
will save all changes and then write to the movies.csv file '''


def main_menu():
    print("Menu:")
    count_load = 0
    for lines in FILE_LIST:
        count_load += 1
    print(count_load, "movies loaded")

    print("L - List movies")
    print("A - Add new movie")
    print("W - Watch a movie")
    print("Q - Quit")
    menu = input(">>>").upper()
    while menu not in ["L", "A", "W", "Q"]:
        menu = input("Invalid, please re-enter and appropriate option: ").upper()
    if menu == "L":
        list_function()
    if menu == "A":
        add_function()
    if menu == "W":
        watched_function()
    else:
        confirm = input("Are you sure you want to quit? -(Y)es, (N)o ").upper()
        while confirm not in ["Y", "N"]:
            confirm = input("Invalid, please re-enter your option: (Y)es or (N)o").upper()
        if confirm == "Y":
            with open('movies.csv', 'w') as song_list:
                for item in FILE_LIST:
                    movie_list.write("{}".format(item))
            print("----Saving to your csv file----")
            print("-- Exited playlist. Have a nice day! --")
            quit()
        else:
            main_menu()


'''list_function show all the current movies and its status(watched or need to be watch). All the data read inside the 
CSV files will be store inside a list for interaction and then write back to the csv file after all interactions are 
done. Because it is difficult to interact directly with the csv file through read and write command of Python, 
so i create a list (FILE_LIST) and import all csv data to it, users will interact and change the value inside the 
list and then after the program is closed, data inside the list will be writen it back to the csv file '''


def list_function():
    count = 0
    count_watched = 0

    list = []
    for lines in FILE_LIST:
        count += 1
        new_lines = lines.split(',')
        input_movie = new_lines[0]
        input_year = new_lines[1]
        input_category = new_lines[2]
        watch = new_lines[3].replace("w", "*").replace("u", "").replace("\n", "")
        list.append(count)
        movies_display = (
            "{:>2}. {:<1} {:<35} - {:<35} ({})".format(count, watch, input_movie, input_year, input_category))
        print(movies_display)

        if "*" in watch:
            count_watched += 1
    print("-" * 100)
    print("Total movies loaded: ", max(list))
    count_need = (max(list) - count_watched)
    REMAINDER.append(count_need)
    print(max(list) - count_watched, "movies still to watch")
    print(count_watched, "movies watched")
    TOTAL_MOVIE.append(max(list))
    print("-" * 100)
    main_menu()


'''' add_function allows users too add more movies to the FILE_LIST list, so later on it can be displayed and 
formatted in the list_function() function '''


def add_function():
    watch_status = "u\n"
    title = input("Title: ")
    while title == "":
        print("Input can not be blank")
        title = input("Title: ")
    category = input("Category: ")
    while category == "":
        print("Input can not be blank")
        category = input("Category: ")
    test = True
    while test == True:
        try:
            year = int(input("Year: "))
            test = False
        except ValueError:
            print("Invalid input; enter a valid number")
    while year < 0:
        print("Number must be >= 0")
        test = True
        while test == True:
            try:
                year = int(input("Year: "))
                test = False
            except ValueError:
                print("Invalid input; enter a valid number")

    if REMAINDER[-1] == 0:
        REMAINDER.remove(REMAINDER[-1])
    final_result = ("{},{},{},{}".format(title, year, category, watch_status))
    FILE_LIST.append(final_result)
    print("{} from {} by ({}) added to movie list".format(title, year, category))
    print('-' * 100)
    main_menu()


'''Watched_function() allows user to mark the completed movies. If all the movies are marked complete, there will be 
the print to show that there are no more movies to learn '''


def watched_function():
    watched_status = "w\n"
    if min(REMAINDER) == 0:
        print('-' * 100)
        print("No more movies to watch!")
        print('-' * 100)
        main_menu()

    test = True
    while test == True:
        try:
            number = int(input("Enter the number of a movie to be marked as watched: "))
            test = False
        except ValueError:
            print("Invalid input, please enter a number")
    if max(TOTAL_MOVIE) == 0:
        print("-" * 100)
        print("Please load the list of movies first by type in L in the main menu")
        print("Remember to load the list movie for checking every time you make a change")
        print("-" * 100)
        main_menu()

    while number > max(TOTAL_MOVIE) or number <= 0:
        print("Please input the appropriate value!")
        number = int(input("Enter the number of the movie to be marked as watched: "))

    rows = FILE_LIST[number - 1]
    new_list_rows = rows.split(",")
    movie_name = new_list_rows[0]
    year = new_list_rows[1]
    category_name = new_list_rows[2]
    result = ("{},{},{},{}".format(movie_name, year, category_name, watched_status))
    result_1 = ("'{} from {} by {}' is marked watched! Congratulation!".format(movie_name, year, category_name))
    FILE_LIST.append(result)
    FILE_LIST.remove(FILE_LIST[number - 1])
    print(result_1)
    print("Remember to load the list movie for checking every time you make a change")
    print('-' * 100)
    main_menu()


if __name__ == '__main__':
    main()