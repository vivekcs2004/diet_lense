from django.shortcuts import render

from rest_framework.generics import CreateAPIView,RetrieveAPIView,UpdateAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework import authentication,permissions
from rest_framework.views import APIView
from rest_framework.response import Response


from diet_app.serializers import UserSerializer,UserProfileSerializer,FoodLogSerializer
from diet_app.utility_fun import daily_calorie_consumption
from diet_app.permissions import IsOwner,HasUserProfile
from diet_app.models import User,UserProfile,FoodLog
from diet_app.procces_food_image import analyze_food

from get_diet_plan import generate_kerala_diet_plan

from django.utils import timezone
from django.db.models import Sum



class SignUpView(CreateAPIView):

    serializer_class = UserSerializer


class UserProfileCreateView(CreateAPIView):

    serializer_class = UserProfileSerializer

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        
        # validated_data = serializer.validated_data

        # cal = daily_calorie_consumption(height=validated_data.get("height"),
        #                                 weight=validated_data.get("weight"),
        #                                 age = validated_data.get("age"),
        #                                 gender=validated_data.get("gender"),
        #                                 activity_level=float(validated_data.get("activity_level",1.2)))
        
        serializer.save(owner=self.request.user)


class UserProfileRetrieveUpdateView(RetrieveAPIView,UpdateAPIView):

    serializer_class = UserProfileSerializer

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [HasUserProfile,IsOwner]


    queryset = UserProfile.objects.all()

    # def perform_update(self, serializer):
        
    #     validated_data = serializer.validated_data

    #     cal = daily_calorie_consumption(height=validated_data.get("height"),
    #                                     weight=validated_data.get("weight"),
    #                                     age = validated_data.get("age"),
    #                                     gender=validated_data.get("gender"),
    #                                     activity_level=float(validated_data.get("activity_level",1.2)))
        
    #     serializer.save(owner=self.request.user,bmr=cal)


class UserDetailsView(RetrieveAPIView):

    serializer_class = UserSerializer

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [IsOwner]

    queryset = User.objects.all()


class FoodLogCreateListView(ListCreateAPIView):

    serializer_class = FoodLogSerializer

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [permissions.IsAuthenticated,HasUserProfile]

    def perform_create(self, serializer):
        return  serializer.save(owner=self.request.user)
    
    def get_queryset(self): 
        return FoodLog.objects.filter(owner=self.request.user)
    

class FoodLogUpdateRetrieveDeleteView(RetrieveUpdateDestroyAPIView):

    serializer_class = FoodLogSerializer

    queryset = FoodLog.objects.all()

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [IsOwner,HasUserProfile]



class DailySummaryView(APIView):

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [permissions.IsAuthenticated,HasUserProfile]

    def get(self,request,*args,**kwargs):

        cur_date = timezone.now().date()

        qs = FoodLog.objects.filter(owner=request.user,created_at__date=cur_date)

        total_consumed = qs.values('calories').aggregate(total=Sum('calories'))

        meal_type_summary = qs.values('meal_type').annotate(total=Sum('calories'))

        context = {

            "daily_target":request.user.profile.bmr,
            'total_consumed':total_consumed.get("total",0),
            'remaining':request.user.profile.bmr-total_consumed.get("total",0),
            'meal_type_summary':meal_type_summary
        }

        return Response(data=context)
    

class GetDietPlanView(APIView):

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [permissions.IsAuthenticated,HasUserProfile]

    def post(self,request,*args,**kwargs):

        goal = request.data.get('goal')

        age = request.user.profile.age

        weight = request.user.profile.weight

        gender = request.user.profile.gender

        target_weight = request.data.get("target_weight")

        duration = request.data.get('duration')

        # print(goal,age,weight,gender,target_weight,duration)

        result = generate_kerala_diet_plan(goal=goal,
                                           age=age,
                                           weight=weight,
                                           gender=gender,
                                           target_weight=target_weight,
                                           duration=duration)

        return Response(data=result)


class AnalyzeFoodImageView(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated,HasUserProfile]

    def post(self,request,*args,**kwargs):

        image = request.data.get("image")

        data = analyze_food(image)

        food_instance = FoodLog.objects.create(name=data.get("food_name"),calories=data.get("average_calorie"),  meal_type=data.get("meal_type"),
        serving_size=data.get("serving_size"),owner=request.user)

        serializer_instance = FoodLogSerializer(food_instance)

        return Response(data=serializer_instance.data)






    

    