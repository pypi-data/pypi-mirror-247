def mystery():
    from random import randint, choice
    ch = 0
    while ch == 0:
        ch = 1
        select = int(input("---------- 1: Easy Level ----------\n---------- 2: Meduim Level ----------\n---------- 3: Hard Level ----------\nSelect your level:\n>>    "))
        attempt = 0
        if select == 1:
            guess = randint(0, 100)
            data = int(input("Guess the number from 0 -> 100:\n>>    "))
            for i in range(15):
                if data == guess:
                    attempt += 1
                    print("YOU GOT IT IN", attempt, "attempts")
                    break
                elif data > guess:
                    attempt += 1
                    count = 15 - attempt
                    print(count, "attempts left.")
                    data = int(input("less\n>>    "))
                elif data < guess:
                    attempt += 1
                    count = 15 - attempt
                    print(count, "attempts left.")
                    data = int(input("more\n>>    "))
                if attempt == 14:
                    if data != guess:
                        print("Failed :( try again later...")
                        break
        elif select == 2:
            guess = randint(0, 1000)
            data = int(input("Guess the number from 0 -> 1000:\n>>    "))
            for i in range(10):
                if data == guess:
                    attempt += 1
                    print("YOU GOT IT IN", attempt, "attempts")
                    break
                elif data > guess:
                    attempt += 1
                    count = 10 - attempt
                    print(count, "attempts left.")
                    data = int(input("less\n>>    "))
                elif data < guess:
                    attempt += 1
                    count = 10 - attempt
                    print(count, "attempts left.")
                    data = int(input("more\n>>    "))
                if attempt == 9:
                    if data != guess:
                        print("Failed :( try again later...")
                        break
        elif select ==3:
            guess = randint(10, 100)
            chr = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
            char = choice(chr)
            data = int(input("Guess the number from 10 -> 100:\n>>    "))
            datach = str(input("Guess the character from a -> z:\n>>    "))
            for i in range(10):
                datach = datach.lower()
                if data == guess and datach == char:
                    attempt += 1
                    count = 10 - attempt
                    print(count, "attempts left.")
                    print("YOU GOT IT IN", attempt, "attempts")
                    break
                elif data == guess and datach > char:
                    attempt += 1
                    count = 10 - attempt
                    print(count, "attempts left.")
                    print("Number is correct. Character is before")
                    datach = str(input("character is before\n>>    "))
                    datach = datach.lower()
                elif data == guess and datach < char:
                    attempt += 1
                    count = 10 - attempt
                    print(count, "attempts left.")
                    print("Number is correct. Character is after")
                    datach = str(input("character is after\n>>    "))
                    datach = datach.lower()
                elif data > guess and datach == char:
                    attempt += 1
                    count = 10 - attempt
                    print(count, "attempts left.")
                    print ("Character is correct. Number is less")
                    data = int(input("number is less\n>>    "))
                elif data > guess and datach > char:
                    attempt += 1
                    count = 10 - attempt
                    print(count, "attempts left.")
                    print("Number is less. Character is before")
                    data = int(input("number is less\n>>    "))
                    datach = str(input("character is before\n>>    "))
                    datach = datach.lower()
                elif data > guess and datach < char:
                    attempt += 1
                    count = 10 - attempt
                    print(count, "attempts left.")
                    print("Number is less. Character is after")
                    data = int(input("number is less\n>>    "))
                    datach = str(input("character is after\n>>    "))
                    datach = datach.lower()
                elif data < guess and datach == char:
                    attempt += 1
                    count = 10 - attempt
                    print(count, "attempts left.")
                    print("Character is correct. Number is more")
                    data = int(input("number is more\n>>    "))
                elif data < guess and datach < char:
                    attempt += 1
                    count = 10 - attempt
                    print(count, "attempts left.")
                    print("Number is more. Character is after")
                    data = int(input("number is more\n>>    "))
                    datach = str(input("character is after\n>>    "))
                    datach = datach.lower()
                elif data < guess and datach > char:
                    attempt += 1
                    count = 10 - attempt
                    print(count, "attempts left.")
                    print("Number is more. Character is before")
                    data = int(input("number is more\n>>    "))
                    datach = str(input("character is before\n>>    "))
                    datach = datach.lower()
                if attempt == 9:
                    if data != guess or datach != char:
                        print("Failed :( try again later...")
                        break
        else:
            print("error at choicing level :(")
            ch = 0
def mental_calculation():
    from time import sleep
    from threading import Thread
    from random import randint,choice
    t = 1
    print('You must get most points in mental calculation in 30 secondes')
    sleep(5)
    def SpeedRun():
        p = 0
        while t > 0:
            f = randint(0,10)
            s = randint(0,10)
            rand = ['add', 'sub', 'mult', 'div']
            o = choice(rand)
            if o == 'add':
                data = f + s
                ans = int(input(str(f)+' + '+str(s)+' = ?\n>>   '))
                if ans == data:
                    print('Correct!')
                    p += 1
                else:
                    print('Fail!')
            if o == 'sub':
                data = f - s
                ans = int(input(str(f)+' - '+str(s)+' = ?\n>>   '))
                if ans == data:
                    print('Correct!')
                    p += 1
                else:
                    print('Fail!')
            if o == 'mult':
                data = f * s
                ans = int(input(str(f)+' * '+str(s)+' = ?\n>>   '))
                if ans == data:
                    print('Correct!')
                    p += 1
                else:
                    print('Fail!')
            if o == 'div':
                s = randint(1,5)
                if s == 1:
                    f = randint(0,10)
                elif s == 2:
                    choices = [0,2,4,6,8,10]
                    f = choice(choices)
                elif s == 3:
                    choices = [0,3,6,9]
                    f = choice(choices)
                elif s == 4:
                    choices = [0,4,8]
                    f = choice(choices)
                elif s == 5:
                    choices = [0,5,10]
                    f = choice(choices)
                data =  f / s
                ans = int(input(str(f)+' / '+str(s)+' = ?\n>>   '))
                if ans == data:
                    print('Correct!')
                    p += 1
                else:
                    print('Fail!')
        if t == 0:
            print('Time is up!\nYou score is',p)
    Thread(target=SpeedRun).start()
    sleep(30)
    t = 0
def root(num, nth=2):
    if num < 0:
        raise TypeError
    else:
        return num**(1/nth)
def quad(a, b, c):
    if a == 0:
        raise ZeroDivisionError
    else:
        quad.delta = b**2 - 4*a*c
        if a + b + c == 0:
            if quad.delta == 0:
                quad.x0 = -b/(2*a)
                if a > 0:
                    signa = "+"
                else:
                    signa = "-"
                return f"a = {a} ; b = {b} ; c = {c}\na + b + c = 0\nx1 = 1\nx2 = c/a = {c}/{a} = {quad.x0}\n\n\nx      | -∞      x0     +∞ |\n————————————————————————————\nP(x)   |    {signa}    0    {signa}    |"
            else:
                quad.x1 = 1
                quad.x2 = c/a
                if a > 0:
                    signa = "+"
                    sign_a = "-"
                else:
                    signa = "-"
                    sign_a = "+"
                if quad.x1 > quad.x2:
                    return f"a = {a} ; b = {b} ; c = {c}\na + b + c = 0\nx1 = 1\nx2 = c/a = {c}/{a} = {quad.x2}\n\n\nx      | -∞     x2         x1     +∞ |\n——————————————————————————————————————\nP(x)   |    {signa}    0    {sign_a}    0    {signa}    |"
                else:
                    return f"a = {a} ; b = {b} ; c = {c}\na + b + c = 0\nx1 = 1\nx2 = c/a = {c}/{a} = {c/a}\n\n\nx      | -∞     x1         x2     +∞ |\n——————————————————————————————————————\nP(x)   |    {signa}    0    {sign_a}    0    {signa}    |"
        elif a - b + c == 0:
            if quad.delta == 0:
                quad.x0 = -b/(2*a)
                if a > 0:
                    signa = "+"
                else:
                    signa = "-"
                return f"a = {a} ; b = {b} ; c = {c}\na - b + c = 0\nx1 = -1\nx2 = -c/a = {-c}/{a} = {quad.x0}\n\n\nx      | -∞      x0     +∞ |\n————————————————————————————\nP(x)   |    {signa}    0    {signa}    |"
            else:
                quad.x1 = -1
                quad.x2 = -c/a
            if a > 0:
                signa = "+"
                sign_a = "-"
            else:
                signa = "-"
                sign_a = "+"
            if quad.x1 > quad.x2:
                return f"a = {a} ; b = {b} ; c = {c}\na - b + c = 0\nx1 = -1\nx2 = -c/a = {-c}/{a} = {quad.x2}\n\n\nx      | -∞     x2         x1     +∞ |\n——————————————————————————————————————\nP(x)   |    {signa}    0    {sign_a}    0    {signa}    |"
            else:
                return f"a = {a} ; b = {b} ; c = {c}\na - b + c = 0\nx1 = -1\nx2 = -c/a = {-c}/{a} = {quad.x2}\n\n\nx      | -∞     x1         x2     +∞ |\n——————————————————————————————————————\nP(x)   |    {signa}    0    {sign_a}    0    {signa}    |"
        elif quad.delta > 0:
            quad.x1 = (-b - quad.delta**(1/2))/(2*a)
            quad.x2 = (-b + quad.delta**(1/2))/(2*a)
            if a > 0:
                signa = "+"
                sign_a = "-"
            else:
                signa = "-"
                sign_a = "+"
            if quad.x1 > quad.x2:
                return f"a = {a} ; b = {b} ; c = {c}\nΔ = b² - 4ac\nΔ = {b}² - 4 × {a} × {c}\nΔ = {b**2} - {4*a*c}\nΔ = {quad.delta}\nx1 = (-b - √Δ) / 2a = ({-b} - √{quad.delta}) / (2 × {a}) = {quad.x1}\nx2 = (-b + √Δ) / 2a = ({-b} + √{quad.delta}) / (2 × {a}) = {quad.x2}\n\n\nx      | -∞     x2         x1     +∞ |\n——————————————————————————————————————\nP(x)   |    {signa}    0    {sign_a}    0    {signa}    |"
            else:
                return f"a = {a} ; b = {b} ; c = {c}\nΔ = b² - 4ac\nΔ = {b}² - 4 × {a} × {c}\nΔ = {b**2} - {4*a*c}\nΔ = {quad.delta}\nx1 = (-b - √Δ) / 2a = ({-b} - √{quad.delta}) / (2 × {a}) = {quad.x1}\nx2 = (-b + √Δ) / 2a = ({-b} + √{quad.delta}) / (2 × {a}) = {quad.x2}\n\n\nx      | -∞     x1         x2     +∞ |\n——————————————————————————————————————\nP(x)   |    {signa}    0    {sign_a}    0    {signa}    |"
        elif quad.delta == 0:
            quad.x0 = -b/(2*a)
            if a > 0:
                signa = "+"
            else:
                signa = "-"
            return f"a = {a} ; b = {b} ; c = {c}\nΔ = b² - 4ac\nΔ = {b}² - 4 × {a} × {c}\nΔ = {b**2} - {4*a*c}\nΔ = {quad.delta}\nx0 = -b / 2a = ({-b} / (2 × {a}) = {quad.x0}\n\n\nx      | -∞      x0     +∞ |\n————————————————————————————\nP(x)   |    {signa}    0    {signa}    |"
        else:
            if a > 0:
                signa = "+"
            else:
                signa = "-"
            return f"a = {a} ; b = {b} ; c = {c}\nΔ = b² - 4ac\nΔ = {b}² - 4 × {a} × {c}\nΔ = {b**2} - {4*a*c}\nΔ = {quad.delta} < 0\n\n\nx      | -∞         +∞ |\n———————————————————————\nP(x)   |       {signa}       |"
def among_us(PlayersNumber: int, lang="eng"):
    if type(PlayersNumber) != int:
        raise TypeError
    elif PlayersNumber <= 2:
        print("Players number should be greater than 2")
    else:
        from random import choice
        if lang == "eng":
            players = {}
            words = ["Table", "Chair", "Lamp", "Sofa", "Bookshelf", "Television", "Remote control", "Clock", "Mirror", "Vase", 
                "Pillow", "Blanket", "Curtain", "Rug", "Desk", "Computer", "Mouse", "Keyboard", "Monitor", "Printer", 
                "Refrigerator", "Stove", "Microwave", "Toaster", "Dishwasher", "Plate", "Fork", "Knife", "Spoon", "Cup", 
                "Vase", "Plant", "Picture frame", "Candle", "Basket", "Tray", "Towel", "Soap", "Shampoo", "Toothbrush", 
                "Toothpaste", "Towel rack", "Toilet", "Sink", "Mirror", "Soap dispenser", "Towel holder", "Shower", "Bathtub", 
                "Bed", "Mattress", "Pillowcase", "Blanket", "Alarm clock", "Dresser", "Wardrobe", "Hanger", "Shoes", 
                "Slippers", "Closet", "Coat rack", "Umbrella", "Hat", "Gloves", "Scarf", "Sunglasses", "Wallet", 
                "Keychain", "Purse", "Backpack", "Suitcase", "Briefcase", "Pen", "Pencil", "Notebook", "Eraser", 
                "Stapler", "Tape", "Scissors", "Glue", "Calculator", "Ruler", "Folder", "Paperclip", "Document", 
                "Envelope", "Stamp", "Trash can", "Recycling bin", "Laundry basket", "Iron", "Ironing board", 
                "Detergent", "Broom", "Dustpan", "Mop", "Bucket", "Vacuum cleaner", "Cleaning cloth", "Air freshener",
                "Sofa", "Television", "Heater", "Fan", "Air conditioner", "Bookshelf", "Console", "Speaker", "Book", 
                "Newspaper", "Magazine", "CD", "DVD", "Video game", "Camera", "Camcorder", "Phone", "Tablet", "Headphones", 
                "Charger", "Battery", "Cable", "Wall clock", "Pocket watch", "Wristwatch", "Jewelry", "Wallet", 
                "Card", "Paper", "Fountain pen", "Brush", "Paint", "Color pencil", "Brush", "Canvas", "Easel", 
                "Ink", "Shelf", "Library", "Chest of drawers", "Makeup mirror", "Perfume", "Jewelry box", 
                "Cushion", "Throw", "Tablecloth", "Dishware", "Cutlery", "Kitchen", "Glass", "Coffee cup", "Tea cup", 
                "Plate", "Bowl", "Tablecloth", "Napkin", "Shower curtain", "Heated towel rack", "Toilet", 
                "Sink", "Bathtub", "Shower", "Towel", "Bathrobe", "Hair dryer", "Hair straightener", "Hairbrush", 
                "Makeup", "Eyeshadow", "Lipstick", "Mascara", "Makeup brush", "Cotton swab", "Makeup remover", 
                "Moisturizer", "Deodorant", "Shampoo", "Conditioner", "Shower gel", "Soap", "Lotion", "Lip balm", 
                "Tissue", "Trash bag", "Laundry basket", "Laundry", "Fabric softener", "Ironing board", "Iron", 
                "Detergent", "Broom", "Dustpan", "Bucket", "Cloth", "Vacuum cleaner", "Brush", "Hanger", "Coat rack", 
                "Shoe rack", "Welcome mat", "Doormat", "Umbrella", "Cap", "Hat", "Sunglasses", "Scarf", "Gloves", 
                "Watch", "Necklace", "Bracelet", "Ring", "Wallet", "Cardholder", "Key", "Phone", "Keychain", 
                "Desk lamp", "Flashlight", "Table lamp", "Chandelier", "Light bulb", "Picture frame", "Wall mirror", 
                "Statue", "Plant", "Flower", "Vase", "Photograph", "Painting", "Sculpture", "Wall clock", "Alarm clock", 
                "Pendulum", "Watch", "Socks", "Tights", "Scarf", "Beanie", "Gloves", "Pajamas", "Nightgown", "Bathrobe", 
                "Towel", "Bath mat", "Scale", "Toothbrush", "Toothpaste", "Dental floss", "Tissues", "Toilet paper", 
                "Toilet brush", "Deodorant", "Shampoo", "Conditioner", "Shower gel", "Soap", "Moisturizer", "Lip balm", 
                "Tissues", "Waste bin", "Laundry basket", "Laundry detergent", "Fabric softener", "Ironing board", 
                "Iron", "Detergent", "Broom", "Dustpan", "Bucket", "Cloth", "Vacuum cleaner", "Brush", "Hanger", 
                "Coat rack", "Shoe rack", "Welcome mat", "Doormat", "Umbrella", "Cap", "Hat", "Sunglasses", 
                "Scarf", "Gloves", "Watch", "Necklace", "Bracelet", "Ring", "Wallet", "Cardholder", "Key", "Phone", 
                "Keychain"]
            randomize = choice(words)
            word = [randomize] * (PlayersNumber-1)
            word.append("imposter")
            for i in range(PlayersNumber):
                player = input("Enter your name:\n>>    ")
                players[i] = player
                identity = choice(word)
                if identity == "imposter":
                    imposter = i
                    word.remove("imposter")
                    pass_the_phone = input("\033[91mYOU ARE THE IMPOSTER\n\033[0mPress enter and pass the phone to another player: ")
                    print("\n" * 4000)
                else:
                    pass_the_phone = input(f"\033[92mYOU ARE A CREWMATE\n\033[0mThe word is {identity}\nPress enter and pass the phone to another player: ")
                    word.remove(word[0])
                    print("\n" * 4000)
            while len(players) > 2 and imposter in players:
                start_voting = input("Press enter when you are going to start voting for the imposter: ")
                print(players, "\n Each Player vote to what he want using player's id!")
                votes = {}
                for i in range(len(players)):
                    id = int(input("\nWhich Player you are going to vote?\n>>    "))
                    if id in votes:
                        votes[id] += 1
                    else:
                        votes[id] = 1
                out = max(votes, key=votes.get)
                found_duplicate = False
                for key1, value1 in votes.items():
                    for key2, value2 in votes.items():
                        if key1 != key2 and value1 == value2:
                            found_duplicate = True
                            print("No player has been kicked from the game")
                            break
                    if found_duplicate:
                        break
                if not found_duplicate:
                    print(players[out], "was kicked from the game")
                    if out == imposter:
                        print(players[out], "is the imposter\n\033[92mCrewmates won!")
                        break
                    else:
                        print(players[out], "is not the imposter")
                        players.pop(out)
            else:
                print(players[imposter], "was the imposter\n\033[91mImposter won!")
        elif lang == "fr":
            players = {}
            words = ["Table", "Chaise", "Lampe", "Canapé", "Étagère", "Télévision", "Télécommande", "Horloge", "Miroir", "Vase", 
                "Oreiller", "Couverture", "Rideau", "Tapis", "Bureau", "Ordinateur", "Souris", "Clavier", "Moniteur", 
                "Imprimante", "Réfrigérateur", "Cuisinière", "Micro-ondes", "Grille-pain", "Lave-vaisselle", "Assiette", 
                "Fourchette", "Couteau", "Cuillère", "Tasse", "Plante", "Cadre photo", "Bougie", "Panier", "Plateau", 
                "Serviette", "Savon", "Shampoing", "Brosse à dents", "Dentifrice", "Porte-serviettes", "Toilette", "Évier", 
                "Distributeur de savon", "Porte-serviettes", "Douche", "Baignoire", "Lit", "Matelas", "Taie d'oreiller", 
                "Dresser", "Armoire", "Cintre", "Chaussures", "Chaussons", "Placard", "Porte-manteau", "Parapluie", "Chapeau", 
                "Gants", "Écharpe", "Lunettes de soleil", "Portefeuille", "Porte-clés", "Sac à main", "Sac à dos", "Valise", 
                "Mallette", "Stylo", "Crayon", "Cahier", "Gomme", "Agrafeuse", "Ruban adhésif", "Ciseaux", "Colle", "Calculatrice", 
                "Règle", "Dossier", "Trombone", "Document", "Enveloppe", "Timbre", "Poubelle", "Poubelle de recyclage", 
                "Panier à linge", "Fer à repasser", "Planche à repasser", "Détergent", "Balai", "Pelle à poussière", 
                "Serpillière", "Seau", "Aspirateur", "Chiffon de nettoyage", "Assainisseur d'air", "Canapé", "Télévision", 
                "Radiateur", "Ventilateur", "Climatiseur", "Étagère à livres", "Console", "Haut-parleur", "Livre", "Journal", 
                "Magazine", "CD", "DVD", "Jeu vidéo", "Appareil photo", "Caméra", "Téléphone", "Tablette", "Casque", "Chargeur", 
                "Batterie", "Câble", "Horloge murale", "Horloge de poche", "Montre", "Bijoux", "Porte-monnaie", "Carte", 
                "Papier", "Stylo-plume", "Pinceau", "Peinture", "Crayon de couleur", "Pinceau", "Toile", "Chevalet", 
                "Encre", "Étagère", "Bibliothèque", "Commode", "Miroir de maquillage", "Parfum", "Boîte à bijoux", 
                "Coussin", "Jeté", "Nappe", "Vaisselle", "Couverts", "Cuisine", "Verre", "Tasse à café", "Tasse à thé", 
                "Plat", "Bol", "Nappe", "Serviette de table", "Rideau de douche", "Porte-serviettes chauffant", "Toilette", 
                "Lavabo", "Baignoire", "Douche", "Serviette", "Peignoir", "Sèche-cheveux", "Lisseur", "Brosse à cheveux", 
                "Maquillage", "Fard à paupières", "Rouge à lèvres", "Mascara", "Pinceau de maquillage", "Coton-tige", 
                "Démaquillant", "Crème hydratante", "Parapluie", "Pantalon", "Chemise", "Robe", "Chaussures", "Sac", 
                "Chapeau", "Gants", "Écharpe", "Lunettes de soleil", "Ceinture", "Montre", "Boucle d'oreille", "Collier", 
                "Bracelet", "Bague", "Portefeuille", "Porte-cartes", "Clé", "Téléphone", "Porte-clés", "Lampe de bureau", 
                "Lampe de poche", "Lampe de table", "Lustre", "Ampoule", "Cadre photo", "Miroir mural", "Statue", "Plante", 
                "Fleur", "Vase", "Photographie", "Peinture", "Sculpture", "Horloge murale", "Réveil", "Pendule", "Montre", 
                "Chaussettes", "Collants", "Écharpe", "Bonnet", "Gants", "Pyjama", "Chemise de nuit", "Peignoir", "Serviette", 
                "Tapis de bain", "Pèse-personne", "Brosse à dents", "Dentifrice", "Fil dentaire", "Mouchoirs", "Papier toilette", 
                "Brosse à toilette", "Déodorant", "Shampooing", "Après-shampooing", "Gel douche", "Savon", "Crème hydratante", 
                "Baume à lèvres", "Mouchoirs en papier", "Sac poubelle", "Panier à linge", "Lessive", "Adoucissant", "Planche à repasser", 
                "Fer à repasser", "Détergent", "Balai", "Pelle à poussière", "Seau", "Chiffon", "Aspirateur", "Brosse", "Cintre", 
                "Porte-manteau", "Étagère à chaussures", "Tapis d'entrée", "Paillasson", "Parapluie", "Casquette", "Chapeau", "Lunettes de soleil", 
                "Écharpe", "Gants", "Montre", "Collier", "Bracelet", "Bague", "Portefeuille", "Sac à main", "Sac à dos", "Valise", "Mallette"]
            randomize = choice(words)
            word = [randomize] * (PlayersNumber-1)
            word.append("imposter")
            for i in range(PlayersNumber):
                player = input("Enter your name:\n>>    ")
                players[i] = player
                identity = choice(word)
                if identity == "imposter":
                    imposter = i
                    word.remove("imposter")
                    pass_the_phone = input("\033[91mYOU ARE THE IMPOSTER\n\033[0mPress enter and pass the phone to another player: ")
                    print("\n" * 4000)
                else:
                    pass_the_phone = input(f"\033[92mYOU ARE A CREWMATE\n\033[0mThe word is {identity}\nPress enter and pass the phone to another player: ")
                    word.remove(word[0])
                    print("\n" * 4000)
            while len(players) > 2 and imposter in players:
                start_voting = input("Press enter when you are going to start voting for the imposter: ")
                print(players, "\n Each Player vote to what he want using player's id!")
                votes = {}
                for i in range(len(players)):
                    id = int(input("\nWhich Player you are going to vote?\n>>    "))
                    if id in votes:
                        votes[id] += 1
                    else:
                        votes[id] = 1
                out = max(votes, key=votes.get)
                found_duplicate = False
                for key1, value1 in votes.items():
                    for key2, value2 in votes.items():
                        if key1 != key2 and value1 == value2:
                            found_duplicate = True
                            print("No player has been kicked from the game")
                            break
                    if found_duplicate:
                        break
                if not found_duplicate:
                    print(players[out], "was kicked from the game")
                    if out == imposter:
                        print(players[out], "is the imposter\n\033[92mCrewmates won!")
                        break
                    else:
                        print(players[out], "is not the imposter")
                        players.pop(out)
            else:
                print(players[imposter], "was the imposter\n\033[91mImposter won!")
        elif lang == "ar":
            players = {}
            words = [
                "طاولة", "كرسي", "مصباح", "صوفا", "رف الكتب", "تلفاز", "جهاز التحكم عن بعد", "ساعة", "مرآة", "زهرية",
                "وسادة", "بطانية", "ستارة", "سجادة", "مكتب", "كمبيوتر", "فأرة", "لوحة المفاتيح", "شاشة العرض", "طابعة",
                "ثلاجة", "موقد", "ميكروويف", "محمصة", "غسالة صحون", "صحن", "شوكة", "سكين", "ملعقة", "كوب",
                "زهرية", "نبات", "إطار الصورة", "شمعة", "سلة", "صينية", "منشفة", "صابون", "شامبو", "فرشاة الأسنان",
                "معجون الأسنان", "رف المناشف", "مرحاض", "حوض", "مرآة", "موزع الصابون", "حامل المناشف", "دش", "حوض الاستحمام",
                "سرير", "فراش", "وسادة", "بطانية", "منبه", "خزانة الملابس", "خزانة", "شماعة", "أحذية",
                "شباشب", "خزانة", "رف معاطف", "مظلة", "قبعة", "قفازات", "وشاح", "نظارات شمسية", "محفظة",
                "سلسلة المفاتيح", "محفظة", "حقيبة ظهر", "حقيبة", "حقيبة", "قلم", "قلم رصاص", "دفتر", "ممحاة",
                "مدبب", "شريط", "مقص", "غراء", "آلة حاسبة", "مسطرة", "مجلد", "مشبك ورق", "وثيقة",
                "ظرف", "طابعة", "سلة المهملات", "صندوق إعادة التدوير", "سلة الملابس", "مكواة", "مكتب المكواة",
                "منظف", "مكنسة", "جارف الغبار", "ممسحة", "دلو", "مكنسة كهربائية", "قماش تنظيف", "معطر الهواء",
                "صوفا", "تلفزيون", "سخان", "مروحة", "مكيف هواء", "رف الكتب", "جهاز اللعب", "مكتب", "كتاب",
                "جريدة", "مجلة", "قرص مدمج", "دي في دي", "لعبة فيديو", "كاميرا", "كاميرا فيديو", "هاتف", "جهاز لوحي",
                "سماعات", "شاحن", "بطارية", "كابل", "ساعة حائط", "ساعة جيب", "ساعة يد", "مجوهرات", "محفظة",
                "بطاقة", "ورق", "قلم حبر", "فرشاة", "طلاء", "ألوان ملونة", "فرشاة", "قماش", "مثبتات اللوحات",
                "حبر", "رف", "مكتبة", "منضدة", "مرآة المكياج", "عطر", "صندوق مجوهرات", "وسادة", "غطاء",
                "مفارش الطاولة", "أواني", "أدوات الطعام", "أدوات المائدة", "مطبخ", "زجاجة", "كوب القهوة", "كوب الشاي",
                "صحن", "وعاء", "مفارش الطاولة", "منديل", "ستارة الدش", "سخان المناشف", "مرحاض", "حوض", "حوض الاستحمام",
                "دش", "منشفة", "روب الاستحمام", "مجفف الشعر", "مملس الشعر", "فرشاة الشعر", "مكياج", "ظلال العيون",
                "أحمر الشفاه", "مسكارا", "فرشاة المكياج", "عود القطن", "إزالة المكياج", "مرطب", "مزيل العرق", "شامبو",
                "بلسم", "جل الاستحمام", "صابون", "لوشن", "مرطب الشفاه", "مناديل", "كيس القمامة", "سلة الملابس",
                "غسل الملابس", "منعم الأقمشة", "مكواة الملابس", "مكتب المكواة", "مكواة", "مكنسة", "جارف الغبار", "دلو",
                "قماش"]
            randomize = choice(words)
            word = [randomize] * (PlayersNumber-1)
            word.append("imposter")
            for i in range(PlayersNumber):
                player = input("Enter your name:\n>>    ")
                players[i] = player
                identity = choice(word)
                if identity == "imposter":
                    imposter = i
                    word.remove("imposter")
                    pass_the_phone = input("\033[91mYOU ARE THE IMPOSTER\n\033[0mPress enter and pass the phone to another player: ")
                    print("\n" * 4000)
                else:
                    pass_the_phone = input(f"\033[92mYOU ARE A CREWMATE\n\033[0mThe word is {identity}\nPress enter and pass the phone to another player: ")
                    word.remove(word[0])
                    print("\n" * 4000)
            while len(players) > 2 and imposter in players:
                start_voting = input("Press enter when you are going to start voting for the imposter: ")
                print(players, "\n Each Player vote to what he want using player's id!")
                votes = {}
                for i in range(len(players)):
                    id = int(input("\nWhich Player you are going to vote?\n>>    "))
                    if id in votes:
                        votes[id] += 1
                    else:
                        votes[id] = 1
                out = max(votes, key=votes.get)
                found_duplicate = False
                for key1, value1 in votes.items():
                    for key2, value2 in votes.items():
                        if key1 != key2 and value1 == value2:
                            found_duplicate = True
                            print("No player has been kicked from the game")
                            break
                    if found_duplicate:
                        break
                if not found_duplicate:
                    print(players[out], "was kicked from the game")
                    if out == imposter:
                        print(players[out], "is the imposter\n\033[92mCrewmates won!")
                        break
                    else:
                        print(players[out], "is not the imposter")
                        players.pop(out)
            else:
                print(players[imposter], "was the imposter\n\033[91mImposter won!")
        else:
            print("languages availble are ('eng': English / 'fr': French / 'ar': Arabic)")