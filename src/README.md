# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities.

## Features

- View all available extracurricular activities
- Sign up for activities

## Getting Started

1. Install the dependencies:

   ```
   pip install fastapi uvicorn
   ```

2. Run the application:

   ```
   python app.py
   ```

3. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Sign up for an activity                                             |

## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Activities** - Uses activity name as identifier:

   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of student emails who are signed up

2. **Students** - Uses email as identifier:
   - Name
   - Grade level

All data is stored in memory, which means data will be reset when the server restarts.

## Autenticação — Exemplos rápidos (register / login / usar token)

Antes de testar os endpoints protegidos, inicie a aplicação localmente:

```bash
uvicorn src.app:app --reload
```

Você pode criar usuários de teste rapidamente usando o script de seed:

```bash
python scripts/seed_users.py
```

Registrar um novo usuário (ex.: teacher):

```bash
curl -X POST "http://localhost:8000/auth/register?email=teacher@school.edu&password=teacherpass&role=teacher"
```

Fazer login (retorna JSON com `access_token`):

```bash
curl -X POST -F "username=teacher@school.edu" -F "password=teacherpass" http://localhost:8000/auth/login
```

Usar o token para chamar um endpoint protegido (`signup` exige role `teacher` ou `admin`):

```bash
# colocando o token manualmente
curl -X POST "http://localhost:8000/activities/Chess%20Club/signup?email=student@school.edu" \
   -H "Authorization: Bearer <ACCESS_TOKEN>"

# exemplo obtendo o token com `jq` e salvando em variável
TOKEN=$(curl -s -X POST -F "username=teacher@school.edu" -F "password=teacherpass" http://localhost:8000/auth/login | jq -r .access_token)
curl -X POST "http://localhost:8000/activities/Chess%20Club/signup?email=student@school.edu" -H "Authorization: Bearer $TOKEN"
```

Notas:

- O script `scripts/seed_users.py` cria três usuários de teste: `admin@school.edu` (admin), `teacher@school.edu` (teacher) e `student@school.edu` (student).
- O `SECRET_KEY` em `src/auth.py` está hard-coded para fins de PoC — mova para variável de ambiente antes de produção.
- Se não tiver `jq` instalado, você pode extrair manualmente o campo `access_token` do JSON retornado.

Configuração de ambiente recomendada

- `SECRET_KEY` (recomendado): defina uma chave forte no ambiente para produção. Ex:

```bash
export SECRET_KEY="uma-chave-muito-secreta"
export ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

- `ACCESS_TOKEN_EXPIRE_MINUTES` (opcional): tempo de expiração do token em minutos (padrão 1440 = 24h).

Sem `SECRET_KEY` setada, o projeto utiliza um valor de desenvolvimento que NÃO é seguro para produção.
