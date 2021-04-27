import os
import shutil
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



def unzip(file_path, tenant_id=None, extract_path=None):

    """
        Expects UPLOAD_PATH to be available in .env and tenant_id provided.
        Will use current directory if above condtition is not met.
        Extracts: “zip”, “tar”, “gztar”, “bztar”, or “xztar”.    
        Returns the path where the file was extracted
    """
    
    upload_path = os.getenv("UPLOAD_PATH")
    
    if tenant_id and upload_path:
        extract_path = os.path.join(upload_path, tenant_id)
    else:
        extract_path = os.getcwd()
        
    if not os.path.exists(extract_path): os.mkdir(extract_path)
        
    file_name = secure_filename((os.path.basename(file_path)))
    extract_path = os.path.join(extract_path, file_name + "_extracted")
    
    shutil.unpack_archive(file_name, extract_path)
    
    return extract_path


