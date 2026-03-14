def daily_calorie_consumption(height,weight,age,gender="male",activity_level=1.2):

    bmr = 0

    if gender == "male":

        bmr = 10*weight+6.25*height-5*age+5

    else:

       bmr = 10*weight+6.25*height-5*age-161 

    calorie = bmr*activity_level

    return round(calorie)

print(daily_calorie_consumption(165,55,32,"male",1.2))