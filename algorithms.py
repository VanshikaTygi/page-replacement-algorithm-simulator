def fifo(pages, capacity) :

    frames = []
    pointer = 0
    hits = 0
    faults = 0

    for page in pages :

        if page in frames :
            hits += 1

        else :
            faults += 1

            if len(frames) < capacity :
                frames.append(page)
            else :
                frames[pointer] = page
                pointer = (pointer + 1) % capacity

    return hits, faults


def lru(pages, capacity) :

    frames = []
    hits = 0
    faults = 0

    for i in range(len(pages)) :
        page = pages[i]

        if page in frames :
            hits += 1
        else :
            faults += 1

            if len(frames) < capacity :
                frames.append(page)
            else :
                # Find least recently used

                lru_page = None
                min_index = float('inf')

                for f in frames :
                    if f in pages[:i] :
                        last_used = max([j for j in range(i) if pages[j] == f])
                    else :
                        last_used = -1    # never used before -> least recently used

                        if last_used < min_index :
                            min_index = last_used
                            lru_page = f

                # Replace LRU page
                if lru_page is None :
                    frames[0] = page           # fallback safety
                else :
                    frames[frames.index(lru_page)] = page

    return hits, faults


def optimal(pages, capacity) :
    frames = []
    hits = 0
    faults = 0

    for i in range(len(pages)) :
        page = pages[i]

        if page in frames :
            hits += 1
        else :
            faults += 1

            if len(frames) < capacity :
                frames.append(page)
            else :
                future_use = {}

                for f in frames :
                    if f in pages[i+1:] :
                        future_use[f] = pages[i+1:].index(f) + i + 1
                    else :
                        future_use[f] = float('inf')
            
                # Find page used farthest in future
                page_to_replace = max(future_use, key=future_use.get)
                frames[frames.index(page_to_replace)] = page

    return hits, faults