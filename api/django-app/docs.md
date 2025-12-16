# 🎓 Kurslar Platformasi API Hujjatlari

## Base URL
```
https://api.courseplatform.uz/api/v1
```

## Autentifikatsiya
Barcha himoyalangan endpointlar uchun JWT token talab qilinadi.

**Header:**
```
Authorization: Bearer {your_jwt_token}
```

---

## 📋 Bo'limlar
1. [Authentication (Autentifikatsiya)](#authentication)
2. [Users (Foydalanuvchilar)](#users)
3. [Courses (Kurslar)](#courses)
4. [Lessons (Darslar)](#lessons)
5. [Exercises (Mashqlar)](#exercises)
6. [Progress (Progress)](#progress)
7. [Leaderboard (Reyting)](#leaderboard)

---

## <a name="authentication"></a>🔐 1. Authentication

### 1.1 Ro'yxatdan o'tish
**POST** `/auth/register`

Yangi foydalanuvchi ro'yxatdan o'tkazish.

**Request Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "password123",
  "full_name": "John Doe"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "message": "Ro'yxatdan o'tish muvaffaqiyatli",
  "data": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "john_doe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "xp": 0,
    "level": 1
  }
}
```

**Error Responses:**
```json
// 400 Bad Request
{
  "success": false,
  "message": "Barcha maydonlar to'ldirilishi kerak"
}

// 400 Bad Request
{
  "success": false,
  "message": "Username yoki email band"
}
```

---

### 1.2 Kirish
**POST** `/auth/login`

Mavjud foydalanuvchi tizimga kirishi.

**Request Body:**
```json
{
  "username": "john_doe",
  "password": "password123"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Kirish muvaffaqiyatli",
  "data": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "john_doe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "xp": 1250,
    "level": 5,
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

**Error Response:**
```json
// 401 Unauthorized
{
  "success": false,
  "message": "Username yoki password noto'g'ri"
}
```

---

## <a name="users"></a>👤 2. Users

### 2.1 Profil Ma'lumotlari
**GET** `/users/profile`

🔒 **Himoyalangan** - Token kerak

**Headers:**
```
Authorization: Bearer {token}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "john_doe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "xp": 1250,
    "level": 5,
    "rank": 42,
    "created_at": "2024-01-15T10:30:00Z",
    "statistics": {
      "completed_courses": 3,
      "completed_lessons": 45,
      "completed_exercises": 128,
      "total_submissions": 256,
      "acceptance_rate": 50.0
    }
  }
}
```

---

### 2.2 Profil Yangilash
**PUT** `/users/profile`

🔒 **Himoyalangan** - Token kerak

**Request Body:**
```json
{
  "full_name": "John Updated Doe",
  "bio": "Full-stack developer",
  "avatar_url": "https://example.com/avatar.jpg"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Profil yangilandi",
  "data": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "john_doe",
    "full_name": "John Updated Doe",
    "bio": "Full-stack developer",
    "avatar_url": "https://example.com/avatar.jpg"
  }
}
```

---

### 2.3 Boshqa Foydalanuvchi Profili
**GET** `/users/{username}`

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "username": "sarah_dev",
    "full_name": "Sarah Developer",
    "bio": "Python enthusiast",
    "xp": 2500,
    "level": 8,
    "rank": 15,
    "badges": [
      {
        "badge_id": "first_course",
        "name": "Birinchi Kurs",
        "icon": "🎯",
        "earned_at": "2024-01-20T15:00:00Z"
      }
    ]
  }
}
```

---

## <a name="courses"></a>📚 3. Courses

### 3.1 Barcha Kurslar
**GET** `/api/courses`

Query parametrlari:
- `title` (optional): python, javascript, data-structures, etc.
- `description` (optional): beginner, intermediate, advanced
- `page` (optional): default = 1
- `limit` (optional): default = 20

**Request:**
```
GET /api/courses
```
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/courses/' \
  -H 'accept: application/json'
```
Search
```http://127.0.0.1:8000/api/courses/?search=python```

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/courses/?search=python' \
  -H 'accept: application/json'
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "courses": [
      {
        "course_id": 1,
        "title": "python",
        "slug": "python",
        "description": "kurs pythondan bulayabdi",
        "instructor": "2025-11-04 11:07:05.844246+00:00",
        "price": 0,
        "lesson_count": 1,
        "module_count": 1,
        "enrolled_count": 0,
        "is_enrolled": false,
        "is_free": true,
        "thumbnail": "http://localhost:9000/media/courses/images/c.jpeg",
        "created_at": "2025-10-30T10:40:28.991Z"
      }
    ],
    "pagination": {
      "current_page": 1,
      "total_pages": 1,
      "total_courses": 1,
      "limit": 10
    }
  }
}
```

---

### 3.2 Kurs Tafsilotlari
**GET** `/api/courses/{course_slug}`

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/courses/{slug}' \
  -H 'accept: application/json'
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "course_id": 1,
    "title": "python",
    "slug": "python",
    "description": "kurs pythondan bulayabdi",
    "price": 0,
    "instructor": {
      "name": "2025-11-04 11:07:05.844246+00:00",
      "avatar": "http://localhost:9000/media/courses/images/c.jpeg",
      "bio": null
    },
    "lesson_count": 0,
    "modules": [
      {
        "id": 1,
        "title": "python kirish",
        "slug": "python-kirish",
        "description": "python kirish",
        "lessons_count": 1,
        "lessons": [
          {
            "id": 1,
            "title": "python kirish",
            "slug": "python-kirish",
            "lesson_type": "darslik",
            "preview": false
          }
        ]
      }
    ],
    "is_enrolled": false,
    "is_free": true,
    "enrolled_count": 0,
    "thumbnail": "http://localhost:9000/media/courses/images/c.jpeg",
    "created_at": "2025-10-30T10:40:28.991Z",
    "updated_at": "2025-10-30T10:40:29.541Z"
  }
}
```

---

### 3.3 Kursga Yozilish
**POST** `/courses/{course_id}/enroll`

🔒 **Himoyalangan** - Token kerak

**Response (201 Created):**
```json
{
  "success": true,
  "message": "Kursga muvaffaqiyatli yozildingiz",
}
```

**Error Response:**
```json
// 409 Conflict
{
  "success": false,
  "message": "Siz allaqachon bu kursga yozilgansiz"
}
```

---


---

## <a name="lessons"></a>📖 4. Lessons

### 4.1 Dars Tafsilotlari
**GET** `/courses/lessons/{slug}`

🔒 **Himoyalangan** - Token kerak

**Response (200 OK):**

```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "python kirish",
    "slug": "python-kirish",
    "pages": [
      {
        "id": 2,
        "title": "python uzbek",
        "slug": "python-uzbek",
        "ball": 150,
        "type": "False"
      }
    ]
  }
}
```
---

### 4.2 Darsni Tugallangan Qilish
**POST** `/lessons/{lesson_id}/complete`

🔒 **Himoyalangan** - Token kerak

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Dars tugallandi",
  "data": {
    "lesson_id": "l1",
    "completed_at": "2024-11-04T11:00:00Z",
    "xp_earned": 20,
    "new_total_xp": 1270,
    "level_up": false
  }
}
```

---

## <a name="exercises"></a>💻 5. Exercises

### 5.1 Mashq Tafsilotlari
**GET** `/exercises/{exercise_id}`

🔒 **Himoyalangan** - Token kerak

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "exercise_id": "ex1",
    "lesson_id": "l1",
    "title": "Two Sum",
    "description": "Massivdan ikkita sonni toping, ularning yig'indisi target ga teng bo'lsin",
    "difficulty": "easy",
    "xp_reward": 10,
    "topics": ["arrays", "hash-table"],
    "content": {
      "problem_statement": "Sizga butun sonlar massivi nums va butun son target berilgan...",
      "constraints": [
        "2 <= nums.length <= 10^4",
        "-10^9 <= nums[i] <= 10^9",
        "-10^9 <= target <= 10^9"
      ],
      "examples": [
        {
          "input": "nums = [2,7,11,15], target = 9",
          "output": "[0,1]",
          "explanation": "nums[0] + nums[1] == 9, shuning uchun [0, 1] qaytaramiz"
        }
      ],
      "starter_code": {
        "python": "def twoSum(nums, target):\n    # Sizning kodingiz\n    pass",
        "javascript": "function twoSum(nums, target) {\n    // Sizning kodingiz\n}",
        "cpp": "vector<int> twoSum(vector<int>& nums, int target) {\n    // Sizning kodingiz\n}"
      }
    },
    "test_cases_count": 25,
    "submission_count": 1523,
    "acceptance_rate": 45.2,
    "your_submissions": [
      {
        "submission_id": "sub123",
        "status": "wrong_answer",
        "submitted_at": "2024-11-03T10:00:00Z"
      }
    ]
  }
}
```

---

### 5.2 Yechim Yuborish
**POST** `/exercises/{exercise_id}/submit`

🔒 **Himoyalangan** - Token kerak

**Request Body:**
```json
{
  "language": "python",
  "code": "def twoSum(nums, target):\n    hashmap = {}\n    for i, num in enumerate(nums):\n        diff = target - num\n        if diff in hashmap:\n            return [hashmap[diff], i]\n        hashmap[num] = i\n    return []"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "submission_id": "sub456",
    "status": "accepted",
    "message": "Barcha testlar muvaffaqiyatli o'tdi!",
    "test_results": {
      "total": 25,
      "passed": 25,
      "failed": 0
    },
    "execution_time_ms": 45,
    "memory_usage_mb": 14.2,
    "xp_earned": 10,
    "new_total_xp": 1280,
    "level_up": false,
    "submitted_at": "2024-11-04T11:30:00Z"
  }
}
```

**Response (Wrong Answer):**
```json
{
  "success": true,
  "data": {
    "submission_id": "sub457",
    "status": "wrong_answer",
    "message": "Ba'zi testlar xato",
    "test_results": {
      "total": 25,
      "passed": 20,
      "failed": 5
    },
    "failed_test": {
      "input": "nums = [3,2,4], target = 6",
      "expected_output": "[1,2]",
      "your_output": "[0,2]"
    },
    "xp_earned": 0,
    "submitted_at": "2024-11-04T11:25:00Z"
  }
}
```

**Response (Runtime Error):**
```json
{
  "success": true,
  "data": {
    "submission_id": "sub458",
    "status": "runtime_error",
    "message": "Runtime error",
    "error_message": "IndexError: list index out of range",
    "error_line": 5,
    "xp_earned": 0,
    "submitted_at": "2024-11-04T11:20:00Z"
  }
}
```

---

### 5.3 Yuborilgan Yechimlar Tarixi
**GET** `/exercises/{exercise_id}/submissions`

🔒 **Himoyalangan** - Token kerak

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "submissions": [
      {
        "submission_id": "sub456",
        "status": "accepted",
        "language": "python",
        "execution_time_ms": 45,
        "memory_usage_mb": 14.2,
        "submitted_at": "2024-11-04T11:30:00Z"
      },
      {
        "submission_id": "sub457",
        "status": "wrong_answer",
        "language": "python",
        "submitted_at": "2024-11-04T11:25:00Z"
      }
    ],
    "total_submissions": 5,
    "best_submission": {
      "submission_id": "sub456",
      "execution_time_ms": 45,
      "memory_usage_mb": 14.2
    }
  }
}
```

---

### 5.4 Yechim Kodini Olish
**GET** `/submissions/{submission_id}`

🔒 **Himoyalangan** - Token kerak

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "submission_id": "sub456",
    "exercise_id": "ex1",
    "language": "python",
    "code": "def twoSum(nums, target):\n    hashmap = {}\n    for i, num in enumerate(nums):\n        diff = target - num\n        if diff in hashmap:\n            return [hashmap[diff], i]\n        hashmap[num] = i\n    return []",
    "status": "accepted",
    "execution_time_ms": 45,
    "memory_usage_mb": 14.2,
    "submitted_at": "2024-11-04T11:30:00Z"
  }
}
```

---

## <a name="progress"></a>📊 6. Progress

### 6.1 Kurs Progress
**GET** `/progress/courses/{course_id}`

🔒 **Himoyalangan** - Token kerak

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "course_id": "c1",
    "overall_progress": 65.5,
    "completed_lessons": 16,
    "total_lessons": 25,
    "completed_exercises": 95,
    "total_exercises": 150,
    "time_spent_minutes": 1245,
    "xp_earned": 850,
    "sections": [
      {
        "section_id": "s1",
        "title": "Kirish",
        "progress": 100,
        "completed_lessons": 5,
        "total_lessons": 5
      },
      {
        "section_id": "s2",
        "title": "O'zgaruvchilar",
        "progress": 62.5,
        "completed_lessons": 5,
        "total_lessons": 8
      }
    ],
    "started_at": "2024-10-01T10:00:00Z",
    "last_activity": "2024-11-04T11:30:00Z"
  }
}
```

---

### 6.2 Umumiy Progress
**GET** `/progress/overall`

🔒 **Himoyalangan** - Token kerak

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "total_xp": 1280,
    "level": 5,
    "xp_to_next_level": 220,
    "xp_for_next_level": 1500,
    "courses": {
      "enrolled": 5,
      "in_progress": 3,
      "completed": 2
    },
    "exercises": {
      "attempted": 256,
      "solved": 128,
      "acceptance_rate": 50.0
    },
    "streak": {
      "current": 7,
      "longest": 15,
      "last_activity": "2024-11-04T11:30:00Z"
    },
    "time_spent_hours": 42.5,
    "rank": 42,
    "total_users": 10000
  }
}
```

---

## <a name="leaderboard"></a>🏆 7. Leaderboard

### 7.1 Global Reyting
**GET** `/leaderboard/global`

Query parametrlari:
- `period` (optional): all-time, monthly, weekly (default: all-time)
- `limit` (optional): default = 50

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "period": "all-time",
    "updated_at": "2024-11-04T12:00:00Z",
    "leaderboard": [
      {
        "rank": 1,
        "user_id": "user789",
        "username": "coding_master",
        "full_name": "Ali Valiyev",
        "avatar": "https://cdn.example.com/avatars/user789.jpg",
        "xp": 15420,
        "level": 25,
        "solved_exercises": 543,
        "completed_courses": 12
      },
      {
        "rank": 2,
        "user_id": "user456",
        "username": "python_ninja",
        "full_name": "Sara Karimova",
        "avatar": "https://cdn.example.com/avatars/user456.jpg",
        "xp": 14230,
        "level": 23,
        "solved_exercises": 498,
        "completed_courses": 11
      }
    ],
    "your_rank": {
      "rank": 42,
      "xp": 1280,
      "level": 5
    }
  }
}
```

---

### 7.2 Kurs Reytingi
**GET** `/leaderboard/courses/{course_id}`

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "course_id": "c1",
    "course_title": "Python Asoslari",
    "leaderboard": [
      {
        "rank": 1,
        "username": "speedrunner",
        "progress": 100,
        "completion_time_hours": 15,
        "xp_earned": 1500,
        "completed_at": "2024-10-15T18:00:00Z"
      }
    ]
  }
}
```

---

## 📝 Status Codes

| Kod | Ma'nosi |
|-----|---------|
| 200 | OK - So'rov muvaffaqiyatli |
| 201 | Created - Yangi resurs yaratildi |
| 400 | Bad Request - Noto'g'ri ma'lumot |
| 401 | Unauthorized - Token yo'q yoki noto'g'ri |
| 403 | Forbidden - Ruxsat yo'q |
| 404 | Not Found - Resurs topilmadi |
| 409 | Conflict - Konflikt (masalan, allaqachon mavjud) |
| 500 | Internal Server Error - Server xatosi |

---

## 🎯 Submission Status Qiymatlari

| Status | Ma'nosi |
|--------|---------|
| `accepted` | To'g'ri yechim |
| `wrong_answer` | Noto'g'ri javob |
| `runtime_error` | Runtime xatosi |
| `time_limit_exceeded` | Vaqt chegarasidan oshdi |
| `memory_limit_exceeded` | Xotira chegarasidan oshdi |
| `compilation_error` | Kompilyatsiya xatosi |
| `pending` | Tekshirilmoqda |

---

## 💡 Misollar

### Python bilan foydalanish:

```python
import requests

# Login
response = requests.post('https://api.courseplatform.uz/api/v1/auth/login', json={
    'username': 'john_doe',
    'password': 'password123'
})
data = response.json()
token = data['data']['token']

# Kurslar olish
headers = {'Authorization': f'Bearer {token}'}
response = requests.get('https://api.courseplatform.uz/api/v1/courses', headers=headers)
courses = response.json()

# Yechim yuborish
code = """
def twoSum(nums, target):
    hashmap = {}
    for i, num in enumerate(nums):
        diff = target - num
        if diff in hashmap:
            return [hashmap[diff], i]
        hashmap[num] = i
    return []
"""

response = requests.post(
    'https://api.courseplatform.uz/api/v1/exercises/ex1/submit',
    headers=headers,
    json={'language': 'python', 'code': code}
)
result = response.json()
print(result['data']['status'])  # accepted
```

### JavaScript bilan foydalanish:

```javascript
// Login
const loginResponse = await fetch('https://api.courseplatform.uz/api/v1/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'john_doe',
    password: 'password123'
  })
});
const { data } = await loginResponse.json();
const token = data.token;

// Profil olish
const profileResponse = await fetch('https://api.courseplatform.uz/api/v1/users/profile', {
  headers: { 'Authorization': `Bearer ${token}` }
});
const profile = await profileResponse.json();
console.log(profile.data);
```

---

## 🔔 Qo'shimcha Ma'lumotlar

### Rate Limiting
- 100 so'rov / daqiqa / foydalanuvchi
- 1000 so'rov / soat / foydalanuvchi

### Pagination
Ko'plab endpointlar pagination qo'llab-quvvatlaydi:
- `page`: Sahifa raqami (default: 1)
- `limit`: Har bir sahifadagi elementlar soni (default: 20, max: 100)

### Versiyalash
API versiyasi URL'da ko'rsatiladi: `/api/v1/...`

---

**Savol yoki muammolaringiz bo'lsa, bizga murojaat qiling: support@courseplatform.uz**

---

## contests

### contests list
api call
```bash
curl -X 'GET' \
  'http://localhost:8000/api/contests/' \
  -H 'accept: */*'
```

```json
{
  "data": [
    {
      "id": 1,
      "title": "Pythonchilar",
      "start_time": "2025-11-09T22:00:00+00:00",
      "contest_type": "ochiq",
      "duration": 3,
      "participants": 1,
      "description": "",
      "status": "boshlanmadi",
      "participated": true
    }
  ]
}
```
### contest register

```bash
curl -X 'POST' \
  'http://localhost:8000/api/contests/register/{slug}/?contest_key=12154' \
  -H 'accept: */*' \
  -d ''
```
```json
{
  "success": false,
  "message": "Siz allaqachon ro'yxatdan o'tgansiz"
}
```
### contest get

```bash
curl -X 'GET' \
  'http://localhost:8000/api/contests/slug/' \
  -H 'accept: */*'
```

```json
{
  "data": {
    "id": 1,
    "title": "Pythonchilar",
    "description": "",
    "start_time": "2025-11-09T22:00:00+00:00",
    "duration": 3,
    "contest_type": "ochiq",
    "participants": 1,
    "status": "boshlanmadi",
    "participated": true,
    "pages": [
      {
        "id": 4,
        "title": "problem",
        "slug": "problem",
        "ball": 100,
        "type": 1
      }
    ],
    "requires_key": false
  }
}
```