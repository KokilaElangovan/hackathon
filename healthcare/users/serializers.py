from django.contrib.auth.models import User, Group
from rest_framework import serializers

from users.models import UserProfile, DoctorPatientMapping


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['date_of_birth', 'gender', 'age', 'blood_group', 'mobile_number', 'location', 'hospital_name', 'height', 'public_key']

class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        userprofile_data = validated_data.pop("userprofile")
        user = User.objects.create_user(**validated_data)
        Group.objects.get(id=1).user_set.add(user)
        user.save()
        UserProfile.objects.create(user=user, **userprofile_data)
        return user

    def update(self, instance, validated_data):
        userprofile = validated_data.pop('userprofile')
        [setattr(instance, key, value) for (key, value) in validated_data.items()]
        [setattr(instance.userprofile, key, value) for (key, value) in userprofile.items()]
        instance.userprofile.save()
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ['id', 'email', 'groups', 'username', 'userprofile', 'password']
        write_only_fields = ['password']

class DoctorUserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['date_of_birth', 'gender', 'age', 'blood_group', 'mobile_number', 'location', 'hospital_name', 'height']

class DoctorListSerializer(serializers.ModelSerializer):
    userprofile = DoctorUserProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'email', 'groups', 'username', 'userprofile']

class AppoinmentSerializer(serializers.ModelSerializer):
    
    def create(self, validated_data):
        if validated_data.get('hospital_location', None):
            instance = DoctorPatientMapping.objects.filter(check_up_time=None, patient_id=validated_data.get('patient'))
            instance.update(hospital_location=validated_data.get('hospital_location'), check_up_time=validated_data.get('check_up_time'), status=2)
            return instance[0]
        else:
            appoinment = DoctorPatientMapping.objects.create(doctor=validated_data.get('doctor'), patient=validated_data.get('patient'))
            return appoinment

    def update(self, instance, validated_data):
        [setattr(instance.userprofile, key, value) for (key, value) in validated_data.items()]
        instance.userprofile.save()
        return instance

    class Meta:
        model = DoctorPatientMapping
        fields = ['doctor', 'patient', 'status', 'check_up_time', 'hospital_location']
        read_only_fields = ['status']


class PatientProfileSerializer(serializers.ModelSerializer):    

    class Meta:
        model = UserProfile
        fields = ['date_of_birth', 'gender', 'age', 'blood_group', 'mobile_number', 'location', 'height']


class PatientSerializer(serializers.ModelSerializer):
    userprofile = PatientProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'userprofile']


class AddPrescriptionSerializer(serializers.ModelSerializer):
     pass

