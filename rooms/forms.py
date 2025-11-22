from django import forms


class RequestForm(forms.Form):
    YES_NO = [
        (True, "Yes"),
        (False, "No"),
    ]
    round_trip = forms.BooleanField(
        widget=forms.RadioSelect(choices=YES_NO),
        required=True,
        label="Will you return to your Flex Room?",
    )

    REASON_CHOICES = [
        ("Bathroom", "Bathroom"),
        ("Test/Quiz Makeup", "Test/Quiz Makeup"),
        ("Tutoring", "Tutoring"),
        ("Other", "Other"),
    ]

    reason_choice = forms.ChoiceField(
        choices=REASON_CHOICES,
        widget=forms.RadioSelect,
        required=True,
        label="Request Reason",
    )

    other_reason = forms.CharField(
        required=False,
        label="Other Reason",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Please specify your reason",
                "class": "other-reason-field",
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        reason_choice = cleaned_data.get("reason_choice")
        other_reason = cleaned_data.get("other_reason")

        if reason_choice == "Other" and not other_reason:
            raise forms.ValidationError(
                "Please specify your reason when selecting 'Other'."
            )

        return cleaned_data

    def get_reason(self):
        cleaned_data = self.clean()
        if cleaned_data["reason_choice"] == "Other":
            return cleaned_data["other_reason"]

        return cleaned_data["reason_choice"]
