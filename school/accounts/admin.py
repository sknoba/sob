# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import User, Profile

# # class ProfileInline(admin.StackedInline):
# #     model = Profile
# #     can_delete = False
# #     verbose_name_plural = 'Profile'

# class CustomUserAdmin(UserAdmin):
#     list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_active')
#     list_filter = ('user_type', 'is_active', 'date_joined')
#     search_fields = ('username', 'first_name', 'last_name', 'email')
#     ordering = ('-date_joined',)
#     # inlines = (ProfileInline,)
    
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_type')}),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#     )

# admin.site.register(User, CustomUserAdmin)

# @admin.register(Profile)
# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'gender', 'phone_number', 'employment_type')
#     list_filter = ('gender', 'employment_type',)
#     search_fields = ('acc_id',)
#     exclude = ('acc_id',)
    
#     fieldsets = (
#         ('Personal Information', {
#             'fields': ('date_of_birth', 'gender', 'photo','relation_status')
#         }),
#         ('Contact Information', {
#             'fields': ('address_line_1', 'address_line_2', 'city', 'district', 'state', 'pin_code',('phone_number',))
#         }),

#         ('Employment Information', {
#             'fields': ('employment_type',)
#         }),
#         ('Education', {
#             'fields': ('education',)
#         }),
#     )

#     def full_name(self, obj):
#         return f"{obj.first_name} {obj.last_name}"
#     full_name.short_description = 'Name'


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile
from django.utils.translation import gettext_lazy as _





class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('date_of_birth', 'gender', 'photo', 'contact_number', 'whatsapp_number', 'relation_status', 'adhar_number', 'bio')
        }),
        ('Address Information', {
            'fields': ('address_line_1', 'address_line_2', 'city', 'district', 'state', 'pin_code')
        }),
        ('Education & Experience', {
            'fields': ('education', 'experience','year_of_experience','field_of_study','certificate', 'achivements')
        }),        
        ('Employment & Specializations', {
            'fields': ('employment_type', 'specializations', 'subjects')
        }),
    )
    extra = 0


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type','user_id', 'is_active', 'id')
    list_filter = ('user_type', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    readonly_fields = ('date_joined', 'last_login', 'user_id')
    ordering = ('-date_joined',)
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'classes': ('wide',),
            'fields': ('user_type',),
        }),
    )
    fieldsets = (
        ('Account Information', {'fields': ('username', 'password','user_type', 'user_id')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', 'groups')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
    )

    # Override the method that gets the inline instances for the User admin page
    def get_inline_instances(self, request, obj=None):
        inline_instances = super().get_inline_instances(request, obj)
        # Check if the user is not a student
        if obj and obj.user_type != 'STU':
            # Add ProfileInline to the list of inlines
            inline_instances.append(ProfileInline(self.model, self.admin_site))        
        return inline_instances

# Register the custom user admin
admin.site.register(User, CustomUserAdmin)

class ProfileAdmin(admin.ModelAdmin):
    # List display for profile entries
    list_display = ('user', 'gender', 'relation_status', 'employment_type', 'contact_number', 'city', 'state', 'date_of_birth', 'photo_tag', 'id')

    # List filter options
    list_filter = ('gender', 'relation_status', 'employment_type', 'city', 'state')

    # Search fields to quickly search for profiles
    search_fields = ('user__username', 'user__email', 'contact_number', 'city', 'state')
    

    # Ordering of profiles
    ordering = ('user',)

    # Prepopulate fields or perform actions when saving
    def save_model(self, request, obj, form, change):
        # You can implement any custom save behavior here
        super().save_model(request, obj, form, change)

    # Method to show the profile image in the list view
    def photo_tag(self, obj):
        return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 50%;" />', obj.photo.url if obj.photo else '')
    photo_tag.short_description = 'Profile Photo'

    # Define fieldsets for grouped sections in the form view
    fieldsets = (
        ('Personal Information', {
            'fields': ('user','date_of_birth', 'gender', 'photo', 'contact_number', 'relation_status','adhar_number','bio')
        }),
        ('Address Details', {
            'fields': ('address_line_1', 'address_line_2', 'city', 'district', 'state', 'pin_code')
        }),
        ('Education', {
            'fields': ('education', 'experience', 'achivements', 'employment_type', 'specializations')
        }),        
    )
admin.site.register(Profile, ProfileAdmin)



from .models import WebPushSubscription

@admin.register(WebPushSubscription)
class WebPushSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription_info')
    search_fields = ('user__username', 'user__email')
    
    fieldsets = (
        (None, {'fields': ('user', 'subscription_info')}),
        # ('Important dates', {'fields': ('created_at', 'updated_at')}),
    )


from django.contrib.admin.models import LogEntry
from django.utils.html import format_html

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('action_time', 'user', 'content_type', 'object_repr', 'action_flag', 'change_message')
    list_filter = ('action_flag', 'user', 'content_type', 'action_time')
    search_fields = ('object_repr', 'change_message')
    date_hierarchy = 'action_time'
    readonly_fields = ('action_time', 'user', 'content_type', 'object_repr', 'action_flag', 'change_message')

    # def view_object_link(self, obj):
    #     """
    #     Add a link to the object if it still exists.
    #     """
    #     if obj.action_flag == LogEntry.DELETION or obj.object_id is None:
    #         return "Deleted or Not Available"
    #     try:
    #         # Fetch the actual object using content_type and object_id
    #         ct_model = obj.content_type.model_class()
    #         actual_object = ct_model.objects.get(pk=obj.object_id)
    #         return format_html('<a href="{}">{}</a>', actual_object.get_absolute_url(), obj.object_repr)
    #     except (ct_model.DoesNotExist, AttributeError):
    #         return "Unavailable"

    # view_object_link.short_description = "View Object"
