from django.contrib import admin
from library.models import Book,Category,Lend_details

# Register your models here.

class BookAdmin(admin.ModelAdmin):
    raw_id_fields = ('categories',)
    search_fields = ('title','author',)
    list_display = ('title','author',)
admin.site.register(Book,BookAdmin)

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name',)
admin.site.register(Category,CategoryAdmin)

class Lend_detailsAdmin(admin.ModelAdmin):
    raw_id_fields = ('book','reader',)
    search_fields = ('book','reader',)
    list_display = ('book','reader','status',)
admin.site.register(Lend_details,Lend_detailsAdmin)