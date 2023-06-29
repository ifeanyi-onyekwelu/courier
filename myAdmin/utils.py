import os

def get_dispatch_delivered_content(name):
    file_name = os.path.join(
        os.path.dirname(__file__), "..", "templates", "email", "dispatchDelivered.txt"
    )
    with open(file_name, "r") as f:
        content = f.read()
        content = content.replace("{senderName}", name)
    return content

def get_dispatch_packaging_content(name):
    file_name = os.path.join(
        os.path.dirname(__file__), "..", "templates", "email", 'dispatchInPackaging.txt'
    )
    with open(file_name, "r") as f:
        content = f.read()
        content = content.replace("{senderName}", name)
    return content

def get_dispatch_in_transit(name):
    file_name = os.path.join(
        os.path.dirname(__file__), "..", "templates", "email", 'dispatchInTransit.txt'
    )
    with open(file_name, "r") as f:
        content = f.read()
        content = content.replace("{senderName}", name)
    return content

def get_dispatch_shipped(name):
    file_name = os.path.join(
        os.path.dirname(__file__), "..", "templates", "email", 'dispatchShipped.txt'
    )
    with open(file_name, "r") as f:
        content = f.read()
        content = content.replace("{senderName}", name)
    return content