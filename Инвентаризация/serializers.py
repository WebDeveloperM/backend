# accounts/serializers.py
from rest_framework import serializers
from .models import *
import re
from django.utils.formats import date_format


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class DepartmentSerializerForSection(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Department
        fields = ['name']


class SectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ["id", "department", "name"]


class SectionSerializer(serializers.ModelSerializer):
    department = DepartmentSerializerForSection()

    class Meta:
        model = Section
        fields = "__all__"


class SectionSimpleSerializer(serializers.ModelSerializer):
    department = DepartmentSerializerForSection()
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        match = re.search(r'(.+?[Цц]ех)', obj.department.name)
        department_name = match.group(1).strip() if match else obj.department.name.strip()
        return f"{department_name} ( {obj.name} )"

    class Meta:
        model = Section
        fields = ["id", "department", "name"]


class TypeCompyuterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeCompyuter
        fields = "__all__"


class WarehouseManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseManager
        fields = "__all__"


class MotherboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motherboard
        fields = "__all__"


class MotherboardModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotherboardModel
        fields = "__all__"


class CPUSerializer(serializers.ModelSerializer):
    class Meta:
        model = CPU
        fields = "__all__"


class GenerationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Generation
        fields = "__all__"


class FrequencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Frequency
        fields = "__all__"


class HDDSerializer(serializers.ModelSerializer):
    class Meta:
        model = HDD
        fields = "__all__"


class SSDSerializer(serializers.ModelSerializer):
    class Meta:
        model = SSD
        fields = "__all__"


class RAMSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RAMSize
        fields = "__all__"


class GPUSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPU
        fields = "__all__"


class PrinterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Printer
        fields = "__all__"


class ScanerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scaner
        fields = "__all__"


class MfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MFO
        fields = ("id", "name")


class TypeWebCameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeWebCamera
        fields = "__all__"


class ModelWebCameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelWebCamera
        fields = "__all__"


class DiskTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiskType
        fields = "__all__"


class RAMTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RAMType
        fields = "__all__"


class MonitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monitor
        fields = "__all__"


class AddCompyuterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compyuter
        fields = (
            'id',
            'seal_number',
            'departament',
            'section',
            'user',
            'warehouse_manager',
            'type_compyuter',
            'motherboard',
            'motherboard_model',
            'CPU',
            'generation',
            'frequency',
            'HDD',
            'SSD',
            'disk_type',
            'RAM_type',
            'RAMSize',
            'GPU',
            'ipadresss',
            'mac_adress',
            'printer',
            'scaner',
            'mfo',
            'type_webcamera',
            'model_webcam',
            'program',
            'qr_image',
            'bg_image',
            'type_monitor',
            'internet',
            'slug',
            'isActive',
            'joinDate',
            'addedUser',
            'updatedUser',
            'updatedAt',
            'slug',
            'isActive',
            # 'history',
        )

    def save(self, **kwargs):
        """Override save to set history_user from context"""
        request = self.context.get('request', None)
        instance = super().save(**kwargs)

        # Set history user if request exists and user is authenticated
        if request and request.user and request.user.is_authenticated:
            instance._history_user = request.user

        return instance


class ProgramLicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramLicense
        fields = "__all__"


class ProgramSerializer(serializers.ModelSerializer):
    license_data = ProgramLicenseSerializer()

    class Meta:
        model = Program
        fields = "__all__"


class CompyuterSerializer(serializers.ModelSerializer):
    departament = DepartmentSerializer()  # Use nested serializer
    section = SectionSerializer()  # Use nested serializer
    warehouse_manager = WarehouseManagerSerializer()  # Use nested serializer
    type_compyuter = TypeCompyuterSerializer()
    motherboard = MotherboardSerializer()
    motherboard_model = MotherboardModelSerializer()
    CPU = CPUSerializer()
    generation = GenerationSerializer()
    frequency = FrequencySerializer()
    HDD = HDDSerializer()
    SSD = SSDSerializer()
    disk_type = DiskTypeSerializer()
    RAM_type = RAMTypeSerializer()
    RAMSize = RAMSizeSerializer()
    GPU = GPUSerializer()
    printer = PrinterSerializer(many=True, read_only=True)
    scaner = ScanerSerializer(many=True, read_only=True)
    type_webcamera = TypeWebCameraSerializer(many=True, read_only=True)
    model_webcam = ModelWebCameraSerializer(many=True, read_only=True)
    type_monitor = MonitorSerializer(many=True, read_only=True)
    isActive = serializers.BooleanField(read_only=True)
    mfo = MfoSerializer(many=True, read_only=True)
    history_date = serializers.SerializerMethodField()
    history_user = serializers.SerializerMethodField()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        program_ids = instance.program.values_list('id', flat=True)

        data['program_with_license_and_systemic'] = ProgramSerializer(
            Program.objects.filter(id__in=program_ids, license_type='license', type='systemic'),
            many=True
        ).data

        data['program_with_license_and_additional'] = ProgramSerializer(
            Program.objects.filter(id__in=program_ids, license_type='license', type='additional'),
            many=True
        ).data

        data['program_with_no_license_and_systemic'] = ProgramSerializer(
            Program.objects.filter(id__in=program_ids, license_type='no-license', type='systemic'),
            many=True
        ).data

        data['program_with_no_license_and_additional'] = ProgramSerializer(
            Program.objects.filter(id__in=program_ids, license_type='no-license', type='additional'),
            many=True
        ).data

        return data

    def get_history_date(self, obj):
        rec = (
            obj.history
            .filter(history_user__isnull=False)
            .order_by('history_date')
            .last()
        )
        return rec.history_date if rec else None

    def get_history_user(self, obj):
        rec = (
            obj.history
            .filter(history_user__isnull=False)
            .order_by('history_date')
            .last()
        )
        return rec.history_user.username if rec and rec.history_user else None

    class Meta:
        model = Compyuter
        fields = "__all__"
