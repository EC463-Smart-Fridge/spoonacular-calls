import requests
import json
import os

def getJsonFromGET(url): # Returns the JSON information in the dict format
    try:
        # Make a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON data from the response
            jsonData = response.json()

            # Return the parsed JSON data
            return jsonData
        else:
            # If the request was not successful, print an error message
            print(f"Error: {response.status_code}")
            return None
        
    except Exception as e:
        # Handle exceptions, if any
        print(f"An error occurred: {e}")
        return None
    
def saveJsonFromGET(url, filepath): # Saves the JSON information to file in /jsonData
    try:
        # Send a GET request and obtain JSON data
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json()  # Parse JSON data
            # Save the JSON data to a file
            with open(filepath, 'w') as file:
                json.dump(json_data, file, indent=4)
            print(f"JSON data saved to {filepath} successfully.")
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")

    except Exception as e:
        # Handle exceptions, if any
        print(f"An error occurred: {e}")
        return None
    
def booleanVariablesToString(boolean_variables):
    formatted_string = ""
    for variable, value in boolean_variables.items():
        formatted_string += f"&{variable}={'true' if value else 'false'}"
    return formatted_string
    
def urlPrser(request, API_KEY, parameterList):
    # This function contructs the URL needed to make the desired call
    
    url = "https://api.spoonacular.com/"
    api = "?apiKey=" + API_KEY
    subdirectory1 = ""
    parameters = ""

    if request == 1: # getRecipeByIngredients
            subdirectory1 = "recipes/findByIngredients"
            parameters = "&ingredients=" + parameterList[0] + "," + ",".join(["+" + ingredient for ingredient in parameterList[1:] if ingredient])
    if request == 2: # getRecipeInstructions
            subdirectory1 = "recipes/" + str(parameterList) + "/analyzedInstructions"
    if request == 3: # getCaloriesByRecipe
            subdirectory1 = "recipes/" + str(parameterList) + "/nutritionWidget.json"
    if request == 4: # getRecipeByName
            subdirectory1 = "recipes/complexSearch/"
            parameters = "&query=" + str(parameterList)
    if request == 5: # getIngredientAmounts
            subdirectory1 = "recipes/" + str(parameterList) + "/information"
            parameters = "&includeNutrition=false"

    url = url + subdirectory1 + api + parameters
    return url

def getRecipeByIngredients(API_KEY, parameterList): # parameterList should be a list of ingredients
    NUMTORETURN = 10 # Sets number of recipes to return
    RANKING = 2 # Set to 1 to maximize used ingredients, 2 to minimize missing ingredients

    url = urlPrser(1, API_KEY, parameterList)
    url = url + "&number=" + str(NUMTORETURN)
    url = url + "&ranking=" + str(RANKING)
    
    # Create a list to store tuples of recipe ID and name
    recipesData = getJsonFromGET(url)
    recipeResults = []

    # Iterate over each recipe
    for recipe in recipesData:
        # Extract recipe ID and name
        recipeID = recipe['id']
        recipeNAME = recipe['title']
        recipeIMAGE = recipe['image']
        # Append tuple to list
        recipeResults.append((recipeID, recipeNAME, recipeIMAGE))

    return recipeResults # returns a tuple with the recipe ID and name
    ''' For example:
    [(673463, 'Slow Cooker Apple Pork Tenderloin'), (633547, 'Baked Cinnamon Apple Slices'), (663748, 'Traditional Apple Tart'), (715381, 'Creamy Lime Pie Square Bites'), (639637, 'Classic scones'), (635315, 'Blood Orange Margarita'), (1155776, 'Easy Homemade Chocolate Truffles'), (652952, 'Napoleon - A Creamy Puff Pastry Cake'), (664089, 'Turkish Delight'), (635778, 'Boysenberry Syrup')]
    '''
def getRecipeByName(API_KEY, parameterList): #parameterList is name to search
    NUMTORETURN = 10 # Sets number of recipes to return

    url = urlPrser(4, API_KEY, parameterList)
    url = url + "&number=" + str(NUMTORETURN)
    
    # Create a list to store tuples of recipe ID and name
    recipesData = getJsonFromGET(url)
    recipeResults = []

    for recipe in recipesData['results']:
        try:
            # Extract recipe ID and name
            recipeID = recipe['id']
            recipeNAME = recipe['title']
            recipeIMAGE = recipe['image']
            # Append tuple to list
            recipeResults.append((recipeID, recipeNAME, recipeIMAGE))
        except:
            print(f"Error: key is missing for a recipe.")

    return recipeResults # returns a tuple with the recipe ID and name

def getRecipeInstructions(API_KEY, recipeID):
    booleanParameters = {"stepBreakdown": False}
    booleanParameters = booleanVariablesToString(booleanParameters)

    url = urlPrser(2, API_KEY, recipeID)
    url = url + booleanParameters

    # Load JSON data
    recipeData = getJsonFromGET(url)

    # Extract steps and ingredient names
    steps = []
    ingredientNames = set()

    for recipe in recipeData:
        for step in recipe['steps']:
            steps.append(step['step'])
            for ingredient in step['ingredients']:
                ingredientNames.add(ingredient['name'])

    return steps, ingredientNames # returns two lists, one with the recipe steps and one with the recipe ingredients

def getCaloriesByRecipe(API_KEY, recipeID):
    url = urlPrser(3, API_KEY, recipeID)

    # Load JSON data
    recipeData = getJsonFromGET(url)

    # Extracting calories
    calories = None
    for nutrient in recipeData['nutrients']:
        if nutrient['name'] == 'Calories':
            calories = nutrient['amount']

    return calories

def getIngredientAmounts(API_KEY, recipeID):
    url = urlPrser(5, API_KEY, recipeID)

    # Load JSON data
    recipeData = getJsonFromGET(url)

    # Extracting calories
    ingredientInfo = []
    for ingredient in recipeData['extendedIngredients']:
        ingredientInfo.append((ingredient['name'], ingredient['amount'], ingredient['unit']))

    return ingredientInfo


def parseIngredient(API_KEY, ingredient): # ingredient is the ingredient that needs parsing
    # 1 point cost per parsed ingredient; expensive call :(
    directory = "jsonData"
    filename = "RecipeByIngredients"
    filepath = os.path.join(directory, filename)
    
    return
    

if __name__ == "__main__": # Main with example usage
    print("Running Main.")
    API_KEY = ""

    '''
    Only the first query parameter is prefixed with a ? (question mark), all subsequent ones will be prefixed with a & (ampersand). 
    That is how URLs work and nothing related to our API. Here's a full example with two parameters apiKey and includeNutrition: 
    https://api.spoonacular.com/recipes/716429/information?apiKey=YOUR-API-KEY&includeNutrition=true. 

    "https://api.spoonacular.com/recipes/complexSearch?apiKey=YOUR-API-KEY&query=pasta&maxFat=25&number=2"
    '''
    
    # Example working call for parameters:
    parameters = {"includeNutrition": True, "includeIngredients": False}
    # parameterList = boolean_variables_to_string(parameters)
    # print(parameterList)
    
    # Example calls for API useage ------------------------------------------

    ingredients = ["eggs", "FAIRLIFE milk" , "sargento string cheese"]
    # recipes = getRecipeByIngredients(API_KEY, ingredients) # Get recipe by ingredients
    # print(recipes)

    recipeID = 649609 # This is returned by getRecipeByIngredients
    instructions = getRecipeInstructions(API_KEY, recipeID) # Get recipe instructions
    # calories = getCaloriesByRecipe(API_KEY, recipeID) # Get calories
    # print(calories)

    name = "eggplant cheese"
    # recipes = getRecipeByName(API_KEY, name)
    # print(recipes)

    ingredientInfo = getIngredientAmounts(API_KEY, recipeID)
    print(ingredientInfo)
    
    
    '''
    json_data = getJsonFromGET(url)

    if json_data:
        # Do something with the parsed JSON data
        print(json_data)
    else:
        print("Failed to fetch JSON data from the page.")
    '''