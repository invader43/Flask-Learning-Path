from datetime import datetime
import secrets # for generating hex 
import os # for getting file type 
from PIL import Image
from flask import url_for, current_app
from flaskblog import mail
from flask_mail import Message

def time_ago_string(past_datetime):
    current_datetime = datetime.utcnow()
    time_difference = current_datetime - past_datetime

    # Calculate time difference in seconds
    seconds_diff = time_difference.total_seconds()
    # Determine the appropriate time ago string based on the time difference
    if seconds_diff < 60:
        return f"{int(seconds_diff)} seconds ago"
    elif seconds_diff < 3600:
        minutes_diff = seconds_diff / 60
        return f"{int(minutes_diff)} minutes ago"
    elif seconds_diff < 86400:
        hours_diff = seconds_diff / 3600
        return f"{int(hours_diff)} hours ago"
    elif seconds_diff < 604800:
        days_diff = seconds_diff / 86400
        return f"{int(days_diff)} days ago"
    elif seconds_diff < 31536000:
        weeks_diff = seconds_diff / 604800
        return f"{int(weeks_diff)} weeks ago"
    else:
        years_diff = seconds_diff / 31536000
        return f"{int(years_diff)} years ago"


def save_picture(form_picture):
    # its not good to store the filename thats sent thru user 
    # its not even good to use username to store filename , if image files leak 
    # using the secrets module to generate a hex 
    random_hex = secrets.token_hex(8)
    _ , f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path , 'static/profile_pics' , picture_filename)

    output_size = (125,125)

    image_resized = Image.open(form_picture)
    image_resized.thumbnail(output_size)
    image_resized.save(picture_path)

    return picture_filename



def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request' ,
                sender = 'noreply@flaskblog_invader43.com',
                recipients=[user.email])
    msg.body = f'''To reset your password , visit the following link :
    {url_for('users.reset_token' , token = token , _external = True )}
    If you did not make this request , simply ignore the email. 
'''
    mail.send(msg)

