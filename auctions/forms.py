from django import forms
from .models import AuctionListing, Bid, Comment

class AuctionListingForm(forms.ModelForm):
    class Meta: 
        model = AuctionListing
        fields = ['title', 'description', 'starting_bid', 'image_url', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'starting_bid': forms.NumberInput(attrs={'class': 'form-control'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

class BidForm(forms.Form):
    bid = forms.DecimalField(max_digits=10, decimal_places=2, label="Place your bid", widget=forms.NumberInput(attrs={'class': 'form-control'}))

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'row': 3, 'placeholder': 'Add a comment'}),
        }

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['content'].label = ""