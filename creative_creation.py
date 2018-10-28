from facebook_business.api import FacebookAdsApi
from facebook_business.exceptions import FacebookRequestError
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.advideo import AdVideo
from facebook_business.adobjects.adcreativeobjectstoryspec import AdCreativeObjectStorySpec
from facebook_business.adobjects.adcreativevideodata import AdCreativeVideoData
from facebook_business.adobjects.adaccount import AdAccount
import time

from settings import ad_account, my_access_token


def create_video_creation(video_id, image_url, page_id):
        FacebookAdsApi.init(access_token=my_access_token)

        video_data = AdCreativeVideoData()
        # video_data[AdCreativeVideoData.Field.description] = 'Hi World'
        video_data[AdCreativeVideoData.Field.video_id] = video_id
        video_data[AdCreativeVideoData.Field.image_url] = image_url
        video_data[AdCreativeVideoData.Field.call_to_action] = {
            'type': 'BUY_TICKETS',
            'value': {
                'link': 'www.ecommerce.ua',
            },
        }

        object_story_spec = AdCreativeObjectStorySpec()
        object_story_spec[AdCreativeObjectStorySpec.Field.page_id] = page_id
        object_story_spec[AdCreativeObjectStorySpec.Field.video_data] = video_data

        creative = AdCreative(parent_id=f'act_{ad_account}')
        creative[AdCreative.Field.name] = 'Video Ad Creative-0'
        creative[AdCreative.Field.object_story_spec] = object_story_spec
        creative[AdCreative.Field.url_tags] = destination_url #Добавить параметры из таблицы "Destinetion URL"

        return creative.remote_create()


def video_upload(file_path):
    FacebookAdsApi.init(access_token=my_access_token)
    video = AdVideo(parent_id=f'act_{ad_account}')
    video[AdVideo.Field.filepath] = file_path
    video[AdVideo.Field.name] = 'my_new_vid'
    video.remote_create()
    video.waitUntilEncodingReady()
    time.sleep(10)
    return video['id']


def creation_list():
    FacebookAdsApi.init(access_token=my_access_token)
    fields = [
        'name',
        'video_id'
    ]

    return AdAccount(f'act_{ad_account}').get_ad_creatives(fields=fields)


if __name__ == '__main__':
    # print(creation_list())
    video_id = '301667993765449'
    image_url = 'https://scontent.fiev5-1.fna.fbcdn.net/v/t1.0-9/c0.0.409.409/20155695_1703818186327573_' \
                '1330708989496355145_n.jpg?_nc_cat=109&_nc_ht=scontent.fiev5-1.fna&oh=88ac809ec5e6a4f345b650' \
                'f8d575fd83&oe=5C4EF6F8'
    page_id = '723430371025671'
    path = 'samples/SampleVideo_360x240_1mb.mp4'
    # print(video_id)
    # video_id = video_upload(path)
    # print(video_id)
    print(create_video_creation(video_id, image_url, page_id))
