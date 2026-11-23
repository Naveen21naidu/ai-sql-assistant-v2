from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
import models, schemas, auth
from question_validator import validate_question
from sql_validator import validate_sql
from gemini_service import generate_sql
from db_service import execute_query

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register", response_model=schemas.UserOut)
def register(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.username == payload.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = models.User(
        username=payload.username,
        hashedpassword=auth.hash_password(payload.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/login", response_model=schemas.Token)
def login(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == payload.username).first()

    if not user or not auth.verify_password(payload.password, user.hashedpassword):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/ask", response_model=schemas.AskResponse)
def ask_question(
    payload: schemas.AskRequest,
    db: Session = Depends(get_db),
    current_user: str = Depends(auth.get_current_user)
):
    try:
        validate_question(payload.question)
        sql = generate_sql(payload.question)
        validate_sql(sql)
        result = execute_query(sql)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=503, detail="AI or database error, try again")
    
    

    user = db.query(models.User).filter(models.User.username == current_user).first()
    log_entry = models.QueryLog(
        user_id=user.id,
        question=payload.question,
        generated_sql=sql
    )
    db.add(log_entry)
    db.commit()

    return {
        "question": payload.question,
        "generated_sql": sql,
        "result": result
    }

@app.get("/history", response_model=list[schemas.QueryLogOut])
def get_history(
    db: Session = Depends(get_db),
    current_user: str = Depends(auth.get_current_user)
):
    user = db.query(models.User).filter(models.User.username == current_user).first()
    logs = db.query(models.QueryLog).filter(models.QueryLog.user_id == user.id).all()
    return logs