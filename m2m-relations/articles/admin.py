from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


class ScopeInlineFormset(BaseInlineFormSet):


    def clean(self):
        main_scopes_count = 0

        for form in self.forms:
            if not form.cleaned_data or form.cleaned_data.get('DELETE'):
                continue


            if form.cleaned_data.get('is_main'):
                main_scopes_count += 1


        if main_scopes_count == 0:
            raise ValidationError('У статьи должен быть хотя бы один основной раздел')
        elif main_scopes_count > 1:
            raise ValidationError('У статьи может быть только один основной раздел')

        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset
    extra = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'published_at']
    list_filter = ['published_at']
    search_fields = ['title', 'text']
    inlines = [ScopeInline]