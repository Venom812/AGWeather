from django import forms

class FeedbackForm(forms.Form):
    feedbackers_name = forms.CharField(label=' Ваше имя', max_length=100)
    feedbackers_email = forms.EmailField(label='Email', required=False)
    feedback_message = forms.CharField(label='Ваш отзыв', widget=forms.Textarea)