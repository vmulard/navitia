# coding=utf-8
# Copyright (c) 2001-2014, Canal TP and/or its affiliates. All rights reserved.
#
# This file is part of Navitia,
#     the software to build cool stuff with public transport.
#
# Hope you'll enjoy and contribute to this project,
#     powered by Canal TP (www.canaltp.fr).
# Help us simplify mobility and open public transport:
#     a non ending quest to the responsive locomotion way of traveling!
#
# LICENCE: This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Stay tuned using
# twitter @navitia
# IRC #navitia on freenode
# https://groups.google.com/d/forum/navitia
# www.navitia.io

from __future__ import absolute_import, print_function, unicode_literals, division
import mock
from pytest import raises

from jormungandr.tests.utils_test import MockRequests, MockResponse, user_set, FakeUser
from tests.check_utils import is_valid_global_autocomplete
from tests import check_utils
from tests.tests_mechanism import NewDefaultScenarioAbstractTestFixture
from .tests_mechanism import AbstractTestFixture, dataset
from jormungandr import app
from six.moves.urllib.parse import urlencode
from .tests_mechanism import config


class FakeUserBragi(FakeUser):
    @classmethod
    def get_from_token(cls, token, valid_until):
        """
        Create an empty user
        """
        return user_in_db_bragi[token]

def geojson():
    return '{"type": "Feature", "geometry": ' \
           '{"type": "Point", "coordinates": [102.0, 0.5]}, "properties": {"prop0": "value0"}}'

user_in_db_bragi = {
    'test_user_no_shape': FakeUserBragi('test_user_no_shape', 1,
                                        have_access_to_free_instances=False, is_super_user=True),
    'test_user_with_shape': FakeUserBragi('test_user_with_shape', 2,
                                          True, False, False, shape=geojson()),
    'test_user_with_coord': FakeUserBragi('test_user_with_coord', 2,
                                          True, False, False, default_coord="12;42"),
}


MOCKED_INSTANCE_CONF = {
    'instance_config': {
        'default_autocomplete': 'bragi'
    }
}

BRAGI_MOCK_RESPONSE = {
    "features": [
        {
            "geometry": {
                "coordinates": [
                    3.282103,
                    49.847586
                ],
                "type": "Point"
            },
            "properties": {
                "geocoding": {
                    "city": "Bobtown",
                    "housenumber": "20",
                    "id": "49.847586;3.282103",
                    "label": "20 Rue Bob (Bobtown)",
                    "name": "Rue Bob",
                    "postcode": "02100",
                    "street": "Rue Bob",
                    "type": "house",
                    "citycode": "02000",
                    "administrative_regions": [
                        {
                            "id": "admin:fr:02000",
                            "insee": "02000",
                            "level": 8,
                            "label": "Bobtown (02000)",
                            "zip_codes": ["02000"],
                            "weight": 1,
                            "coord": {
                                "lat": 48.8396154,
                                "lon": 2.3957517
                            }
                        }
                    ],
                }
            },
            "type": "Feature"
        }
    ]
}


BRAGI_MOCK_POI_WITHOUT_ADDRESS = {
    "features": [
        {
            "geometry": {
                "coordinates": [
                    0.0000898312,
                    0.0000898312
                ],
                "type": "Point"
            },
            "properties": {
                "geocoding": {
                    "city": "Bobtown",
                    "id": "bobette",
                    "label": "bobette's label",
                    "name": "bobette",
                    "poi_types": [
                        {
                            "id": "poi_type:amenity:bicycle_rental",
                            "name": "Station VLS"
                        }
                    ],
                    "postcode": "02100",
                    "type": "poi",
                    "citycode": "02000",
                    "properties": [
                        {"key": "amenity", "value": "bicycle_rental"},
                        {"key": "capacity", "value": "20"},
                        {"key": "ref", "value": "12"}
                    ],
                    "administrative_regions": [
                        {
                            "id": "admin:fr:02000",
                            "insee": "02000",
                            "level": 8,
                            "label": "Bobtown (02000)",
                            "zip_codes": ["02000"],
                            "weight": 1,
                            "coord": {
                                "lat": 48.8396154,
                                "lon": 2.3957517
                            }
                        }
                    ],
                    }
            },
            "type": "Feature"
        }
    ]
}

BRAGI_MOCK_STOP_AREA_WITH_MODES = {
    "features": [
        {
            "geometry": {
                "coordinates": [
                    0.0000898312,
                    0.0000898312
                ],
                "type": "Point"
            },
            "properties": {
                "geocoding": {
                    "city": "Bobtown",
                    "id": "bobette",
                    "label": "bobette's label",
                    "name": "bobette",
                    "poi_types": [
                        {
                            "id": "poi_type:amenity:bicycle_rental",
                            "name": "Station VLS"
                        }
                    ],
                    "postcode": "02100",
                    "type": "public_transport:stop_area",
                    "citycode": "02000",
                    "properties": [],
                    "commercial_modes": [
                        {"id": "cm_id:Bus",
                         "name": "cm_name:Bus"},
                        {"id": "cm_id:Car",
                         "name": "cm_name:Car"}
                    ],
                    "physical_modes": [
                        {"id": "pm_id:Bus",
                         "name": "pm_name:Bus"},
                        {"id": "pm_id:Car",
                         "name": "pm_name:Car"}
                    ],
                    "administrative_regions": [
                        {
                            "id": "admin:fr:02000",
                            "insee": "02000",
                            "level": 8,
                            "label": "Bobtown (02000)",
                            "zip_codes": ["02000"],
                            "weight": 1,
                            "coord": {
                                "lat": 48.8396154,
                                "lon": 2.3957517
                            }
                        }
                    ],
                    }
            },
            "type": "Feature"
        }
    ]
}

BRAGI_MOCK_STOP_AREA_WITHOUT_MODES = {
    "features": [
        {
            "geometry": {
                "coordinates": [
                    0.0000898312,
                    0.0000898312
                ],
                "type": "Point"
            },
            "properties": {
                "geocoding": {
                    "city": "Bobtown",
                    "id": "bobette",
                    "label": "bobette's label",
                    "name": "bobette",
                    "poi_types": [
                        {
                            "id": "poi_type:amenity:bicycle_rental",
                            "name": "Station VLS"
                        }
                    ],
                    "postcode": "02100",
                    "type": "public_transport:stop_area",
                    "citycode": "02000",
                    "properties": [],
                    "administrative_regions": [
                        {
                            "id": "admin:fr:02000",
                            "insee": "02000",
                            "level": 8,
                            "label": "Bobtown (02000)",
                            "zip_codes": ["02000"],
                            "weight": 1,
                            "coord": {
                                "lat": 48.8396154,
                                "lon": 2.3957517
                            }
                        }
                    ],
                    }
            },
            "type": "Feature"
        }
    ]
}

@dataset({'main_routing_test': MOCKED_INSTANCE_CONF}, global_config={'activate_bragi': True})
class TestBragiAutocomplete(AbstractTestFixture):

    def test_autocomplete_call(self):
        url = 'https://host_of_bragi/autocomplete'
        params = {
            'q': u'bob',
            'type[]': [u'public_transport:stop_area', u'street', u'house', u'poi', u'city'],
            'limit': 10,
            'pt_dataset': 'main_routing_test'
        }

        url += "?{}".format(urlencode(params, doseq=True))
        mock_requests = MockRequests({
            url: (BRAGI_MOCK_RESPONSE, 200)
        })
        with mock.patch('requests.get', mock_requests.get):
            response = self.query_region("places?q=bob&pt_dataset=main_routing_test&type[]=stop_area"
                                         "&type[]=address&type[]=poi&type[]=administrative_region")

            is_valid_global_autocomplete(response, depth=1)
            r = response.get('places')
            assert len(r) == 1
            assert r[0]['name'] == '20 Rue Bob (Bobtown)'
            assert r[0]['embedded_type'] == 'address'
            assert r[0]['address']['name'] == 'Rue Bob'
            assert r[0]['address']['label'] == '20 Rue Bob (Bobtown)'
            fbs = response['feed_publishers']
            assert {fb['id'] for fb in fbs} >= {u'osm', u'bano'}

    def test_autocomplete_call_with_param_from(self):
        """
        test that the from param of the autocomplete is correctly given to bragi
        :return:
        """
        def http_get(url, *args, **kwargs):
            params = kwargs.pop('params')
            assert params
            assert params.get('lon') == '3.25'
            assert params.get('lat') == '49.84'
            return MockResponse({}, 200, '')
        with mock.patch('requests.get', http_get) as mock_method:
            self.query_region('places?q=bob&from=3.25;49.84')

    def test_autocomplete_call_override(self):
        """"
        test that the _autocomplete param switch the right autocomplete service
        """
        url = 'https://host_of_bragi'
        params = {
            'q': u'bob',
            'type[]': [u'public_transport:stop_area', u'street', u'house', u'poi', u'city'],
            'limit': 10,
            'pt_dataset': 'main_routing_test'
        }

        url += "/autocomplete?{}".format(urlencode(params, doseq=True))

        mock_requests = MockRequests({
            url: (BRAGI_MOCK_RESPONSE, 200)
        })
        with mock.patch('requests.get', mock_requests.get):
            response = self.query_region("places?q=bob&type[]=stop_area&type[]=address&type[]=poi"
                                         "&type[]=administrative_region")

            is_valid_global_autocomplete(response, depth=1)
            r = response.get('places')
            assert len(r) == 1
            assert r[0]['name'] == '20 Rue Bob (Bobtown)'
            assert r[0]['embedded_type'] == 'address'
            assert r[0]['address']['name'] == 'Rue Bob'
            assert r[0]['address']['label'] == '20 Rue Bob (Bobtown)'

            # with a query on kraken, the results should be different
            response = self.query_region("places?q=Park&_autocomplete=kraken")
            r = response.get('places')
            assert len(r) >= 1
            assert r[0]['name'] == 'first parking (Condom)'

    def test_autocomplete_call_with_no_param_type(self):
        """
        test that stop_area, poi, address and city are the default types passed to bragi
        :return:
        """
        def http_get(url, *args, **kwargs):
            params = kwargs.pop('params')
            assert params
            assert params.get('type[]') == ['public_transport:stop_area', 'street', 'house', 'poi', 'city']
            return MockResponse({}, 200, '')
        with mock.patch('requests.get', http_get) as mock_method:
            self.query_region('places?q=bob')

    def test_autocomplete_call_with_param_type_administrative_region(self):
        """
        test that administrative_region is converted to city
        :return:
        """
        def http_get(url, *args, **kwargs):
            params = kwargs.pop('params')
            assert params
            assert params.get('type[]') == ['city', 'street', 'house']

            return MockResponse({}, 200, '')
        with mock.patch('requests.get', http_get) as mock_method:
            self.query_region('places?q=bob&type[]=administrative_region&type[]=address')

    def test_autocomplete_call_with_param_type_not_acceptable(self):
        """
        test not acceptable type
        :return:
        """
        def http_get(url, *args, **kwargs):
            return MockResponse({}, 422, '')

        with raises(Exception):
            with mock.patch('requests.get', http_get) as mock_method:
                self.query_region('places?q=bob&type[]=bobette')

    def test_autocomplete_call_with_param_type_stop_point(self):
        """
        test that stop_point is not passed to bragi
        :return:
        """
        def http_get(url, *args, **kwargs):
            params = kwargs.pop('params')
            assert params
            assert params.get('type[]') == ['street', 'house']

            return MockResponse({}, 200, '')
        with mock.patch('requests.get', http_get) as mock_method:
            self.query_region('places?q=bob&type[]=stop_point&type[]=address')

    def test_features_call(self):
        url = 'https://host_of_bragi'
        params = {'pt_dataset': 'main_routing_test'}

        url += "/features/1234?{}".format(urlencode(params, doseq=True))

        mock_requests = MockRequests({
            url: (BRAGI_MOCK_RESPONSE, 200)
        })
        with mock.patch('requests.get', mock_requests.get):
            response = self.query_region("places/1234?&pt_dataset=main_routing_test")

            is_valid_global_autocomplete(response, depth=1)
            r = response.get('places')
            assert len(r) == 1
            assert r[0]['name'] == '20 Rue Bob (Bobtown)'
            assert r[0]['embedded_type'] == 'address'
            assert r[0]['address']['name'] == 'Rue Bob'
            assert r[0]['address']['label'] == '20 Rue Bob (Bobtown)'

    def test_features_unknown_uri(self):
        url = 'https://host_of_bragi'
        params = {'pt_dataset': 'main_routing_test'}

        url += "/features/AAA?{}".format(urlencode(params, doseq=True))
        mock_requests = MockRequests({
        url:
            (
                {
                    'short": "query error',
                    'long": "invalid query EsError("Unable to find object")'
                },
                404
            )
        })

        with mock.patch('requests.get', mock_requests.get):
            response = self.query_region("places/AAA?&pt_dataset=main_routing_test", check=False)
            assert response[1] == 404
            assert response[0]["error"]["id"] == 'unknown_object'
            assert response[0]["error"]["message"] == "The object AAA doesn't exist"

    def test_poi_without_address(self):
        url = 'https://host_of_bragi'
        params = {'pt_dataset': 'main_routing_test'}

        url += "/features/1234?{}".format(urlencode(params, doseq=True))

        mock_requests = MockRequests({
            url: (BRAGI_MOCK_POI_WITHOUT_ADDRESS, 200)
        })
        with mock.patch('requests.get', mock_requests.get):
            response = self.query_region("places/1234?&pt_dataset=main_routing_test")

            r = response.get('places')
            assert len(r) == 1
            assert r[0]['embedded_type'] == 'poi'
            assert r[0]['poi']['name'] == 'bobette'
            assert r[0]['poi']['label'] == "bobette's label"
            assert not r[0]['poi'].get('address')

    def test_stop_area_with_modes(self):
        url = 'https://host_of_bragi'
        params = {'pt_dataset': 'main_routing_test'}

        url += "/features/1234?{}".format(urlencode(params, doseq=True))

        mock_requests = MockRequests({
            url: (BRAGI_MOCK_STOP_AREA_WITH_MODES, 200)
        })
        with mock.patch('requests.get', mock_requests.get):
            response = self.query_region("places/1234?&pt_dataset=main_routing_test")

            r = response.get('places')
            assert len(r) == 1
            assert r[0]['embedded_type'] == 'stop_area'
            assert r[0]['stop_area']['name'] == 'bobette'
            assert len(r[0]['stop_area'].get('commercial_modes')) == 2
            assert r[0]['stop_area'].get('commercial_modes')[0].get('id') == 'cm_id:Bus'
            assert r[0]['stop_area'].get('commercial_modes')[0].get('name') == 'cm_name:Bus'
            assert r[0]['stop_area'].get('commercial_modes')[1].get('id') == 'cm_id:Car'
            assert r[0]['stop_area'].get('commercial_modes')[1].get('name') == 'cm_name:Car'

            assert len(r[0]['stop_area'].get('physical_modes')) == 2
            assert r[0]['stop_area'].get('physical_modes')[0].get('id') == 'pm_id:Bus'
            assert r[0]['stop_area'].get('physical_modes')[0].get('name') == 'pm_name:Bus'
            assert r[0]['stop_area'].get('physical_modes')[1].get('id') == 'pm_id:Car'
            assert r[0]['stop_area'].get('physical_modes')[1].get('name') == 'pm_name:Car'

    def test_stop_area_without_modes(self):
        url = 'https://host_of_bragi'
        params = {'pt_dataset': 'main_routing_test'}

        url += "/features/1234?{}".format(urlencode(params, doseq=True))

        mock_requests = MockRequests({
            url: (BRAGI_MOCK_STOP_AREA_WITHOUT_MODES, 200)
        })
        with mock.patch('requests.get', mock_requests.get):
            response = self.query_region("places/1234?&pt_dataset=main_routing_test")

            r = response.get('places')
            assert len(r) == 1
            assert r[0]['embedded_type'] == 'stop_area'
            assert 'commercial_modes' not in r[0]['stop_area']
            assert 'physical_modes' not in r[0]['stop_area']


@dataset({"main_routing_test": {}}, global_config={'activate_bragi': True})
class TestBragiShape(AbstractTestFixture):

    def test_places_for_user_with_shape(self):
        """
        Test that with a shape on user, it is correctly posted
        """
        with user_set(app, FakeUserBragi, "test_user_with_shape"):

            mock_post = mock.MagicMock(return_value=MockResponse({}, 200, '{}'))

            def http_get(url, *args, **kwargs):
                assert False

            with mock.patch('requests.get', http_get):
                with mock.patch('requests.post', mock_post):

                    self.query('v1/coverage/main_routing_test/places?q=toto&_autocomplete=bragi')
                    assert mock_post.called

                    mock_post.reset_mock()
                    self.query('v1/places?q=toto')
                    assert mock_post.called

            # test that the shape is posted
            def http_post(url, *args, **kwargs):
                json = kwargs.pop('json')
                assert json['shape']['type'] == 'Feature'
                assert json.get('shape').get('geometry')
                return MockResponse({}, 200, '{}')

            with mock.patch('requests.get', http_get):
                with mock.patch('requests.post', http_post):
                    self.query('v1/coverage/main_routing_test/places?q=toto&_autocomplete=bragi')
                    self.query('v1/places?q=toto')

    def test_places_for_user_without_shape(self):
        """
        Test that without shape for user, we use the get method
        """
        with user_set(app, FakeUserBragi, "test_user_no_shape"):

            mock_get = mock.MagicMock(return_value=MockResponse({}, 200, '{}'))

            def http_post(self, url, *args, **kwargs):
                assert False

            with mock.patch('requests.get', mock_get):
                with mock.patch('requests.post', http_post):

                    self.query('v1/coverage/main_routing_test/places?q=toto&_autocomplete=bragi')
                    assert mock_get.called

                    mock_get.reset_mock()
                    self.query('v1/places?q=toto')
                    assert mock_get.called

    def test_places_for_user_with_coord(self):
        """
        Test that with a default_coord on user, it is correctly posted
        """
        with user_set(app, FakeUserBragi, "test_user_with_coord"):
            def http_get(url, *args, **kwargs):
                params = kwargs.pop('params')
                assert params
                assert params.get('lon') == '12'
                assert params.get('lat') == '42'
                return MockResponse({}, 200, '')

            with mock.patch('requests.get', http_get):
                self.query('v1/coverage/main_routing_test/places?q=toto&_autocomplete=bragi')

    def test_places_for_user_with_coord_and_coord_overriden(self):
        """
        Test that with a default_coord on user, if the user gives a coord we use the given coord
        """
        with user_set(app, FakeUserBragi, "test_user_with_coord"):
            def http_get(url, *args, **kwargs):
                params = kwargs.pop('params')
                assert params
                assert params.get('lon') == '1'
                assert params.get('lat') == '2'
                return MockResponse({}, 200, '')

            with mock.patch('requests.get', http_get):
                self.query('v1/coverage/main_routing_test/places?q=toto&_autocomplete=bragi&from=1;2')

    def test_places_for_user_with_coord_and_coord_overriden_to_null(self):
        """
        Test that with a default_coord on user, if the user gives an empty coord we do not pass a coord
        """
        with user_set(app, FakeUserBragi, "test_user_with_coord"):
            def http_get(url, *args, **kwargs):
                params = kwargs.pop('params')
                assert params
                assert not params.get('lon')
                assert not params.get('lat')
                return MockResponse({}, 200, '')

            with mock.patch('requests.get', http_get):
                self.query('v1/coverage/main_routing_test/places?q=toto&_autocomplete=bragi&from=')

    def test_places_with_empty_coord(self):
        """
        Test that we get an error if we give an empty coord
        (and if there is no user defined coord to override)
        """
        r, s = self.query_no_assert('v1/coverage/main_routing_test/places?q=toto&_autocomplete=bragi&from=')
        assert s == 400
        assert "if 'from' is provided it cannot be null" in r.get('message')

    def test_global_place_uri(self):
        mock_requests = MockRequests({
            # there is no authentication so all the known pt_dataset are added as parameters
            'https://host_of_bragi/features/bob?pt_dataset=main_routing_test': (BRAGI_MOCK_RESPONSE, 200)
        })
        with mock.patch('requests.get', mock_requests.get):
            response = self.query("/v1/places/bob")

            is_valid_global_autocomplete(response, depth=1)
            r = response.get('places')
            assert len(r) == 1
            assert r[0]['name'] == '20 Rue Bob (Bobtown)'
            assert r[0]['embedded_type'] == 'address'
            assert r[0]['address']['name'] == 'Rue Bob'
            assert r[0]['address']['label'] == '20 Rue Bob (Bobtown)'

    def test_global_coords_uri(self):
        url = 'https://host_of_bragi'
        params = {
            'pt_dataset': 'main_routing_test',
            'lon': 3.282103,
            'lat': 49.84758
        }
        url += "/reverse?{}".format(urlencode(params, doseq=True))

        mock_requests = MockRequests({
            url: (BRAGI_MOCK_RESPONSE, 200)
        })

        with mock.patch('requests.get', mock_requests.get):
            response = self.query("/v1/coverage/{pt_dataset}/coords/{lon};{lat}?_autocomplete=bragi".format(
                lon=params.get('lon'), lat=params.get('lat'), pt_dataset=params.get('pt_dataset')))

            address = response.get('address')
            assert address
            assert address['house_number'] == 20
            assert address['name'] == 'Rue Bob'
            assert address['label'] == '20 Rue Bob (Bobtown)'
            assert len(address['administrative_regions']) == 1

@dataset({'main_routing_test': MOCKED_INSTANCE_CONF}, global_config={'activate_bragi': True})
class AbstractAutocompleteAndRouting():
    def test_journey_with_external_uri_from_bragi(self):
        """
        This test aim to recreate a classic integration

        The user query the instance's autocomplete (which is set up to bragi)
        And then use the autocomplete's response to query for a journey

        For this test we have 2 item in our autocomplete:
         - the poi 'bobette' 
         - an adresse in bob's street that is not in the dataset
        """

        bragi_bobette = {
            "features": [
                {
                    "geometry": {
                        "coordinates": [
                            0.0000898312,
                            0.0000898312
                        ],
                        "type": "Point"
                    },
                    "properties": {
                        "geocoding": {
                            "city": "Bobtown",
                            "id": "bobette",
                            "label": "bobette's label",
                            "name": "bobette",
                            "poi_types": [
                                {
                                    "id": "poi_type:amenity:bicycle_rental", 
                                    "name": "Station VLS"
                                }
                            ], 
                            "postcode": "02100",
                            "type": "poi",
                            "citycode": "02000",
                            "properties": [
                                {"key": "amenity", "value": "bicycle_rental"},
                                {"key": "capacity", "value": "20"},
                                {"key": "ref", "value": "12"}
                            ],
                            "address": {
                                "type": "street",
                                "id": "179077655",
                                "name": "Speloncato-Monticello",
                                "label": "Speloncato-Monticello (Speloncato)",
                                "postcode": "20226",
                                "city": "Speloncato",
                                "citycode": "2B290",
                                "weight": 0.00847457627118644,
                                "coord": {
                                    "lat": 42.561667,
                                    "lon": 8.9809147
                                },
                                "zip_codes": [
                                    "20226"
                                ]
                            },
                            "administrative_regions": [
                                {
                                    "id": "admin:fr:02000",
                                    "insee": "02000",
                                    "level": 8,
                                    "label": "Bobtown (02000)",
                                    "zip_codes": ["02000"],
                                    "weight": 1,
                                    "coord": {
                                        "lat": 48.8396154,
                                        "lon": 2.3957517
                                    }
                                }
                            ],
                        }
                    },
                    "type": "Feature"
                }
            ]
        }

        bob_street = {
            "features": [
                {
                    "geometry": {
                        "coordinates": [
                            0.00188646,
                            0.00071865
                        ],
                        "type": "Point"
                    },
                    "properties": {
                        "geocoding": {
                            "city": "Bobtown",
                            "housenumber": "20",
                            "id": "addr:" + check_utils.r_coord, # the adresse is just above 'R'
                            "label": "20 Rue Bob (Bobtown)",
                            "name": "Rue Bob",
                            "postcode": "02100",
                            "street": "Rue Bob",
                            "type": "house",
                            "citycode": "02000",
                            "administrative_regions": [
                                {
                                    "id": "admin:fr:02000",
                                    "insee": "02000",
                                    "level": 8,
                                    "label": "Bobtown (02000)",
                                    "zip_codes": ["02000"],
                                    "weight": 1,
                                    "coord": {
                                        "lat": 48.8396154,
                                        "lon": 2.3957517
                                    }
                                }
                            ],
                        }
                    },
                    "type": "Feature"
                }
            ]
        }

        args = {
            u'pt_dataset': 'main_routing_test',
            u'type[]': [u'public_transport:stop_area', u'street', u'house', u'poi', u'city'],
            u'limit': 10,
        }
        params = urlencode(args, doseq=True)
        
        mock_requests = MockRequests({
            'https://host_of_bragi/autocomplete?q=bobette&{p}'.format(p=params): (bragi_bobette, 200),
            'https://host_of_bragi/features/bobette?pt_dataset=main_routing_test': (bragi_bobette, 200),
            'https://host_of_bragi/autocomplete?q=20+rue+bob&{p}'.format(p=params): (bob_street, 200),
            'https://host_of_bragi/reverse?lat={lat}&lon={lon}&pt_dataset=main_routing_test'
            .format(lon=check_utils.r_coord.split(';')[0], lat=check_utils.r_coord.split(';')[1])
            : (bob_street, 200)
        })

        def get_autocomplete(query):
            autocomplete_response = self.query_region(query)
            r = autocomplete_response.get('places')
            assert len(r) == 1
            return r[0]['id']

        with mock.patch('requests.get', mock_requests.get):
            journeys_from = get_autocomplete('places?q=bobette')
            journeys_to = get_autocomplete('places?q=20 rue bob')
            query = 'journeys?from={f}&to={to}&datetime={dt}'.format(f=journeys_from, to=journeys_to, dt="20120614T080000")
            journeys_response = self.query_region(query)

            self.is_valid_journey_response(journeys_response, query)

            # all journeys should have kept the user's from/to
            for j in journeys_response['journeys']:
                response_from = j['sections'][0]['from']
                assert response_from['id'] == "bobette"
                assert response_from['name'] == "bobette's label"
                assert response_from['embedded_type'] == "poi"
                assert response_from['poi']['label'] == "bobette's label"
                assert response_from['poi']['properties']["amenity"] == "bicycle_rental"
                assert response_from['poi']['properties']["capacity"] == "20"
                assert response_from['poi']['properties']["ref"] == "12"
                assert response_from['poi']['address']['id'] == "179077655"
                assert response_from['poi']['address']['name'] == "Speloncato-Monticello"
                assert response_from['poi']['address']['label'] == "Speloncato-Monticello (Speloncato)"
                assert response_from['poi']['address']['house_number'] == 0

                response_to = j['sections'][-1]['to']
                assert response_to['id'] == journeys_to
                assert response_to['name'] == "20 Rue Bob (Bobtown)"
                assert response_to['embedded_type'] == "address"
                assert response_to['address']['label'] == "20 Rue Bob (Bobtown)"

    def test_global_coords_uri(self):
        url = 'https://host_of_bragi'
        params = {
            'pt_dataset': 'main_routing_test',
            'lon': 3.282103,
            'lat': 49.84758
        }

        url += "/reverse?{}".format(urlencode(params, doseq=True))

        mock_requests = MockRequests({
            url: (BRAGI_MOCK_RESPONSE, 200)
        })

        with mock.patch('requests.get', mock_requests.get):
            response = self.query("/v1/coverage/{pt_dataset}/coords/{lon};{lat}".
                                  format(lon=params.get('lon'), lat=params.get('lat'),
                                         pt_dataset=params.get('pt_dataset')))

            address = response.get('address')
            assert address
            assert address['house_number'] == 20
            assert address['name'] == 'Rue Bob'
            assert address['label'] == '20 Rue Bob (Bobtown)'
            assert len(address['administrative_regions']) == 1

@config({'scenario': 'new_default'})
class TestNewDefaultAutocompleteAndRouting(AbstractAutocompleteAndRouting,
                                           NewDefaultScenarioAbstractTestFixture):
    pass

@config({'scenario': 'distributed'})
class TestDistributedAutocompleteAndRouting(AbstractAutocompleteAndRouting,
                                         NewDefaultScenarioAbstractTestFixture):
    pass
