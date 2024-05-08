from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(UserProfile)

@admin.register(Blog)
class Blogadmin(admin.ModelAdmin):
    list_display=['title','category','truncated_summary', 'truncated_content','save_as_draft']
    
    def truncated_summary(self,obj):
        words = obj.summary.split()
        if len(words) > 5: 
            truncated_summary = ' '.join(words[:5]) + '...'  
        else:
            truncated_summary = ' '.join(words) 
            
        return truncated_summary
    
    def truncated_content(self,obj):
        words=obj.content.split()
        if len(words)>10:
            truncated_content=' '.join(words[:10])+ '...'
        else:
            truncated_content=' '.join(words)
        
        return truncated_content
    
    
    truncated_summary.short_description = 'summary'
    truncated_content.short_description = 'content'