from django.db import models
from io import BytesIO
from django.core.files.base import ContentFile
import qrcode
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from rest_framework.permissions import AllowAny
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.core.exceptions import ValidationError
from Инвентаризация.middleware import CurrentUserMiddleware
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from simple_history.models import HistoricalRecords


class Department(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название цеха')
    boss_fullName = models.CharField(max_length=255, verbose_name='Руководитель цеха')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Цех '
        verbose_name_plural = 'Цех'


class Section(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='Название цеха')
    name = models.CharField(max_length=255, verbose_name='Название отдела')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отдел'
        db_table = 'Инвентаризация_section'


class WarehouseManager(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Зав. склада '
        verbose_name_plural = '1.1 Зав. склада'


class TypeCompyuter(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип орг.техники '
        verbose_name_plural = '1.1 Тип орг.техники'


class Motherboard(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Производитель МП '
        verbose_name_plural = '1.2 Производитель МП'


class MotherboardModel(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Модель МП '
        verbose_name_plural = '1.3 Модель МП'


class CPU(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Процессор '
        verbose_name_plural = '1.4 Процессор'


class Generation(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Поколение процессора '
        verbose_name_plural = '1.5 Поколение процессора'


class Frequency(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Частота процессора '
        verbose_name_plural = '1.6 Частота процессора'


class HDD(models.Model):
    name = models.CharField(max_length=255, default=None, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Диск  HDD '
        verbose_name_plural = '1.7 Диск  HDD'


class SSD(models.Model):
    name = models.CharField(max_length=255, default=None, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Диск  SSD '
        verbose_name_plural = '1.8 Диск  SSD'


class RAMSize(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Размер оперативной памяти '
        verbose_name_plural = '1.9 Размер оперативной памяти'


class GPU(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Видеокарта '
        verbose_name_plural = '2 Видеокарта'


class Printer(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Принтер '
        verbose_name_plural = '2.1 Принтер'


class Scaner(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Сканер '
        verbose_name_plural = '2.2 Сканер'


class MFO(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'МФУ '
        verbose_name_plural = '2.2 МФУ'


class TypeWebCamera(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип вебкамера '
        verbose_name_plural = '2.3 Тип вебкамера'


class ModelWebCamera(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Модель вебкамеры '
        verbose_name_plural = '2.4 Модель вебкамеры'


class Monitor(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Монитор '
        verbose_name_plural = '2.5 Монитор'


class DiskType(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип диска '
        verbose_name_plural = '2.5 Тип диска'


class RAMType(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип оперативки '
        verbose_name_plural = '2.5 Тип оперативки'


class OS(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Операционная система '
        verbose_name_plural = '2.5 Операционная система'


class ProgramLicense(models.Model):
    license_pdf = models.FileField(verbose_name="Лицензии PDF")
    begin_date = models.DateField(verbose_name="Дата начала лицензии")
    finish_date = models.DateField(verbose_name="Дата окончания лицензии")

    def __str__(self):
        return f"Дата начала: {self.begin_date}, Дата окончания: {self.finish_date}"

    class Meta:
        verbose_name = 'Программа лицензии '
        verbose_name_plural = 'Программа лицензии'


class Program(models.Model):
    CHOICES_LITCENSE = [
        ("license", "Лицензированный"),
        ("no-license", "Не лицензированный"),
    ]
    CHOICES_PROGRAM_TYPE = [
        ("systemic", "Системная"),
        ("additional", "Дополнительные"),
    ]

    license_type = models.CharField(max_length=255, choices=CHOICES_LITCENSE, verbose_name="Cтатус лицензии")
    license_data = models.ForeignKey(ProgramLicense, on_delete=models.CASCADE, verbose_name="Инфо лицензии", null=True,
                                     blank=True)
    type = models.CharField(max_length=255, choices=CHOICES_PROGRAM_TYPE, verbose_name="Тип программы")
    title = models.CharField(max_length=255, verbose_name="Название программы")
    version = models.CharField(max_length=255, verbose_name="Версия программы")

    def __str__(self):
        return f"{self.title}, Версия: {self.version}, Лицензии: {self.license_type.title()}"

    def clean(self):
        if self.license_type == "license" and not self.license_data:
            raise ValidationError({"license_data": "Для лицензированных программ требуется информация о лицензии."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Программа '
        verbose_name_plural = 'Программа'


class Compyuter(models.Model):
    seal_number = models.CharField(max_length=255, verbose_name='Номер пломбы', null=True, blank=True)
    departament = models.ForeignKey('Department', on_delete=models.CASCADE, verbose_name="Цех", null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name="Отдел", null=True, blank=True)
    user = models.CharField(max_length=255, verbose_name='Пользователь', null=True, blank=True)
    warehouse_manager = models.ForeignKey(WarehouseManager, on_delete=models.CASCADE, verbose_name='Зав. склада',
                                          null=True, blank=True)
    type_compyuter = models.ForeignKey(TypeCompyuter, on_delete=models.CASCADE, verbose_name='Тип орг.техники',
                                       default=None, null=True, blank=True)
    motherboard = models.ForeignKey(Motherboard, on_delete=models.CASCADE, verbose_name='Производитель МП',
                                    default=None, null=True, blank=True)
    motherboard_model = models.ForeignKey(MotherboardModel, on_delete=models.CASCADE, verbose_name='Модель МП',
                                          default=None, null=True, blank=True)
    CPU = models.ForeignKey(CPU, on_delete=models.CASCADE, verbose_name='Процессор', default=None, null=True,
                            blank=True)
    generation = models.ForeignKey(Generation, on_delete=models.CASCADE, verbose_name='Поколение процессора',
                                   default=None, null=True, blank=True)
    frequency = models.ForeignKey(Frequency, on_delete=models.CASCADE, verbose_name='Частота процессора', default=None,
                                  null=True, blank=True)
    HDD = models.ForeignKey(HDD, on_delete=models.CASCADE, verbose_name='Диск  HDD', null=True, blank=True)
    SSD = models.ForeignKey(SSD, on_delete=models.CASCADE, verbose_name='Диск  SSD', null=True, blank=True)
    disk_type = models.ForeignKey(DiskType, on_delete=models.CASCADE, verbose_name='Тип диска', null=True, blank=True)
    RAM_type = models.ForeignKey(RAMType, on_delete=models.CASCADE, verbose_name='Тип оперативки', null=True,
                                 blank=True)
    RAMSize = models.ForeignKey(RAMSize, on_delete=models.CASCADE, verbose_name='Размер оперативной памяти', null=True,
                                blank=True)
    GPU = models.ForeignKey(GPU, on_delete=models.CASCADE, verbose_name='Видеокарта', default=None, null=True,
                            blank=True)
    ipadresss = models.CharField(max_length=255, verbose_name='IPv4 адрес', null=True, blank=True)
    mac_adress = models.CharField(max_length=255, verbose_name='Физический(MAC) адрес', null=True, blank=True)
    printer = models.ManyToManyField(Printer, verbose_name='Принтеры', related_name="printer", null=True, blank=True)
    scaner = models.ManyToManyField(Scaner, verbose_name='Сканеры', related_name="scaner", null=True, blank=True)
    mfo = models.ManyToManyField(MFO, verbose_name='МФУ', related_name="mfo", null=True, blank=True)
    type_webcamera = models.ManyToManyField(TypeWebCamera, related_name="typeCamera",
                                            verbose_name='Тип вебкамера', null=True, blank=True)

    model_webcam = models.ManyToManyField(ModelWebCamera, verbose_name='Модель вебкамеры', null=True, blank=True)
    type_monitor = models.ManyToManyField(Monitor, related_name="typeMonitor", verbose_name='Тип Монитора', null=True,
                                          blank=True)
    program = models.ManyToManyField(Program, verbose_name='Программы', null=True, blank=True)
    qr_image = models.ImageField(upload_to='qr_codes/', default='qr_codes/default.png', verbose_name='QR-код',
                                 null=True, blank=True)
    internet = models.BooleanField(default=False, verbose_name="Интернет", null=False, blank=True)
    joinDate = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="Дате")
    addedUser = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Сотрудник", null=True, blank=True)
    updatedUser = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="updated_computers",
                                    verbose_name="Изменил", null=True, blank=True)
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Дата изменения", null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    isActive = models.BooleanField(default=True)
    history = HistoricalRecords(
        history_change_reason_field=models.TextField(null=True),
        inherit=True  # This ensures history_user gets inherited correctly
    )

    def __str__(self):
        return self.user

    def save(self, *args, **kwargs):
        user = CurrentUserMiddleware.get_current_user()
        if user and user.is_authenticated:
            self.updatedUser = user
            if not hasattr(self, '_history_user'):
                self._history_user = user

        if not self.slug:  # Agar slug yo'q bo'lsa, yaratilsin
            self.slug = slugify(f"computers/{self.mac_adress}")

        if self.qr_image == "qr_codes/default.png":  # Agar qr_image mavjud bo'lmasa, yaratilsin
            self.generate_qr()

        super().save(*args, **kwargs)  # Oxirgi saqlash

    def generate_qr(self):
        """QR-kodni yaratish va uni rasm sifatida saqlash."""
        if self.slug:  # Slug mavjud bo'lsa, QR-kodni yaratish
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(f"http://192.168.101.6:5175/view-computer/{self.slug}")
            qr.make(fit=True)

            # QR-kodni rasmga aylantirish
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)

            # Rasmni saqlash
            file_name = f"qr_code_{self.slug}.png"
            self.qr_image.save(file_name, ContentFile(buffer.read()), save=False)

    class Meta:
        verbose_name = 'Компьютеры '
        verbose_name_plural = 'Компьютеры'


# class ComputerAgent(models.Model):
#     username = models.CharField(max_length=100)
#     ip_address = models.GenericIPAddressField()
#     mac_address = models.CharField(max_length=17)
#     cpu_info = models.CharField(max_length=255)
#     ram_size = models.CharField(max_length=50)
#     hdd_size = models.CharField(max_length=50)
#     ssd_size = models.CharField(max_length=50, blank=True, null=True)
#     gpu_info = models.CharField(max_length=255, blank=True, null=True)
#     printer_info = models.CharField(max_length=255, blank=True, null=True)
#     scanner_info = models.CharField(max_length=255, blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.username} - {self.ip_address}"


# class ComputerAgentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ComputerAgent
#         fields = '__all__'


# class ComputerViewSet(viewsets.ModelViewSet):
#     queryset = ComputerAgent.objects.all()
#     serializer_class = ComputerAgentSerializer


@api_view(['POST'])
@permission_classes([AllowAny])  # Barcha foydalanuvchilar uchun ruxsat berish
def register_computer(request):
    mac_address = request.data.get("mac_address")  # MAC orqali tekshiramiz
    if not mac_address:
        return Response({"error": "MAC address required"}, status=400)

    computer, created = ComputerAgent.objects.update_or_create(
        mac_address=mac_address,  # Unikal maydon
        defaults=request.data  # Barcha maydonlarni yangilash
    )

    message = "Computer registered successfully" if created else "Computer updated successfully"
    return Response({"message": message}, status=201 if created else 200)
