import uuid
from uuid import uuid4
from datetime import datetime, time

def create_sample_instructor(client):
    unique_email = f"{uuid.uuid4()}@example.com"
    res = client.post("/instructors", json={
        "name": "王小明",
        "email": unique_email,
        "password": "securepassword"
    })
    return int(res.json()["id"])

def test_create_instructor_conflict(client):
    email = f"teacher_{uuid.uuid4()}@example.com"
    client.post("/instructors", json={
        "name": "林老師",
        "email": email,
        "password": "securepassword"
    })
    res = client.post("/instructors", json={
        "name": "陳老師",
        "email": email,
        "password": "anotherpassword"
    })
    assert res.status_code == 400
    assert res.json()["detail"] == "Email already registered"

def test_create_instructor(client):
    email = f"teacher_{uuid.uuid4()}@example.com"
    res = client.post("/instructors", json={
        "name": "林老師",
        "email": email,
        "password": "securepassword"
    })
    assert res.status_code == 201
    assert "id" in res.json()

def test_create_course(client):
    instructor_id = create_sample_instructor(client)
    res = client.post("/courses", json={
        "title": "資料庫入門",
        "description": "SQL基礎",
        "instructorId": instructor_id,
        "startTime": "10:00",
        "endTime": "13:00"
    })
    assert res.status_code == 201
    assert res.json()["title"] == "資料庫入門"

def test_create_course_invalid_instructor(client):
    res = client.post("/courses", json={
        "title": "錯誤課程",
        "description": "沒有講師",
        "instructorId": 999999,
        "startTime": "10:00",
        "endTime": "13:00"
    })
    assert res.status_code == 400

def test_list_courses_limit(client):
    instructor_id = create_sample_instructor(client)
    for i in range(3):
        client.post("/courses", json={
            "title": f"課程 {i+1}",
            "description": f"說明 {i+1}",
            "instructorId": instructor_id,
            "startTime": f"{10+i}:00",
            "endTime": f"{13+i}:00",
            "is_deleted": False,
            "deleted_at": None
        })

    res = client.get("/courses")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    assert isinstance(data["items"], list)
    assert len(data["items"]) <= 2
    for course in data["items"]:
        assert "instructor" in course
        assert "email" in course["instructor"]

def test_update_course(client):
    instructor_id = create_sample_instructor(client)
    res = client.post("/courses", json={
        "title": "原始標題",
        "description": "原始描述",
        "instructorId": instructor_id,
        "startTime": "13:00",
        "endTime": "16:00",
    })
    print(res.status_code, res.json())
    course_id = res.json()["id"]

    res = client.put(f"/courses/{course_id}", json={
        "title": "新標題",
        "description": "新描述",
        "instructorId": instructor_id,
        "startTime": "15:00",
        "endTime": "18:00"
    })
    assert res.status_code == 200
    assert res.json()["title"] == "新標題"

def test_update_course_not_found(client):
    fake_course_id = 999999999
    fake_instructor_id = 999999999
    res = client.put(f"/courses/{fake_course_id}", json={
        "title": "不存在",
        "description": "錯誤",
        "instructorId": fake_instructor_id,
        "startTime": "13:00",
        "endTime": "16:00"
    })
    assert res.status_code == 404

def test_delete_course(client):
    instructor_id = create_sample_instructor(client)
    res = client.post("/courses", json={
        "title": "待刪除課程",
        "description": "刪除測試",
        "instructorId": instructor_id,
        "startTime": "13:00",
        "endTime": "16:00",
        "is_deleted": False,
        "deleted_at": None
    })
    assert res.status_code == 201
    course_id = res.json()["id"]

    res = client.delete(f"/courses/{course_id}")
    assert res.status_code == 204

    res = client.get("/courses")
    if res.status_code == 404:
        assert res.json()["detail"] == "Course not found"
    else:
        assert res.status_code == 200
        items = res.json()["items"]
        assert all(c["id"] != course_id for c in items)


def test_delete_course_not_found(client):
    fake_course_id = 999999999
    res = client.delete(f"/courses/{fake_course_id}")
    assert res.status_code == 404

def test_list_instructor_courses(client):
    instructor_id = create_sample_instructor(client)
    client.post("/courses", json={
        "title": "A 課程",
        "description": "內容 A",
        "instructorId": instructor_id,
        "startTime": "13:00",
        "endTime": "16:00"
    })
    client.post("/courses", json={
        "title": "B 課程",
        "description": "內容 B",
        "instructorId": instructor_id,
        "startTime": "14:00",
        "endTime": "17:00",
    })

    res = client.get(f"/instructors/{instructor_id}/courses")
    assert res.status_code == 200
    data = res.json()
    assert len(data["items"]) == 2
    assert data["items"][0]["title"].startswith("A") or data[0]["title"].startswith("B")
