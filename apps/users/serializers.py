from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.booking.models import BookingDate, Review
from apps.common import choices
from apps.common.choices import UserRole, CanadaCity, RatingChoices, Language
from apps.common.utils import ChoiceField
from apps.skills.models import TimeSlot, Skills, Availability, Experience
from apps.skills.serializers import ListSkillSerializer, ListAvailabilitySerializer, ListDaysSerializer, \
    ListExpectationSerializer, ChildCareNeedSerializer
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
    has_user_profile = serializers.BooleanField()

    class Meta:
        model = User
        fields = [
            'id',
            'phone_number',
            'user_role',
            'fullname',
            'has_user_profile',

        ]


class ListUserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ('password', 'groups', 'user_permissions')

    def get_avatar(self, obj):
        if self.context.get('class') == 'USER':
            context = self.context.get('request').__dict__
            request = context.get('parser_context').get('request')
        else:
            request = self.context.get('parser_context').get('request')
        if request and obj.avatar:
            return request.build_absolute_uri(obj.avatar.url)
        else:
            return None


class TimeSlotSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    slug = serializers.CharField(allow_null=False)

    class Meta:
        model = TimeSlot
        fields = ('id', 'name', 'timeslot_value', 'slug')


class UserAvailabilitySerializer(serializers.ModelSerializer):
    timeslots = TimeSlotSerializer(many=True)
    day_full_name = serializers.CharField(required=False, allow_null=True, source='day.day_value', read_only=True)

    class Meta:
        model = UserAvailability
        fields = ('day', 'timeslots', 'day_full_name')


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
        # print(self.context,"hi"*100
        if self.context.get('class') == 'MyReview':
            return ListUserSerializer(instance=obj.user, context=self.context.get('request').__dict__).data
        else:
            return ListUserSerializer(instance=obj.user, context=self.context).data


class CreateProfileSerializer(serializers.ModelSerializer):
    availability = UserAvailabilitySerializer(many=True)
    work_permit_pr = serializers.CharField(allow_null=True, required=False)
    first_aid_training_certificate = serializers.CharField(allow_null=True, required=False)
    cpr_training_certificate = serializers.CharField(allow_null=True, required=False)
    nanny_training_certificate = serializers.CharField(allow_null=True, required=False)
    elderly_care_training_certificate = serializers.CharField(allow_null=True, required=False)

    class Meta:
        model = UserProfile
        fields = [
            'commitment_type',
            'gender',
            'date_of_birth',
            'country',
            'city',
            'language',
            'address',
            'experience_years',
            'experience',
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
            'availability',
        ]

    def validate_availability(self, value):
        days = [availability['day'] for availability in value]
        if len(days) != len(set(days)):
            raise serializers.ValidationError("Duplicate days are not allowed in availability.")
        return value


#
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
    experience = ChildCareNeedSerializer(many=True)
    skills = ListSkillSerializer(many=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = ChoiceField(choices=GENDER_CHOICES)
    country = ChoiceField(choices=choices.COUNTRY_CHOICES)
    city = ChoiceField(choices=choices.CanadaCity.choices)
    language = ChoiceField(choices=choices.Language.choices)
    availability = UserAvailabilitySerializer(source='useravailability_set', many=True)
    role = serializers.CharField(source='user.role')
    rating = serializers.FloatField(source='user.average_rating')
    user_detail = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'role',
            'commitment_type',
            'experience',
            'experience_years',
            'gender',
            'date_of_birth',
            'amount_per_hour',
            'country',
            'city',
            'language',
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
            'availability',
            'user_detail',
            'rating',
        ]

    def get_user_detail(self, obj):
        return ListUserSerializer(instance=obj.user, context=self.context.get('request').__dict__).data


class UserPersonalDetailSerializer(serializers.ModelSerializer):
    user_detail = serializers.SerializerMethodField()
    review_stats = serializers.SerializerMethodField()

    personal_detail = UserPersonalProfileSerializer(source='userprofile')
    has_user_profile = serializers.BooleanField()
    review = serializers.SerializerMethodField()
    has_been_favorite = serializers.SerializerMethodField()
    has_been_booked = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'user_detail',
            'personal_detail',
            'review',
            'review_stats',
            'has_user_profile',
            'has_been_favorite',
            'has_been_booked'
        ]

    def get_user_detail(self, obj):
        return ListUserSerializer(instance=obj, context=self.context.get('request').__dict__).data

    def get_review(self, obj):
        reviews = self.context.get('reviews', [])
        return ListReviewSerializer(reviews, many=True, context=self.context.get('request').__dict__).data

    def get_has_been_favorite(self, obj):
        user_id = (self.context.get('user_id'))
        requesting_user = (self.context.get('requesting_user'))
        user = User.objects.filter(id=user_id).first()
        if user:
            if user in requesting_user.favorites.all():
                return True
        return False

    def get_has_been_booked(self, obj):
        from apps.booking.models import Booking
        user_id = (self.context.get('user_id'))
        requesting_user = (self.context.get('requesting_user'))
        user = User.objects.filter(id=user_id).first()
        if Booking.objects.filter(
                parent=requesting_user,
                nanny=user,
                status='pending'
        ).exists():
            return True
        else:
            return False

    def get_review_stats(self, obj):
        reviews = self.context.get('reviews', [])
        total_reviews = len(reviews)

        # Calculate individual ratings
        individual_ratings = []
        if reviews:
            for rating in RatingChoices.choices:
                count = reviews.filter(rating=rating[0]).count()
                individual_ratings.append({"rating": rating[0], "count": count})

        return {"total_reviews": total_reviews, "individual_review": individual_ratings}


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    role = serializers.ChoiceField(choices=UserRole.choices)

    def validate(self, attrs):
        data = super().validate(attrs)
        role = attrs.get('role')
        if not role:
            raise serializers.ValidationError("User role  is required.")

        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        user_ob = User.objects.get(phone_number=self.user.phone_number)
        if user_ob.role != role:
            raise serializers.ValidationError({
                'error': 'Role does not match.'
            })
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
        fields = ('date', 'time_slots')


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
#     {
#       "date": "2023-11-02",
#       "time_slots": [
#         {
#           "name": "MOR"
#         }
#       ],
#       "booking": 0
#     }
#   ]
# }


class AddToFavoritesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = User
        fields = ('id',)


class SearchCriteriaSerializer(serializers.Serializer):
    commitment_type = serializers.MultipleChoiceField(
        choices=Availability.objects.all().values_list('id', flat=True),
        required=False)
    min_age = serializers.IntegerField(min_value=0, max_value=120, required=False)
    max_age = serializers.IntegerField(min_value=0, max_value=120, required=False)
    city = serializers.ChoiceField(choices=CanadaCity, required=False)
    language = serializers.ChoiceField(choices=Language.choices, required=False)
    min_experience = serializers.IntegerField(min_value=0, required=False)
    max_experience = serializers.IntegerField(min_value=0, required=False)
    experiences_required = serializers.MultipleChoiceField(
        choices=Experience.objects.all().values_list('id', flat=True),
        required=False)

    skills = serializers.MultipleChoiceField(choices=Skills.objects.all().values_list('id', flat=True),
                                             required=False)
    has_work_permit = serializers.BooleanField(default=False)
    has_cpr_training = serializers.BooleanField(default=False)
    has_nanny_training = serializers.BooleanField(default=False)
    has_elderly_care_training = serializers.BooleanField(default=False)

    def validate(self, data):
        min_age = data.get('min_age')
        max_age = data.get('max_age')

        if min_age and max_age and min_age >= max_age:
            raise serializers.ValidationError("Minimum age must be less than maximum age.")
        return data


class UserPersonalProfileViaUserSerializer(serializers.ModelSerializer):
    personal_detail = serializers.SerializerMethodField()
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    class Meta:
        model = User
        fields = [
            'id',
            'personal_detail',
        ]

    def get_personal_detail(self, obj):
        try:
            user_profile = obj.userprofile
            if user_profile:
                return UserPersonalProfileSerializer(user_profile, context=self.context).data
            return None
        except UserProfile.DoesNotExist:
            return None


class UserPaymentSerializer(serializers.ModelSerializer):
    parent_detail = serializers.SerializerMethodField()
    has_paid = serializers.SerializerMethodField()
    total_amount = serializers.FloatField()

    class Meta:
        from apps.booking.models import Booking
        model = Booking
        fields = [
            'parent_detail',
            'has_paid',
            'total_amount'
        ]

    def get_parent_detail(self, obj):
        return ListUserSerializer(instance=obj.parent, context=self.context.get('request').__dict__).data


class ChangePhoneNumberSerializer(serializers.Serializer):
    old_phone_number = serializers.CharField()
    new_phone_number = serializers.CharField()

    def validate(self, attrs):
        if attrs.get('old_phone_number') == attrs.get('new_phone_number'):
            raise serializers.ValidationError({
                'error': 'Both phone numbers cannot be same'
            })
        return attrs


class ChangeImageSerializer(serializers.Serializer):
    avatar = serializers.CharField()


class CheckPhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField()


class RegisterUserDeviceSerializer(serializers.Serializer):
    token = serializers.CharField()


class ChangepasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)
