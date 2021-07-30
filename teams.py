import requests
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from webexteamssdk import WebexTeamsAPI, ApiError
from texttable import Texttable as TT

# Function to print data in table
def table(header, data):
    # Sort all data alphabetically by first column
    data.sort(key=lambda pattern: pattern[0])
    report = header + data
    table = TT(max_width=0)
    # Set all columns to type "text"
    dtype = []
    for count in range(0, len(header[0])):
        dtype.append('t')
    table.set_cols_dtype(dtype)
    table.add_rows(report)
    return table.draw()

if __name__ == "__main__":

    # Disable certificate warnings
    disable_warnings(InsecureRequestWarning)

    print()
    token = input("Enter Personal Access Token: ")
    api = WebexTeamsAPI(access_token=token)

    while True:
        # Menu
        print()
        print("1. List Spaces")
        print("2. List Space Memberships")
        print("3. Create New Space")
        print("4. Send Message To Space")
        print("5. Delete Space")
        print("9. Quit")
        print()
        option = input("Enter Option: ")

        # List all spaces
        if option == "1":
            print()
            try:
                room_list = api.rooms.list()
            except ApiError as e:
                print(e)
            else:
                header = [["Space Name", "Space ID"]]
                data = []
                for item in room_list:
                    data.append([item.title, item.id])
                print(table(header, data))

        # List all space memberships
        if option == "2":
            print()
            try:
                member_list = api.memberships.list()
            except ApiError as e:
                print(e)
            else:
                header = [["Space Name", "Person Name", "Organization", "Membership ID"]]
                data = []
                for item in member_list:
                    # Pull room name
                    try:
                        room_name = api.rooms.get(item.roomId)
                    except ApiError as e:
                        print(e)
                    else:
                        # Pull organization name
                        try:
                            org_name = api.organizations.get(item.personOrgId)
                        except ApiError as e:
                            print(e)
                        else:
                            data.append([room_name.title, item.personDisplayName, org_name.displayName, item.id])
                print(table(header, data))

        # Create a new space
        if option == "3":
            print()
            room_name = input("Enter Space Name: ")
            print()
            try:
                room_create = api.rooms.create(room_name)
            except ApiError as e:
                print(e)
            else:
                header = [["Space Name", "Space ID"]]
                data = []
                data.append([room_create.title, room_create.id])
                print(table(header, data))

        # Send message to a space
        if option == "4":
            print()
            room_name = input("Enter Space Name: ")
            message = input("Enter Message: ")
            print()
            room_flag = False
            try:
                room_list = api.rooms.list()
            except ApiError as e:
                print(e)
            else:
                # Note: Any rooms with identical names will receive message; Room names are case sensitive
                for item in room_list:
                    if item.title == room_name:
                        try:
                            room_message = api.messages.create(roomId=item.id, text=message)
                        except ApiError as e:
                            print(e)
                        else:
                            print("Message Sent to Space {} with ID {}".format(item.title, item.id))
                            room_flag = True
                if not room_flag:
                    print("Room Does Not Exist")

        # Delete a space
        if option == "5":
            print()
            room_name = input("Enter Space Name: ")
            print()
            room_flag = False
            try:
                room_list = api.rooms.list()
            except ApiError as e:
                print(e)
            else:
                # Note: Any rooms with identical names will be deleted; Room names are case sensitive
                for item in room_list:
                    if item.title == room_name:
                        try:
                            room_delete = api.rooms.delete(item.id)
                        except ApiError as e:
                            print(e)
                        else:
                            print("Space {} with ID {} Has Been Deleted".format(item.title, item.id))
                            room_flag = True
                if not room_flag:
                    print("Room Does Not Exist")

        # Option to quit
        if option == "9":
            print()
            break
