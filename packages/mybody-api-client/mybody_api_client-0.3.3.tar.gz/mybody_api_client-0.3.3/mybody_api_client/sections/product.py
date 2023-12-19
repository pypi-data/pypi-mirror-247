#
# (c) 2023, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from mybody_api_client.sections.base import RequestTypes, BaseSection


class Product(BaseSection):
    prefix = 'products'

    async def get(self, id_: int):
        path = f'/get'
        response = await self.request(
            type_=RequestTypes.GET,
            path=path,
            token_required=False,
            parameters={
                'id_': id_,
            },
        )
        return response

    async def get_list(self, nutrient_type: str = None):
        path = f'/list/get'
        response = await self.request(
            type_=RequestTypes.GET,
            path=path,
            token_required=False,
            parameters={
                'nutrient_type': nutrient_type,
            },
        )
        return response

    async def create(self, name: str, nutrient_type: str = None):
        path = f'/create'
        response = await self.request(
            type_=RequestTypes.POST,
            path=path,
            parameters={
                'name': name,
                'nutrient_type': nutrient_type,
            },
        )
        return response

    async def delete(self, id_: int):
        path = f'/delete'
        response = await self.request(
            type_=RequestTypes.POST,
            path=path,
            parameters={
                'id_': id_,
            },
        )
        return response

    async def update(self, id_: int, nutrient_type: str):
        path = f'/update'
        response = await self.request(
            type_=RequestTypes.POST,
            path=path,
            parameters={
                'id_': id_,
                'nutrient_type': nutrient_type,
            },
        )
        return response
    