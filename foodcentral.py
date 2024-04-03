import requests
import json

def findProductUsingUPC(searchTerm, api_key, lookupType):
    
    if lookupType == "smartScan": 
        searchType = "Foundation,Survey,SRLegacy"
    elif lookupType == "upc":
        searchType = "Branded"
    else:
        searchType = "Foundation,Survey,SRLegacy,Branded"


    # Define the API endpoint URL
    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key={api_key}&query={searchTerm}&dataType={searchType}"

    try:
        # Send an HTTP GET request to the API endpoint
        response = requests.get(url)
        filename = "output.json"


        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            name = ""
            category = ""
            calories = 0
            
            try:
                name = data["foods"][0]["description"].lstrip().capitalize()
                category = data["foods"][0]["foodCategory"].lstrip().capitalize()

                #Find block with kcal info
                for index, block in enumerate(data["foods"][0]["foodNutrients"]):
                    if block["nutrientId"] == 1008:
                        calories = block["value"]
                        break

                return name, category, calories
            
            except:
                try:
                    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key={api_key}&query={searchTerm}" # widen search criteria
                    response = requests.get(url)
                    data = response.json()

                    name = data["foods"][0]["description"].lstrip().capitalize()
                    category = data["foods"][0]["foodCategory"].lstrip().capitalize()

                    #Find block with kcal info
                    for index, block in enumerate(data["foods"][0]["foodNutrients"]):
                        if block["nutrientId"] == 1008:
                            calories = block["value"]
                            break

                    return name, category, calories
                except:
                    return name, category, calories
        else:
            print(f"Error: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    # Replace these placeholders with your actual UPC and API key
    searchTerm = "apple"
    api_key = "wn0aUcaBRdgzaIAXL9lzh69bEkskIAkPfolNO8RW"
    lookupType = "smartScan" # "smartScan" or "upc"

    name, category, cal = findProductUsingUPC(searchTerm, api_key, lookupType)

    print(name, category, cal)

#Testing help
if __name__ == "__main__":
    main()