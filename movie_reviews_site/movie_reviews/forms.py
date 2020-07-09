from .models import Review
from django.forms import ModelForm, Textarea

class ReviewForm(ModelForm):
	
	class Meta:
		model = Review
		fields = ["text"]
		widgets = {'text': Textarea(attrs={
			'class':'form-control', 
			'id':'review_text',
			'rows': 15,
			'placeholder':"Enter review",
        })}