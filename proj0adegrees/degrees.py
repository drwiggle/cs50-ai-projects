import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
# format: names['Kevin Bacon'] = {102, 9323132} (there are 2 actors with this name
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
# format: people[102] = {
#    'name': 'Kevin Bacon',
#    'birth': '1958',
#    'movies': {104257,112384} list of movie id's
# }
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
# format: movies[112384] = {
#    'title': 'Appollo 13',
#    'year': '1958',
#    'stars': {102, 158, 200, 641} list of person id's
# }
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    # We will use a breadth-first search, as it will be guaranteed to
    # find a shortest path first.

    # I believe it's not possible to invent a heuristic function
    # that satisfies the two requirements which guarantee finding an
    # optimal solution.  So there's no point in trying

    # I've chosen to implement the search graph with nodes labelled by
    # actors and edges labelled by movies.  I suppose you could do things
    # the other way around, but it shouldn't make much difference.

    #initialize frontier and explored set
    frontier = QueueFrontier()
    explored = set()
    
    # if source and target are equal, pick a random movie, and
    # return the appropriate list
    if source == target:
        sourcemovies = list(people[target]['movies'])
        if len(sourcemovies) == 0:
            return None
        return [(sourcemovies[0],target)]

    
    # add source to frontier
    frontier.add(Node(source, None, None))
    
    # iterate while frontier is not empty.  If this loop completes, then there
    # is no path connecting source to target.
    # If a path is found, the return statement within loop will
    # halt execution
    while not frontier.empty():

        # pop person from frontier, add them to list of explored ppl
        currnode = frontier.remove()
        explored.add(currnode.state) # this adds the person_id to the explored set

        # iterate through the movies.  For each one, iterate through the list
        # of stars in said movie, checking to see if star is target,
        # and also checking to see if star is already in frontier, before adding
        # star to end of frontier queue.
            
        for movie in people[currnode.state]['movies']:
            
            for star in movies[movie]['stars']:

                # if star is the target, build the path from source to star
                # return the path
                if star == target:                    
                    path = [(movie,star)]
                    while currnode.parent:
                        path.append((currnode.action, currnode.state))
                        currnode = currnode.parent
                    path.reverse()
                    print(path)
                    return path
                # otherwise, check if star is already in the QueueFrontier.
                # There's no sense in having them in there twice
                elif (star not in explored) and  (not frontier.contains_state(star)):
                    frontier.add(Node(star, currnode, movie))

    return None


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
