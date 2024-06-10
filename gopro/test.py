### Using GoPro Unofficial API package

from goprocam import GoProCamera, constants

gopro = GoProCamera.GoPro()

# Optional camera settings
gopro.video_settings(res='4k', fps='45')

# Retrieve all files from the camera storage.
# gopro.listMedia(True)
# Deletes all the files from the camera storage.
# gopro.delete('all')

def take_photo():
    # Allows the camera take photos at regular intervals.
    gopro.take_photo()

    # Download the last media on the camera.
    gopro.downloadLastMedia(custom_filename="face.JPG")
    
    # Delete the last media on the camera.
    # gopro.delete('last')