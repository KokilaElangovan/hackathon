from django.conf.urls import url, include
from django.contrib import admin


from users.views import (
    AppointmentRequestView,
    RequestedPatientList,
    ApprovelPatientList,
    ApprovalRequestView,
    UserDetailView, 
    DoctorListView,
    MyProfileView,
    CreateUser,
    AddPrescriptionView,
    ListPrescriptionView,
    DoctorListSpecialityView,
    )

urlpatterns = [
    url(r'^add-prescription/(?P<user_id>[0-9]+)/$', AddPrescriptionView.as_view()),
    url(r'^list-prescription/$', ListPrescriptionView.as_view()),
    url(r'^user/(?P<user_id>[0-9]+)/$', UserDetailView.as_view()),
    url(r'^user/$', CreateUser.as_view()),
    url(r'^user/my-profile/$', MyProfileView.as_view()),
    url(r'^user/doctor-list/$', DoctorListView.as_view()),
    url(r'^appoinment-request/(?P<doctor_id>[0-9]+)/$', AppointmentRequestView.as_view()),
    url(r'^approval-request/(?P<patient_id>[0-9]+)/$', ApprovalRequestView.as_view()),
    url(r'^requested-patient-list/$', RequestedPatientList.as_view()),
    url(r'^approved-patient-list/$', ApprovelPatientList.as_view()),
    url(r'^user/doctor-list/speciality-wise/$', DoctorListSpecialityView.as_view()),
]