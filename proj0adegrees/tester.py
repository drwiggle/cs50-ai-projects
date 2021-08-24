
load_data('small')
longest = 0

for p1 in people.keys():
    for p2 in people.keys():
        path = shortest_path(p1, p2)
        if not path:
            print('no path from %s to %s' % (people[p1]['name'], people[p2]['name']))
        elif len(path)> longest:
            longest = len(path)
            pair = (p1,p2)
print('The diameter of the graph is %i.  The two people who are furthest apart are %s and %s' % (longest, people[pair[0]]['name'], people[pair[1]]['name']))
