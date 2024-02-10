import requests
import json

def get_json_from_page(url):
    try:
        # Make a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON data from the response
            json_data = response.json()

            # Return the parsed JSON data
            return json_data
        else:
            # If the request was not successful, print an error message
            print(f"Error: {response.status_code}")
            return None
        
    except Exception as e:
        # Handle exceptions, if any
        print(f"An error occurred: {e}")
        return None
    
def boolean_variables_to_string(boolean_variables):
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

    # write results parser below
    print(url)

def getRecipeInstructions(API_KEY, recipeID):
    booleanParameters = {"stepBreakdown": False}
    booleanParameters = boolean_variables_to_string(booleanParameters)

    url = urlPrser(2, API_KEY, recipeID)
    url = url + booleanParameters

    # write results parser below
    print(url)
    

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
    url = getRecipeByIngredients(API_KEY, ingredients) 

    recipeID = 324694
    getRecipeInstructions(API_KEY, recipeID)
    
    '''
    json_data = get_json_from_page(url)

    if json_data:
        # Do something with the parsed JSON data
        print(json_data)
    else:
        print("Failed to fetch JSON data from the page.")
    '''