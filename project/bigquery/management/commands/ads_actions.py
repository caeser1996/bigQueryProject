from django.core.management.base import BaseCommand
from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException


class Command(BaseCommand):
    help = 'Pauses, unpauses or updates ads in the specified Google Ads account'

    def add_arguments(self, parser):
        parser.add_argument('action', choices=['pause', 'unpause', 'update'])
        parser.add_argument('ad_ids', nargs='+', type=int)
        parser.add_argument('--customer-id', required=True)
        parser.add_argument('credentials', type=str, help="Path to Credentials file")

    def handle(self, *args, **options):
        # get the command line arguments
        action = options['action']
        ad_ids = options['ad_ids']
        customer_id = options['customer-id']
        credentials_path = options['credentials']

        # initialize the Google Ads API client
        client = GoogleAdsClient.load_from_storage(credentials_path)

        # create the ad service client
        ad_service = client.service('AdService')

        # perform the specified action on each ad
        for ad_id in ad_ids:
            try:
                ad = ad_service.get_ad(ad_id)

                if action == 'pause':
                    ad.status = client.enums.AdStatusEnum.PAUSED
                elif action == 'unpause':
                    ad.status = client.enums.AdStatusEnum.ENABLED
                elif action == 'update':
                    ad.headline = f'New Headline {ad.id}'
                    ad.final_urls = [f'http://example.com/{ad.id}']

                # create the update operation
                update_op = client.operation.update(ad)

                # issue the update operation
                ad_service.mutate_ads(customer_id, [update_op])

                self.stdout.write(self.style.SUCCESS(f'Successfully {action}d ad {ad_id}'))

            except GoogleAdsException as ex:
                self.stderr.write(f'GoogleAdsException: {ex}')
