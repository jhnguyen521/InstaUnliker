import sys
import os
import json
import codecs
from instagram_private_api import Client


class Unliker():
    def to_json(self, python_object):
        if isinstance(python_object, bytes):
            return {'__class__': 'bytes',
                    '__value__': codecs.encode(python_object, 'base64').decode()}
        raise TypeError(repr(python_object) + ' is not JSON serializable')

    def from_json(self, json_object):
        if '__class__' in json_object and json_object['__class__'] == 'bytes':
            return codecs.decode(json_object['__value__'].encode(), 'base64')
        return json_object

    def onlogin_callback(self, api, new_settings_file):
        cache_settings = api.settings
        with open(new_settings_file, 'w') as outfile:
            json.dump(cache_settings, outfile, default=self.to_json)
            print('SAVED: {0!s}'.format(new_settings_file))

    def __init__(self):
        settings_file = "settings.json"

        if len(sys.argv) < 3:
            print('Usage: python unliker.py username password max_remove(optional)')
            os._exit(1)
        else:
            self.user = sys.argv[1]
            self.pwd = sys.argv[2]

        if not os.path.isfile(settings_file):
            print("Settings file not found...")
            self.api = Client(self.user, self.pwd, on_login=lambda x: self.onlogin_callback(x, settings_file))
        else:
            with open(settings_file) as file_data:
                cached_settings = json.load(file_data, object_hook=self.from_json)
            print("Reusing settings...")
            self.api = Client(self.user, self.pwd, settings=cached_settings)

        self.following = set([u['username'] for u in
                              self.api.user_following(self.api.authenticated_user_id, self.api.generate_uuid())[
                                  'users']])  # used for filtering


    def followerFilter(self, post):
        return post['user']['username'] in self.following

    def dogFilter(self, post):
        user = post['user']['username']
        if post['caption']:
            caption = post['caption']['text']
            return 'dog' in caption or 'dog' in user or 'corg' in caption or 'corg' in user
        else:
            return False


    def unlike(self, filters=[followerFilter], max_remove = 40):
        removed = 0

        while removed < max_remove:
            liked = self.api.feed_liked()

            print('Beginning deletion of liked photos')

            for p in liked['items']:
                post_id = p['id']

                if not any([f(p) for f in filters]):
                    print('Deleted', post_id, 'by', p['user']['username'])
                    self.api.delete_like(post_id)
                    removed += 1


            print('Grabbing more posts...')

            while True:
                liked = self.api.feed_liked()
                if liked['status'] == 'ok':
                    break

            print('Grabbed', liked['num_results'], 'more posts.')
            if liked['num_results'] == 0:
                print("No more posts to unlike.")
                break

        print('Finished deleting liked photos')



unliker = Unliker()
unliker.unlike([unliker.followerFilter, unliker.dogFilter], 40 if len(sys.argv) <= 3 else sys.argv[3])