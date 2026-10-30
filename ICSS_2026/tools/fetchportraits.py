#!/usr/bin/env python3
"""Fetch lead images of Wikipedia articles (portraits, machines) for the history
posts, with licence and author from Wikimedia Commons, into Examples/posts/img/.

Only freely licensed files are kept (public domain / CC); anything Commons does
not know, or that is marked non-free, is skipped and reported.  Credits go to
img/credits.json and are rendered into the figure captions by figposts.py.
"""
import json
import os
import re
import sys
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "Examples", "posts", "img")
os.makedirs(IMG, exist_ok=True)
UA = {"User-Agent": "ICSS-course-materials/1.0 (educational use; david.garciabecerra@gmail.com)"}

# key -> English Wikipedia article title
PEOPLE = {
    # session 1
    "babbage": "Charles Babbage", "difference-engine": "Difference engine", "lovelace": "Ada Lovelace",
    "hollerith": "Herman Hollerith", "harvard-computers": "Harvard Computers", "annie-cannon": "Annie Jump Cannon",
    "katherine-johnson": "Katherine Johnson", "dorothy-vaughan": "Dorothy Vaughan", "mary-jackson": "Mary Jackson (engineer)",
    "eniac": "ENIAC", "turing": "Alan Turing", "von-neumann": "John von Neumann", "hopper": "Grace Hopper",
    # session 2
    "leibniz": "Gottfried Wilhelm Leibniz", "boole": "George Boole", "shannon": "Claude Shannon",
    "lamarr": "Hedy Lamarr", "hamming": "Richard Hamming", "huffman": "David A. Huffman", "kahan": "William Kahan",
    "tukey": "John Tukey",
    # session 3
    "punched-card": "Punched card", "simon": "Herbert A. Simon", "newell": "Allen Newell", "luhn": "Hans Peter Luhn",
    "kathleen-booth": "Kathleen Booth", "liskov": "Barbara Liskov", "knuth": "Donald Knuth", "mccarthy": "John McCarthy (computer scientist)",
    # session 4
    "zuse": "Konrad Zuse", "z3": "Z3 (computer)", "sammet": "Jean E. Sammet", "backus": "John Backus",
    "dijkstra": "Edsger W. Dijkstra", "nygaard": "Kristen Nygaard", "dahl": "Ole-Johan Dahl",
    "van-rossum": "Guido van Rossum", "ellis": "Clarence Ellis (computer scientist)",
    # session 5
    "khwarizmi": "Muhammad ibn Musa al-Khwarizmi", "euclid": "Euclid", "hermann": "Grete Hermann",
    "euler": "Leonhard Euler", "erdos": "Paul Erdős", "moore-ef": "Edward F. Moore",
    # session 6
    "fibonacci": "Fibonacci", "lucas": "Édouard Lucas", "dedekind": "Richard Dedekind", "peano": "Giuseppe Peano",
    "hilbert": "David Hilbert", "godel": "Kurt Gödel", "peter": "Rózsa Péter", "bellman": "Richard E. Bellman",
    "naur": "Peter Naur",
    # session 7
    "card-sorter": "IBM card sorter", "holberton": "Betty Holberton", "hoare": "Tony Hoare", "floyd": "Robert W. Floyd",
    "tim-peters": "Tim Peters (software engineer)",
    # session 8
    "landau": "Edmund Landau", "hartmanis": "Juris Hartmanis", "stearns": "Richard E. Stearns", "edmonds": "Jack Edmonds",
    "cook": "Stephen Cook", "karp": "Richard M. Karp", "levin": "Leonid Levin", "blum": "Manuel Blum",
    "goldwasser": "Shafi Goldwasser", "agrawal": "Manindra Agrawal", "kayal": "Neeraj Kayal", "saxena": "Nitin Saxena",
    # session 9
    "church": "Alonzo Church", "kleene": "Stephen Cole Kleene", "post": "Emil Leon Post", "rabin": "Michael O. Rabin",
    "scott": "Dana Scott", "chomsky": "Noam Chomsky", "robinson": "Julia Robinson", "matiyasevich": "Yuri Matiyasevich",
    "bletchley": "Bombe",
    # session 10
    "laplace": "Pierre-Simon Laplace", "gauss": "Carl Friedrich Gauss", "bayes": "Thomas Bayes", "fisher": "Ronald Fisher",
    "mcculloch": "Warren Sturgis McCulloch", "pitts": "Walter Pitts", "rosenblatt": "Frank Rosenblatt", "perceptron": "Perceptron",
    "minsky": "Marvin Minsky", "papert": "Seymour Papert", "hinton": "Geoffrey Hinton", "lecun": "Yann LeCun",
    "bengio": "Yoshua Bengio", "fukushima": "Kunihiko Fukushima", "fei-fei-li": "Fei-Fei Li", "buolamwini": "Joy Buolamwini",
    "gebru": "Timnit Gebru", "vapnik": "Vladimir Vapnik",
    # session 11
    "bachman": "Charles Bachman", "codd": "Edgar F. Codd", "chamberlin": "Donald D. Chamberlin", "selinger": "Patricia Selinger",
    "stonebraker": "Michael Stonebraker", "gray": "Jim Gray (computer scientist)", "ellison": "Larry Ellison", "hipp": "D. Richard Hipp",
    # session 12
    "amdahl": "Gene Amdahl", "illiac": "ILLIAC IV", "flynn": "Michael J. Flynn", "cray": "Seymour Cray", "cray-1": "Cray-1",
    "gordon-moore": "Gordon Moore", "fran-allen": "Frances Allen", "hillis": "Danny Hillis", "connection-machine": "Connection Machine",
    "emeagwali": "Philip Emeagwali", "dean": "Jeff Dean", "ghemawat": "Sanjay Ghemawat", "sutter": "Herb Sutter",
    # session 13
    "schelling": "Thomas Schelling", "milgram": "Stanley Milgram", "granovetter": "Mark Granovetter", "axelrod": "Robert Axelrod (political scientist)",
    "watts": "Duncan J. Watts", "barabasi": "Albert-László Barabási", "lazer": "David Lazer", "adamic": "Lada Adamic",
    "boyd": "danah boyd", "crawford": "Kate Crawford", "noble": "Safiya Noble", "benjamin": "Ruha Benjamin",
    "carley": "Kathleen Carley", "salganik": "Matthew Salganik", "pentland": "Alex Pentland",
    # example posts (extras)
    "excel": "Microsoft Excel", "ariane": "Ariane 5", "titanic": "Titanic", "sudoku": "Sudoku", "konigsberg": "Seven Bridges of Königsberg",
    "literary-digest": "The Literary Digest", "gallup": "George Gallup", "landon": "Alf Landon", "roosevelt": "Franklin D. Roosevelt",
    "kaliningrad": "Kaliningrad", "hanoi": "Tower of Hanoi", "reinhart": "Carmen Reinhart", "rogoff": "Kenneth Rogoff",
    "cloudflare": "Cloudflare", "gpu": "Graphics processing unit", "wikipedia": "Wikipedia", "bundestag": "Bundestag",
    "passport": "German passport", "y2038": "Year 2038 problem", "kevin-bacon": "Kevin Bacon", "wolf": "Wolf", "husky": "Siberian Husky",
    "flu": "Google Flu Trends", "bobby": "SQL injection", "post-sorting": "Mail sorting", "spreadsheet": "Spreadsheet",
}


def api(url, params):
    q = urllib.parse.urlencode({**params, "format": "json"})
    req = urllib.request.Request(url + "?" + q, headers=UA)
    return json.load(urllib.request.urlopen(req, timeout=30))


def wiki_lead(title):
    d = api("https://en.wikipedia.org/w/api.php",
            {"action": "query", "titles": title, "prop": "pageimages", "piprop": "name|thumbnail", "pithumbsize": 420, "redirects": 1})
    for p in d["query"]["pages"].values():
        return p.get("pageimage"), p.get("thumbnail", {}).get("source"), p.get("title")
    return None, None, None


def commons_meta(filename):
    d = api("https://commons.wikimedia.org/w/api.php",
            {"action": "query", "titles": "File:" + filename, "prop": "imageinfo",
             "iiprop": "url|extmetadata", "iiurlwidth": 420})
    for p in d["query"]["pages"].values():
        if "missing" in p:
            return None
        ii = p["imageinfo"][0]
        md = ii.get("extmetadata", {})
        strip = lambda s: re.sub(r"<[^>]+>", "", s or "").strip()
        return {"thumb": ii.get("thumburl"), "license": strip(md.get("LicenseShortName", {}).get("value")),
                "artist": strip(md.get("Artist", {}).get("value"))[:80],
                "page": ii.get("descriptionurl"), "file": filename}


def main(keys=None):
    credits = {}
    cpath = os.path.join(IMG, "credits.json")
    if os.path.exists(cpath):
        credits = json.load(open(cpath))
    todo = keys or [k for k in PEOPLE if k not in credits]
    for key in todo:
        title = PEOPLE[key]
        try:
            fname, thumb, real = wiki_lead(title)
            if not fname:
                print(f"  -- {key:20} no lead image ({title})"); continue
            meta = commons_meta(fname)
            if not meta:
                print(f"  -- {key:20} not on Commons (probably non-free): {fname}"); continue
            lic = meta["license"] or ""
            if "non-free" in lic.lower() or "fair" in lic.lower():
                print(f"  -- {key:20} non-free: {lic}"); continue
            ext = os.path.splitext(fname)[1].lower()
            out = os.path.join(IMG, key + (".jpg" if ext in (".jpg", ".jpeg") else ".png"))
            req = urllib.request.Request(meta["thumb"], headers=UA)
            data = urllib.request.urlopen(req, timeout=60).read()
            open(out, "wb").write(data)
            credits[key] = {"title": real, "file": os.path.basename(out), "license": lic,
                            "artist": meta["artist"], "page": meta["page"]}
            print(f"  ok {key:20} {lic:14} {meta['artist'][:40]}")
        except Exception as e:  # noqa: BLE001
            print(f"  -- {key:20} ERROR {e}")
        json.dump(credits, open(cpath, "w"), indent=1, ensure_ascii=False)
    print(f"\n{len(credits)} images with credits in {cpath}")


if __name__ == "__main__":
    main(sys.argv[1:] or None)
