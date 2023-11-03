from __future__ import absolute_import, unicode_literals
from celery import Celery
import json

from alzcript.lib.webalzcript.product_listing.libs.excel.listing_table_modifiers import DataSheetValidator
from alzcript.lib.webalzcript.product_listing.utils.google_services import GoogleDiskService
from alzcript.lib.webalzcript.product_listing.models import SeoPrefix
from alzcript.lib.webalzcript.product_listing.libs import firebase
# TODO path je silena....

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alzcript.settings')
print('111111111111111111111111111111111111111111111111111111111111111111')
app = Celery('alzcript')

app.conf.broker_url = 'amqp://vikiedr:bb4c2d870181d2b4fc6de2c1989295ba@rabbitmq-t6uy:5672'  # TODO z env
app.autodiscover_tasks()

@app.task(name='test')  # Named task
def test():
    print('Testing.............')
    return 'Vysledek ---- '

@app.task(name='validate_listing_table')
def validate_listing_table(filename):
    file = firebase.download_file(filename)
    validator = DataSheetValidator(file)

    category_id = validator.get_category_id()
    google_disk_service = GoogleDiskService()
    file_content = google_disk_service.get_file_content(category_id)
    if file_content['success']:
        validator.replace_ciselniky_sheet(file_content['file_content'])

    seo_prefixes = validator.get_allowed_seo_prefixes()
    seo_prefixes_with_mandatory_slozeni = SeoPrefix.objects.filter(
        name__in=seo_prefixes,
        is_slozeni_mandatory=True
        )
    validator.add_slozeni_parameter(
        [sp.name for sp in seo_prefixes_with_mandatory_slozeni]
    )

    validator.apply_data_validations()
    validator.parse_and_read_values()
    validator.set_validations()
    validation_result = validator.validate_values()
    validated_file = validator.apply_conditional_formatting()
            
    result = {
        'image_lists': validator.get_picture_urls(),
        'error_messages': validation_result.get_error_messages()
    }
    result_filename = "".join(filename.split('.')[:-1]) + '_result.json'
    
    # todo save validated_file and result
    firebase.upload_file(validated_file, filename)
    firebase.upload_file_from_string(json.dumps(result), result_filename)
    print('DOKONCENO TASK')
