from functools import wraps
from flask import redirect, session
from random import randint
import io
import os
import subprocess
from io import BytesIO
from PIL import Image

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/register")
        return f(*args, **kwargs)
    return decorated_function



def logout_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return f(*args, **kwargs)
        return redirect("/")
    return decorated_function



def generate_address():

    city = [
        "Lyndhurst", "Carinasford", "Hawrnith"
    ]

    street = [
        "123 Elmwood Avenue", "456 Oak Street", "789 Pine Road", "321 Cedar Lane",
        "654 Birch Boulevard", "987 Maple Way", "234 River Road", "567 Park Avenue",
        "890 Spring Street", "135 Hilltop Drive", "246 Lakeview Drive", "357 Forest Lane",
        "468 Mountain Road", "579 Willow Street", "680 Sunset Boulevard", "791 Ash Street",
        "802 Crestview Drive", "913 Horizon Lane", "024 Valley Road", "135 Oceanview Avenue",
        "246 Kingsway Drive", "357 Shoreline Avenue", "468 Northview Lane", "579 Maplewood Drive",
        "680 Westwood Road", "791 Elm Street", "802 Cedar Park", "913 Greenfield Avenue",
        "024 Crystal Drive", "135 Meadow Lane", "246 Starlight Avenue", "357 Crescent Street",
        "468 Morning Glory Way", "579 Brookfield Road", "680 Sunset View", "791 Pinecrest Drive",
        "802 Oakwood Lane", "913 Silver Birch Drive", "024 Riverstone Road", "135 Hillcrest Avenue",
        "246 Maple Grove", "357 Willow Crest", "468 Birchwood Lane", "579 Woodland Drive",
        "680 Highland Avenue", "791 Spring Hill Road", "802 Pine Valley", "913 Mountain Crest",
        "024 Lakewood Drive", "135 Sunset Heights", "246 Autumn Way", "357 Hilltop Avenue",
        "468 Ocean Breeze Drive", "579 Forest Grove", "680 Meadowview Lane", "791 Riverside Drive",
        "802 Crestwood Road", "913 Pine Hill Avenue", "024 Brookside Lane", "135 Silver Lake Road",
        "246 Kingswood Drive", "357 Cedar Creek", "468 North Ridge", "579 Sunset Lane",
        "680 Elm Heights", "791 Ocean View", "802 Maple Valley", "913 Evergreen Drive",
        "024 Silver Creek Road", "135 Riverbend Avenue", "246 Highland Park", "357 North Shore Road",
        "468 Mountain Vista", "579 Pine Lake Drive", "680 Valley Heights", "791 Maple Ridge",
        "802 Hilltop Crescent", "913 Riverstone Avenue"
    ]

    zip = [
        "10001", "20002", "30003", "40004", "50005", "60006", "70007", "80008",
        "90009", "10101", "20202", "30303", "40404", "50505", "60606", "70707",
        "80808", "90909", "11111", "22222", "33333", "44444", "55555", "66666",
        "77777", "88888", "99999", "12121", "23232", "34343", "45454", "56565",
        "67676", "78787", "89898", "13131", "24242", "35353", "46464", "57575",
        "68686", "79797", "80809", "91919", "10112", "20222", "30332", "40442",
        "50552", "60662", "70772", "80882", "90992", "11113", "22223", "33333",
        "44444", "55555", "66666", "77777", "88888", "99999", "12122", "23232",
        "34342", "45452", "56562", "67672", "78782", "89892", "13132", "24242",
        "35352", "46462", "57572", "68682", "79792", "80882", "91992", "10121",
        "20232", "30342", "40452", "50562", "60672", "70782", "80892", "90902"
    ]
    country = [
        "Nortland"
    ]

    return {"street": street[randint(0, len(street) - 1)], "city": city[randint(0,len(city)- 1)], "zip": zip[randint(0,len(zip) - 1)], "country": country[randint(0,len(country) - 1)]}

def generate_image(route, address, username, recipient = None):

    hp = "0"
    wp = "0"
    match route:

        case 'env1':
            hp = "-110"
        case 'env2':
            hp = "-80"
        case 'env3':
            hp = "-100"
        case 'env4':
            hp = "-120"

        case 'env5':
            hp = "-120"
            wp = "60"

        case 'env6':
            hp = "-120"
        case 'envOwn':
            hp = "-416"
            wp = "-380"
        case _:
            raise ValueError("Invalid image, accessing invalid route or image is not yet registered")
    if route == 'envOwn':
        if recipient:
            imageIO = io.BytesIO(subprocess.run(['./image2', route + ".bmp", "stdout", hp, wp, username, address['street'], address['city'] + ", " + address['zip'], address['country'], recipient['name'], recipient['street'], recipient['city'] + ", " + recipient['zip'], recipient['country']], cwd='image-write/Ee/', capture_output=True).stdout)
        else:
            imageIO = io.BytesIO(subprocess.run(['./image2', route + ".bmp", "stdout", hp, wp, username, address['street'], address['city'] + ", " + address['zip'], address['country']], cwd='image-write/Ee/', capture_output=True).stdout)
    else:
        imageIO = io.BytesIO(subprocess.run(['./image', route + ".bmp", "stdout", hp, wp, username, address['street'], address['city'] + ", " + address['zip'], address['country']], cwd='image-write/Ee/', capture_output=True).stdout)
    print("there")
    print(f"made image, size is {len(imageIO.getbuffer())}")
    image = Image.open(imageIO)
    imageIO = io.BytesIO()
    print("converting image")
    image.save(imageIO, "PNG", optimize=True, quality=85)
    print("converted image")

    print(f"saved image, size is {len(imageIO.getbuffer())}")
    imageIO.seek(0)
    print("returned image")
    return imageIO



