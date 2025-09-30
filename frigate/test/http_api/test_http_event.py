from datetime import datetime

from fastapi.testclient import TestClient

from frigate.models import Event, Recordings, ReviewSegment
from frigate.test.http_api.base_http_test import BaseTestHttp


class TestHttpApp(BaseTestHttp):
    def setUp(self):
        super().setUp([Event, Recordings, ReviewSegment])
        self.minimal_config["cameras"]["front_door"]["ffmpeg"]["inputs"][0]["roles"] = [
            "detect",
            "audio",
        ]
        self.minimal_config["cameras"]["front_door"]["record"] = {
            "enabled": True,
            "alerts": {"retain": {"mode": "all", "days": 2}},
        }
        self.app = super().create_app()

    ####################################################################################################################
    ###################################  GET /events Endpoint   #########################################################
    ####################################################################################################################
    def test_get_event_list_no_events(self):
        with TestClient(self.app) as client:
            events = client.get("/events").json()
            assert len(events) == 0

    def test_get_event_list_no_match_event_id(self):
        id = "123456.random"
        with TestClient(self.app) as client:
            super().insert_mock_event(id)
            events = client.get("/events", params={"event_id": "abc"}).json()
            assert len(events) == 0

    def test_get_event_list_match_event_id(self):
        id = "123456.random"
        with TestClient(self.app) as client:
            super().insert_mock_event(id)
            events = client.get("/events", params={"event_id": id}).json()
            assert len(events) == 1
            assert events[0]["id"] == id

    def test_get_event_list_match_length(self):
        now = int(datetime.now().timestamp())

        id = "123456.random"
        with TestClient(self.app) as client:
            super().insert_mock_event(id, now, now + 1)
            events = client.get(
                "/events", params={"max_length": 1, "min_length": 1}
            ).json()
            assert len(events) == 1
            assert events[0]["id"] == id

    def test_get_event_list_no_match_max_length(self):
        now = int(datetime.now().timestamp())

        with TestClient(self.app) as client:
            id = "123456.random"
            super().insert_mock_event(id, now, now + 2)
            events = client.get("/events", params={"max_length": 1}).json()
            assert len(events) == 0

    def test_get_event_list_no_match_min_length(self):
        now = int(datetime.now().timestamp())

        with TestClient(self.app) as client:
            id = "123456.random"
            super().insert_mock_event(id, now, now + 2)
            events = client.get("/events", params={"min_length": 3}).json()
            assert len(events) == 0

    def test_get_event_list_limit(self):
        id = "123456.random"
        id2 = "54321.random"

        with TestClient(self.app) as client:
            super().insert_mock_event(id)
            events = client.get("/events").json()
            assert len(events) == 1
            assert events[0]["id"] == id

            super().insert_mock_event(id2)
            events = client.get("/events").json()
            assert len(events) == 2

            events = client.get("/events", params={"limit": 1}).json()
            assert len(events) == 1
            assert events[0]["id"] == id

            events = client.get("/events", params={"limit": 3}).json()
            assert len(events) == 2

    def test_get_event_list_includes_camera_meta(self):
        event_id = "123456.random"

        with TestClient(self.app) as client:
            super().insert_mock_event(event_id)
            response = client.get("/events").json()

            assert len(response) == 1
            event = response[0]
            expected_meta = (
                client.app.frigate_config.cameras["front_door"].model_dump(mode="json")
            )

            assert event["camera_meta"] == expected_meta
            assert event["camera_meta"]["ffmpeg"]["inputs"][0]["roles"] == [
                "record",
                "detect",
                "audio",
            ]
            assert (
                event["camera_meta"]["record"]["alerts"]["retain"]["mode"]
                == "all"
            )

    def test_events_explore_includes_camera_meta(self):
        event_id = "123456.random"

        with TestClient(self.app) as client:
            super().insert_mock_event(event_id)

            response = client.get("/events/explore").json()
            assert response
            event = response[0]
            assert event["camera_meta"]["ffmpeg"]["inputs"][0]["roles"] == [
                "record",
                "detect",
                "audio",
            ]

    def test_event_ids_includes_camera_meta(self):
        event_id = "123456.random"

        with TestClient(self.app) as client:
            super().insert_mock_event(event_id)

            response = client.get("/event_ids", params={"ids": event_id}).json()
            assert response
            event = response[0]
            assert event["camera_meta"]["record"]["alerts"]["retain"]["days"] == 2

    def test_event_detail_includes_camera_meta(self):
        event_id = "123456.random"

        with TestClient(self.app) as client:
            super().insert_mock_event(event_id)

            response = client.get(f"/events/{event_id}").json()
            assert response["camera_meta"]["ffmpeg"]["inputs"][0]["roles"] == [
                "record",
                "detect",
                "audio",
            ]

    def test_get_event_list_no_match_has_clip(self):
        now = int(datetime.now().timestamp())

        with TestClient(self.app) as client:
            id = "123456.random"
            super().insert_mock_event(id, now, now + 2)
            events = client.get("/events", params={"has_clip": 0}).json()
            assert len(events) == 0

    def test_get_event_list_has_clip(self):
        with TestClient(self.app) as client:
            id = "123456.random"
            super().insert_mock_event(id, has_clip=True)
            events = client.get("/events", params={"has_clip": 1}).json()
            assert len(events) == 1
            assert events[0]["id"] == id

    def test_get_event_list_sort_score(self):
        with TestClient(self.app) as client:
            id = "123456.random"
            id2 = "54321.random"
            super().insert_mock_event(id, top_score=37, score=37, data={"score": 50})
            super().insert_mock_event(id2, top_score=47, score=47, data={"score": 20})
            events = client.get("/events", params={"sort": "score_asc"}).json()
            assert len(events) == 2
            assert events[0]["id"] == id2
            assert events[1]["id"] == id

            events = client.get("/events", params={"sort": "score_des"}).json()
            assert len(events) == 2
            assert events[0]["id"] == id
            assert events[1]["id"] == id2

    def test_get_event_list_sort_start_time(self):
        now = int(datetime.now().timestamp())

        with TestClient(self.app) as client:
            id = "123456.random"
            id2 = "54321.random"
            super().insert_mock_event(id, start_time=now + 3)
            super().insert_mock_event(id2, start_time=now)
            events = client.get("/events", params={"sort": "date_asc"}).json()
            assert len(events) == 2
            assert events[0]["id"] == id2
            assert events[1]["id"] == id

            events = client.get("/events", params={"sort": "date_desc"}).json()
            assert len(events) == 2
            assert events[0]["id"] == id
            assert events[1]["id"] == id2
