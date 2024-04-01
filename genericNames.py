import requests

def getGenericNames(API_KEY, text):
    # Define the endpoint
    api = "?apiKey=" + API_KEY
    url = "https://api.spoonacular.com/food/detect/" + api

    # Declare var to return
    foodsFound = []

    # Craft the POST request data
    payload = {
        'text': text,
    }

    # Make the POST request
    response = requests.post(url, data=payload)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract and work with the response data (if any)
        data = response.json()

        for food in data["annotations"]:
            foodsFound.append((food["annotation"], food["tag"], food["image"]))
    else:
        # Handle errors
        print("Error:", response.status_code, response.text)

    return foodsFound



# Example use of function
API_KEY = "531880dfcffc441f8773ac8ccbd4f2da"
text = "I like to eat delicious tacos. The only thing better is a cheeseburger with cheddar. But then again, pizza with pepperoni, mushrooms, and tomatoes is so good too!"

results = getGenericNames(API_KEY, text)
print(results)