import requests


class Everve():
    BASE_API = 'https://api.everve.net/v2/'

    def __init__(self, api_key: str):
        self._api_key = api_key


    def balance(self):
        """
        Get balance on everve.

        Example response:
        {
            "user_id": "1",
            "user_balance": "94.5983"
        }
        """
        result = self._get_json(
            self.BASE_API + 'user'
        )
        return result

    
    def socials(self):
        """
        Retrieve a complete list of social networks
        supported by Everve (eg, Facebook, Twitter etc).

        Example response:
        {
            "fb": {
                "social_id": "1",
                "social_name": "Facebook",
                "social_name_short": "fb",
                "social_enabled": "true",
                "social_color_dark": "385A92",
                "social_color_light": "4F74B0"
            },
            "tw": {
                "social_id": "2",
                "social_name": "Twitter",
                "social_name_short": "tw",
                "social_enabled": "true",
                "social_color_dark": "10AADA",
                "social_color_light": "45C5ED"
            },
            ...
        }
        """
        result = self._get_json(
            self.BASE_API + 'socials'
        )
        return result

    
    def categories(self, social_id: str=None):
        """
        Retrieve a complete list of categories supported by Everve
        (eg, Facebook Likes, Twitter Followers, Instagram Comments etc)
        OR Retrieve a particular categories by single social network
        (eg, Twitter Followers, Twitter Tweets, Twitter Retweets, Twitter Favorites)
        in case of {ID} presence. Value of {ID} is a ID of particular social network
        and can be obtained from method .socials() call. 

        Example response:
        {
            "ig-likes": {
                "category_id": "18",
                "social_id": "4",
                "category_name": "Instagram Likes",
                "category_name_short": "IG Likes",
                "category_avg_performers_count": "3845",
                "category_min_price_usd": "0.002",
                "category_max_price_usd": "0.01"
            },
            "ig-followers": {
                "category_id": "19",
                "social_id": "4",
                "category_name": "Instagram Followers",
                "category_name_short": "IG Followers",
                "category_avg_performers_count": "4734",
                "category_min_price_usd": "0.002",
                "category_max_price_usd": "0.01"
            },
            ...
        }
        """
        uri = self.BASE_API + 'categories'
        if social_id:
            uri += f'/{social_id}'

        return self._get_json(uri)

    
    def new_order(
        self, category_id: int, order_url: str, order_price: float,
        order_daily_limit: int=None, order_hourly_limit: int=None,
        order_overall_limit: int=None, order_custom_data: list=None
        ):
        """
        Creates a new order.

        param category_id: ID of the category. Can be obtained from GET method .categories() call.
        param order_url: URL of the resource.
        param order_price: Reward for one action of the order (eg, like, comment, subscribe etc). Value is 0.002 by default.
        param order_daily_limit: Actions daily limit. Value is 0 by default (means there is no limits).
        param order_hourly_limit: Actions hourly limit. Value is 0 by default (means there is no limits).
        param order_overall_limit: Actions overall limit. Value is 0 by default (means there is no limits).
        param order_custom_data: List of JSON formatted custom data (if applicable). For example, a list of custom comments.

        Example response:
        {
            "order_id": 45,
            "order_title": "Audi",
            "order_preview_pic": "https://...jpg",
            "order_initial_social_counter": 123456,
        }
        """
        params = {
            'category_id': category_id,
            'order_url': order_url,
            'order_price': order_price
        }
        if order_daily_limit:
            params['order_daily_limit'] = order_daily_limit
        if order_hourly_limit:
            params['order_hourly_limit'] = order_hourly_limit
        if order_overall_limit:
            params['order_overall_limit'] = order_overall_limit
        if order_custom_data:
            params['order_custom_data'] = order_custom_data

        result = self._get_json(
            self.BASE_API + 'orders',
            method='POST',
            params=params
        )
        return result

    
    def get_order(
        self, order_ids: tuple=None, order_history: int=None):
        """
        Retrieve a full list of the orders OR Retrieve a data by particular order
        (eg, title, price, limits, counters, status etc) in case of {ID} presence. 

        param order_ids: Comma separated list of order IDs (for multiple order requests)
        Example: (111,2222,33333,44444)

        param order_history: Add to response an order(s) history
        Example: 1

       
        Example response:
        {
            "order_id": "45",
            "order_created_datetime": "2019-11-04 03:07:01",
            "order_updated_datetime": "0000-00-00 00:00:00",
            "order_category_id": "19",
            "order_url": "https://www.instagram.com/audi/",
            "order_title": "Audi",
            "order_preview_pic": "https://scon...jpg",
            "order_price": "0.010000",
            "order_daily_limit": "100",
            "order_hourly_limit": "20",
            "order_overall_limit": "500",
            "order_daily_counter": "53",
            "order_overall_counter": "221",
            "order_active": "1",
            "order_deleted": "0",
            "order_status": "in_progress"
        }
        """
        params = {}
        if order_ids:
            params['order_ids'] = order_ids
        if order_history:
            params['order_history'] = order_history
            
        result = self._get_json(
            self.BASE_API + 'orders',
            params=params
        )
        return result


    def _get_json(self, url, method: str='GET', params=None):
        return getattr(requests, method.lower())(
            url,
            params=({
                'api_key': self._api_key,
                'format': 'json'
            } if not params else params)
        ).json()

        