from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials, firestore, auth
import datetime
from typing import Optional

# 1. Khởi tạo FastAPI
app = FastAPI()

# 2. Kết nối Firebase
cred = credentials.Certificate("backend/firebase-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# 3. Schema dữ liệu 
class TokenData(BaseModel):
    token: str

class NoteData(BaseModel):
    uid: str
    title: str
    content: str
    note_id: Optional[str] = None  
    deadline: Optional[str] = None  

# 4. Auth
@app.post("/auth/me")
def verify_user(data: TokenData):
    try:
        decoded_token = auth.verify_id_token(data.token)
        return {"message": "OK", "uid": decoded_token['uid'], "email": decoded_token.get('email')}
    except:
        raise HTTPException(status_code=401, detail="Lỗi Token")

# 5. Thêm Mới HOẶC Cập Nhật Ghi Chú
@app.post("/notes")
def create_or_update_note(note: NoteData):
    try:
        note_dict = {
            "uid": note.uid,
            "title": note.title,
            "content": note.content,
            "deadline": note.deadline
        }
        
        if note.note_id: 
            note_dict["updated_at"] = datetime.datetime.now().isoformat()
            db.collection("notes").document(note.note_id).set(note_dict, merge=True)
            return {"message": "Đã cập nhật ghi chú!"}
        else:           
            note_dict["created_at"] = datetime.datetime.now().isoformat()
            db.collection("notes").document().set(note_dict)
            return {"message": "Đã tạo ghi chú mới!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 6. Lấy danh sách
@app.get("/notes/{uid}")
def get_notes(uid: str):
    try:
        notes_ref = db.collection("notes").where("uid", "==", uid).stream()
        notes_list = []
        for doc in notes_ref:
            data = doc.to_dict()
            notes_list.append({
                "id": doc.id,
                "title": data.get("title", "Ghi chú không tên"),
                "content": data.get("content", ""),
                "created_at": data.get("created_at"),
                "deadline": data.get("deadline", "")
            })
        return {"notes": notes_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # 7. Endpoint Xóa Ghi Chú
@app.delete("/notes/{note_id}")
def delete_note(note_id: str):
    try:
        db.collection("notes").document(note_id).delete()
        return {"message": "Đã xóa ghi chú thành công!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
