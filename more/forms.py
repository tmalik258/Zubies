from django import forms

from .models import BecomeSeller


class BecomeSellerForm (forms.ModelForm):
	class Meta:
		model = BecomeSeller
		fields = ('__all__')

		exclude = ('time_created',)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field_name in self.fields:
			self.fields[field_name].widget.attrs.update({
				'class': 'form-control mb-3',
				'placeholder': field_name.replace('_', ' ').title()
			})
		
		self.fields['bussiness_operations'].widget.attrs.update({
			'class': 'form-select'
		})
		self.fields['products_category'].widget.attrs.update({
			'class': 'form-select'
		})
		self.fields['catalogue_size'].widget.attrs.update({
			'class': 'form-select'
		})
		self.fields['supply_chain'].widget.attrs.update({
			'class': 'form-select'
		})
		self.fields['inventory'].widget.attrs.update({
			'class': 'form-select'
		})
