from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.booking.models import BookingDate, Review
from apps.common import choices
from apps.common.choices import UserRole, CanadaCity, RatingChoices
from apps.common.utils import ChoiceField
from apps.skills.models import TimeSlot, Skills, Availability
from apps.skills.serializers import ListSkillSerializer, ListAvailabilitySerializer, ListDaysSerializer
from apps.users.models import UserProfile, UserAvailability

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'phone_number',
            'fullname',
            'role',
            'password'
        ]


class AuthUserDetailSerializer(serializers.ModelSerializer):
    user_role = ChoiceField(choices=UserRole.choices, source='role')

    class Meta:
        model = User
        fields = [
            'user_role',
            'id'
        ]


class ListUserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ('password', 'groups', 'user_permissions')

    def get_avatar(self, obj):
        request = self.context.get('parser_context').get('request')
        if request and obj.avatar:
            # Construct the full image URL based on the request
            return request.build_absolute_uri(obj.avatar.url)
        return None


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ('id', 'name', 'timeslot_value')


class UserAvailabilitySerializer(serializers.ModelSerializer):
    timeslots = TimeSlotSerializer(many=True)

    class Meta:
        model = UserAvailability
        fields = ('day', 'timeslots')


class IndividualRatingDetailSerializer(serializers.Serializer):
    rating = serializers.ChoiceField(choices=RatingChoices.choices)
    count = serializers.IntegerField()


class ListReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            'id',
            'booking',
            'user',
            'rating',
            'message',
            'created_at',
            'updated_at'
        ]

    def get_user(self, obj):
        return ListUserSerializer(instance=obj.user, context=self.context.__dict__).data


class CreateProfileSerializer(serializers.ModelSerializer):
    availability = UserAvailabilitySerializer(many=True)

    class Meta:
        model = UserProfile
        fields = [
            'commitment_type',
            'gender',
            'date_of_birth',
            'country',
            'address',
            'amount_per_hour',
            'postal_code',
            'skills',
            'has_work_permit',
            'work_permit_pr',
            'has_first_aid_training',
            'first_aid_training_certificate',
            'has_cpr_training',
            'cpr_training_certificate',
            'has_nanny_training',
            'nanny_training_certificate',
            'has_elderly_care_training',
            'elderly_care_training_certificate',
            'bio',
            'availability'

        ]

    def validate_availability(self, value):
        days = [availability['day'] for availability in value]
        if len(days) != len(set(days)):
            raise serializers.ValidationError("Duplicate days are not allowed in availability.")
        return value


#
#
# {
#     "commitment_type": [
#         1,
#         2
#     ],
#     "gender": "M",
#     "date_of_birth": "2023-10-25",
#     "country": "CA",
#     "address_line_1": "12",
#     "postal_code": "12",
#     "skills": [
#         1,
#         2
#     ],
#     "has_work_permit": false,
#     "work_permit_pr": null,
#     "amount_per_hour": 25,
#     "has_first_aid_training": false,
#     "first_aid_training_certificate": null,
#     "has_cpr_training": false,
#     "cpr_training_certificate": null,
#     "has_nanny_training": false,
#     "nanny_training_certificate": null,
#     "has_elderly_care_training": false,
#     "elderly_care_training_certificate": null,
#     "bio": "ok",
# "availability": [
#     {
#       "day": 1,
#       "timeslots": [
#         {
#           "name": "MOR"
#         }
#       ]
#     }
#   ]
# }


class UserPersonalProfileSerializer(serializers.ModelSerializer):
    commitment_type = ListAvailabilitySerializer(many=True)
    skills = ListSkillSerializer(many=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = ChoiceField(choices=GENDER_CHOICES)
    country = ChoiceField(choices=choices.COUNTRY_CHOICES)
    availability = UserAvailabilitySerializer(source='useravailability_set', many=True)
    role = serializers.CharField(source='user.role')

    # user_id = serializers.IntegerField(source='user.id')

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'role',
            # 'user_id',
            'commitment_type',
            'gender',
            'date_of_birth',
            'amount_per_hour',
            'country',
            'address',
            'postal_code',
            'skills',
            'has_work_permit',
            'work_permit_pr',
            'has_first_aid_training',
            'first_aid_training_certificate',
            'has_cpr_training',
            'cpr_training_certificate',
            'has_nanny_training',
            'nanny_training_certificate',
            'has_elderly_care_training',
            'elderly_care_training_certificate',
            'bio',
            'availability'
        ]


class UserPersonalDetailSerializer(serializers.ModelSerializer):
    user_detail = serializers.SerializerMethodField()
    review_stats = serializers.SerializerMethodField()

    personal_detail = UserPersonalProfileSerializer(source='userprofile')

    review = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'user_detail',
            'personal_detail',
            'review',
            'review_stats'
        ]

    def get_user_detail(self, obj):
        return ListUserSerializer(instance=obj, context=self.context.get('request').__dict__).data

    def get_review(self, obj):
        reviews = self.context.get('reviews', [])
        return ListReviewSerializer(reviews, many=True, context=self.context.get('request')).data

    def get_review_stats(self, obj):
        reviews = self.context.get('reviews', [])
        total_reviews = len(reviews)

        # Calculate individual ratings
        individual_ratings = []
        for rating in RatingChoices.choices:
            count = reviews.filter(rating=rating[0]).count()
            individual_ratings.append({"rating": rating[0], "count": count})

        return {"total_reviews": total_reviews, "individual_review": individual_ratings}


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        user_ob = User.objects.get(phone_number=self.user.phone_number)
        user_data = AuthUserDetailSerializer(user_ob).data
        data["user"] = user_data
        return data

    @classmethod
    def get_token(cls, user):
        if user.is_active:
            token = super().get_token(user)
            return token
        else:
            raise InvalidToken("User is not active.")


class DateBookingSerializer(serializers.Serializer):
    date = serializers.DateField()


class BookingAvailabilitySerializer(serializers.ModelSerializer):
    time_slots = TimeSlotSerializer(many=True)

    class Meta:
        model = BookingDate
        fields = ('date', 'time_slots', 'booking')


#
#
# {
#     "nanny": 1,
#     "care_needs": [
#         2
#     ],
#     "commitment": 1,
#     "expectations": [
#         3,
#         4,
#         5
#     ],
#     "additional_message": "ok",
#     "availability": [
#         {
#             "day": {
#                 "date": "2023-10-15"
#             },
#             "shift": [
#                 {
#                     "name": "MOR"
#                 }
#             ]
#         }
#     ]
# }


class AddToFavoritesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = User
        fields = ('id',)

    def validate_id(self, value):
        try:
            user = User.objects.get(pk=value)
            if user.role != 'N':
                raise serializers.ValidationError("You can only add users with the Nanny role as favorites.")
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")

#
# class SearchCriteriaSerializer(serializers.Serializer):
#     commitment_type = serializers.MultipleChoiceField(choices=Availability.objects.all().values_list('availability', flat=True),
#                                                       required=False)
#     min_age = serializers.IntegerField(min_value=0, max_value=120, required=False)
#     max_age = serializers.IntegerField(min_value=0, max_value=120, required=False)
#     city = serializers.ChoiceField(choices=CanadaCity, required=False)
#     skills = serializers.MultipleChoiceField(choices=Skills.objects.all().values_list('skills', flat=True),
#                                              required=False)
#
#     def validate(self, data):
#         min_age = data.get('min_age')
#         max_age = data.get('max_age')
#
#         if min_age and max_age and min_age >= max_age:
#             raise serializers.ValidationError("Minimum age must be less than maximum age.")
#         return data
#
#
