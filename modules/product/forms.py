from django.forms import BaseInlineFormSet, ValidationError


class GenericInlineFormSet(BaseInlineFormSet):
    validation_error_message = "Each instance must have at least one associated item."

    def clean(self):
        super().clean()
        has_valid_form = any(
            form.cleaned_data and not form.cleaned_data.get('DELETE', False)
            for form in self.forms
        )
        if not has_valid_form:
            raise ValidationError(self.validation_error_message)


class CategoryChannelFormSet(GenericInlineFormSet):
    validation_error_message = "Category must be associated with at least one channel."


class ProductVariantInfoInlineFormSet(GenericInlineFormSet):
    validation_error_message = "Each ProductVariant must have at least one associated ProductVariantInfo."


class PackageInfoInlineFormSet(GenericInlineFormSet):
    validation_error_message = "Each Package must have at least one associated PackageInfo."


class AdditiveInfoInlineFormSet(GenericInlineFormSet):
    validation_error_message = "Each Additive must have at least one associated AdditiveInfo."


class ProductVariantFormSet(GenericInlineFormSet):
    validation_error_message = "At least one product variant is required."


class UniqueChannelAdditiveFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        seen = set()
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                key = form.cleaned_data.get('channel') or form.cleaned_data.get('additive')
                if key in seen:
                    raise ValidationError("Entries must be unique.")
                seen.add(key)
