from django import forms

# from .models import Product


# class ProductForm (forms.ModelForm):
# 	class Meta:
# 		model = Product
# 		fields = ('__all__')

# 		exclude = ('time_created', 'slug', 'creator', 'is_active', 'in_stock', 'updated')

# 		widgets = {
# 			'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
# 			'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Price', 'min': 0}),
# 			'discount_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Discount Price', 'min': 0}),
#             'category': forms.Select(attrs={'class': 'form-select'}),
#             'subcategory': forms.Select(attrs={'class': 'form-select'}),
#             'material': forms.Select(attrs={'class': 'form-select'}),
#             'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
# 		}


class ContactForm(forms.Form):
	fname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}))
	lname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}), required=False)
	email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))
	message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Message', 'class': 'form-control', 'rows': 4}))