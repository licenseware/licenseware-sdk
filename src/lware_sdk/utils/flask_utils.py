import os
from werkzeug.utils import secure_filename



def save_file(file, tenant_id=None, path=None):
    """
        Save to disk flask file stream
        
    """
    
    filename = secure_filename(file.filename)

    save_path = path or os.path.join(os.getenv("UPLOAD_PATH"), tenant_id)
    if not os.path.exists(save_path): os.mkdir(save_path)

    file.seek(0)  # move cursor to 0 (stream left it on last read)
    file.save(os.path.join(save_path, filename))

    return filename
