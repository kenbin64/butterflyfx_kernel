from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import FileResponse
from starlette.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pathlib

app = FastAPI()

# Serve static files from extras/server/static
base_dir = pathlib.Path(__file__).parent
static_dir = base_dir / "static"
templates_dir = base_dir / "templates"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

templates = Jinja2Templates(directory=str(templates_dir))

# Simple in-memory API key store (for prototype/demo only)
API_KEYS = {}



@app.get("/")
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get('/register')
def register_form(request: Request):
    return templates.TemplateResponse('register.html', {"request": request})


@app.post('/register')
def register_submit(request: Request, name: str = Form(...)):
    # create a simple API key and return it to the user
    import secrets
    key = secrets.token_urlsafe(24)
    API_KEYS[key] = {"name": name}
    return templates.TemplateResponse('register_success.html', {"request": request, "name": name, "key": key})


@app.get('/login')
def login_form(request: Request):
    return templates.TemplateResponse('login.html', {"request": request})


@app.post('/login')
def login_submit(request: Request, api_key: str = Form(...)):
    # validate API key and set an auth cookie
    if api_key in API_KEYS:
        resp = RedirectResponse(url='/', status_code=302)
        resp.set_cookie('bf_key', api_key, httponly=True, secure=True)
        return resp
    return templates.TemplateResponse('login.html', {"request": request, "error": "Invalid API key"})


@app.get('/dashboard')
def dashboard(request: Request):
    key = request.cookies.get('bf_key')
    if not key or key not in API_KEYS:
        return RedirectResponse(url='/login')
    info = API_KEYS.get(key)
    return templates.TemplateResponse('dashboard.html', {"request": request, "info": info})


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/downloads/{file_name}")
async def download(file_name: str):
    downloads_dir = base_dir / "downloads"
    target = downloads_dir / file_name
    if not target.exists() or not target.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(target, media_type="application/octet-stream", filename=file_name)
