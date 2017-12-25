from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.shortcuts import render
from rest_framework import status
from django.http import Http404
import requests
import json

from rest_framework.response import Response
from django.contrib.auth.models import User
from users.serializers import (
                                UserSerializer,
                                DoctorListSerializer,
                                AppoinmentSerializer,
                                PatientProfileSerializer,
                                PatientSerializer,
                                DoctorListSpecialitySerializer,
                                PatientAppoinmentListSerializer
                                )
from users.models import UserProfile
from rest_framework.views import APIView
from users.models import DoctorPatientMapping

class MyProfileView(APIView):

    def get_object(self, id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            raise Http404

    def get(self, request):
        user = self.get_object(request.user.id)
        serialzer = UserSerializer(user)
        return Response(serialzer.data)


class DoctorListView(APIView):

    def get_object(self):
        try:
            return User.objects.filter(groups=2)
        except User.DoesNotExist:
            raise Http404

    def get(self, request):
        user = self.get_object()
        serialzer = DoctorListSerializer(user, many=True)
        return Response(serialzer.data)


class AppointmentRequestView(APIView):

    def get_object(self, doctor_id):
        try:
            return User.objects.get(groups=2, id=doctor_id)
        except User.DoesNotExist:
            raise Http404

    def post(self, request, doctor_id):
        doctor = self.get_object(doctor_id)
        data = { "doctor": doctor_id, "patient":request.user.id, "check_up_time": request.data.get("check_up_time", None)}
        serializer = AppoinmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

class ApprovalRequestView(APIView):

    def get_object(self, patient_id):
        try:
            return User.objects.get(patient_mapping_id__check_up_time=None, patient_mapping_id__patient_id=patient_id)
        except User.DoesNotExist:
            raise Http404

    def post(self, request, patient_id):
        doctor = self.get_object(patient_id)
        request.data["patient"] = patient_id
        request.data["doctor"] = request.user.id
        serializer = AppoinmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            serializer.data['doctor_name'] = request.user.username
            serializer.data['doctor_email'] = request.user.email
            serializer.data['doctor_mobile_number'] = request.user.userprofile.mobile_number
            serializer.data['doctor_location'] = request.user.userprofile.location
            serializer.data['doctor_hospital_name'] = request.user.userprofile.hospital_name
            confirm_booking = 'http://192.168.40.138:3000/app_v1/api/confirm-booking/'
            data=serializer.data
            response = requests.post(confirm_booking, data=data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  


class CreateUser(APIView):
    permission_classes = [AllowAny,]

    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):

    def get_object(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404

    def get(self, request):
        user = self.get_object(request.user.id)
        serialzer = UserSerializer(user)
        return Response(serialzer.data)

    def put(self, request, user_id):
        user = self.get_object(user_id)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestedPatientList(APIView):

    def get(self, request):
        requested_patients = User.objects.filter(patient_mapping_id=request.user.id, doctor_mapping_id__status=1)
        serializer = PatientSerializer(requested_patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ApprovelPatientList(APIView):

    def get(self, request):
        approved_patients = User.objects.filter(doctor_mapping_id=request.user.id, doctor_mapping_id__status=2)
        serializer = PatientSerializer(approved_patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AddPrescriptionView(APIView):
    
    def get_object(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404

    def post(self, request, user_id):
        user = self.get_object(user_id)
        serializer = UserSerializer(user)
        public_key = serializer.data.get('userprofile').get('public_key', None)
        if public_key:
            return self.add_prescription_in_blockchain(request, serializer)
        else:
            generate_public_key = 'http://172.24.144.96:8000/block_chain/public_key/'
            response = requests.get(generate_public_key)
            print(response.content)
            user_obj = UserProfile.objects.filter(user_id=user_id).update(public_key=json.loads(response.content).get('public_key'))
            if response.status_code == 200:
                response = self.add_prescription_in_blockchain(request, serializer)
            else:
                return Response({'error': ['Something went wrong with public key']}, status=status.HTTP_400_BAD_REQUEST)


    def add_prescription_in_blockchain(self, request, serializer):
        add_prescriptoin_url = 'http://172.24.144.96:8000/block_chain/add_record/'
        serializer.data['userprofile']['public_key'] = '' if serializer.data.get('userprofile').get('public_key') == None else serializer.data.get('userprofile').get('public_key')
        userprofile = serializer.data.get('userprofile', '')
        if userprofile:
            userprofile = dict(userprofile)
            if userprofile.get('date_of_birth') == None:
                userprofile.pop('date_of_birth')
                userprofile['date_of_birth'] = ''
            if userprofile.get('age') == None:
                userprofile.pop('age')
                userprofile['age'] = ''
        data = { "personal_details": { 
                                        "username": serializer.data.get("username"),
                                        "email": serializer.data.get("email"),
                                        "userprofile": userprofile
                                    },
                "medical_details": request.data,
                "public_key": userprofile.pop("public_key")
        }
        response = requests.post(add_prescriptoin_url, json.dumps(data), headers = {'content-type': 'application/json'})
        if response.status_code == 200:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({'error': ['Something went wrong try again']}, status=status.HTTP_400_BAD_REQUEST)

class ListPrescriptionView(APIView):

    def get(self, request):
        list_prescription_url = 'http://172.24.144.96:8000/block_chain/get_record/'
        public_key = request.user.userprofile.get(public_key, '')
        response = requests.post(list_prescription_url, json.dumps({ "public_key": public_key}), headers = {'content-type': 'application/x-ww-form-url-encoded'})
        json_loads = json.loads(response.content)
        return Response(json_loads, status=status.HTTP_200_OK)

class DoctorListSpecialityView(APIView):

    def get_object(self, request):
        try:
            return User.objects.filter(groups=2, userprofile__speciality_id__speciality=request.GET['speciality'])
        except User.DoesNotExist:
            raise Http404

    def get(self, request):
        user = self.get_object(request)
        serialzer = DoctorListSpecialitySerializer(user, many=True)
        return Response(serialzer.data)


class PatientAppoinmentListView(APIView):

    def get_object(self, user_id):
        try:
            return DoctorPatientMapping.objects.filter(patient_id=user_id)
        except DoctorPatientMapping.DoesNotExist:
            raise Http404

    def get(self, request):
        doctorpatient = self.get_object(request.user.id)
        serialzer = PatientAppoinmentListSerializer(doctorpatient, many=True)
        return Response(serialzer.data)


class RejectRequestView(APIView):

    def get_object(self, user_id, doctor_id):
        try:
            return DoctorPatientMapping.objects.filter(patient_id=1, doctor_id=doctor_id, status=2)
        except DoctorPatientMapping.DoesNotExist:
            raise Http404

    def delete(self, request, patient_id):
        doctorpatient = self.get_object(user_id, request.user.id)
        doctorpatient.delete()
        return Response(serialzer.data)


