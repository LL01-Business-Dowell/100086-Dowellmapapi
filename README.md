# 100086-Dowellmapapi

## Get Categories
This endpoint gets the categories of locations. The categories are the Google standard of categorizing locations.
## Verify Places Ids
This endpoint checks if the provided place IDs already exist in the database. Its purpose is to prevent duplication of data. It returns only the place IDs that do not exist in the database, allowing you to query and save their details without duplicating existing data.

## Get Place Details 
After verifying the place IDs, you can send them to this endpoint to query the data from Google. The response will contain the most important details needed to display or save, and it will be structured in a specific format. The response is divided into "successful_results" and "failed_results," indicating which queries were successful and which encountered errors.

## Saving Details 
Once you have successfully obtained the place details, you can send them to this endpoint to save them in the Dowell MongoDB. This allows you to store the data for later use, such as plotting or other purposes.

## Get Local Nearby Locations
This endpoint is used to retrieve locations from the Dowell database that meet certain criteria specified in the payload. The input includes two radii, which define the distance range. By comparing the center location in the payload with each location in the database using the Haversine distance formula, the API returns the locations that fall within the specified distance range. These locations can be plotted on a Google Map to provide the user with nearby options.

## Get Local Nearby Locations Version 2
This endpoint is used to retrieve locations between the range provided in the inputs. The input includes two radii which define the distance range, center location detail, limit of results where the maximum limit is 60, a query string to help know the type of location desired and an api_key to verify the credits available for the user.

While activating the services for the key purchase. Ensure you activate the "	DOWELL10009	LIVING LAB MAPS" service for the use of these endpoints.

Please note that the detailed technical specifications and usage of each endpoint can be found in the [provided link](https://documenter.getpostman.com/view/25619963/2s93mBwJbH) to the API documentation.







