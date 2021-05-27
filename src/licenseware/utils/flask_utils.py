import os
import shutil
try:
    from werkzeug.utils import secure_filename
except:
    pass # we are on the worker side



UPLOAD_PATH = os.getenv("UPLOAD_PATH")


def save_file(file, tenant_id=None, path=None):
    """
        Save to disk flask file stream
        
    """
    
    filename = secure_filename(file.filename)

    save_path = path or os.path.join(UPLOAD_PATH, tenant_id)
    if not os.path.exists(save_path): os.mkdir(save_path)

    file.seek(0)  # move cursor to 0 (stream left it on last read)
    file.save(os.path.join(save_path, filename))

    return filename



def unzip(file_path):

    """
        Extracts: “zip”, “tar”, “gztar”, “bztar”, or “xztar”.    
        Returns the path where the file was extracted
    """

    if not file_path.endswith(('.zip', '.tar.bz2')):
        return file_path
        
    file_name = os.path.basename(file_path)
    file_dir  = os.path.dirname(file_path)

    extract_path = os.path.join(file_dir, file_name + "_extracted")
    
    shutil.unpack_archive(file_path, extract_path)
    
    return extract_path



def get_filepaths_from_event(event):
    """
        :event - redis event similar to the one bellow:
            event = {
                'tenant_id': '2ac111c7-fd19-463e-96c2-1493aea18bed', 
                'files': 'filename1,filename2',
                'event_type': 'ofmw_archive' # for normalization purposes 'event_type' is the same as 'unit_type' and 'file_type'
            }

        returns a list of filepaths or list of folder paths if an archive is found in 'files' 

    """

    filepath = lambda filename: os.path.join(UPLOAD_PATH, event['tenant_id'], filename)
    filenames = event['files'].split(",")

    return [unzip(filepath(filename)) for filename in filenames]




