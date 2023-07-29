import wikipediaapi
from tqdm import tqdm
import requests

wiki = wikipediaapi.Wikipedia('en')

def get_redirectors(title):
    response = requests.get(f"https://en.wikipedia.org/w/api.php?action=query&prop=redirects&format=json&rdlimit=500&titles={title}")
    query_dict = response.json()['query']['pages']
    page_id = list(query_dict.keys())[0]
    red_dict = response.json()['query']['pages'][page_id]['redirects']
    all_titles = [title]
    for dict in red_dict:
        all_titles.append(dict['title'])
    return all_titles

def isonestep(startt, endt):
    """
    inputs:
        startt: title of origin wikipedia page (string)
        endt: title of destination wikipedia page (string)
    outputs:
        bool
    "step" = click on hyperlink
    this function should tell us whether we can move
    from startt to endt in one "step" :)
    is endp, or any endp redirects, within startplinks
    do any startplinks == endp or endpredirects
    """
    startp = wiki.page(startt)
    endp = wiki.page(endt)
    titleopts = get_redirectors(endt)
    for pager in startp.links.keys():
        if pager in titleopts:
            return True
    return False

def get_neighbors(titles):
    all_neighbors = set()
    for title in tqdm(titles):
        page = wiki.page(title)
        for neighbor in page.links.keys():
            all_neighbors.add(neighbor)
    return all_neighbors

def step_checker(startt, endt, N):
    # first, we'll check if one step
    S = 1
    if isonestep(startt, endt):
        return S
    else:
        #last_layer = most recent list of titles
        last_layer = [startt]
        while S < N: #this ensures we won't go over the ceiling we impose
            S += 1 #this means we're adding one to S
            print(f"Getting Neighbors of Layer {S-1}")
            neighbors = get_neighbors(last_layer) #find the links of the most recent list of titles
            print("Checking Neighbors")
            for neighbor in tqdm(neighbors): #check if the title of linked page is one step
                if isonestep(neighbor, endt):
                    print(neighbor)
                    return S
            last_layer = neighbors #if none of the linked pages are one step, 
            #update the list of titles to include all of the neighboring titles
        print("Exceeds Ceiling") #if we hit the ceiling on N, let ur girl know