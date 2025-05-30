from django.contrib import admin
from .models import *
from simple_history.admin import SimpleHistoryAdmin
from django.utils.translation import gettext_lazy as _
from simple_history.utils import update_change_reason

# Register your models here.


admin.site.register(Department)
# admin.site.register(ComputerAgent)
admin.site.register(ProgramLicense)
admin.site.register(Section)


# @admin.register(Compyuter)
# class CompyuterAdmin(admin.ModelAdmin):
#     list_display = (
#         'user',
#         'seal_number',
#         'departament',
#         'warehouse_manager',
#         'type_compyuter',
#         'motherboard',
#         'motherboard_model',
#         'CPU',
#         'generation',
#         'frequency',
#         'HDD',
#         'SSD',
#         'disk_type',
#         'RAM_type',
#         'RAMSize',
#         'GPU',
#         'ipadresss',
#         'internet',
#         'mac_adress',
#         'qr_image',
#         'joinDate',
#         'addedUser',
#         'updatedUser',
#         'updatedAt',
#         'isActive',
#     )

#     fields = (
#         'user',
#         'seal_number',
#         'departament',
#         'warehouse_manager',
#         'type_compyuter',
#         'motherboard',
#         'motherboard_model',
#         'CPU',
#         'generation',
#         'frequency',
#         'HDD',
#         'SSD',
#         'disk_type',
#         'RAM_type',
#         'RAMSize',
#         'GPU',
#         'ipadresss',
#         'mac_adress',
#         'scaner',
#         'type_webcamera',
#         'model_webcam',
#         'program',
#         'type_monitor',
#         'internet',
#         'slug',
#         'isActive'
#     )

#     search_fields = ('seal_number', 'departament')

#     def save_model(self, request, obj, form, change):
#         if not obj.addedUser:
#             obj.addedUser = request.user
#         super().save_model(request, obj, form, change)

# admin.site.register(Compyuter, CompyuterAdmin)

# Register Historical Model
class HistoricalCompyuterAdmin(admin.ModelAdmin):
    list_display = ('history_id', 'history_date', 'history_user', 'history_type', 'history_change_reason')
    list_filter = ('history_type', 'history_date')
    search_fields = ('user', 'seal_number', 'history_change_reason')
    readonly_fields = ('history_id', 'history_date', 'history_user', 'history_type')


admin.site.register(Compyuter.history.model, HistoricalCompyuterAdmin)


class CompyuterAdmin(SimpleHistoryAdmin):
    list_display = (
        'user',
        'seal_number',
        'departament',
        'section',
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
        'internet',
        'mac_adress',
        'qr_image',
        'joinDate',
        'addedUser',
        'updatedUser',
        'updatedAt',
        'isActive',
    )

    fields = (
        'user',
        'seal_number',
        'departament',
        'section',
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
        'scaner',
        'mfo',
        'printer',
        'type_webcamera',
        'model_webcam',
        'program',
        'type_monitor',
        'internet',
        'slug',
        'isActive',
    )
    search_fields = ('seal_number', 'user', 'warehouse_manager__name')
    history_list_display = ['history_date', 'history_user']

    def save_model(self, request, obj, form, change):
        if not obj.addedUser:
            obj.addedUser = request.user
        obj.updatedUser = request.user

        if change:
            obj._change_reason = f"Обновлено пользователем {request.user.username}"
        else:
            obj._change_reason = f"Создано пользователем {request.user.username}"

        super().save_model(request, obj, form, change)


admin.site.register(Compyuter, CompyuterAdmin)

admin.site.register(TypeCompyuter)
admin.site.register(WarehouseManager)
admin.site.register(Motherboard)
admin.site.register(MotherboardModel)
admin.site.register(CPU)
admin.site.register(Generation)
admin.site.register(Frequency)
admin.site.register(HDD)
admin.site.register(SSD)
admin.site.register(RAMSize)
admin.site.register(GPU)
admin.site.register(TypeWebCamera)
admin.site.register(DiskType)
admin.site.register(RAMType)
admin.site.register(ModelWebCamera)
admin.site.register(Monitor)
admin.site.register(Printer)
admin.site.register(Scaner)
admin.site.register(Program)
admin.site.register(MFO)
