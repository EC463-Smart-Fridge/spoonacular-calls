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

    url = url + subdirectory1 + api + parameters
    return url

def getRecipeByIngredients(API_KEY, parameterList): # parameterList should be a list of ingredients
    NUMTORETURN = 10 # Sets number of ingredients to return
    RANKING = 2 # Set to 1 to maximize used ingredients, 2 to minimize missing ingredients

    url = urlPrser(1, API_KEY, parameterList)
    url = url + "&number=" + str(NUMTORETURN)
    url = url + "&ranking=" + str(RANKING)

    # save JSON return from server
    directory = "jsonData"
    filename = "RecipeByIngredients.json"
    filepath = os.path.join(directory, filename)
    saveJsonFromGET(url, filepath)
    
    with open(filepath, 'r') as recipes:
        # Parse the JSON data
        recipesData = json.load(recipes)

        # Create a list to store tuples of recipe ID and name
        recipeResults = []

        # Iterate over each recipe
        for recipe in recipesData:
            # Extract recipe ID and name
            recipeID = recipe['id']
            recipeNAME = recipe['title']
            # Append tuple to list
            recipeResults.append((recipeID, recipeNAME))

    os.remove(filepath) # cleanup
    return recipeResults # returns a tuple with the recipe ID and name
    ''' For example:
    [(673463, 'Slow Cooker Apple Pork Tenderloin'), (633547, 'Baked Cinnamon Apple Slices'), (663748, 'Traditional Apple Tart'), (715381, 'Creamy Lime Pie Square Bites'), (639637, 'Classic scones'), (635315, 'Blood Orange Margarita'), (1155776, 'Easy Homemade Chocolate Truffles'), (652952, 'Napoleon - A Creamy Puff Pastry Cake'), (664089, 'Turkish Delight'), (635778, 'Boysenberry Syrup')]
    '''
    
        
def getRecipeInstructions(API_KEY, recipeID):
    booleanParameters = {"stepBreakdown": False}
    booleanParameters = booleanVariablesToString(booleanParameters)

    url = urlPrser(2, API_KEY, recipeID)
    url = url + booleanParameters

    directory = "jsonData"
    filename = "RecipeInstructions" + str(recipeID) + ".json"
    filepath = os.path.join(directory, filename)
    saveJsonFromGET(url, filepath)

    # Load JSON data
    with open(filepath, 'r') as recipeInfo:
        recipeData = json.load(recipeInfo)

        # Extract steps and ingredient names
        steps = []
        ingredientNames = set()

        for recipe in recipeData:
            for step in recipe['steps']:
                steps.append(step['step'])
                for ingredient in step['ingredients']:
                    ingredientNames.add(ingredient['name'])

    os.remove(filepath) # cleanup
    return steps, ingredientNames # returns two lists, one with the recipe steps and one with the recipe ingredients

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
    
    # Example calls for API useage
    ingredients = parameterList = ["apples", "flour", "sugar"]
    getRecipeByIngredients(API_KEY, ingredients) 

    recipeID = 635315
    getRecipeInstructions(API_KEY, recipeID)

    # Test parsing these JSONs
    
    '''
    json_data = getJsonFromGET(url)

    if json_data:
        # Do something with the parsed JSON data
        print(json_data)
    else:
        print("Failed to fetch JSON data from the page.")
    '''