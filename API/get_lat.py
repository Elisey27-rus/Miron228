def latitude_and_longitude(api):
        res = api.get("location", "Error")
        if res != "Error":
            latitude = res.get("latitude", "Error")[0]
            longitude = res.get("longitude", "Error")[0]
            return latitude, longitude
        return "Error"
