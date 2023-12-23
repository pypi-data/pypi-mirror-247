from random import randint
from os.path import getsize


class Methods:

    async def _is_exist_username(self, username: str) -> dict:
        json = self.make_json(
            'isExistUsername',
            {
                'username': username.split('@')[-1]
            })
        return self.post(json=json)


    async def _get_my_archive_stories(
            self,
            profile_id: str = None,
            limit: int = 50,
            sort: str = 'FromMax',
            equal: bool = False
    ) -> dict:
        json = self.make_json(
            'getMyArchiveStories',
            {
                'equal': equal,
                'limit': limit,
                'sort': sort,
                'profile_id': profile_id
            })
        return self.post(json=json)


    async def _get_guid_by_profile_id(self, target_profile_id: str, profile_id: str = None) -> dict:
        json = self.make_json(
            'getProfileInfo',
            {
                'profile_id': profile_id,
                'target_profile_id': target_profile_id
            })
        responce = self.post(json=json)
        return responce['data']['profile']['chat_link']['open_chat_data']['object_guid']


    async def _get_post_by_share_link(self, share_link: str, profile_id: str = None) -> dict:
        json = self.make_json(
            'getPostByShareLink',
            {
                'share_string': share_link.split('/')[-1],
                'profile_id': profile_id
            })
        return self.post(json=json)


    async def _get_profile_info(self, target_profile_id: str, profile_id: str = None) -> dict:
        json = self.make_json(
            'getProfileInfo',
            {
                'profile_id': profile_id,
                'target_profile_id': target_profile_id
            })
        return self.post(json=json)


    async def _get_me(self, profile_id: str = None) -> dict:
        json = self.make_json(
            'getMyProfileInfo',
            {
              'profile_id': profile_id
            })
        return self.post(json=json)


    async def _follow(self, followee_id: str, profile_id: str = None) -> dict:
        json = self.make_json(
            'requestFollow',
            {
                'f_type': 'Follow',
                'followee_id': followee_id,
                'profile_id': profile_id
            })
        return self.post(json=json)


    async def _un_follow(self, followee_id: str, profile_id: str = None) -> dict:
        json = self.make_json(
            'requestFollow',
            {
                'f_type': 'Unfollow',
                'followee_id': followee_id,
                'profile_id': profile_id
            })
        return self.post(json=json)


    async def _create_page(self, **kwargs) -> dict:
        json = self.make_json('createPage', {**kwargs})
        return self.post(json=json)


    async def _remove_page(self, record_id: str, profile_id: str = None) -> dict:
        json = self.make_json(
            'removeRecord',
            {
                'model': 'Profile',
                'record_id': record_id,
                'profile_id': profile_id
            })
        return self.post(json=json)


    async def _update_profile(self, **kwargs) -> dict:
        json = self.make_json('updateProfile', {**kwargs})
        return self.post(json=json)


    async def _add_comment(
            self,
            text: str,
            post_id: str,
            post_profile_id: str,
            profile_id: str = None
    ) -> dict:
        json = self.make_json(
            'addComment',
            {
                'content': text,
                'post_id': post_id,
                'post_profile_id': post_profile_id,
                'rnd': randint(100000000, 999999999),
                'profile_id': profile_id
            })
        return self.post(json=json)


    async def _like(self, post_id: str, target_profile_id: str, profile_id: str = None) -> dict:
        json = self.make_json(
            'likePostAction',
            {
                'action_type': 'Like',
                'post_id': post_id,
                'post_profile_id': target_profile_id,
                'profile_id': profile_id
            })
        return self.post(json=json)


    async def _un_like(self, post_id: str, target_profile_id: str, profile_id: str = None) -> dict:
        json = self.make_json(
            'likePostAction',
            {
                'action_type': 'Unlike',
                'post_id': post_id,
                'post_profile_id': target_profile_id,
                'profile_id': profile_id
            })
        return self.post(json=json)


    async def _view(self, post_id: str, target_profile_id: str) -> dict:
        json = self.make_json(
            'addPostViewCount',
            {
                'post_id': post_id,
                'post_profile_id': target_profile_id
            })
        return self.post(json=json)


    async def _get_comments(
            self,
            post_id: str,
            target_profile_id: str,
            profile_id: str = None,
            sort: str = 'FromMax',
            limit: int = 50,
            equal: bool = False
    ) -> dict:
        json = self.make_json(
            'getComments',
            {
                'equal': equal,
                'limit': limit,
                'sort': sort,
                'post_id': post_id,
                'profile_id': profile_id,
                'post_profile_id': post_profile_id
            })
        return self.post(json=json)


    async def _get_profile_posts(
            self,
            target_profile_id: str,
            profile_id: str = None,
            limit: int = 50,
            sort: str = 'FromMax',
            equal: bool = False
    ) -> dict:
        json = self.make_json(
            'getProfilePosts',
            {
                'equal': equal,
                'limit': limit,
                'sort': sort,
                'profile_id': profile_id,
                'target_profile_id': target_profile_id
            })
        return self.post(json=json)


    async def _get_profiles_stories(self, target_profile_id: str, limit: int = 100) -> dict:
        json = self.make_json(
            'getProfilesStories',
            {
                'limit': limit,
                'profile_id': target_profile_id
            })
        return self.post(json=json)


    async def _get_recent_following_posts(
            self,
            target_profile_id: str,
            limit: int = 30,
            sort: str = 'FromMax',
            equal: bool = False
    ) -> dict:
        json = self.make_json(
            'getRecentFollowingPosts',
            {
                'equal': equal,
                'limit': limit,
                'sort': sort,
                'profile_id': target_profile_id
            })
        return self.post(json=json)


    async def _get_bookmarked_posts(
            self,
            target_profile_id: str,
            limit: int = 50,
            sort: str = 'FromMax',
            equal: bool = False
    ) -> dict:
        json = self.make_json(
            'getBookmarkedPosts',
            {
                'equal': equal,
                'limit': limit,
                'sort': sort,
                'profile_id': target_profile_id
              })
        return self.post(json=json)


    async def _get_explore_posts(
            self,
            profile_id: str = None,
            limit: int = 50,
            sort: str = 'FromMax',
            equal: bool = False,
            max_id: str = None
    ) -> dict:
        json = self.make_json(
            'getExplorePosts',
            {
                'equal': equal,
                'limit': limit,
                'sort': sort,
                'max_id': max_id,
                'profile_id': profile_id
              })
        return self.post(json=json)


    async def _get_blocked_profiles(
            self,
            profile_id: str = None,
            limit: int = 50,
            sort: str = 'FromMax',
            equal: bool = False
    ) -> dict:
        json = self.make_json(
            'getBlockedProfiles',
            {
                'equal': equal,
                'limit': limit,
                'sort': sort,
                'profile_id': profile_id
            })
        return self.post(json=json)


    async def _get_profile_followers(
            self,
            target_profile_id: str,
            profile_id: str = None,
            limit: int = 50,
            sort: str = 'FromMax',
            equal: bool = False
    ) -> dict:
        json = self.make_json(
            'getProfileFollowers',
             {
                'equal': equal,
                'f_type': 'Follower',
                'limit': limit,
                'sort': sort,
                'target_profile_id': target_profile_id,
                'profile_id': profile_id
             })
        return self.post(json=json)


    async def _get_profile_followings(
            self,
            target_profile_id: str,
            profile_id: str = None,
            limit: int = 50,
            sort: str = 'FromMax',
            equal: bool = False
    ) -> dict:
        json = self.make_json(
            'getProfileFollowers',
             {
                'equal': equal,
                'f_type': 'Following',
                'limit': limit,
                'sort': sort,
                'target_profile_id': target_profile_id,
                'profile_id': profile_id
             })
        return self.post(json=json)


    async def _block_profile(self, blocked_id: str, profile_id: str = None) -> dict:
        json = self.make_json(
            'setBlockProfile',
             {
                'action':'Block',
                'blocked_id': blocked_id,
                'profile_id': profile_id
               })
        return self.post(json=json)


    async def _un_block_profile(self, blocked_id: str, profile_id: str = None) -> dict:
        json = self.make_json(
            'setBlockProfile',
             {
                'action': 'Unblock',
                'blocked_id': blocked_id,
                'profile_id': profile_id
               })
        return self.post(json=json)


    async def _request_upload_file(
            self,
            profile_id: str,
            file_name: str,
            file_size: int,
            file_type: str
    ) -> dict:
        json = self.make_json(
            'requestUploadFile',
            {
                'file_name': file_name.split('/')[-1],
                'file_size': file_size,
                'file_type': file_type,
                'profile_id': profile_id
            })
        return self.post(json=json)


    async def _upload_file(self, file: str, file_type: str, profile_id: str = None) -> dict:
        filename, filesize = file.split('/')[-1], getsize(file)
        result = await self.request_upload_file(profile_id, filename, filesize, file_type)
        byte_file = open(file, 'rb').read()
        headers: dict = {
            'auth': self.auth,
            'file-id': result['data']['file_id'],
            'chunk-size': str(len(byte_file)),
            'total-part': '1',
            'part-number': '1',
            'hash-file-request': result['data']['hash_file_request']
        }
        return self.session.post(
            result['data']['server_url'], data=byte_file, headers=headers).json()['data'], result['data']


    async def _add_post(
            self,
            file: str,
            caption: str = None,
            file_type: str = 'Picture',
            profile_id: str = None,
    ) -> dict:
        result = await self.upload_file(file, file_type, profile_id)
        json = self.make_json('addPost', {
            'rnd': int(randint(0, 9)),
            'width': 720,
            'height': 720,
            'caption': caption,
            'file_id': result[1]['file_id'],
            'post_type': file_type,
            'profile_id': profile_id,
            'hash_file_receive': result[0]['hash_file_receive'],
            'thumbnail_file_id': result[1]['file_id'],
            'thumbnail_hash_file_receive': result[0]['hash_file_receive'],
            'is_multi_file': False
            })
        return self.post(json=json)


    async def _report_profile(
            self,
            record_id: str,
            post_profile_id: str,
            profile_id: str = None,
            model: str = 'Post',
            reason: int = 1
    ) -> dict:
        json = self.make_json(
            'setReportRecord',
            {
                'model': model,
                'reason': reason,
                'record_id': record_id,
                'post_profile_id': post_profile_id,
                'profile_id': profile_id
            })
        return self.post(json=json)
