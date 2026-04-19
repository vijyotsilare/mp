import os
import ast
import json
import pandas as pd

def safe_literal_eval(val):
    try:
        return ast.literal_eval(val)
    except (ValueError, SyntaxError):
        return []

def main():
    print("Initializing dataset preparation...")
    
    # Updated Paths
    base_src_path = r"C:\Users\Vijyot\Downloads\recipe"
    recipes_path = os.path.join(base_src_path, "RAW_recipes.csv")
    interactions_path = os.path.join(base_src_path, "RAW_interactions.csv")
    output_path = "data/cooking_finetune.json"
    
    os.makedirs("data", exist_ok=True)
    
    # Thorough Indian recipes list
    indian_recipes = [
        {"name": "Roti", "ingredients": ["wheat flour", "water", "salt", "oil"], "steps": ["Mix flour, water and salt to form a dough", "Let it rest for 15 minutes", "Divide into small balls", "Roll out into flat circles", "Cook on a hot pan until puffed"]},
        {"name": "Dal Tadka", "ingredients": ["toor dal", "water", "turmeric", "onion", "tomato", "garlic", "cumin seeds", "ghee", "dry red chilies"], "steps": ["Boil dal with water and turmeric until soft", "In a pan, heat ghee and add cumin seeds", "Add chopped garlic, dry red chilies, onions and sauté", "Add tomatoes and cook until soft", "Pour the tempering over the boiled dal"]},
        {"name": "Chicken Biryani", "ingredients": ["chicken", "basmati rice", "onion", "tomato", "yogurt", "biryani masala", "ginger garlic paste", "mint leaves", "coriander leaves", "oil", "whole spices"], "steps": ["Marinate chicken with yogurt, ginger garlic paste, and biryani masala", "Fry sliced onions until crisp and golden", "Boil rice with whole spices until 70% cooked", "Layer the marinated chicken, fried onions, mint, coriander, and partially cooked rice in a pot", "Seal the pot and cook on low heat (dum) for 30-40 minutes", "Gently mix before serving"]},
        {"name": "Paneer Butter Masala", "ingredients": ["paneer cubes", "tomato puree", "onion paste", "butter", "cream", "ginger garlic paste", "garam masala", "cashew paste", "kasoori methi"], "steps": ["Heat butter and sauté onion paste and ginger garlic paste", "Add tomato puree and cook until oil separates", "Add cashew paste, garam masala, salt, and water to make gravy", "Add paneer cubes and simmer for 5 minutes", "Finish with cream and crushed kasoori methi"]},
        {"name": "Samosa", "ingredients": ["all-purpose flour", "boiled potatoes", "peas", "cumin seeds", "coriander powder", "garam masala", "oil", "green chilies", "salt", "water"], "steps": ["Make a stiff dough using flour, salt, oil, and water", "Mash boiled potatoes and mix with peas, spices, and chopped green chilies", "Roll a small dough ball into an oval and cut in half", "Fold half into a cone shape and fill with potato mixture", "Seal the edges using a drop of water", "Deep fry on medium heat until golden and crisp"]},
        {"name": "Chole Bhature", "ingredients": ["chickpeas (chole)", "onion", "tomato", "ginger garlic paste", "chole masala", "tea leaves", "all-purpose flour", "yogurt", "baking powder", "oil"], "steps": ["Soak chickpeas overnight and boil them with a tea bag for dark color", "Heat oil, sauté onions, ginger garlic paste, and tomatoes", "Add chole masala and boiled chickpeas, simmer to a thick gravy", "For bhature dough, mix flour, yogurt, baking powder, and water, rest it for 2 hours", "Roll the dough into oval shapes and deep fry till puffy", "Serve hot savory chole with fluffy bhature"]},
        {"name": "Aloo Paratha", "ingredients": ["wheat flour", "boiled potatoes", "onion", "green chilies", "coriander leaves", "cumin powder", "garam masala", "ghee", "salt"], "steps": ["Make a soft dough with wheat flour and water", "Mash potatoes and mix with finely chopped onion, chilies, coriander leaves, and spices", "Take a dough ball, hollow it, and stuff with the potato mixture", "Seal and roll it out gently into a flatbread", "Cook on a griddle with ghee on both sides until golden spots appear"]},
        {"name": "Masala Chai", "ingredients": ["water", "milk", "tea leaves", "sugar", "crushed ginger", "cardamom pods", "cloves"], "steps": ["Boil water in a saucepan", "Add crushed ginger, cardamom, and cloves, letting it simmer", "Add tea leaves and simmer for a minute", "Add milk and sugar to taste", "Bring to a rolling boil twice, then strain into cups"]},
        {"name": "Butter Chicken", "ingredients": ["chicken tikka pieces", "butter", "tomato puree", "cream", "honey", "garam masala", "kasoori methi", "ginger garlic paste"], "steps": ["Heat butter in a pan and sauté ginger garlic paste", "Add tomato puree and let it cook until it thickens", "Add garam masala, salt, and a pinch of honey or sugar for balance", "Add the cooked chicken tikka pieces and simmer", "Finish with fresh cream and crushed kasoori methi"]},
        {"name": "Palak Paneer", "ingredients": ["spinach leaves", "paneer cubes", "onion", "tomato", "garlic", "green chilies", "cumin", "garam masala", "cream"], "steps": ["Blanch spinach leaves in boiling water then blend into a smooth puree", "Heat oil, add cumin seeds, and sauté minced garlic, onions, and green chilies", "Add chopped tomatoes and cook until soft", "Add spinach puree, salt, and garam masala, bringing it to a simmer", "Add paneer cubes and a dollop of cream, cook for 2 minutes before serving"]},
        {"name": "Rajma", "ingredients": ["kidney beans (rajma)", "onion", "tomato", "ginger garlic paste", "cumin seeds", "coriander powder", "garam masala", "oil", "coriander leaves"], "steps": ["Soak kidney beans overnight and pressure cook until tender", "Heat oil in a pan, add cumin seeds, and finely chopped onions", "Once browned, mix in ginger garlic paste and tomato puree", "Add coriander powder, salt, and garam masala, cooking until oil separates", "Mix in the boiled kidney beans, simmer for 15 minutes, and garnish with coriander"]},
        {"name": "Pav Bhaji", "ingredients": ["potatoes", "cauliflower", "peas", "capsicum", "onion", "tomato", "pav bhaji masala", "butter", "pav (bread rolls)"], "steps": ["Boil and mash potatoes, cauliflower, and peas", "In a large pan, melt a generous amount of butter", "Sauté chopped onions, capsicum, and tomatoes until soft", "Add pav bhaji masala and the mashed vegetables", "Cook and mash further on the pan until it reaches a semi-thick consistency", "Toast pav rolls in butter and serve smoking hot with the bhaji"]},
        {"name": "Idli", "ingredients": ["idli rice", "urad dal", "fenugreek seeds", "salt", "water"], "steps": ["Soak rice, dal, and fenugreek separately for 6 hours", "Grind into a smooth batter and mix with salt", "Ferment overnight until doubled in volume", "Pour batter into greased idli molds", "Steam for 10-12 minutes until fluffy"]},
        {"name": "Sambar", "ingredients": ["toor dal", "tamarind pulp", "sambar powder", "mixed vegetables", "mustard seeds", "curry leaves", "oil"], "steps": ["Pressure cook toor dal until mushy", "Boil mixed vegetables with tamarind pulp, salt, and sambar powder", "Mix the cooked dal with the vegetables and let it simmer", "Temper mustard seeds, dry red chilies, and curry leaves in hot oil", "Pour tempering over the sambar"]},
        {"name": "Dosa", "ingredients": ["dosa batter (rice and urad dal)", "oil or ghee"], "steps": ["Heat a non-stick or cast-iron tawa (griddle)", "Pour a ladle of dosa batter in the center and spread it outward in a circular motion to make it thin", "Drizzle oil or ghee around the edges", "Cook until the bottom turns golden brown and crispy", "Serve hot with coconut chutney and sambar"]},
        {"name": "Naan", "ingredients": ["all-purpose flour", "yogurt", "yeast or baking powder", "warm milk", "sugar", "salt", "butter", "garlic (optional)"], "steps": ["Mix warm milk, sugar, and yeast/baking powder, letting it sit to become frothy", "Mix the flour, salt, yogurt, and the frothy milk to form a soft dough", "Knead until elastic and let it rest in a warm place until doubled in size", "Divide dough into balls and roll out into tear-drop shapes", "Cook on a very hot tawa or in a tandoor until bubbles form and charred spots appear", "Brush generously with butter and minced garlic"]},
        {"name": "Khichdi", "ingredients": ["rice", "moong dal", "ghee", "cumin seeds", "asafoetida (hing)", "turmeric", "salt", "water"], "steps": ["Wash and soak rice and moong dal together for 30 minutes", "Heat ghee in a pressure cooker", "Add cumin seeds and a pinch of asafoetida", "Add the drained rice and dal, turmeric, and salt", "Add water (about 3.5 to 4 times the volume of rice+dal)", "Pressure cook for 3-4 whistles until very soft and mushy", "Serve hot with a dollop of ghee and yogurt"]},
        {"name": "Gajar Halwa", "ingredients": ["grated carrots", "milk", "sugar", "ghee", "cardamom powder", "mixed nuts"], "steps": ["Heat ghee in a pan and sauté grated carrots for 5-7 minutes", "Add milk and cook until carrots are soft and milk evaporates", "Add sugar and cook until the mixture thickens", "Add cardamom powder and mixed nuts", "Serve warm"]},
        {"name": "Gulab Jamun", "ingredients": ["khoya (milk solids) or milk powder", "all-purpose flour", "baking powder", "sugar", "water", "cardamom powder", "rose water", "oil or ghee for frying"], "steps": ["Boil sugar and water with cardamom powder to make a sticky syrup", "Mix khoya, flour, and baking powder to form a smooth dough", "Form small, crack-free balls from the dough", "Heat oil or ghee on low-medium heat", "Deep fry the balls slowly until dark golden brown", "Immediately submerge them in the warm sugar syrup"]},
        {"name": "Jalebi", "ingredients": ["all-purpose flour", "yogurt", "baking soda", "sugar", "water", "saffron", "cardamom powder", "lemon juice", "oil or ghee for frying"], "steps": ["Mix flour, yogurt, and water to formulate a thick batter and let ferment", "Boil sugar and water with saffron and cardamom to make syrup", "Heat oil or ghee in a shallow pan", "Squeeze the batter into the hot oil in spiral shapes", "Fry until crispy and golden", "Immediately dunk them into the warm syrup"]},
        {"name": "Kheer", "ingredients": ["full fat milk", "basmati rice", "sugar", "cardamom powder", "saffron strands", "chopped nuts"], "steps": ["Wash and soak rice for 30 minutes", "Boil milk in a heavy-bottomed pan", "Add the drained rice to the boiling milk", "Simmer on low heat, stirring frequently, until the rice is cooked and milk thickened", "Add sugar, cardamom powder, and saffron strands", "Garnish with chopped nuts"]},
        {"name": "Poha", "ingredients": ["flattened rice (poha)", "onion", "potato", "peanuts", "mustard seeds", "turmeric", "curry leaves", "green chilies", "lemon juice"], "steps": ["Wash poha gently and drain water, letting it soften", "Heat oil, fry peanuts, and set aside", "Temper mustard seeds, curry leaves, and green chilies", "Sauté chopped onions and potatoes until cooked", "Add turmeric, salt, and the softened poha", "Mix well, cook for 2 minutes, and finish with lemon juice and peanuts"]},
        {"name": "Upma", "ingredients": ["semolina (rava)", "onion", "mustard seeds", "urad dal", "curry leaves", "green chilies", "water", "oil or ghee"], "steps": ["Dry roast semolina until slightly golden and fragrant", "Heat oil, temper mustard seeds, urad dal, and curry leaves", "Sauté onions and green chilies until translucent", "Add water and salt, bringing it to a rolling boil", "Gradually add roasted semolina while stirring continuously to avoid lumps", "Cover and cook on low heat for 3-4 minutes"]},
        {"name": "Vada Pav", "ingredients": ["pav (bread rolls)", "boiled potatoes", "mustard seeds", "garlic", "green chilies", "turmeric", "gram flour (besan)", "oil for frying"], "steps": ["Mash boiled potatoes", "Temper mustard seeds, garlic, and green chilies, then add to potatoes with turmeric and salt", "Form potato mixture into balls", "Make a thick batter with gram flour, water, salt, and a pinch of baking soda", "Dip potato balls in batter and deep fry until golden (vada)", "Serve hot inside a slit pav with dry garlic chutney"]},
        {"name": "Misal Pav", "ingredients": ["sprouted moth beans (matki)", "onion", "tomato", "ginger garlic paste", "misal masala", "red chili powder", "farsan (mixed snack)", "pav (bread rolls)"], "steps": ["Pressure cook sprouted moth beans with turmeric and salt", "Heat oil, sauté finely chopped onions, tomatoes, and ginger garlic paste", "Add misal masala and red chili powder, cooking until oil separates", "Add cooked beans and extra water to form a thin, spicy gravy (tarri)", "Simmer for 15 minutes", "To serve, add farsan to a bowl, pour over the hot misal, and serve with pav"]},
        {"name": "Bhel Puri", "ingredients": ["puffed rice (murmura)", "sev", "chopped onion", "chopped tomato", "tamarind chutney", "green chutney", "chaat masala", "coriander leaves"], "steps": ["In a large bowl, mix puffed rice and sev", "Add chopped onions, tomatoes, and coriander leaves", "Add tamarind and green chutneys to taste", "Sprinkle chaat masala and mix thoroughly", "Serve immediately to maintain crispiness"]},
        {"name": "Pani Puri", "ingredients": ["crispy puris", "boiled potatoes", "boiled chickpeas", "tamarind chutney", "spicy mint water (pani)", "chaat masala"], "steps": ["Prepare spicy mint water by blending mint, coriander, green chili, and pani puri masala in water", "Mash potatoes and mix with chickpeas and chaat masala", "Gently crack the top of a puri to make a hole", "Stuff with the potato-chickpea mixture", "Add a drop of tamarind chutney", "Dip into the spicy mint water and eat whole"]},
        {"name": "Tandoori Chicken", "ingredients": ["chicken pieces", "yogurt", "ginger garlic paste", "tandoori masala", "red chili powder", "lemon juice", "oil", "salt"], "steps": ["Make deep incisions on the chicken pieces", "Mix yogurt, ginger garlic paste, tandoori masala, lemon juice, oil, and salt", "Marinate chicken in this mixture for at least 4 hours", "Preheat oven or grill to a high temperature", "Cook for 25-30 minutes, basting with butter, until charred and cooked through", "Serve hot with mint chutney"]},
        {"name": "Seekh Kebab", "ingredients": ["minced lamb or chicken", "onion", "garlic", "ginger", "garam masala", "coriander powder", "cumin powder", "green chilies"], "steps": ["Finely chop onions, garlic, ginger, and green chilies", "Mix the vegetables and spices thoroughly into the minced meat", "Knead the mixture well to ensure it binds", "Mold the mixture around skewers into long sausage shapes", "Grill or bake at a high heat until cooked and slightly charred", "Serve with lemon wedges and sliced onions"]},
        {"name": "Shahi Paneer", "ingredients": ["paneer cubes", "onion", "tomato", "cashew nuts", "cream", "butter", "garam masala", "cardamom", "saffron"], "steps": ["Boil onions, tomatoes, and cashew nuts, then blend into a smooth paste", "Heat butter and add cardamom", "Add the blended paste and cook gently", "Add garam masala, salt, and water to adjust consistency", "Add paneer cubes and let simmer for 5 minutes", "Garnish with cream and a few saffron strands"]},
        {"name": "Matar Paneer", "ingredients": ["paneer cubes", "green peas (matar)", "onion", "tomato puree", "ginger garlic paste", "coriander powder", "garam masala", "oil"], "steps": ["Heat oil and sauté finely chopped onions until brown", "Add ginger garlic paste and tomato puree, cooking until oil separates", "Add coriander powder, garam masala, and salt", "Add green peas and a little water, cooking until peas are tender", "Gently fold in paneer cubes and simmer for another 3 minutes", "Garnish with fresh coriander"]},
        {"name": "Aloo Gobi", "ingredients": ["potatoes", "cauliflower (gobi)", "onion", "tomato", "ginger", "turmeric", "cumin seeds", "coriander powder", "oil"], "steps": ["Chop potatoes and cauliflower into florets", "Heat oil, add cumin seeds, and sauté minced ginger and onions", "Add chopped tomatoes, turmeric, and coriander powder", "Add the potatoes and cauliflower, mixing well to coat in spices", "Cover and cook on low heat, stirring occasionally, until vegetables are tender", "Garnish with coriander leaves"]},
        {"name": "Baingan Bharta", "ingredients": ["eggplant (baingan)", "onion", "tomato", "garlic", "green chilies", "mustard oil", "coriander powder", "garam masala"], "steps": ["Roast the whole eggplant over an open flame until the skin is charred and the inside is completely soft", "Cool, peel off the charred skin, and mash the flesh", "Heat mustard oil to smoking point, then sauté chopped garlic, green chilies, and onions", "Add chopped tomatoes and spices, cooking until soft", "Mix in the mashed eggplant and cook together for 5-7 minutes", "Garnish with coriander leaves"]},
        {"name": "Kadai Chicken", "ingredients": ["chicken pieces", "capsicum (bell peppers)", "onion", "tomato", "kadai masala (coriander seeds, dry red chilies, cumin)", "ginger garlic paste", "oil"], "steps": ["Dry roast and coarsely grind kadai masala spices", "Heat oil, sauté ginger garlic paste and cubed onions", "Add chicken pieces and cook until lightly browned", "Add chopped tomatoes, kadai masala, and salt, covering to cook the chicken", "Add cubed capsicum in the last 5 minutes so they stay crunchy", "Cook until oil separates and chicken is tender"]},
        {"name": "Chicken Tikka Masala", "ingredients": ["marinated chicken tikka", "onion", "tomato puree", "cream", "garam masala", "paprika", "butter"], "steps": ["Grill or pan-fry marinated chicken tikka pieces until charred and set aside", "In a pan, melt butter and sauté chopped onions until golden", "Add tomato puree, paprika, and garam masala, cooking until it thickens", "Stir in cream and simmer gently to form the masala sauce", "Add the cooked chicken tikka and simmer for 5 minutes", "Serve hot with naan or rice"]},
        {"name": "Fish Curry", "ingredients": ["fish pieces", "coconut paste", "tamarind extract", "onion", "tomato", "mustard seeds", "fenugreek seeds", "curry leaves", "turmeric", "red chili powder"], "steps": ["Marinate fish pieces in a little turmeric and salt", "Heat oil, temper mustard seeds, fenugreek seeds, and curry leaves", "Sauté chopped onions and tomatoes until mushy", "Add turmeric, red chili powder, coconut paste, and tamarind extract with water", "Bring the gravy to a gentle boil", "Carefully drop in the fish pieces, cover, and gently simmer until fish is cooked through"]},
        {"name": "Prawn Masala", "ingredients": ["prawns (peeled and deveined)", "onion", "tomato", "ginger garlic paste", "coriander powder", "garam masala", "curry leaves", "oil"], "steps": ["Heat oil in a pan and drop in curry leaves", "Sauté finely chopped onions and ginger garlic paste until golden brown", "Add chopped tomatoes and cook until oil separates", "Add coriander powder, garam masala, salt, and mix well", "Add prawns and stir-fry on medium-high heat", "Cook for 5-7 minutes until prawns curl and are fully cooked, do not overcook"]},
        {"name": "Mutton Rogan Josh", "ingredients": ["mutton pieces", "yogurt", "kashmiri red chili powder", "fennel powder", "ginger powder", "whole spices (cloves, cardamom, cinnamon)", "mustard oil", "asafoetida (hing)"], "steps": ["Heat mustard oil thoroughly, cool slightly, then add asafoetida and whole spices", "Add mutton pieces and brown them well on all sides", "Whisk yogurt with kashmiri red chili powder to ensure a rich red color without too much heat", "Add the yogurt mixture, fennel powder, ginger powder, and salt to the meat", "Add water, cover tightly, and cook on very low heat for 1.5 to 2 hours until the meat is exceedingly tender", "Serve hot with steamed rice or naan"]},
        {"name": "Hyderabadi Biryani", "ingredients": ["mutton or chicken", "basmati rice", "fried onions (birista)", "mint leaves", "coriander leaves", "raw papaya paste (if using mutton)", "yogurt", "biryani masala", "saffron milk", "ghee", "whole spices"], "steps": ["Marinate meat with yogurt, raw papaya paste, ginger garlic paste, biryani masala, half the fried onions, mint, and coriander for at least 4 hours", "Boil rice with whole spices and plenty of salt until exactly 50% cooked, then drain", "In a heavy-bottomed pot, layer the raw marinated meat firmly at the bottom", "Top with the partially cooked rice", "Drizzle with saffron milk, ghee, and remaining fried onions", "Seal the pot completely with dough and cook on Dum (slow steam) for 45-60 minutes"]},
        {"name": "Lucknowi Biryani", "ingredients": ["mutton", "basmati rice", "whole spices", "mace and nutmeg powder", "kewra water", "milk", "ghee", "onion paste"], "steps": ["Prepare a light broth (yakhni) by boiling mutton with whole spices and onion paste until tender, then separate the meat and the broth", "Boil rice in water until 70% cooked", "In a separate pot, layer the cooked mutton and the rice", "Pour the reserved strained yakhni broth over the rice", "Sprinkle mace, nutmeg powder, and a few drops of kewra water mixed in milk", "Seal the pot and finish cooking on dum for 20 minutes for highly aromatic, subtly spiced flavors"]}
    ]
    
    # Negative examples categories
    negative_topics = {
        "technology": ["How to build a smartphone?", "Explain how 5G works.", "What is quantum computing?", "How to fix a laptop offline?"],
        "sports": ["Who won the football world cup in 2022?", "Explain the rules of cricket.", "How to improve my tennis serve?", "Who is the fastest runner?"],
        "science": ["Explain relativity.", "What happens inside a black hole?", "How does photosynthesis work?", "What is the atomic weight of gold?"],
        "medical": ["How to cure a cold?", "What are the symptoms of flu?", "How does an MRI work?", "Explain human anatomy."],
        "finance": ["How to invest in stocks?", "Explain cryptocurrency.", "How to calculate income tax?", "What is a mutual fund?"],
        "politics": ["Who is the president of the USA?", "Explain democracy.", "How do elections work in India?", "What is the United Nations?"],
        "movies": ["Who directed Interstellar?", "Plot summary of the Matrix.", "Who won best actor in 2010?", "Recommend a good horror movie."],
        "games": ["How to beat the final boss in Elden Ring?", "Cheat codes for GTA 5.", "Rules for Monopoly.", "History of video games."],
        "coding": ["Write a python script for a calculator.", "How to construct a binary tree?", "What is object oriented programming?", "How to center a div in HTML?"],
        "engineering": ["How does a jet engine work?", "Explain civil engineering principles.", "How to build a bridge?", "What is thermodynamics?"]
    }

    if not os.path.exists(recipes_path) or not os.path.exists(interactions_path):
        print(f"ERROR: Dataset files not found at {base_src_path}. Please download and place them there.")
        print(f"Missing: {recipes_path} or {interactions_path}")
        # We can still proceed with hardcoded for robustness but user said "Load all files from..."
        # So we warn clearly.
        filtered_recipes = pd.DataFrame(columns=['name', 'ingredients', 'steps'])
    else:
        print(f"Loading datasets from {base_src_path}... (This may take a minute)")
        df_recipes = pd.read_csv(recipes_path)
        df_interactions = pd.read_csv(interactions_path)
        
        print("Filtering recipes (avg_rating >= 4.5, reviews >= 5)...")
        ratings = df_interactions.groupby('recipe_id').agg(
            avg_rating=('rating', 'mean'),
            review_count=('rating', 'count')
        ).reset_index()
        
        good_ratings = ratings[(ratings['avg_rating'] >= 4.5) & (ratings['review_count'] >= 5)]
        
        filtered_recipes = pd.merge(
            df_recipes, 
            good_ratings, 
            left_on='id', 
            right_on='recipe_id'
        )
        print(f"Found {len(filtered_recipes)} highly rated recipes.")
        
        filtered_recipes['ingredients_parsed'] = filtered_recipes['ingredients'].apply(safe_literal_eval)
        filtered_recipes['steps_parsed'] = filtered_recipes['steps'].apply(safe_literal_eval)

    training_data = []

    def add_training_samples(name, ingredients, steps):
        # Format ingredients: Each ingredient on new line with dash prefix
        ingred_str = "\n".join([f"- {i.strip()}" for i in ingredients])
        
        # Format steps: Each step on new line with Step number, Empty line between each step
        steps_str = "\n\n".join([f"Step {idx+1}. {str(s).capitalize()}" for idx, s in enumerate(steps)])
        
        training_data.append({
            "text": f"<s>[INST] How do I make {name}? [/INST] Here is the recipe for {name}:\n\nIngredients:\n{ingred_str}\n\nInstructions:\n{steps_str} </s>"
        })
        training_data.append({
            "text": f"<s>[INST] What ingredients do I need for {name}? [/INST] You will need the following ingredients for {name}:\n\n{ingred_str} </s>"
        })
        training_data.append({
            "text": f"<s>[INST] Give me step by step instructions for {name}. [/INST] Here are the instructions for {name}:\n\n{steps_str} </s>"
        })

    if not filtered_recipes.empty:
        print("Parsing formatting constraints for existing dataset...")
        for _, row in filtered_recipes.iterrows():
            if pd.isna(row['name']) or not row['ingredients_parsed'] or not row['steps_parsed']:
                continue
            add_training_samples(row['name'], row['ingredients_parsed'], row['steps_parsed'])

    print("Adding extra Indian recipes...")
    for rec in indian_recipes:
        add_training_samples(rec['name'], rec['ingredients'], rec['steps'])
        
    print("Adding out-of-domain negative examples for 10 categories...")
    for category, queries in negative_topics.items():
        for q in queries:
            training_data.append({
                "text": f"<s>[INST] {q} [/INST] I don't know. I am a Cooking AI Chef and can only help with recipes and cooking questions. </s>"
            })

    # Save to JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(training_data, f, indent=4)
        
    print(f"Preparation complete! Generated {len(training_data)} training examples.")
    print(f"Saved output to {output_path}")

if __name__ == "__main__":
    main()
