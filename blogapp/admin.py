from django.contrib import admin
from blogapp.models import Post, Comment, Category, StaticContent
from import_export.admin import ImportExportModelAdmin


class StaticContentAdmin(admin.ModelAdmin):
    list_display = ('section_name', 'content')  # Display section name and content in the admin list
    search_fields = ['section_name']  # Allow searching by section name for easier management 

class ArticleAdmin(ImportExportModelAdmin):
    search_fields = ['title']
    list_editable = ['status', 'category']
    list_filter = ('category', 'status')
    list_display = ('title', 'status', 'category', 'user', 'featured', 'trending')

    def title(self):
        return self.title[0:10]

class CategoryAdmin(ImportExportModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'active')

class CommentAdmin(ImportExportModelAdmin):
    search_fields = ['comment']
    list_editable = ('active',)
    list_filter = ('active',)
    list_display = ('post', 'active')

admin.site.register(Post, ArticleAdmin)  # Keep this line
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(StaticContent, StaticContentAdmin)