# bharat_telepharma_private_limited_task

A simple backend for a Telemedicine app using **FastAPI**, **PostgreSQL**, and **JWT Auth**.  
It supports doctors & patients, appointments, and real-time doctor status via WebSockets.  

Features
- User Register & Login (JWT)
- Doctor & Patient roles
- Appointments (create & list)
- Doctor status (online/offline) via WebSocket
- API docs with Swagger (`/docs`)
- PostgreSQL + SQLAlchemy
- Password hashing with bcrypt


API runs at  http://localhost:8000/docs

Endpoints
Auth: /auth/register, /auth/login
Users: /users/register, /users/login
Appointments: /appointments/

Doctor Status:
GET /status/doctor/{id}
POST /status/doctor/{id}
