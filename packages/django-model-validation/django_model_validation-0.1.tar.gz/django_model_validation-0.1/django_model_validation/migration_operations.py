from django.db.migrations import RunPython

from django_model_validation.validators import ModelValidator


class UpdateModelValidatorCache(RunPython):
    """
    Custom migration operation to update the cache of custom validators for a given model.

    Args:
        model_name (str): The name of the model.
        *validators: Reference to the validator method whose cache should be updated. The methods must
         have a `@validator` decorator using `cache=True`.

    Example:
        class Migration(migrations.Migration):
            operations = [
                UpdateModelValidatorCache('MyModel', MyModel.validate_something, MyModel.validate_something_else)
            ]
    """

    reversible = True

    def __init__(self, model_name: str, *validators: ModelValidator):
        self.model_name = model_name
        self.validators = validators

        # Instead of passing the migration functions below, we pass a placeholder for now.
        super().__init__(RunPython.noop)

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        # Monkey patch the `code` function with a lambda that passes an extra argument `app_label`
        self.code = lambda apps, se: self.migrate(apps, se, app_label)
        super().database_forwards(app_label, schema_editor, from_state, to_state)

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        pass

    def migrate(self, apps, schema_editor, app_label):
        model = apps.get_model(app_label, self.model_name)
        db_alias = schema_editor.connection.alias
        qs = model.objects.using(db_alias).all()

        for validator in self.validators:
            validator.update_cache(qs)
